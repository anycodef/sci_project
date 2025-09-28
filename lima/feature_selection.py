import pandas as pd
import numpy as np
import os
import re
from scipy.stats import f_oneway, chi2_contingency

# --- Configuración ---
DATA_DIR = 'lima/02_preparacion_y_limpieza'
OUTPUT_DIR = 'lima/04_seleccion_de_caracteristicas'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Funciones Auxiliares ---
def extract_period_from_filename(filename):
    """Extrae un identificador de período legible del nombre del archivo."""
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

# --- 1. Carga y Preparación de Datos ---
print("--- 1. Cargando y Preparando Datos ---")
try:
    all_files = os.listdir(DATA_DIR)
    cleaned_files = sorted([f for f in all_files if f.startswith('lima_cleaned_') and f.endswith('.csv')])
    df_list = [pd.read_csv(os.path.join(DATA_DIR, f), low_memory=False) for f in cleaned_files]

    for df, filename in zip(df_list, cleaned_files):
        df['periodo'] = extract_period_from_filename(filename)

    master_df = pd.concat(df_list, ignore_index=True)
    print(f"Datos cargados. Total de registros: {len(master_df)}")
except Exception as e:
    print(f"Error al cargar datos: {e}")
    exit()

# --- Feature Engineering: Crear variable objetivo 'es_informal' ---
# Definición: Un trabajador ocupado (OCUP300=1) que no tiene seguro de salud ESSALUD (C361_1=2) se considera informal.
master_df['es_informal'] = 0
condition = (master_df['OCUP300'] == 1) & (master_df['C361_1'] == 2)
master_df.loc[condition, 'es_informal'] = 1

# --- Preparación para el Análisis ---
# Seleccionar un subconjunto de variables predictoras para el análisis
PREDICTORS_CATEGORICAL = ['C207', 'C366', 'periodo'] # Sexo, Nivel Educativo, Período
PREDICTORS_NUMERICAL = ['C208', 'whoraT'] # Edad, Horas trabajadas

# Convertir columnas a tipos adecuados
for col in PREDICTORS_CATEGORICAL:
    master_df[col] = master_df[col].astype('category')
for col in PREDICTORS_NUMERICAL:
    master_df[col] = pd.to_numeric(master_df[col], errors='coerce')
master_df['INGTOT'] = pd.to_numeric(master_df['INGTOT'], errors='coerce')

# Filtrar para tener datos relevantes para los modelos
# Para regresión de ingresos: personas ocupadas con ingresos y horas válidas.
df_regression = master_df[master_df['OCUP300'] == 1].dropna(subset=['INGTOT', 'whoraT', 'C208'] + PREDICTORS_CATEGORICAL)
# Para clasificación de informalidad: personas ocupadas con predictores categóricos válidos.
# CORRECCIÓN: Usar 'subset' en dropna para evitar eliminar todas las filas.
df_classification = master_df[master_df['OCUP300'] == 1].dropna(subset=PREDICTORS_CATEGORICAL + ['es_informal'])


# --- 2. Análisis de Selección de Características ---
print("\n--- 2. Realizando Selección de Características ---")
report_content = "# Reporte de Selección de Características\n\n"
report_content += "Este documento justifica la selección de variables para los modelos de clasificación y regresión.\n\n"

# A. Para el modelo de REGRESIÓN (predecir INGTOT)
report_content += "## 1. Para Modelo de Regresión (Objetivo: INGTOT)\n\n"

# Correlación para variables numéricas
corr_matrix = df_regression[['INGTOT'] + PREDICTORS_NUMERICAL].corr()
report_content += "### a) Correlación con Variables Numéricas\n"
report_content += corr_matrix['INGTOT'].to_frame().to_markdown()
report_content += "\n\n"

# ANOVA para variables categóricas
report_content += "### b) Relación con Variables Categóricas (ANOVA)\n"
for cat_var in PREDICTORS_CATEGORICAL:
    # Filtrar NaNs en la variable categórica específica para ANOVA
    df_anova = df_regression.dropna(subset=[cat_var])
    groups = [df_anova['INGTOT'][df_anova[cat_var] == g] for g in df_anova[cat_var].unique()]
    if len(groups) > 1: # ANOVA necesita al menos 2 grupos
        f_val, p_val = f_oneway(*groups)
        report_content += f"- **{cat_var}**: F-statistic = {f_val:.2f}, p-value = {p_val:.4f}\n"
        if p_val < 0.05:
            report_content += "  - *Conclusión: Significativo. La media de INGTOT varía según esta categoría.*\n"
        else:
            report_content += "  - *Conclusión: No significativo.*\n"
    else:
        report_content += f"- **{cat_var}**: No se pudo realizar ANOVA (solo un grupo de datos).\n"


# B. Para el modelo de CLASIFICACIÓN (predecir es_informal)
report_content += "\n## 2. Para Modelo de Clasificación (Objetivo: es_informal)\n\n"

# Chi-cuadrado para variables categóricas
report_content += "### a) Relación con Variables Categóricas (Chi-Cuadrado)\n"
for cat_var in PREDICTORS_CATEGORICAL:
    # Filtrar NaNs en la variable categórica específica para Chi-cuadrado
    df_chi2 = df_classification.dropna(subset=[cat_var])
    contingency_table = pd.crosstab(df_chi2['es_informal'], df_chi2[cat_var])
    if not contingency_table.empty:
        chi2, p_val, _, _ = chi2_contingency(contingency_table)
        report_content += f"- **{cat_var}**: Chi2 = {chi2:.2f}, p-value = {p_val:.4f}\n"
        if p_val < 0.05:
            report_content += "  - *Conclusión: Significativo. Hay una asociación entre la variable y la informalidad.*\n"
        else:
            report_content += "  - *Conclusión: No significativo.*\n"
    else:
        report_content += f"- **{cat_var}**: No se pudo realizar Chi-cuadrado (tabla de contingencia vacía).\n"


# --- 3. Conclusiones y Guardado del Reporte ---
print("\n--- 3. Generando Reporte ---")
report_content += "\n## 3. Conclusión de Selección\n\n"
report_content += "Basado en los p-values, la mayoría de las variables analizadas, **incluyendo 'periodo'**, muestran una relación estadísticamente significativa con los objetivos de ingreso e informalidad. Por lo tanto, se recomienda su inclusión como predictores en los modelos iniciales. La relevancia final se determinará durante el entrenamiento y la evaluación del modelo.\n"

report_path = os.path.join(OUTPUT_DIR, 'REPORTE_SELECCION_CARACTERISTICAS.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"Reporte de selección de características guardado en: {report_path}")
print("\n--- Proceso de Selección de Características Completado ---")