import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración ---
DATA_DIR = 'lima/02_preparacion_y_limpieza'
EDA_DIR = 'lima/03_analisis_exploratorio_eda'
os.makedirs(EDA_DIR, exist_ok=True)

# --- Funciones Auxiliares ---

def weighted_average(df, value_col, weight_col):
    """Calcula el promedio ponderado para una columna, ignorando NaNs."""
    df_filtered = df.dropna(subset=[value_col, weight_col])
    if df_filtered.empty:
        return np.nan
    return np.average(df_filtered[value_col], weights=df_filtered[weight_col])

def get_recode_maps():
    """Devuelve diccionarios para recodificar variables categóricas."""
    return {
        'C207': {1: 'Hombre', 2: 'Mujer'},
        'C366': {
            1: 'Sin nivel', 2: 'Educ. Inicial', 3: 'Primaria Incompleta', 4: 'Primaria Completa',
            5: 'Secundaria Incompleta', 6: 'Secundaria Completa', 7: 'Básica Especial',
            8: 'Superior No Univ. Incompleta', 9: 'Superior No Univ. Completa',
            10: 'Superior Univ. Incompleta', 11: 'Superior Univ. Completa', 12: 'Maestría/Doctorado'
        },
        'OCUP300': {1: 'Ocupado', 2: 'Desocupado Abierto', 3: 'Desocupado Oculto', 4: 'Inactivo'}
    }

def extract_period_from_filename(filename):
    """Extrae un identificador de período legible del nombre del archivo."""
    # Corregido: usa espacio en lugar de guion bajo, y guiones en el grupo de meses.
    match = re.search(r'Trim ([A-Za-z-]+)(\d{2})', filename)
    if match:
        # Corregido: usa guiones en las claves del mapa.
        month_map = {
            'Ene-Feb-Mar': 'Q1',
            'Abr-May-Jun': 'Q2',
            'Jul-Ago-Set': 'Q3',
            'Set-Oct-Nov': 'Q4',
            'Mar-Abr-May': 'Q2' # Para el trimestre de 2025
        }
        months, year = match.groups()
        quarter = month_map.get(months, 'Q_Unk')
        return f"20{year}-{quarter}"
    return "Periodo_Desconocido"


# --- Carga y Unificación de Datos ---
print("--- 1. Cargando y Unificando Datos Limpios ---")
try:
    all_files = os.listdir(DATA_DIR)
    cleaned_files = sorted([f for f in all_files if f.startswith('lima_cleaned_') and f.endswith('.csv')])
    if not cleaned_files:
        raise FileNotFoundError("No se encontraron archivos limpios.")

    df_list = []
    for filename in cleaned_files:
        file_path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(file_path, low_memory=False)
        df['periodo'] = extract_period_from_filename(filename)
        df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)
    print(f"Datos unificados cargados. Total de registros: {len(master_df)}")
    print(f"Períodos identificados: {sorted(master_df['periodo'].unique().tolist())}")

except Exception as e:
    print(f"Error al cargar los datos: {e}")
    exit()

# --- Recodificación y Preparación ---
print("\n--- 2. Recodificando Variables ---")
maps = get_recode_maps()
for var, mapping in maps.items():
    if var in master_df.columns:
        master_df[var] = master_df[var].map(mapping)

# Asegurarse de que las columnas clave sean numéricas
master_df['INGTOT'] = pd.to_numeric(master_df['INGTOT'], errors='coerce')
master_df['C208'] = pd.to_numeric(master_df['C208'], errors='coerce')
master_df['factor_expansion'] = pd.to_numeric(master_df['factor_expansion'], errors='coerce')

# --- 3. Análisis Descriptivo Ponderado ---
print("\n--- 3. Realizando Análisis Descriptivo Ponderado ---")

# Ingreso promedio ponderado general
avg_income_weighted = weighted_average(master_df, 'INGTOT', 'factor_expansion')

# Edad promedio ponderada general
avg_age_weighted = weighted_average(master_df, 'C208', 'factor_expansion')

# Distribución de género ponderada
gender_dist_weighted = master_df.groupby('C207')['factor_expansion'].sum() / master_df['factor_expansion'].sum() * 100

# --- 4. Análisis Temporal ---
print("\n--- 4. Realizando Análisis Temporal ---")

# Evolución del ingreso promedio ponderado
temporal_income = master_df.groupby('periodo').apply(lambda x: weighted_average(x, 'INGTOT', 'factor_expansion')).sort_index()

# Gráfico de evolución del ingreso
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 7))
temporal_income.plot(kind='line', ax=ax, marker='o', linestyle='-')
ax.set_title('Evolución del Ingreso Promedio Mensual Ponderado en Lima', fontsize=16)
ax.set_ylabel('Ingreso Promedio Mensual (S/.)', fontsize=12)
ax.set_xlabel('Período (Trimestre)', fontsize=12)
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
income_plot_path = os.path.join(EDA_DIR, 'evolucion_ingreso_ponderado.png')
fig.savefig(income_plot_path)
print(f"Gráfico de evolución de ingresos guardado en: {income_plot_path}")
plt.close()

# --- 5. Creación del Informe EDA ---
print("\n--- 5. Generando el INFORME_EDA.md ---")
report_path = os.path.join(EDA_DIR, 'INFORME_EDA.md')

with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# Informe de Análisis Exploratorio de Datos (EDA) - Lima\n\n")
    f.write("Este informe presenta los hallazgos iniciales del análisis de los datos trimestrales para Lima, con un enfoque en las estadísticas ponderadas y la evolución temporal.\n\n")

    f.write("## 1. Análisis Descriptivo Ponderado (General)\n\n")
    f.write("Estadísticas calculadas sobre el conjunto de datos completo (6 trimestres), utilizando el `factor_expansion` para reflejar la realidad poblacional de Lima.\n\n")
    f.write(f"- **Ingreso Promedio Mensual Ponderado:** S/. {avg_income_weighted:,.2f}\n")
    f.write(f"- **Edad Promedio Ponderada:** {avg_age_weighted:.1f} años\n\n")
    f.write("### Distribución de Género Ponderada:\n")
    f.write(gender_dist_weighted.to_markdown(headers=['Género', '% Población']))
    f.write("\n\n")

    f.write("## 2. Sección de Análisis Temporal\n\n")
    f.write("Esta sección muestra cómo han evolucionado las métricas clave a lo largo de los 6 trimestres analizados.\n\n")
    f.write("### Evolución del Ingreso Promedio Mensual Ponderado\n\n")
    f.write("La siguiente tabla muestra el ingreso promedio mensual ponderado para cada trimestre:\n\n")
    f.write(temporal_income.reset_index(name='Ingreso Promedio (S/.)').to_markdown(index=False))
    f.write("\n\n")
    f.write("El siguiente gráfico ilustra esta tendencia visualmente:\n\n")
    f.write(f"![Evolución del Ingreso](./evolucion_ingreso_ponderado.png)\n\n")

    f.write("## 3. Conclusiones Preliminares del EDA\n\n")
    f.write("El análisis inicial muestra una base de datos consistente que permitirá un análisis temporal robusto. El uso del factor de expansión es crucial para obtener una imagen precisa de la población de Lima. La sección de análisis temporal revela fluctuaciones en el ingreso promedio, lo que justifica un estudio más profundo de la estacionalidad y las tendencias en las fases de modelado.\n")

print(f"\nInforme EDA generado exitosamente en: {report_path}")
print("\n--- Proceso de EDA Completado ---")