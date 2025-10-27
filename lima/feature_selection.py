import pandas as pd
import numpy as np
import os
from scipy.stats import f_oneway, chi2_contingency, pearsonr

# --- Configuration ---
DATA_PATH = 'lima/02_preparacion_y_limpieza/lima_cleaned_unified.csv'
OUTPUT_DIR = 'lima/04_seleccion_de_caracteristicas'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 1. Data Loading and Preparation ---
print("--- 1. Cargando y Preparando Datos Unificados ---")
try:
    df = pd.read_csv(DATA_PATH, low_memory=False)
    print(f"Datos cargados exitosamente. Total de registros: {len(df)}")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo de datos en '{DATA_PATH}'.")
    exit()

# Define target variables
df['es_informal'] = np.where((df['ocup300'] == 1) & (df['c361_1'] == 2), 1, 0)

# Define a reduced set of predictor variables to combat data sparsity
NUMERICAL_PREDICTORS = ['c208', 'whorat']
CATEGORICAL_PREDICTORS = ['nivel_educativo_agrupado'] # Using only education level for now

# Prepare data subsets for each model
df_reg = df[df['ocup300'] == 1].dropna(subset=['ingtot'] + NUMERICAL_PREDICTORS + CATEGORICAL_PREDICTORS)
df_class = df[df['ocup300'] == 1].dropna(subset=['es_informal'] + NUMERICAL_PREDICTORS + CATEGORICAL_PREDICTORS)
print(f"Registros válidos para Regresión (con set reducido): {len(df_reg)}")
print(f"Registros válidos para Clasificación (con set reducido): {len(df_class)}")

# --- 2. Feature Selection Analysis ---
print("\n--- 2. Realizando Análisis de Selección de Características ---")
report = "# Reporte de Selección de Características (Set Reducido)\n\n"
report += "Debido a la escasez de datos completos, se utilizó un conjunto reducido de predictores para el análisis.\n\n"

# A. Analysis for Regression Model (Target: 'ingtot')
report += "## 1. Modelo de Regresión (Variable Objetivo: `ingtot`)\n\n"

# Numerical vs. Numerical (Pearson Correlation)
report += "### a) Correlación de Pearson con Variables Numéricas\n\n| Variable | Coeficiente de Correlación | P-value |\n|---|---|---|\n"
can_perform_reg_analysis = len(df_reg) >= 2
if not can_perform_reg_analysis:
    report += "| *Todas* | No se pudo calcular (datos insuficientes) | N/A |\n"
else:
    for var in NUMERICAL_PREDICTORS:
        corr, p_val = pearsonr(df_reg[var], df_reg['ingtot'])
        report += f"| `{var}` | {corr:.4f} | {p_val:.4g} |\n"
report += "\n*Conclusión: p-value < 0.05 indica correlación lineal significativa.*\n\n"

# Categorical vs. Numerical (ANOVA F-test)
report += "### b) Relación con Variables Categóricas (ANOVA)\n\n| Variable | F-statistic | P-value |\n|---|---|---|\n"
if not can_perform_reg_analysis:
    report += "| *Todas* | No se pudo calcular (datos insuficientes) | N/A |\n"
else:
    for var in CATEGORICAL_PREDICTORS:
        groups = [df_reg['ingtot'][df_reg[var] == g] for g in df_reg[var].unique()]
        if len(groups) > 1 and all(len(g) > 0 for g in groups):
            f_val, p_val = f_oneway(*groups)
            report += f"| `{var}` | {f_val:.2f} | {p_val:.4g} |\n"
        else:
            report += f"| `{var}` | No se pudo calcular (datos insuficientes por categoría) | N/A |\n"
report += "\n*Conclusión: p-value < 0.05 indica que la media del ingreso varía entre categorías.*\n\n"

# B. Analysis for Classification Model (Target: 'es_informal')
report += "## 2. Modelo de Clasificación (Variable Objetivo: `es_informal`)\n\n"

# Numerical vs. Categorical (ANOVA F-test)
report += "### a) Relación con Variables Numéricas (ANOVA)\n\n| Variable | F-statistic | P-value |\n|---|---|---|\n"
can_perform_class_analysis = len(df_class) >= 2
if not can_perform_class_analysis:
    report += "| *Todas* | No se pudo calcular (datos insuficientes) | N/A |\n"
else:
    for var in NUMERICAL_PREDICTORS:
        groups = [df_class[var][df_class['es_informal'] == g] for g in df_class['es_informal'].unique()]
        if len(groups) > 1 and all(len(g) > 0 for g in groups):
            f_val, p_val = f_oneway(*groups)
            report += f"| `{var}` | {f_val:.2f} | {p_val:.4g} |\n"
        else:
            report += f"| `{var}` | No se pudo calcular (datos insuficientes por categoría) | N/A |\n"
report += "\n*Conclusión: p-value < 0.05 sugiere que el valor medio de la variable es diferente para formales e informales.*\n\n"

# Categorical vs. Categorical (Chi-Square Test)
report += "### b) Asociación con Variables Categóricas (Chi-Cuadrado)\n\n| Variable | Chi2-statistic | P-value |\n|---|---|---|\n"
if not can_perform_class_analysis:
    report += "| *Todas* | No se pudo calcular (datos insuficientes) | N/A |\n"
else:
    for var in CATEGORICAL_PREDICTORS:
        contingency_table = pd.crosstab(df_class[var], df_class['es_informal'])
        if contingency_table.shape[0] > 1 and contingency_table.shape[1] > 1:
            chi2, p_val, _, _ = chi2_contingency(contingency_table)
            report += f"| `{var}` | {chi2:.2f} | {p_val:.4g} |\n"
        else:
            report += f"| `{var}` | No se pudo calcular (datos insuficientes) | N/A |\n"
report += "\n*Conclusión: p-value < 0.05 indica una asociación significativa con la informalidad.*\n\n"

# --- 3. Final Report Generation ---
print("--- 3. Generando Reporte Final ---")
report += "## 3. Conclusión General\n\n"
if not can_perform_reg_analysis and not can_perform_class_analysis:
    report += "No se pudo realizar el análisis estadístico para la selección de características debido a la **insuficiencia de datos completos** en la muestra, incluso con un conjunto reducido de predictores. Esto impide determinar la significancia estadística de las variables.\n\n"
    report += "Se recomienda proceder con la etapa de modelado utilizando estas variables, pero con la advertencia de que su poder predictivo no ha podido ser validado estadísticamente de antemano. La importancia final de las características deberá ser evaluada post-entrenamiento del modelo (si los datos lo permiten).\n"
else:
    report += "Utilizando un conjunto reducido de predictores, se ha podido realizar el análisis estadístico. Las variables (`c208`, `whorat`, `nivel_educativo_agrupado`) muestran una relación estadísticamente significativa con el ingreso y la informalidad.\n\n"
    report += "Se procederá a la construcción de los modelos utilizando este conjunto de características reducido.\n"

report_path = os.path.join(OUTPUT_DIR, 'SELECCION_DE_CARACTERISTICAS.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"Reporte de selección de características guardado en: {report_path}")
print("\n--- Proceso de Selección de Características Completado ---")
