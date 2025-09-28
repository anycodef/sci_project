import pandas as pd
import numpy as np
import os
import re

# --- Configuración de Rutas ---
# Los archivos se leerán y se sobrescribirán en el mismo directorio
data_dir = 'lima/02_preparacion_y_limpieza'

# --- Códigos Especiales a NaN ---
# Basado en el diccionario de variables y en el script de pipeline original
CODES_TO_NAN = {
    'C208': [99], 'C301_DIA': [99], 'C301_MES': [99], 'C301_ANIO': [9999], 'C308_COD': [9999], 'C309_COD': [9999],
    'C317A': [9999], 'C318_1': [99], 'C318_2': [99], 'C318_3': [99], 'C318_4': [99], 'C318_5': [99],
    'C318_6': [99], 'C318_7': [99], 'C318_T': [99], 'C328_T': [99], 'whoraT': [99], 'I339_1': [999999],
    'C341_T': [999999], 'C342': [999999], 'D344': [999999], 'I345_1': [999999], 'D347_T': [999999],
    'C348': [999999], 'D350': [999999], 'INGTOT': [999999], 'INGTOTP': [999999], 'INGTRABW': [999999]
}

# --- Proceso de Limpieza ---
print("--- Iniciando Script de Limpieza de Datos ---")

try:
    # Obtener la lista de archivos filtrados
    all_files = os.listdir(data_dir)
    filtered_files = [f for f in all_files if f.startswith('lima_filtered_') and f.endswith('.csv')]
    if not filtered_files:
        print(f"Error: No se encontraron archivos 'lima_filtered_*.csv' en '{data_dir}'.")
        exit()
except FileNotFoundError:
    print(f"Error: El directorio '{data_dir}' no fue encontrado.")
    exit()

# Iterar sobre cada archivo filtrado
for filename in filtered_files:
    file_path = os.path.join(data_dir, filename)
    print(f"\nLimpiando archivo: {filename}")

    try:
        df = pd.read_csv(file_path, low_memory=False)

        # 1. Limpiar valores que son solo espacios en blanco
        df = df.replace(r'^\s*$', np.nan, regex=True)

        # 2. Manejar el factor de expansión
        # Encontrar la columna que empieza con 'fa_'
        fa_col_list = [col for col in df.columns if col.startswith('fa_')]
        if fa_col_list:
            fa_col_name = fa_col_list[0]
            # Convertir a numérico, los errores se convierten en NaN
            df[fa_col_name] = pd.to_numeric(df[fa_col_name], errors='coerce')
            # Renombrar a un nombre genérico para consistencia
            df.rename(columns={fa_col_name: 'factor_expansion'}, inplace=True)
            print(f"  - Columna de factor de expansión '{fa_col_name}' renombrada a 'factor_expansion'.")
        else:
            print("  - ADVERTENCIA: No se encontró una columna de factor de expansión ('fa_*').")

        # 3. Reemplazar códigos especiales con NaN
        for column, codes in CODES_TO_NAN.items():
            if column in df.columns:
                # Convertir la columna a tipo numérico antes de reemplazar para evitar errores de tipo mixto
                df[column] = pd.to_numeric(df[column], errors='coerce')
                df[column] = df[column].replace(codes, np.nan)
        print("  - Códigos especiales reemplazados con NaN.")

        # 4. Guardar el archivo limpio, sobrescribiendo el anterior
        # Se renombra para indicar que está limpio
        clean_filename = filename.replace('lima_filtered_', 'lima_cleaned_')
        output_path = os.path.join(data_dir, clean_filename)
        df.to_csv(output_path, index=False)

        # Opcional: Eliminar el archivo filtrado viejo para no tener duplicados
        os.remove(file_path)

        print(f"  - Archivo limpio guardado como: {clean_filename}")

    except Exception as e:
        print(f"  - ERROR al limpiar el archivo {filename}: {e}")

print("\n--- Proceso de Limpieza Completado ---")