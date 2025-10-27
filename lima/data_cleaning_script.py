import pandas as pd
import numpy as np
import os
import re

# --- Configuration ---
DATA_DIR = 'lima/02_preparacion_y_limpieza'
OUTPUT_DIR = 'lima/02_preparacion_y_limpieza'
UNIFIED_FILENAME = 'lima_cleaned_unified.csv'

# --- Mappings and Constants ---
CODES_TO_NAN = {
    'C208': [99], 'C301_DIA': [99], 'C301_MES': [99], 'C301_ANIO': [9999],
    'C304': [9], 'C305': [9],
    'C308_COD': [9999], 'C309_COD': [9999], 'C317A': [9999],
    'C318_1': [99], 'C318_2': [99], 'C318_3': [99], 'C318_4': [99], 'C318_5': [99],
    'C318_6': [99], 'C318_7': [99], 'C318_T': [99], 'C328_T': [99], 'whoraT': [99],
    'C331': [99], 'C339_1': [999999], 'C341_T': [999999], 'C342': [999999],
    'D344': [999999], 'I345_1': [999999], 'C345_1': [999999], 'D347_T': [999999],
    'C348': [999999], 'D350': [999999], 'INGTOT': [999999], 'INGTOTP': [999999],
    'ingtrabw': [999999], 'I339_1': [999999], 'I342': [999999], 'I345_1': [999999],
    'I348': [999999]
}

# --- Main Cleaning Process ---
print("--- Iniciando Script de Limpieza y Unificación de Datos ---")

try:
    all_files = os.listdir(DATA_DIR)
    filtered_files = [f for f in all_files if f.startswith('lima_filtered_') and f.endswith('.csv')]
    if not filtered_files:
        raise FileNotFoundError(f"No se encontraron archivos 'lima_filtered_*.csv' en '{DATA_DIR}'.")

    list_of_dfs = []

    for filename in filtered_files:
        file_path = os.path.join(DATA_DIR, filename)
        print(f"Procesando archivo: {filename}")

        df = pd.read_csv(file_path, low_memory=False)

        # Create 'trimestre' column from filename
        match = re.search(r'Trim (.*?)\d{2}\.csv', filename)
        if match:
            quarter_name = match.group(1).replace('-', '')
            year = re.search(r'(\d{2})', filename).group(1)
            df['trimestre'] = f"20{year}_{quarter_name}"
        else:
            df['trimestre'] = "desconocido"

        list_of_dfs.append(df)

    # Unify all dataframes
    if not list_of_dfs:
        print("No se procesaron archivos. Saliendo.")
        exit()

    unified_df = pd.concat(list_of_dfs, ignore_index=True)
    print(f"\n unification de {len(list_of_dfs)} archivos completada. Total de registros: {len(unified_df)}")

    # --- Data Cleaning on Unified Dataframe ---

    # 1. Standardize column names (lowercase)
    unified_df.columns = unified_df.columns.str.lower()

    # 2. Handle expansion factor
    fa_col = next((col for col in unified_df.columns if col.startswith('fa_')), None)
    if fa_col:
        unified_df.rename(columns={fa_col: 'factor_expansion'}, inplace=True)
        unified_df['factor_expansion'] = pd.to_numeric(unified_df['factor_expansion'], errors='coerce')
        print("  - Columna de factor de expansión estandarizada.")

    # 3. Replace special codes with NaN
    for column, codes in CODES_TO_NAN.items():
        col_lower = column.lower()
        if col_lower in unified_df.columns:
            unified_df[col_lower] = pd.to_numeric(unified_df[col_lower], errors='coerce')
            unified_df[col_lower] = unified_df[col_lower].replace(codes, np.nan)
    print("  - Códigos especiales reemplazados con NaN.")

    # 4. Correct Data Types
    for col in unified_df.columns:
        if unified_df[col].dtype == 'object':
            try:
                unified_df[col] = pd.to_numeric(unified_df[col])
            except (ValueError, TypeError):
                # If conversion to numeric fails, it's likely a true categorical column
                unified_df[col] = unified_df[col].astype('category')
    print("  - Tipos de datos corregidos.")

    # 5. Feature Engineering
    # Create 'grupo_edad' (Age Group)
    if 'c208' in unified_df.columns:
        bins = [0, 14, 24, 39, 59, 98]
        labels = ['0-14', '15-24', '25-39', '40-59', '60+']
        unified_df['grupo_edad'] = pd.cut(unified_df['c208'], bins=bins, labels=labels, right=True)
        print("  - Creada la característica 'grupo_edad'.")

    # Create 'tiene_seguro' (Has Insurance)
    seguro_cols = [f'c361_{i}' for i in range(1, 9)]
    seguro_cols_exist = [col for col in seguro_cols if col in unified_df.columns]
    if seguro_cols_exist:
        unified_df['tiene_seguro'] = unified_df[seguro_cols_exist].apply(lambda x: 1 if (x == 1).any() else 0, axis=1)
        print("  - Creada la característica 'tiene_seguro'.")

    # Create 'nivel_educativo_agrupado'
    if 'c366' in unified_df.columns:
        educ_mapping = {
            1: 'Sin Nivel', 2: 'Sin Nivel',
            3: 'Primaria', 4: 'Primaria',
            5: 'Secundaria', 6: 'Secundaria',
            7: 'Educacion Especial',
            8: 'Superior No Univ.', 9: 'Superior No Univ.',
            10: 'Superior Univ.', 11: 'Superior Univ.',
            12: 'Postgrado'
        }
        unified_df['nivel_educativo_agrupado'] = unified_df['c366'].map(educ_mapping).astype('category')
        print("  - Creada la característica 'nivel_educativo_agrupado'.")

    # Save the unified and cleaned dataframe
    output_path = os.path.join(OUTPUT_DIR, UNIFIED_FILENAME)
    unified_df.to_csv(output_path, index=False)
    print(f"\n Archivo unificado y limpio guardado en: {output_path}")

    # Clean up old filtered files
    for filename in filtered_files:
        os.remove(os.path.join(DATA_DIR, filename))
    print("  - Archivos filtrados intermedios eliminados.")

except (FileNotFoundError, Exception) as e:
    print(f"ERROR: {e}")

print("\n--- Proceso de Limpieza y Unificación Completado ---")
