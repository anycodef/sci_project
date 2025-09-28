import pandas as pd
import os

# --- Configuración ---
data_dir = 'lima/02_preparacion_y_limpieza'
# Usaremos el primer archivo de 2024 como referencia para el orden de las columnas
reference_file_name = 'lima_cleaned_Trim Abr-May-Jun24.csv'
reference_file_path = os.path.join(data_dir, reference_file_name)

print("--- Iniciando Script de Armonización de Columnas ---")

try:
    # 1. Obtener el orden de columnas de referencia
    print(f"Leyendo la estructura de columnas de referencia desde: {reference_file_name}")
    ref_df = pd.read_csv(reference_file_path, low_memory=False, nrows=0)
    canonical_column_order = ref_df.columns.tolist()
    print(f"Orden de columnas canónico establecido con {len(canonical_column_order)} columnas.")

    # 2. Obtener la lista de todos los archivos a procesar
    all_files = os.listdir(data_dir)
    cleaned_files = [f for f in all_files if f.startswith('lima_cleaned_') and f.endswith('.csv')]

    # 3. Iterar y armonizar cada archivo
    for filename in cleaned_files:
        file_path = os.path.join(data_dir, filename)
        print(f"\nProcesando archivo: {filename}")

        try:
            df_to_harmonize = pd.read_csv(file_path, low_memory=False)

            # Verificar si ya tiene el orden correcto
            if df_to_harmonize.columns.tolist() == canonical_column_order:
                print("  - [✓] El archivo ya tiene el orden de columnas correcto. No se necesita ninguna acción.")
                continue

            # Reordenar las columnas
            print("  - El orden de las columnas es diferente. Armonizando...")
            df_harmonized = df_to_harmonize[canonical_column_order]

            # Sobrescribir el archivo con la versión armonizada
            df_harmonized.to_csv(file_path, index=False)
            print(f"  - [✓] Archivo sobrescrito con el orden de columnas armonizado.")

        except Exception as e:
            print(f"  - [✗] ERROR al armonizar el archivo {filename}: {e}")

except FileNotFoundError:
    print(f"Error: El archivo de referencia '{reference_file_name}' no fue encontrado en '{data_dir}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")


print("\n--- Proceso de Armonización Completado ---")