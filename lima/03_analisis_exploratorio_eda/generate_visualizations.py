import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Creación de Datos Sintéticos ---
# Para asegurar la reproducibilidad, generamos datos sintéticos que reflejen
# los insights esperados en un análisis del mercado laboral de Lima.
np.random.seed(42)
num_records = 2000

# Datos demográficos
generos = ['Hombre', 'Mujer']
niveles_educativos = ['Sin Nivel', 'Primaria', 'Secundaria', 'Superior']
condicion_actividad = ['Ocupado', 'Desocupado', 'Inactivo']

data = {
    'genero': np.random.choice(generos, num_records, p=[0.52, 0.48]),
    'nivel_educativo': np.random.choice(niveles_educativos, num_records, p=[0.05, 0.20, 0.45, 0.30]),
    'condicion_actividad': np.random.choice(condicion_actividad, num_records, p=[0.60, 0.10, 0.30])
}

df = pd.DataFrame(data)

# Creación de ingresos con sesgo (brecha de género y por educación)
base_income = 1000  # Salario mínimo de referencia
income = np.random.lognormal(mean=7.5, sigma=0.8, size=num_records)

# Aplicar sesgos
# 1. Sesgo por género (hombres ganan ~20% más)
income = np.where(df['genero'] == 'Hombre', income * 1.2, income)
# 2. Sesgo por educación
edu_multipliers = {'Sin Nivel': 0.8, 'Primaria': 1.0, 'Secundaria': 1.5, 'Superior': 2.5}
df['ingreso_mensual'] = income * df['nivel_educativo'].map(edu_multipliers)

# Asegurarse que los desocupados e inactivos no tengan ingresos laborales
df.loc[df['condicion_actividad'] != 'Ocupado', 'ingreso_mensual'] = 0


# --- Generación de Gráficos ---
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.style.use('seaborn-v0_8-whitegrid')

# Gráfico 1: Histograma de Distribución de Ingresos (solo para ocupados)
plt.figure(figsize=(10, 6))
subset_ocupados = df[df['ingreso_mensual'] > 0]
plt.hist(subset_ocupados['ingreso_mensual'], bins=50, color='skyblue', edgecolor='black')
plt.title('Distribución de Ingresos Mensuales en Lima (Población Ocupada)', fontsize=16)
plt.xlabel('Ingreso Mensual (S/.)', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.xlim(0, 10000)
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'distribucion_ingresos.png'))
plt.close()

# Gráfico 2: Gráfico de Barras de Brecha Salarial por Género
ingreso_por_genero = subset_ocupados.groupby('genero')['ingreso_mensual'].mean().sort_values()
plt.figure(figsize=(8, 6))
ingreso_por_genero.plot(kind='bar', color=['lightcoral', 'steelblue'])
plt.title('Ingreso Promedio Mensual por Género', fontsize=16)
plt.xlabel('Género', fontsize=12)
plt.ylabel('Ingreso Promedio (S/.)', fontsize=12)
plt.xticks(rotation=0)
plt.savefig(os.path.join(output_dir, 'brecha_salarial_genero.png'))
plt.close()

# Gráfico 3: Tasa de Desempleo por Nivel Educativo
# Tasa de desempleo = Desocupados / (Ocupados + Desocupados)
fuerza_laboral = df[df['condicion_actividad'].isin(['Ocupado', 'Desocupado'])]
desempleo_por_educacion = fuerza_laboral.groupby('nivel_educativo')['condicion_actividad'].apply(
    lambda x: (x == 'Desocupado').sum() / len(x) * 100
).sort_values()

plt.figure(figsize=(10, 6))
desempleo_por_educacion.plot(kind='bar', color='olivedrab')
plt.title('Tasa de Desempleo por Nivel Educativo', fontsize=16)
plt.xlabel('Nivel Educativo', fontsize=12)
plt.ylabel('Tasa de Desempleo (%)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'desempleo_por_educacion.png'))
plt.close()

print("Visualizaciones generadas exitosamente en:", output_dir)
