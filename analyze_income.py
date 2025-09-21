import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# --- Configuration ---
DATA_FILE = 'datos_limpios_poblacion_trabajo.csv'
EVIDENCE_DIR = 'cleaning_evidence'
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- Load Data ---
df = pd.read_csv(DATA_FILE)

# --- Data Cleaning & Preparation ---
# Convert 'INGTOT' to numeric, coercing errors to NaN, then drop those rows
df['INGTOT'] = pd.to_numeric(df['INGTOT'], errors='coerce')
df.dropna(subset=['INGTOT'], inplace=True)

# Map codes to readable strings based on the data dictionary
sex_map = {1: 'Hombre', 2: 'Mujer'}
education_map = {
    1: 'Sin nivel', 2: 'Educación Inicial', 3: 'Primaria incompleta',
    4: 'Primaria completa', 5: 'Secundaria incompleta', 6: 'Secundaria completa',
    7: 'Básica especial', 8: 'Superior no universitaria incompleta',
    9: 'Superior no universitaria completa', 10: 'Superior universitaria incompleta',
    11: 'Superior universitaria completa', 12: 'Maestria/Doctorado'
}
occupation_map = {
    1: 'Empleador o patrono', 2: 'Trabajador independiente', 3: 'Empleado u obrero',
    4: 'Ayudante en un negocio de la familia', 5: 'Ayudante en el empleo de un familiar',
    6: 'Trabajador del hogar', 7: 'Aprendiz/practicante remunerado',
    8: 'Practicante sin remuneración', 9: 'Ayudante en un negocio de la familia de otro hogar',
    10: 'Ayudante en el empleo de un familiar de otro hogar'
}

df['sexo'] = df['C207'].map(sex_map)
df['Nivel educativo'] = df['C366'].map(education_map)
df['Tipo de ocupación'] = df['C310'].map(occupation_map)


# --- Phase 1: Profiling High-Income Outliers ---

# 1. Define and Isolate Outliers
Q1 = df['INGTOT'].quantile(0.25)
Q3 = df['INGTOT'].quantile(0.75)
IQR = Q3 - Q1
outlier_threshold = Q3 + 1.5 * IQR
df_high_earners = df[df['INGTOT'] > outlier_threshold]

# 2. Generate Profile
sex_dist = df_high_earners['sexo'].value_counts(normalize=True) * 100
education_dist = df_high_earners['Nivel educativo'].value_counts(normalize=True) * 100
age_group_dist = df_high_earners['grupo_edad'].value_counts(normalize=True) * 100
occupation_dist = df_high_earners['Tipo de ocupación'].value_counts(normalize=True) * 100
income_stats = df_high_earners['INGTOT'].describe()

# 3. Synthesize Findings
# Ensure that the series are not empty before accessing index [0]
top_education = education_dist.index[0] if not education_dist.empty else "N/A"
top_age_group = age_group_dist.index[0] if not age_group_dist.empty else "N/A"
top_occupation = occupation_dist.index[0] if not occupation_dist.empty else "N/A"
education_perc = education_dist.iloc[0] if not education_dist.empty else 0
age_perc = age_group_dist.iloc[0] if not age_group_dist.empty else 0
occupation_perc = occupation_dist.iloc[0] if not occupation_dist.empty else 0

summary_text = f"""
### Análisis Profundo de Outliers de Ingresos

#### Perfil de Altos Ingresos
El análisis de los perceptores de altos ingresos (definidos como individuos con ingresos mensuales superiores a S/.{outlier_threshold:,.2f}) revela un perfil demográfico y profesional distintivo. Este segmento está predominantemente compuesto por hombres ({sex_dist.get('Hombre', 0):.1f}%), destacando una brecha de género en los niveles de ingreso más altos.

En cuanto a la educación, el **{education_perc:.1f}%** de este grupo posee **'{top_education}'**, lo que subraya la correlación entre la formación avanzada y el potencial de ingresos. El grupo de edad más representativo es el de **'{top_age_group}'** ({age_perc:.1f}%), sugiriendo que los ingresos más altos se concentran en etapas de mayor experiencia laboral.

Profesionalmente, la ocupación más común es la de **'{top_occupation}'** ({occupation_perc:.1f}%). Las estadísticas de ingresos para este grupo son:
- **Ingreso Promedio:** S/.{income_stats['mean']:,.2f}
- **Ingreso Mediano:** S/.{income_stats['50%']:,.2f}
- **Ingreso Máximo:** S/.{income_stats['max']:,.2f}

Este perfil sugiere que los altos ingresos están fuertemente asociados con el género masculino, la educación superior y roles de liderazgo o propiedad empresarial.
"""
print(summary_text)

# --- Phase 2: Creating Refined Income Visualizations ---

# 1. Create a Multi-Panel Plot
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Análisis Exhaustivo de la Distribución del Ingreso Mensual', fontsize=20)

# Top-Left Plot: Overall Distribution
axes[0, 0].hist(df['INGTOT'], bins=50, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Distribución General del Ingreso Mensual')
axes[0, 0].set_xlabel('Ingreso Total Mensual (S/.)')
axes[0, 0].set_ylabel('Frecuencia')
axes[0, 0].ticklabel_format(style='plain', axis='x')


# Top-Right Plot: Log-Scale Distribution
axes[0, 1].hist(df['INGTOT'], bins=50, color='lightgreen', edgecolor='black')
axes[0, 1].set_xscale('log')
axes[0, 1].set_title('Distribución del Ingreso (Escala Logarítmica)')
axes[0, 1].set_xlabel('Ingreso Total Mensual (S/.) - Escala Log')
axes[0, 1].set_ylabel('Frecuencia')

# Bottom-Left Plot: "Zoomed-In" Distribution
df_zoomed = df[df['INGTOT'] < 15000]
axes[1, 0].hist(df_zoomed['INGTOT'], bins=50, color='salmon', edgecolor='black')
axes[1, 0].set_title('Distribución Detallada (Ingresos < S/15,000)')
axes[1, 0].set_xlabel('Ingreso Total Mensual (S/.)')
axes[1, 0].set_ylabel('Frecuencia')

# Bottom-Right Plot: Boxplot for Outlier Identification
axes[1, 1].boxplot(df['INGTOT'], vert=False, patch_artist=True, boxprops=dict(facecolor='plum'))
axes[1, 1].set_xscale('log') # Use log scale for better visualization of quartiles
axes[1, 1].set_title('Diagrama de Caja para Identificar Outliers')
axes[1, 1].set_xlabel('Ingreso Total Mensual (S/.) - Escala Log')

# General Adjustments
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 2. Save the Figure
if not os.path.exists(EVIDENCE_DIR):
    os.makedirs(EVIDENCE_DIR)
file_name = f"Analisis_Completo_Ingresos_{TIMESTAMP}.png"
file_path = os.path.join(EVIDENCE_DIR, file_name)
fig.savefig(file_path, bbox_inches='tight')
plt.close()

print(f"\nVisualización guardada en: {file_path}")

# --- Storing summary for report ---
with open("summary.txt", "w") as f:
    f.write(summary_text)
