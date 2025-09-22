import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Get current timestamp for filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define paths
data_path = '02_data_processed/datos_limpios_poblacion_trabajo.csv'
output_dir = '03_cleaning_evidence/'
report_path = '04_reports/analisis_exploratorio_detallado.md'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs('04_reports', exist_ok=True)

# Load data
df = pd.read_csv(data_path)

# Define label mappings
label_map = {
    'C207': 'Sexo',
    'C310': 'Tipo de Ocupación',
    'C366': 'Nivel Educativo',
    'C377': 'Autoidentificación Étnica',
    'es_informal': 'Condición Laboral (Informalidad)',
    'grupo_edad': 'Grupo de Edad',
    'INGTOT': 'Ingreso Total Mensual (S/.)',
    'whoraT': 'Horas Trabajadas por Semana'
}

# Rename columns for easier use
df.rename(columns=label_map, inplace=True)

# Convert 'Horas Trabajadas por Semana' to numeric, coercing errors
df['Horas Trabajadas por Semana'] = pd.to_numeric(df['Horas Trabajadas por Semana'], errors='coerce')
df.dropna(subset=['Horas Trabajadas por Semana'], inplace=True)


print("Data loaded and columns renamed successfully.")

# --- Analysis 1: Occupation Type by Sex ---
plt.figure(figsize=(12, 8))
sns.countplot(data=df, y='Tipo de Ocupación', hue='Sexo', order = df['Tipo de Ocupación'].value_counts().index)
plt.title('Distribución de Tipos de Ocupación por Sexo')
plt.xlabel('Cantidad')
plt.ylabel('Tipo de Ocupación')
plt.legend(title='Sexo')
plt.tight_layout()
ocupacion_por_sexo_path = os.path.join(output_dir, f'ocupacion_por_sexo_{timestamp}.png')
plt.savefig(ocupacion_por_sexo_path)
plt.close()
print(f"Saved: {ocupacion_por_sexo_path}")

# --- Analysis 2: Occupation by Education Level ---
occupation_education = df.groupby(['Nivel Educativo', 'Tipo de Ocupación']).size().unstack(fill_value=0)
occupation_education_perc = occupation_education.apply(lambda x: x / x.sum(), axis=1)
fig, ax = plt.subplots(figsize=(14, 10))
occupation_education_perc.plot(kind='barh', stacked=True, ax=ax, colormap='viridis')
ax.set_title('Distribución Porcentual de Ocupación por Nivel Educativo')
ax.set_xlabel('Proporción')
ax.set_ylabel('Nivel Educativo')
ax.legend(title='Tipo de Ocupación', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
ocupacion_por_nivel_educativo_path = os.path.join(output_dir, f'ocupacion_por_nivel_educativo_{timestamp}.png')
plt.savefig(ocupacion_por_nivel_educativo_path)
plt.close()
print(f"Saved: {ocupacion_por_nivel_educativo_path}")

# --- Analysis 3: Labor Informality by Ethnicity ---
informality_ethnicity = df.groupby(['Autoidentificación Étnica', 'Condición Laboral (Informalidad)']).size().unstack(fill_value=0)
informality_ethnicity_perc = informality_ethnicity.apply(lambda x: x / x.sum(), axis=1)
fig, ax = plt.subplots(figsize=(12, 8))
informality_ethnicity_perc.plot(kind='barh', stacked=True, ax=ax, colormap='coolwarm')
ax.set_title('Tasa de Informalidad Laboral por Autoidentificación Étnica')
ax.set_xlabel('Proporción')
ax.set_ylabel('Autoidentificación Étnica')
ax.legend(title='Condición Laboral', labels=['Formal', 'Informal'], bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
informalidad_por_etnia_path = os.path.join(output_dir, f'informalidad_por_etnia_{timestamp}.png')
plt.savefig(informalidad_por_etnia_path)
plt.close()
print(f"Saved: {informalidad_por_etnia_path}")

# --- Analysis 4: Income Distribution by Education Level and Sex ---
plt.figure(figsize=(16, 10))
sns.boxplot(data=df, x='Ingreso Total Mensual (S/.)', y='Nivel Educativo', hue='Sexo')
plt.title('Distribución del Ingreso por Nivel Educativo y Sexo')
plt.xlabel('Ingreso Total Mensual (S/.) (Escala Logarítmica)')
plt.ylabel('Nivel Educativo')
plt.xscale('log')
plt.legend(title='Sexo')
plt.tight_layout()
ingreso_por_educacion_sexo_path = os.path.join(output_dir, f'ingreso_por_educacion_sexo_{timestamp}.png')
plt.savefig(ingreso_por_educacion_sexo_path)
plt.close()
print(f"Saved: {ingreso_por_educacion_sexo_path}")

# --- Analysis 5: Working Hours by Occupation Type ---
plt.figure(figsize=(14, 8))
sns.boxplot(data=df, x='Horas Trabajadas por Semana', y='Tipo de Ocupación', order = df.groupby('Tipo de Ocupación')['Horas Trabajadas por Semana'].median().sort_values().index)
plt.title('Distribución de Horas Trabajadas por Semana según Tipo de Ocupación')
plt.xlabel('Horas Trabajadas por Semana')
plt.ylabel('Tipo de Ocupación')
plt.tight_layout()
horas_por_tipo_ocupacion_path = os.path.join(output_dir, f'horas_por_tipo_ocupacion_{timestamp}.png')
plt.savefig(horas_por_tipo_ocupacion_path)
plt.close()
print(f"Saved: {horas_por_tipo_ocupacion_path}")
