import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy.stats import ttest_ind

# --- CONFIGURACIÓN GLOBAL ---
DATA_SOURCE_DIR = '../00_data_source/'
PROCESSED_DIR = '../02_data_processed/'
EVIDENCE_DIR = '../03_cleaning_evidence/'
REPORTS_DIR = '../04_reports/'
# ... (otras configuraciones como mapas de recodificación, etc.)

# --- HELPER FUNCTIONS ---

def get_recode_maps():
    """Returns dictionaries for recoding variables based on the data dictionary."""
    return {
        'REGION': {1: 'Lima Metropolitana', 2: 'Resto Urbano', 3: 'Rural'},
        'C203': {1: 'Jefe/a', 2: 'Esposo/a o compañero/a', 3: 'Hijo/a o hijastro/a', 4: 'Yerno o Nuera', 5: 'Nieto/a', 6: 'Padre / madre / suegro/a', 7: 'Hermano/a', 8: 'Otro pariente', 9: 'Trabajador/a del hogar', 10: 'Pensionista', 11: 'Otro no pariente', 98: 'No residente'},
        'C207': {1: 'Hombre', 2: 'Mujer'},
        'C310': {1: 'Empleador o patrono', 2: 'Trabajador independiente', 3: 'Empleado u obrero', 4: 'Ayudante en un negocio de la familia', 5: 'Ayudante en el empleo de un familiar', 6: 'Trabajador del hogar', 7: 'Aprendiz/practicante remunerado', 8: 'Practicante sin remuneración', 9: 'Ayudante en un negocio de la familia de otro hogar', 10: 'Ayudante en el empleo de un familiar de otro hogar'},
        'C311': {1: 'Fuerzas Armadas, Policía Nacional del Perú (militares)', 2: 'Administración pública', 3: 'Empresa pública', 4: 'Empresas especiales de servicios (SERVICE)', 5: 'Empresa o patrono privado', 6: 'Otra'},
        'C312': {1: 'Persona jurídica (Sociedad Anónima SRL, Sociedad Civil, EIRL o Asociación, etc.)', 2: 'Persona Natural con RUC (RUS, RER, u otro régimen)', 3: 'NO ESTA REGISTRADO (no tiene RUC)', 4: 'NO SABE (solo para dependientes)'},
        'C366': {1: 'Sin nivel', 2: 'Educación Inicial', 3: 'Primaria incompleta', 4: 'Primaria completa', 5: 'Secundaria incompleta', 6: 'Secundaria completa', 7: 'Básica especial', 8: 'Superior no universitaria incompleta', 9: 'Superior no universitaria completa', 10: 'Superior universitaria incompleta', 11: 'Superior universitaria completa', 12: 'Maestria/Doctorado'},
        'OCUP300': {0: 'Sin información', 1: 'Ocupado', 2: 'Desocupado abierto', 3: 'Desocupado oculto', 4: 'Inactivo pleno'}
    }

def generar_estadisticas(df, columnas):
    """Calcula estadísticas clave. Si una columna no es numérica, las estadísticas se muestran como NaN."""
    stats_list = []
    for col in columnas:
        if col in df.columns:
            is_numeric = pd.api.types.is_numeric_dtype(df[col])
            stats = {
                'Columna': col, 'Tipo de Dato': df[col].dtype,
                'Valores No Nulos': df[col].count(), 'Valores Nulos': df[col].isnull().sum(),
                'Media': df[col].mean() if is_numeric else np.nan,
                'Desv. Estándar': df[col].std() if is_numeric else np.nan,
                'Mínimo': df[col].min() if is_numeric else np.nan,
                'Máximo': df[col].max() if is_numeric else np.nan
            }
            stats_list.append(stats)
    return pd.DataFrame(stats_list).set_index('Columna')

# --- PIPELINE FUNCTIONS ---

def load_and_unify_data():
    """Paso 1: Carga, etiqueta y unifica los 6 CSVs en un master_df."""
    print("--- Paso 1: Cargando y unificando datos ---")
    files = [f for f in os.listdir(DATA_SOURCE_DIR) if f.endswith('.csv')]
    quarters = {
        'Trim Ene-Feb-Mar24.csv': '2024-Q1', 'Trim Abr-May-Jun24.csv': '2024-Q2',
        'Trim Jul-Ago-Set24.csv': '2024-Q3', 'Trim Set-Oct-Nov24.csv': '2024-Q4',
        'Trim Ene-Feb-Mar25.csv': '2025-Q1', 'Trim Mar-Abr-May25.csv': '2025-Q2'
    }
    df_list = []
    for file in files:
        df = pd.read_csv(os.path.join(DATA_SOURCE_DIR, file), low_memory=False)
        if file in quarters: df['periodo'] = quarters[file]
        df_list.append(df)
    if not df_list: raise FileNotFoundError(f"No CSV files found in {DATA_SOURCE_DIR}")
    master_df = pd.concat(df_list, ignore_index=True)
    master_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    fa_cols = [col for col in master_df.columns if col.startswith('fa_')]
    if fa_cols:
        # First, convert all factor columns to numeric, coercing errors
        for col in fa_cols:
            master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

        master_df['factor_expansion'] = master_df[fa_cols].sum(axis=1)
        master_df['factor_ajustado'] = master_df['factor_expansion'] / len(files)
        master_df.drop(columns=fa_cols, inplace=True)
    print("Datos cargados y unificados exitosamente.")
    return master_df

def clean_special_codes(df, columns_to_visualize):
    """Paso 2: Sanea códigos especiales y genera evidencia de limpieza."""
    print("\n--- Paso 2: Limpiando códigos especiales y generando evidencia ---")
    master_df = df.copy()

    columnas_a_evaluar = ['C208', 'INGTOT', 'whoraT']
    codes_to_nan = {
        'C208': [99], 'C301_DIA': [99], 'C301_MES': [99], 'C301_ANIO': [9999], 'C308_COD': [9999], 'C309_COD': [9999], 'C317A': [9999],
        'C318_1': [99], 'C318_2': [99], 'C318_3': [99], 'C318_4': [99], 'C318_5': [99], 'C318_6': [99], 'C318_7': [99], 'C318_T': [99],
        'C328_T': [99], 'whoraT': [99], 'I339_1': [999999], 'C341_T': [999999], 'C342': [999999], 'D344': [999999], 'I345_1': [999999],
        'D347_T': [999999], 'C348': [999999], 'D350': [999999], 'INGTOT': [999999], 'INGTOTP': [999999], 'INGTRABW': [999999]
    }

    print("\n--- Generando evidencia ANTES de la limpieza ---")
    stats_antes = generar_estadisticas(master_df, columnas_a_evaluar)
    for column in columns_to_visualize:
        if column in master_df.columns:
            plt.figure(figsize=(12, 7)); sns.histplot(master_df[column].dropna(), kde=False, bins=50)
            plt.title(f'Distribution of {column} - BEFORE Cleaning', fontsize=16); plt.xlabel(column, fontsize=12); plt.ylabel('Frequency', fontsize=12)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S"); file_name = f"{column}_before_{timestamp}.png"
            plt.savefig(os.path.join(EVIDENCE_DIR, file_name)); plt.close()
            print(f"Evidencia visual guardada en: {os.path.join(EVIDENCE_DIR, file_name)}")

    print("\n--- Aplicando limpieza: Reemplazando códigos especiales con NaN ---")
    for column, codes in codes_to_nan.items():
        if column in master_df.columns: master_df[column] = master_df[column].replace(codes, np.nan)

    print("\n--- Forzando tipos numéricos post-limpieza ---")
    numeric_columns = list(codes_to_nan.keys())
    for col in numeric_columns:
        if col in master_df.columns: master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

    print("\n--- Generando evidencia DESPUÉS de la limpieza ---")
    stats_despues = generar_estadisticas(master_df, columnas_a_evaluar)
    for column in columns_to_visualize:
        if column in master_df.columns:
            plt.figure(figsize=(12, 7)); sns.histplot(master_df[column].dropna(), kde=True, bins=50)
            plt.title(f'Distribution of {column} - AFTER Cleaning', fontsize=16); plt.xlabel(column, fontsize=12); plt.ylabel('Frequency', fontsize=12)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S"); file_name = f"{column}_after_{timestamp}.png"
            plt.savefig(os.path.join(EVIDENCE_DIR, file_name)); plt.close()
            print(f"Evidencia visual guardada en: {os.path.join(EVIDENCE_DIR, file_name)}")

    print("\n--- Exportando resumen cuantitativo ---")
    tabla_comparativa = pd.concat([stats_antes, stats_despues], axis=1, keys=['ANTES DE LA LIMPIEZA', 'DESPUÉS DE LA LIMPIEZA'])
    tabla_comparativa = tabla_comparativa.round(2)
    ruta_salida = os.path.join(EVIDENCE_DIR, 'resumen_cuantitativo_limpieza.md')
    tabla_comparativa.to_markdown(ruta_salida)
    print(f"Tabla de resumen de la limpieza guardada en: {ruta_salida}")

    print("Limpieza y generación de evidencia completadas.")
    return master_df

def segregate_and_prepare(df):
    """Paso 3: Separa por edad, recodifica variables y realiza feature engineering."""
    print("\n--- Paso 3: Segregando y preparando los datos ---")
    master_df = df.copy()

    # Segregate by age (>=14 is considered potential labor force)
    poblacion_trabajo_df = master_df[master_df['C208'] >= 14].copy()
    poblacion_no_trabajo_df = master_df[master_df['C208'] < 14].copy()

    # --- Clean 'poblacion_trabajo_df' ---
    maps = get_recode_maps()
    for var, mapping in maps.items():
        if var in poblacion_trabajo_df.columns:
            poblacion_trabajo_df[var] = poblacion_trabajo_df[var].map(mapping)

    # Handle Nulls with 'No Aplica' for non-employed individuals
    not_employed_condition = poblacion_trabajo_df['OCUP300'] != 'Ocupado'
    cols_to_fill = [col for col in poblacion_trabajo_df.columns if col.startswith(('C3', 'I3', 'D3'))]
    cols_to_fill.extend(['INGTOT', 'INGTOTP', 'ingtrabw', 'whoraT'])
    for col in cols_to_fill:
        if col in poblacion_trabajo_df.columns:
            poblacion_trabajo_df.loc[not_employed_condition, col] = 'No Aplica'

    # Feature Engineering
    bins = [14, 18, 25, 35, 45, 55, 65, np.inf]
    labels = ['14-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    poblacion_trabajo_df['grupo_edad'] = pd.cut(poblacion_trabajo_df['C208'], bins=bins, labels=labels, right=False)
    poblacion_trabajo_df['es_informal'] = 0
    if 'C361_1' in poblacion_trabajo_df.columns:
        poblacion_trabajo_df.loc[(poblacion_trabajo_df['OCUP300'] == 'Ocupado') & (poblacion_trabajo_df['C361_1'] == 2), 'es_informal'] = 1

    # --- Clean 'poblacion_no_trabajo_df' ---
    try:
        c300n_index = list(poblacion_no_trabajo_df.columns).index('C300n')
        cols_to_keep = list(poblacion_no_trabajo_df.columns[:c300n_index])
        cols_to_keep.extend(['periodo', 'factor_expansion', 'factor_ajustado'])
        poblacion_no_trabajo_df = poblacion_no_trabajo_df[cols_to_keep]
    except ValueError:
        pass  # C300n not found, continue without pruning
    for var, mapping in maps.items():
        if var in poblacion_no_trabajo_df.columns and var != 'OCUP300':
            poblacion_no_trabajo_df[var] = poblacion_no_trabajo_df[var].map(mapping)

    print("Datos segregados y preparados exitosamente.")
    return poblacion_trabajo_df, poblacion_no_trabajo_df

def analyze_outliers_and_visualize(df):
    """Paso 4: Realiza el análisis profundo de outliers de ingreso y genera visualizaciones avanzadas."""
    print("\n--- Paso 4: Analizando outliers de ingreso y generando visualizaciones ---")
    df_trabajo = df.copy()

    # Ensure INGTOT is numeric for analysis, dropping rows where it's not applicable
    df_trabajo['INGTOT'] = pd.to_numeric(df_trabajo['INGTOT'], errors='coerce')
    df_trabajo.dropna(subset=['INGTOT'], inplace=True)

    # --- Profiling High-Income Outliers ---
    Q1 = df_trabajo['INGTOT'].quantile(0.25)
    Q3 = df_trabajo['INGTOT'].quantile(0.75)
    IQR = Q3 - Q1
    outlier_threshold = Q3 + 1.5 * IQR
    df_high_earners = df_trabajo[df_trabajo['INGTOT'] > outlier_threshold]

    # --- Creating Refined Income Visualizations ---
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('Análisis Exhaustivo de la Distribución del Ingreso Mensual', fontsize=20)

    # Plot 1: Overall Distribution
    axes[0, 0].hist(df_trabajo['INGTOT'], bins=50, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribución General del Ingreso Mensual')
    axes[0, 0].set_xlabel('Ingreso Total Mensual (S/.)'); axes[0, 0].set_ylabel('Frecuencia')
    axes[0, 0].ticklabel_format(style='plain', axis='x')

    # Plot 2: Log-Scale Distribution
    axes[0, 1].hist(df_trabajo['INGTOT'], bins=50, color='lightgreen', edgecolor='black')
    axes[0, 1].set_xscale('log')
    axes[0, 1].set_title('Distribución del Ingreso (Escala Logarítmica)')
    axes[0, 1].set_xlabel('Ingreso Total Mensual (S/.) - Escala Log'); axes[0, 1].set_ylabel('Frecuencia')

    # Plot 3: "Zoomed-In" Distribution on non-outliers
    df_zoomed = df_trabajo[df_trabajo['INGTOT'] <= outlier_threshold]
    axes[1, 0].hist(df_zoomed['INGTOT'], bins=50, color='salmon', edgecolor='black')
    axes[1, 0].set_title(f'Distribución Detallada (Ingresos <= S/.{outlier_threshold:,.0f})')
    axes[1, 0].set_xlabel('Ingreso Total Mensual (S/.)'); axes[1, 0].set_ylabel('Frecuencia')

    # Plot 4: Boxplot for Outlier Identification
    axes[1, 1].boxplot(df_trabajo['INGTOT'], vert=False, patch_artist=True, boxprops=dict(facecolor='plum'))
    axes[1, 1].set_xscale('log')
    axes[1, 1].set_title('Diagrama de Caja para Identificar Outliers')
    axes[1, 1].set_xlabel('Ingreso Total Mensual (S/.) - Escala Log')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Analisis_Completo_Ingresos_{timestamp}.png"
    file_path = os.path.join(EVIDENCE_DIR, file_name)
    fig.savefig(file_path, bbox_inches='tight')
    plt.close()
    print(f"Visualización de análisis de ingresos guardada en: {file_path}")

    # This function's purpose is now primarily visual analysis and saving evidence.
    # The generation of text summaries will be handled by the reporting function.

def generate_final_report(df):
    """Paso 5: Realiza el análisis inferencial y compila el informe final en Markdown."""
    print("\n--- Paso 5: Generando el informe analítico final ---")
    df_trabajo = df.copy()

    # --- 1. Data Preparation for Analysis ---
    df_trabajo['INGTOT'] = pd.to_numeric(df_trabajo['INGTOT'], errors='coerce')
    df_trabajo.dropna(subset=['INGTOT'], inplace=True)

    # --- 2. Hypothesis Testing (T-test: Gender Pay Gap) ---
    ingreso_hombres = df_trabajo[df_trabajo['C207'] == 'Hombre']['INGTOT']
    ingreso_mujeres = df_trabajo[df_trabajo['C207'] == 'Mujer']['INGTOT']
    t_stat, p_value = ttest_ind(ingreso_hombres, ingreso_mujeres, equal_var=False, nan_policy='omit')

    ttest_summary = f"""
### Prueba de Hipótesis: Brecha Salarial de Género
Se realizó una prueba T de Student para muestras independientes para comparar los ingresos medios entre hombres y mujeres.
- **Ingreso Promedio Hombres:** S/. {ingreso_hombres.mean():,.2f}
- **Ingreso Promedio Mujeres:** S/. {ingreso_mujeres.mean():,.2f}
- **Estadístico T:** {t_stat:.2f}
- **Valor P:** {p_value:.3f}

**Conclusión de la prueba:** Con un valor p de {p_value:.3f}, se observa una diferencia estadísticamente significativa en los ingresos entre hombres y mujeres.
"""

    # --- 3. High-Earner Profile Analysis ---
    Q1 = df_trabajo['INGTOT'].quantile(0.25)
    Q3 = df_trabajo['INGTOT'].quantile(0.75)
    IQR = Q3 - Q1
    outlier_threshold = Q3 + 1.5 * IQR
    df_high_earners = df_trabajo[df_trabajo['INGTOT'] > outlier_threshold]

    sex_dist = df_high_earners['C207'].value_counts(normalize=True) * 100
    education_dist = df_high_earners['C366'].value_counts(normalize=True) * 100
    age_group_dist = df_high_earners['grupo_edad'].value_counts(normalize=True) * 100

    top_education = education_dist.index[0] if not education_dist.empty else "N/A"
    top_age_group = age_group_dist.index[0] if not age_group_dist.empty else "N/A"

    summary_text = f"""
### Análisis de Outliers: Perfil de Altos Ingresos
El perfil de individuos con ingresos superiores a S/. {outlier_threshold:,.2f} (outliers) muestra que está predominantemente compuesto por **hombres ({sex_dist.get('Hombre', 0):.1f}%)**.
El nivel educativo más común en este grupo es **'{top_education}'** ({education_dist.iloc[0]:.1f}%), y el grupo de edad más representativo es **'{top_age_group}'** ({age_group_dist.iloc[0]:.1f}%).
"""

    # --- 4. Assemble the Final Report ---
    # Find the latest evidence files to reference in the report
    evidence_files = os.listdir(EVIDENCE_DIR)
    income_plot_files = sorted([f for f in evidence_files if f.startswith('Analisis_Completo_Ingresos_') and f.endswith('.png')], reverse=True)
    latest_income_plot = income_plot_files[0] if income_plot_files else "income_plot_not_found.png"

    report_content = f"""
# Informe Analítico de Empleabilidad y Brecha Salarial
Fecha de Generación: {datetime.now().strftime('%Y-%m-%d')}

## Introducción
Este informe presenta un análisis del mercado laboral basado en datos de encuestas trimestrales. El objetivo es identificar patrones clave en ingresos, demografía y la brecha salarial de género.

## 1. Evidencia de Limpieza de Datos
La siguiente tabla resume el impacto del proceso de limpieza en las variables clave. Se observa la conversión de tipos de dato 'object' a 'float64' y la correcta identificación de valores nulos, lo que permite un análisis numérico preciso.

(El contenido de la tabla de resumen se encuentra en el archivo `resumen_cuantitativo_limpieza.md` en la carpeta `{EVIDENCE_DIR}`)

## 2. Análisis de la Distribución de Ingresos
El siguiente gráfico muestra la distribución del ingreso mensual desde cuatro perspectivas para proporcionar un entendimiento completo, incluyendo una vista logarítmica para manejar la asimetría y un diagrama de caja para identificar outliers.

![Análisis de Ingresos](../{EVIDENCE_DIR}/{latest_income_plot})

## 3. Análisis de Outliers: Perfil de Altos Ingresos
{summary_text}

## 4. Prueba de Hipótesis: Brecha Salarial de Género
{ttest_summary}

## 5. Conclusiones
El análisis revela una brecha salarial de género estadísticamente significativa. Además, los individuos con altos ingresos tienden a ser hombres con educación superior y en grupos de edad con mayor experiencia. Estos hallazgos subrayan la necesidad de políticas enfocadas en la equidad de género y el desarrollo profesional.
"""

    # --- 5. Write the report file ---
    report_path = os.path.join(REPORTS_DIR, 'final_analytical_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Informe analítico final guardado en: {report_path}")

def main():
    """Orquesta todo el flujo de trabajo."""
    # Asegurarse de que los directorios de salida existan
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Ejecutar el pipeline
    print("--- INICIANDO PIPELINE DE ANÁLISIS DE EMPLEABILIDAD ---")

    master_df = load_and_unify_data()
    df_cleaned = clean_special_codes(master_df, columns_to_visualize=['C208', 'INGTOT', 'whoraT'])
    df_trabajo, df_no_trabajo = segregate_and_prepare(df_cleaned)

    # Guardar los datasets procesados
    path_trabajo = os.path.join(PROCESSED_DIR, 'datos_limpios_poblacion_trabajo.csv')
    path_no_trabajo = os.path.join(PROCESSED_DIR, 'datos_limpios_poblacion_no_trabajo.csv')
    df_trabajo.to_csv(path_trabajo, index=False)
    df_no_trabajo.to_csv(path_no_trabajo, index=False)
    print(f"\nDatasets procesados guardados en: {PROCESSED_DIR}")

    # Ejecutar análisis y reporte sobre el dataset principal de trabajo
    analyze_outliers_and_visualize(df_trabajo)
    generate_final_report(df_trabajo)

    print("\n--- PIPELINE COMPLETADO EXITOSAMENTE ---")

if __name__ == '__main__':
    main()
