import pandas as pd
import os

# --- Configuración de Rutas ---
source_dir = 'lima/01_datos_iniciales'
filtered_dir = 'lima/02_preparacion_y_limpieza'

print("--- Iniciando Script de Verificación de Filtrado ---")

# Obtener la lista de archivos CSV originales
try:
    all_source_files = os.listdir(source_dir)
    source_csv_files = [f for f in all_source_files if f.endswith('.csv')]
    if not source_csv_files:
        print(f"Error: No se encontraron archivos .csv en el directorio de origen '{source_dir}'.")
        exit()
except FileNotFoundError:
    print(f"Error: El directorio de origen '{source_dir}' no fue encontrado.")
    exit()

all_checks_passed = True

# Iterar sobre cada archivo de origen
for source_filename in source_csv_files:
    source_path = os.path.join(source_dir, source_filename)
    filtered_filename = f"lima_filtered_{source_filename}"
    filtered_path = os.path.join(filtered_dir, filtered_filename)

    print(f"\nVerificando: {source_filename}")

    try:
        # 1. Cargar el archivo original
        df_source = pd.read_csv(source_path, low_memory=False)
        source_total_rows = len(df_source)

        # 2. Contar registros de Lima en el archivo original
        if 'REGION' in df_source.columns:
            source_lima_rows = len(df_source[df_source['REGION'] == 1])
        else:
            print(f"  - ADVERTENCIA: La columna 'REGION' no existe en {source_filename}. Saltando archivo.")
            continue

        # 3. Verificar si el archivo filtrado correspondiente existe
        if not os.path.exists(filtered_path):
            print(f"  - ERROR: El archivo filtrado esperado '{filtered_filename}' no existe.")
            all_checks_passed = False
            continue

        # 4. Cargar el archivo filtrado y contar sus filas
        df_filtered = pd.read_csv(filtered_path, low_memory=False)
        filtered_total_rows = len(df_filtered)

        # 5. Comparar los conteos
        print(f"  - Filas totales en el archivo original: {source_total_rows}")
        print(f"  - Filas de Lima (REGION=1) en original: {source_lima_rows}")
        print(f"  - Filas totales en el archivo filtrado: {filtered_total_rows}")

        if source_lima_rows == filtered_total_rows:
            print("  - [✓] ÉXITO: El número de filas coincide.")
        else:
            print(f"  - [✗] FALLO: ¡Discrepancia en el número de filas! Se esperaban {source_lima_rows} pero se encontraron {filtered_total_rows}.")
            all_checks_passed = False

    except Exception as e:
        print(f"  - ERROR al procesar el archivo {source_filename}: {e}")
        all_checks_passed = False

print("\n--- Verificación Completada ---")
if all_checks_passed:
    print("Resultado final: [✓] Todos los archivos filtrados son correctos y completos.")
else:
    print("Resultado final: [✗] Se encontraron errores. Los datos filtrados no son correctos.")