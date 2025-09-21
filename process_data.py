import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def get_recode_maps():
    """Returns dictionaries for recoding variables based on the data dictionary."""
    maps = {
        'REGION': {1: 'Lima Metropolitana', 2: 'Resto Urbano', 3: 'Rural'},
        'C203': {
            1: 'Jefe/a', 2: 'Esposo/a o compañero/a', 3: 'Hijo/a o hijastro/a',
            4: 'Yerno o Nuera', 5: 'Nieto/a', 6: 'Padre / madre / suegro/a',
            7: 'Hermano/a', 8: 'Otro pariente', 9: 'Trabajador/a del hogar',
            10: 'Pensionista', 11: 'Otro no pariente', 98: 'No residente'
        },
        'C207': {1: 'Hombre', 2: 'Mujer'},
        'C310': {
            1: 'Empleador o patrono', 2: 'Trabajador independiente', 3: 'Empleado u obrero',
            4: 'Ayudante en un negocio de la familia', 5: 'Ayudante en el empleo de un familiar',
            6: 'Trabajador del hogar', 7: 'Aprendiz/practicante remunerado',
            8: 'Practicante sin remuneración', 9: 'Ayudante en un negocio de la familia de otro hogar',
            10: 'Ayudante en el empleo de un familiar de otro hogar'
        },
        'C311': {
            1: 'Fuerzas Armadas, Policía Nacional del Perú (militares)',
            2: 'Administración pública', 3: 'Empresa pública',
            4: 'Empresas especiales de servicios (SERVICE)', 5: 'Empresa o patrono privado',
            6: 'Otra'
        },
        'C312': {
            1: 'Persona jurídica (Sociedad Anónima SRL, Sociedad Civil, EIRL o Asociación, etc.)',
            2: 'Persona Natural con RUC (RUS, RER, u otro régimen)',
            3: 'NO ESTA REGISTRADO (no tiene RUC)', 4: 'NO SABE (solo para dependientes)'
        },
        'C366': {
            1: 'Sin nivel', 2: 'Educación Inicial', 3: 'Primaria incompleta',
            4: 'Primaria completa', 5: 'Secundaria incompleta', 6: 'Secundaria completa',
            7: 'Básica especial', 8: 'Superior no universitaria incompleta',
            9: 'Superior no universitaria completa', 10: 'Superior universitaria incompleta',
            11: 'Superior universitaria completa', 12: 'Maestria/Doctorado'
        },
        'OCUP300': {
            0: 'Sin información', 1: 'Ocupado', 2: 'Desocupado abierto', 3: 'Desocupado oculto', 4: 'Inactivo pleno'
        }
    }
    return maps

def generar_estadisticas(df, columnas):
    """
    Calcula estadísticas clave para una lista de columnas en un DataFrame.
    Si una columna no es numérica, las estadísticas numéricas se muestran como NaN.
    """
    stats_list = []
    for col in columnas:
        if col in df.columns:
            # Check if the column dtype is numeric before calculating stats
            is_numeric = pd.api.types.is_numeric_dtype(df[col])

            stats = {
                'Columna': col,
                'Tipo de Dato': df[col].dtype,
                'Valores No Nulos': df[col].count(),
                'Valores Nulos': df[col].isnull().sum(),
                'Media': df[col].mean() if is_numeric else np.nan,
                'Desv. Estándar': df[col].std() if is_numeric else np.nan,
                'Mínimo': df[col].min() if is_numeric else np.nan,
                'Máximo': df[col].max() if is_numeric else np.nan
            }
            stats_list.append(stats)

    return pd.DataFrame(stats_list).set_index('Columna')

def process_data():
    # --- Phase 1: Data Loading and Unification ---
    files = [f for f in os.listdir('Empleabilidad') if f.endswith('.csv')]
    quarters = {
        'Trim Ene-Feb-Mar24.csv': '2024-Q1', 'Trim Abr-May-Jun24.csv': '2024-Q2',
        'Trim Jul-Ago-Set24.csv': '2024-Q3', 'Trim Set-Oct-Nov24.csv': '2024-Q4',
        'Trim Ene-Feb-Mar25.csv': '2025-Q1', 'Trim Mar-Abr-May25.csv': '2025-Q2'
    }

    df_list = []
    for file in files:
        df = pd.read_csv(os.path.join('Empleabilidad', file), low_memory=False)
        df['periodo'] = quarters[file]
        df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)
    master_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    # Lista de columnas representativas para la auditoría
    columnas_a_evaluar = ['C208', 'INGTOT', 'whoraT']

    # --- Phase 2: Visual Data Cleaning ---

    # Step A: Initial Setup and Configuration
    evidence_dir = 'cleaning_evidence'
    if not os.path.exists(evidence_dir):
        os.makedirs(evidence_dir)
        print(f"Directory '{evidence_dir}' created.")

    columns_to_visualize = ['C208', 'I339_1', 'whoraT']

    codes_to_nan = {
        'C208': [99], 'C301_DIA': [99], 'C301_MES': [99], 'C301_ANIO': [9999],
        'C308_COD': [9999], 'C309_COD': [9999], 'C317A': [9999],
        'C318_1': [99], 'C318_2': [99], 'C318_3': [99], 'C318_4': [99],
        'C318_5': [99], 'C318_6': [99], 'C318_7': [99], 'C318_T': [99],
        'C328_T': [99], 'whoraT': [99], 'I339_1': [999999], 'C341_T': [999999],
        'C342': [999999], 'D344': [999999], 'I345_1': [999999], 'D347_T': [999999],
        'C348': [999999], 'D350': [999999], 'INGTOT': [999999], 'INGTOTP': [999999],
        'INGTRABW': [999999]
    }

    # Step B: Generate "BEFORE" Visual Evidence
    print("\n--- Generating visual evidence BEFORE cleaning ---\n")
    for column in columns_to_visualize:
        if column in master_df.columns:
            plt.figure(figsize=(12, 7))
            sns.histplot(master_df[column].dropna(), kde=False, bins=50)
            plt.title(f'Distribution of {column} - BEFORE Cleaning', fontsize=16)
            plt.xlabel(column, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{column}_before_{timestamp}.png"
            file_path = os.path.join(evidence_dir, file_name)

            plt.savefig(file_path)
            plt.close()
            print(f"Evidence saved to: {file_path}")

    # --- Capture "BEFORE" statistics ---
    print("\n--- Capturando estadísticas ANTES de la limpieza ---")
    stats_antes = generar_estadisticas(master_df, columnas_a_evaluar)

    # Step C: Perform Data Sanitization
    print("\n--- Applying cleaning: Replacing special codes with NaN ---\n")
    for column, codes in codes_to_nan.items():
        if column in master_df.columns:
            master_df[column] = master_df[column].replace(codes, np.nan)

    print("\n--- Enforcing numeric types post-cleaning ---\n")
    numeric_columns = list(codes_to_nan.keys())
    # The original code extended with factor_expansion and factor_ajustado, let's keep that
    fa_cols = [col for col in master_df.columns if col.startswith('fa_')]
    numeric_columns.extend(fa_cols)
    # The user's code did not include these, but they are important from the original logic
    numeric_columns.extend(['factor_expansion', 'factor_ajustado'])


    for col in numeric_columns:
        if col in master_df.columns:
            master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

    # Step D: Generate "AFTER" Visual Evidence
    print("\n--- Generating visual evidence AFTER cleaning ---\n")
    for column in columns_to_visualize:
        if column in master_df.columns:
            plt.figure(figsize=(12, 7))
            sns.histplot(master_df[column].dropna(), kde=True, bins=50) # .dropna() is key
            plt.title(f'Distribution of {column} - AFTER Cleaning', fontsize=16)
            plt.xlabel(column, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{column}_after_{timestamp}.png"
            file_path = os.path.join(evidence_dir, file_name)

            plt.savefig(file_path)
            plt.close()
            print(f"Evidence saved to: {file_path}")

    # --- Capture "AFTER" statistics ---
    print("\n--- Capturando estadísticas DESPUÉS de la limpieza ---")
    stats_despues = generar_estadisticas(master_df, columnas_a_evaluar)

    # --- Generate and Export Quantitative Summary ---
    print("\n--- Generando tabla comparativa de limpieza ---")
    # Combinar los DataFrames con claves para crear un encabezado de múltiples niveles
    tabla_comparativa = pd.concat([stats_antes, stats_despues], axis=1, keys=['ANTES DE LA LIMPIEZA', 'DESPUÉS DE LA LIMPIEZA'])

    # Redondear valores numéricos para mejor legibilidad
    tabla_comparativa = tabla_comparativa.round(2)

    # Guardar la tabla en un archivo Markdown
    ruta_salida = 'cleaning_evidence/resumen_cuantitativo_limpieza.md'
    tabla_comparativa.to_markdown(ruta_salida)

    print(f"\nTabla de resumen de la limpieza guardada en: {ruta_salida}")
    print("\n--- Contenido de la Tabla de Resumen ---")
    print(tabla_comparativa.to_markdown())

    # --- Unify and Adjust Expansion Factor ---
    master_df['factor_expansion'] = master_df[fa_cols].sum(axis=1)
    master_df['factor_ajustado'] = master_df['factor_expansion'] / len(files)
    master_df.drop(columns=fa_cols, inplace=True)

    # --- Phase 2: Data Segregation ---
    # Note: We don't need to explicitly drop rows with NaN in 'C208' because
    # the filtering conditions below (`>= 14` and `< 14`) will not be met
    # for NaN values, so these rows are automatically excluded from both
    # `poblacion_trabajo_df` and `poblacion_no_trabajo_df`.
    poblacion_trabajo_df = master_df[master_df['C208'] >= 14].copy()
    poblacion_no_trabajo_df = master_df[master_df['C208'] < 14].copy()

    # --- Phase 3: Cleaning poblacion_trabajo_df ---
    maps = get_recode_maps()
    for var, mapping in maps.items():
        if var in poblacion_trabajo_df.columns:
            poblacion_trabajo_df[var] = poblacion_trabajo_df[var].map(mapping)

    # Handle Nulls with 'No Aplica'
    not_employed_condition = poblacion_trabajo_df['OCUP300'] != 'Ocupado'

    cols_to_fill = []
    for col in poblacion_trabajo_df.columns:
        if col.startswith('C3'):
            try:
                if int(col.split('_')[0][1:]) >= 308:
                    cols_to_fill.append(col)
            except ValueError:
                continue # Skip columns like C300n

    cols_to_fill.extend([col for col in poblacion_trabajo_df.columns if col.startswith('I3') or col.startswith('D3')])
    cols_to_fill.extend(['INGTOT', 'INGTOTP', 'ingtrabw', 'whoraT'])
    for col in cols_to_fill:
        if col in poblacion_trabajo_df.columns:
            poblacion_trabajo_df.loc[not_employed_condition, col] = 'No Aplica'

    # Feature Engineering: grupo_edad
    bins = [14, 18, 25, 35, 45, 55, 65, np.inf]
    labels = ['14-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    poblacion_trabajo_df['grupo_edad'] = pd.cut(poblacion_trabajo_df['C208'], bins=bins, labels=labels, right=False)

    # Feature Engineering: es_informal
    poblacion_trabajo_df['es_informal'] = 0
    poblacion_trabajo_df.loc[(poblacion_trabajo_df['OCUP300'] == 'Ocupado') & (poblacion_trabajo_df['C361_1'] == 2), 'es_informal'] = 1

    # --- Phase 4: Cleaning poblacion_no_trabajo_df ---
    # Prune irrelevant columns
    try:
        c300n_index = list(poblacion_no_trabajo_df.columns).index('C300n')
        cols_to_keep = list(poblacion_no_trabajo_df.columns[:c300n_index])
        cols_to_keep.extend(['periodo', 'factor_expansion', 'factor_ajustado'])
        poblacion_no_trabajo_df = poblacion_no_trabajo_df[cols_to_keep]
    except ValueError:
        pass # C300n not found

    for var, mapping in maps.items():
        if var in poblacion_no_trabajo_df.columns and var != 'OCUP300':
            poblacion_no_trabajo_df[var] = poblacion_no_trabajo_df[var].map(mapping)

    # --- Final Output ---
    poblacion_trabajo_df.to_csv('datos_limpios_poblacion_trabajo.csv', index=False)
    poblacion_no_trabajo_df.to_csv('datos_limpios_poblacion_no_trabajo.csv', index=False)

if __name__ == '__main__':
    process_data()
