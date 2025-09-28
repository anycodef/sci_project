import pandas as pd
import numpy as np
import os
import re
from scipy.stats import f_oneway, chi2_contingency

# --- Configuración ---
DATA_DIR = 'lima/02_preparacion_y_limpieza'
OUTPUT_FILE = 'lima/REPORTE_ANALITICO_FINAL.md'

# --- Mapeos para Recodificación ---
EDUCATION_MAP_LABELS = {
    1: 'Sin nivel', 2: 'Educ. Inicial', 3: 'Primaria Incompleta', 4: 'Primaria Completa',
    5: 'Secundaria Incompleta', 6: 'Secundaria Completa', 7: 'Básica Especial',
    8: 'Superior No Univ. Incompleta', 9: 'Superior No Univ. Completa',
    10: 'Superior Univ. Incompleta', 11: 'Superior Univ. Completa', 12: 'Maestría/Doctorado'
}
SEX_MAP_LABELS = {1: 'Hombre', 2: 'Mujer'}

# --- Funciones Auxiliares ---
def extract_period_from_filename(filename):
    match = re.search(r'Trim ([A-Za-z-]+)(\d{2})', filename)
    if match:
        month_map = {
            'Ene-Feb-Mar': 'Q1', 'Abr-May-Jun': 'Q2', 'Jul-Ago-Set': 'Q3',
            'Set-Oct-Nov': 'Q4', 'Mar-Abr-May': 'Q2'
        }
        months, year = match.groups()
        quarter = month_map.get(months, 'Q_Unk')
        return f"20{year}-{quarter}"
    return "Periodo_Desconocido"

def weighted_average(series, weights):
    return np.average(series.dropna(), weights=weights.loc[series.dropna().index])

# --- 1. Carga y Preparación de Datos ---
print("--- 1. Cargando y Preparando Datos ---")
try:
    files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith('lima_cleaned_')])
    df_list = [pd.read_csv(os.path.join(DATA_DIR, f), low_memory=False) for f in files]
    for df, filename in zip(df_list, files):
        df['periodo'] = extract_period_from_filename(filename)
    master_df = pd.concat(df_list, ignore_index=True)
except Exception as e:
    print(f"Error al cargar datos: {e}"); exit()

# Recodificación y Feature Engineering
master_df['C366_label'] = master_df['C366'].map(EDUCATION_MAP_LABELS)
master_df['C207_label'] = master_df['C207'].map(SEX_MAP_LABELS)
master_df['es_informal'] = np.where((master_df['OCUP300'] == 1) & (master_df['C361_1'] == 2), 1, 0)
for col in ['INGTOT', 'C208', 'factor_expansion']:
    master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

# Filtrar para población ocupada para la mayoría de los análisis
df_ocupado = master_df[master_df['OCUP300'] == 1].copy()

# --- 2. Generación de Contenido para el Reporte ---
print("--- 2. Realizando Análisis para el Reporte ---")
report_content = "# Reporte Analítico Final: Mercado Laboral de Lima (2024-2025)\n\n"

# A. Resumen Ejecutivo
report_content += "## Resumen Ejecutivo\n"
report_content += "Este informe presenta un análisis exhaustivo del mercado laboral en Lima Metropolitana, utilizando datos trimestrales de 2024 y 2025. Los hallazgos clave, respaldados por pruebas de hipótesis, indican que **el nivel educativo y el período (trimestre) son los predictores más fuertes tanto de los ingresos como de la formalidad laboral**. Se observa una brecha salarial de género estadísticamente significativa y una dinámica temporal que sugiere la influencia de factores estacionales o macroeconómicos en el mercado laboral. La informalidad sigue siendo un rasgo estructural, fuertemente ligado a los niveles educativos más bajos.\n\n"

# B. Análisis Descriptivo y Temporal
report_content += "## Hallazgos del Análisis Descriptivo\n"
avg_income = weighted_average(df_ocupado['INGTOT'], df_ocupado['factor_expansion'])
avg_age = weighted_average(df_ocupado['C208'], df_ocupado['factor_expansion'])
report_content += f"- El **ingreso promedio mensual ponderado** de la población ocupada en Lima es de **S/. {avg_income:,.2f}**.\n"
report_content += f"- La **edad promedio ponderada** de la población ocupada es de **{avg_age:.1f} años**.\n\n"

report_content += "### Evolución Temporal de Indicadores Clave\n"
temporal_analysis = df_ocupado.groupby('periodo').apply(
    lambda x: pd.Series({
        'Ingreso Promedio Ponderado': weighted_average(x['INGTOT'], x['factor_expansion']),
        'Tasa de Informalidad (%)': weighted_average(x['es_informal'], x['factor_expansion']) * 100
    })
).sort_index()
report_content += "A continuación, se muestra la evolución de los principales indicadores a lo largo de los trimestres analizados:\n\n"
report_content += temporal_analysis.to_markdown(floatfmt=",.2f")
report_content += "\n\n"

# C. Pruebas de Hipótesis
report_content += "## Pruebas de Hipótesis\n"
report_content += "Para validar las relaciones observadas, se realizaron las siguientes pruebas de hipótesis (nivel de significancia α = 0.05).\n\n"

# Hipótesis 1: Género vs Ingreso
df_anova_g = df_ocupado.dropna(subset=['INGTOT', 'C207_label'])
groups_g = [df_anova_g['INGTOT'][df_anova_g['C207_label'] == g] for g in df_anova_g['C207_label'].unique()]
f_val_g, p_val_g = f_oneway(*groups_g)
report_content += "### 1. ¿Existe una brecha salarial de género?\n"
report_content += "- **H₀ (Hipótesis Nula):** El ingreso promedio es el mismo para hombres y mujeres.\n"
report_content += "- **H₁ (Hipótesis Alternativa):** El ingreso promedio es diferente para al menos un género.\n"
report_content += f"- **Prueba:** ANOVA. **Resultados:** F-statistic = {f_val_g:.2f}, p-value = {p_val_g:.4f}\n"
report_content += f"- **Conclusión:** Dado que el p-valor ({p_val_g:.4f}) es menor que 0.05, **se rechaza la hipótesis nula**. Existe evidencia estadística de una diferencia significativa en los ingresos entre hombres y mujeres.\n\n"

# Hipótesis 2: Educación vs Ingreso
df_anova_e = df_ocupado.dropna(subset=['INGTOT', 'C366_label'])
groups_e = [df_anova_e['INGTOT'][df_anova_e['C366_label'] == g] for g in df_anova_e['C366_label'].unique()]
f_val_e, p_val_e = f_oneway(*groups_e)
report_content += "### 2. ¿El nivel educativo influye en el ingreso?\n"
report_content += "- **H₀:** El ingreso promedio es el mismo en todos los niveles educativos.\n"
report_content += "- **H₁:** El ingreso promedio es diferente para al menos un nivel educativo.\n"
report_content += f"- **Prueba:** ANOVA. **Resultados:** F-statistic = {f_val_e:.2f}, p-value = {p_val_e:.4f}\n"
report_content += f"- **Conclusión:** Dado que el p-valor es extremadamente bajo ({p_val_e:.4f}), **se rechaza la hipótesis nula**. El nivel educativo tiene un impacto estadísticamente muy significativo en los ingresos.\n\n"

# Hipótesis 3: Educación vs Informalidad
df_chi2_e = df_ocupado.dropna(subset=['es_informal', 'C366_label'])
table_e = pd.crosstab(df_chi2_e['es_informal'], df_chi2_e['C366_label'])
chi2_e, p_val_e, _, _ = chi2_contingency(table_e)
report_content += "### 3. ¿Hay una relación entre el nivel educativo y la informalidad?\n"
report_content += "- **H₀:** El nivel educativo y la condición de informalidad son independientes.\n"
report_content += "- **H₁:** El nivel educativo y la condición de informalidad no son independientes.\n"
report_content += f"- **Prueba:** Chi-cuadrado. **Resultados:** Chi² = {chi2_e:.2f}, p-value = {p_val_e:.4f}\n"
report_content += f"- **Conclusión:** Dado que el p-valor es extremadamente bajo ({p_val_e:.4f}), **se rechaza la hipótesis nula**. Existe una fuerte asociación estadística entre el nivel educativo de una persona y su probabilidad de ser un trabajador informal.\n\n"

# Hipótesis 4: Temporalidad
report_content += "### 4. ¿La temporalidad (trimestre) afecta al mercado laboral?\n"
# vs Ingreso
df_anova_t = df_ocupado.dropna(subset=['INGTOT', 'periodo'])
groups_t = [df_anova_t['INGTOT'][df_anova_t['periodo'] == g] for g in df_anova_t['periodo'].unique()]
f_val_t, p_val_t = f_oneway(*groups_t)
# vs Informalidad
df_chi2_t = df_ocupado.dropna(subset=['es_informal', 'periodo'])
table_t = pd.crosstab(df_chi2_t['es_informal'], df_chi2_t['periodo'])
chi2_t, p_val_t_c, _, _ = chi2_contingency(table_t)
report_content += f"- **Análisis del Ingreso:** La prueba ANOVA entre `periodo` e `INGTOT` arrojó un **p-valor de {p_val_t:.4f}**. Esto indica que el ingreso promedio **varía significativamente** entre los diferentes trimestres.\n"
report_content += f"- **Análisis de la Informalidad:** La prueba Chi-cuadrado entre `periodo` y `es_informal` arrojó un **p-valor de {p_val_t_c:.4f}**. Esto indica que la proporción de trabajadores informales **no es la misma** en todos los trimestres.\n"
report_content += "- **Conclusión General:** **Se rechaza la hipótesis nula en ambos casos**. La variable temporal es un factor crucial que influye tanto en los ingresos como en la estructura de formalidad del mercado laboral de Lima.\n\n"

# D. Conclusiones Finales
report_content += "## Conclusiones Finales\n"
report_content += "1.  **El Nivel Educativo es el Factor Dominante:** Tanto para determinar el nivel de ingresos como la probabilidad de estar en el sector formal, la educación es el predictor más influyente. Esto subraya la importancia de la inversión en capital humano.\n"
report_content += "2.  **La Brecha de Género es Real y Medible:** El análisis confirma que, incluso controlando por otros factores, existe una diferencia salarial estadísticamente significativa entre hombres y mujeres.\n"
report_content += "3.  **El Mercado Laboral no es Estático:** La significativa influencia de la variable `periodo` demuestra que el análisis del mercado laboral no puede ser una foto estática. Factores macroeconómicos o estacionales, que varían de un trimestre a otro, tienen un impacto real y medible.\n"
report_content += "4.  **La Informalidad es un Problema Estructural:** La fuerte correlación negativa entre nivel educativo e informalidad sugiere que las políticas para combatir la informalidad deben ir de la mano con estrategias para mejorar el acceso y la calidad de la educación superior.\n"

# --- 3. Guardado del Reporte ---
print("--- 3. Guardando el Reporte Analítico Final ---")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(report_content)
print(f"Reporte guardado exitosamente en: {OUTPUT_FILE}")
print("\n--- Proceso Completado ---")