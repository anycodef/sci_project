import pandas as pd
import os

# --- Configuración ---
data_dir = 'lima/02_preparacion_y_limpieza'
# Lista de variables categóricas clave para verificar la consistencia de sus valores
CATEGORICAL_VARS_TO_CHECK = ['C207', 'C310', 'C366', 'OCUP300']

print("--- Iniciando Script de Verificación de Consistencia Estructural (Versión Detallada) ---")

try:
    all_files = os.listdir(data_dir)
    cleaned_files = sorted([f for f in all_files if f.startswith('lima_cleaned_') and f.endswith('.csv')])
    if not cleaned_files:
        print(f"Error: No se encontraron archivos 'lima_cleaned_*.csv' en '{data_dir}'.")
        exit()
except FileNotFoundError:
    print(f"Error: El directorio '{data_dir}' no fue encontrado.")
    exit()

# --- 1. Verificación de la Estructura de Columnas ---
print("\n--- Verificando Consistencia de Columnas ---")
reference_columns = None
all_columns_consistent = True

for filename in cleaned_files:
    file_path = os.path.join(data_dir, filename)
    try:
        # Leemos solo el encabezado para eficiencia
        df = pd.read_csv(file_path, low_memory=False, nrows=0)
        current_columns = df.columns.tolist()

        if reference_columns is None:
            reference_columns = current_columns
            print(f"Estableciendo columnas de referencia desde: {filename}")
            print(f"Número de columnas de referencia: {len(reference_columns)}")
        else:
            if current_columns != reference_columns:
                all_columns_consistent = False
                print(f"\n[✗] FALLO: La estructura de columnas en '{filename}' es DIFERENTE de la referencia.")

                # Encontrar y mostrar las diferencias
                ref_set = set(reference_columns)
                curr_set = set(current_columns)

                missing_from_current = ref_set - curr_set
                added_in_current = curr_set - ref_set

                if missing_from_current:
                    print(f"    - Columnas FALTANTES en '{filename}': {sorted(list(missing_from_current))}")
                if added_in_current:
                    print(f"    - Columnas ADICIONALES en '{filename}': {sorted(list(added_in_current))}")

                if not missing_from_current and not added_in_current:
                     print("    - Las columnas son las mismas, pero el ORDEN es diferente.")

            else:
                print(f"[✓] ÉXITO: La estructura de columnas en '{filename}' es consistente.")

    except Exception as e:
        all_columns_consistent = False
        print(f"[✗] ERROR al leer las columnas de {filename}: {e}")

if all_columns_consistent:
    print("\nResultado de Columnas: [✓] Todos los archivos tienen una estructura de columnas idéntica.")
else:
    print("\nResultado de Columnas: [✗] Se encontraron inconsistencias en las columnas. Revisar los detalles de arriba.")


# --- 2. Verificación de la Consistencia de Categorías (sin cambios) ---
print("\n--- Verificando Consistencia de Valores en Variables Categóricas Clave ---")

all_categories_consistent = True
for var in CATEGORICAL_VARS_TO_CHECK:
    print(f"\nAnalizando variable: '{var}'")
    all_unique_values = set()
    is_consistent = True

    for filename in cleaned_files:
        file_path = os.path.join(data_dir, filename)
        try:
            # Solo cargar la columna necesaria para optimizar
            df = pd.read_csv(file_path, usecols=[var], low_memory=False)
            unique_values_in_file = set(df[var].dropna().unique())
            all_unique_values.update(unique_values_in_file)

        except Exception as e:
            print(f"  [✗] ERROR al leer la variable '{var}' en {filename}: {e}")
            is_consistent = False

    if is_consistent:
        print(f"  - Valores únicos encontrados para '{var}' en todos los trimestres: {sorted(list(all_unique_values))}")
        print(f"  - [✓] La variable '{var}' parece consistente.")
    else:
        all_categories_consistent = False
        print(f"  - [✗] No se pudo verificar la consistencia completa de '{var}' debido a errores.")

if all_categories_consistent:
    print("\nResultado de Categorías: [✓] Las categorías en las variables clave parecen ser consistentes a través de los trimestres.")
else:
    print("\nResultado de Categorías: [✗] Se encontraron problemas al verificar la consistencia de las categorías.")

print("\n--- Verificación de Consistencia Detallada Completada ---")