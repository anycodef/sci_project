import pandas as pd
import os

# --- Configuración de Rutas ---
# Rutas relativas a la raíz del proyecto
source_dir = 'lima/01_datos_iniciales'
output_dir = 'lima/02_preparacion_y_limpieza'

# Asegurarse de que el directorio de salida exista
os.makedirs(output_dir, exist_ok=True)

# --- Proceso de Filtrado ---
print("Iniciando el proceso de filtrado de datos para Lima...")

# Obtener la lista de archivos CSV en el directorio de datos iniciales
try:
    all_files = os.listdir(source_dir)
    csv_files = [f for f in all_files if f.endswith('.csv')]
    if not csv_files:
        print(f"Error: No se encontraron archivos .csv en el directorio '{source_dir}'.")
        exit()
except FileNotFoundError:
    print(f"Error: El directorio de origen '{source_dir}' no fue encontrado.")
    exit()

# Iterar sobre cada archivo CSV
for filename in csv_files:
    # Construir la ruta completa del archivo de entrada
    file_path = os.path.join(source_dir, filename)
    print(f"\nProcesando archivo: {filename}")

    try:
        # Cargar el dataset
        df = pd.read_csv(file_path, low_memory=False)

        # Verificar si la columna 'REGION' existe
        if 'REGION' in df.columns:
            # Filtrar los datos para conservar solo los de Lima (REGION == 1)
            # El diccionario indica que Lima Metropolitana es el código 1
            df_lima = df[df['REGION'] == 1].copy()

            # Construir el nombre del archivo de salida
            output_filename = f"lima_filtered_{filename}"
            output_path = os.path.join(output_dir, output_filename)

            # Guardar el nuevo dataset filtrado
            df_lima.to_csv(output_path, index=False)
            print(f"  - Datos de Lima extraídos. Total de registros: {len(df_lima)}")
            print(f"  - Archivo guardado en: {output_path}")
        else:
            print(f"  - Advertencia: La columna 'REGION' no se encontró en {filename}. El archivo no fue procesado.")

    except Exception as e:
        print(f"  - Error al procesar el archivo {filename}: {e}")

print("\nProceso de filtrado completado.")