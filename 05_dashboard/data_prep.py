import pandas as pd
import numpy as np
import os

# --- Configuration ---
DATA_SOURCE_DIR = '../00_data_source/'
OUTPUT_DIR = 'data/'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'processed_data.csv')

# --- Helper Functions ---

def get_recode_maps():
    """Returns dictionaries for recoding variables."""
    return {
        'C207': {1: 'Hombre', 2: 'Mujer'},
        'C366': {1: 'Sin nivel', 2: 'Educación Inicial', 3: 'Primaria incompleta', 4: 'Primaria completa', 5: 'Secundaria incompleta', 6: 'Secundaria completa', 7: 'Básica especial', 8: 'Superior no universitaria incompleta', 9: 'Superior no universitaria completa', 10: 'Superior universitaria incompleta', 11: 'Superior universitaria completa', 12: 'Maestria/Doctorado'},
        'OCUP300': {0: 'Sin información', 1: 'Ocupado', 2: 'Desocupado abierto', 3: 'Desocupado oculto', 4: 'Inactivo pleno'},
        'C310': {1: 'Empleador o patrono', 2: 'Trabajador independiente', 3: 'Empleado u obrero', 4: 'Ayudante en un negocio de la familia', 5: 'Ayudante en el empleo de un familiar', 6: 'Trabajador del hogar', 7: 'Aprendiz/practicante remunerado', 8: 'Practicante sin remuneración', 9: 'Ayudante en un negocio de la familia de otro hogar', 10: 'Ayudante en el empleo de un familiar de otro hogar'},
    }

# --- ETL Pipeline Functions ---

def load_and_unify_data(source_dir):
    """Loads, labels, and unifies all CSVs from the source directory."""
    print(f"Reading data from: {source_dir}")
    files = [f for f in os.listdir(source_dir) if f.endswith('.csv')]
    if not files:
        raise FileNotFoundError(f"No CSV files found in {source_dir}")

    quarters = {
        'Trim Ene-Feb-Mar24.csv': '2024-Q1', 'Trim Abr-May-Jun24.csv': '2024-Q2',
        'Trim Jul-Ago-Set24.csv': '2024-Q3', 'Trim Set-Oct-Nov24.csv': '2024-Q4',
        'Trim Ene-Feb-Mar25.csv': '2025-Q1', 'Trim Mar-Abr-May25.csv': '2025-Q2'
    }

    df_list = []
    for file in files:
        df = pd.read_csv(os.path.join(source_dir, file), low_memory=False)
        if file in quarters:
            df['periodo'] = quarters[file]
        df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)
    master_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    print("Data loaded and unified successfully.")
    return master_df

def clean_special_codes(df):
    """Replaces special codes (e.g., 99, 999999) with NaN."""
    print("Cleaning special codes...")
    codes_to_nan = {
        'C208': [99], 'INGTOT': [999999], 'whoraT': [99], 'I339_1': [999999],
        'C312': [4] # "NO SABE" for C312 is treated as missing
    }

    for column, codes in codes_to_nan.items():
        if column in df.columns:
            df[column] = df[column].replace(codes, np.nan)

    numeric_cols = ['C208', 'INGTOT', 'whoraT', 'I339_1']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    print("Special codes cleaned.")
    return df

def process_working_population(df):
    """Filters for the working population, recodes variables, and engineers features."""
    print("Processing working population data...")
    # Filter for population aged 14 and over
    df_trabajo = df[df['C208'] >= 14].copy()

    # Recode categorical variables
    maps = get_recode_maps()
    for var, mapping in maps.items():
        if var in df_trabajo.columns:
            df_trabajo[var] = df_trabajo[var].map(mapping).astype('category')

    # Rename columns for clarity
    df_trabajo.rename(columns={
        'C207': 'Sexo',
        'C208': 'Edad',
        'C366': 'Nivel_Educativo',
        'C310': 'Tipo_Ocupacion',
        'INGTOT': 'Ingreso_Mensual',
        'whoraT': 'Horas_Trabajo_Semanal'
    }, inplace=True)

    # Feature Engineering: Age Group
    bins = [14, 18, 25, 35, 45, 55, 65, np.inf]
    labels = ['14-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    df_trabajo['Grupo_Edad'] = pd.cut(df_trabajo['Edad'], bins=bins, labels=labels, right=False)

    # Feature Engineering: Informality
    # C312: 1=Juridica, 2=Natural con RUC, 3=Sin RUC. Informal if C312 is 3.
    # C361_1: 1=Tiene seguro, 2=No tiene. Informal if C361_1 is 2.
    # We define informal as being occupied and not having social security.
    df_trabajo['es_informal'] = ((df_trabajo['OCUP300'] == 'Ocupado') & (df_trabajo['C361_1'] == 2)).astype(int)

    # Filter for only the 'Ocupado' population for the final dataset
    df_trabajo = df_trabajo[df_trabajo['OCUP300'] == 'Ocupado'].copy()

    print("Working population processed.")
    return df_trabajo


def main():
    """Main ETL script execution."""
    print("--- Starting Data Preparation ---")

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Run the pipeline
    master_df = load_and_unify_data(DATA_SOURCE_DIR)
    df_cleaned = clean_special_codes(master_df)
    df_final = process_working_population(df_cleaned)

    # Select and reorder columns for the final dataset
    final_columns = [
        'periodo', 'Sexo', 'Edad', 'Grupo_Edad', 'Nivel_Educativo',
        'Tipo_Ocupacion', 'Ingreso_Mensual', 'Horas_Trabajo_Semanal', 'es_informal'
    ]
    # Ensure all columns exist, add if not
    for col in final_columns:
        if col not in df_final.columns:
            df_final[col] = np.nan

    df_final = df_final[final_columns]

    # Save the processed data
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"--- Data preparation complete. Output saved to {OUTPUT_FILE} ---")


if __name__ == '__main__':
    main()
