import pandas as pd
import numpy as np
import os
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, classification_report, roc_auc_score

# --- Configuración ---
DATA_DIR = 'lima/02_preparacion_y_limpieza'
MODEL_DIR = 'lima/05_modelado'
REG_MODEL_DIR = os.path.join(MODEL_DIR, 'modelo_regresion_lima')
CLASS_MODEL_DIR = os.path.join(MODEL_DIR, 'modelo_clasificacion_lima')

# --- Funciones Auxiliares ---
def extract_period_from_filename(filename):
    match = re.search(r'Trim ([A-Za-z-]+)(\d{2})', filename)
    if match:
        month_map = {
            'Ene-Feb-Mar': 'Q1', 'Abr-May-Jun': 'Q2', 'Jul-Ago-Set': 'Q3',
            'Set-Oct-Nov': 'Q4', 'Mar-Abr-May': 'Q2'
        }
        months, year = match.groups()
        quarter = month_map.get(months, 'Q_Unk')
        return f"20{year}-{quarter}"
    return "Periodo_Desconocido"

# --- 1. Carga y Preparación de Datos ---
print("--- 1. Cargando y Preparando Datos para Modelado ---")
try:
    cleaned_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith('lima_cleaned_')])
    df_list = [pd.read_csv(os.path.join(DATA_DIR, f), low_memory=False) for f in cleaned_files]
    for df, filename in zip(df_list, cleaned_files):
        df['periodo'] = extract_period_from_filename(filename)
    master_df = pd.concat(df_list, ignore_index=True)
except Exception as e:
    print(f"Error al cargar datos: {e}"); exit()

# --- Feature Engineering y Selección ---
master_df['es_informal'] = np.where((master_df['OCUP300'] == 1) & (master_df['C361_1'] == 2), 1, 0)
features = ['C207', 'C366', 'periodo', 'C208', 'whoraT']
categorical_features = ['C207', 'C366', 'periodo']
numerical_features = ['C208', 'whoraT']

# --- Pipeline de Preprocesamiento ---
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numerical_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

# --- 2. Modelo de Regresión (Predecir INGTOT) ---
print("\n--- 2. Entrenando Modelo de Regresión ---")
df_reg = master_df[master_df['OCUP300'] == 1].dropna(subset=features + ['INGTOT', 'factor_expansion'])
X_reg = df_reg[features]
y_reg = df_reg['INGTOT']
weights_reg = df_reg['factor_expansion']
X_train_reg, X_test_reg, y_train_reg, y_test_reg, w_train_reg, w_test_reg = train_test_split(
    X_reg, y_reg, weights_reg, test_size=0.2, random_state=42)

reg_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
])

reg_pipeline.fit(X_train_reg, y_train_reg, regressor__sample_weight=w_train_reg)
y_pred_reg = reg_pipeline.predict(X_test_reg)

# Evaluación
r2 = r2_score(y_test_reg, y_pred_reg)
mae = mean_absolute_error(y_test_reg, y_pred_reg)

# Guardar modelo y reporte
joblib.dump(reg_pipeline, os.path.join(REG_MODEL_DIR, 'modelo_regresion.joblib'))
reg_report = f"""
# Reporte del Modelo de Regresión
- **Objetivo:** Predecir `INGTOT` (Ingreso Total).
- **Modelo:** RandomForestRegressor.
- **Justificación del `sample_weight`:** Se usó `factor_expansion` para que el modelo aprenda de una distribución que represente a la población de Lima, no solo a la muestra.
## Métricas de Evaluación
- **R-cuadrado (R²):** {r2:.4f}
- **Error Absoluto Medio (MAE):** S/. {mae:,.2f}
"""
with open(os.path.join(REG_MODEL_DIR, 'REPORTE_MODELO.md'), 'w') as f: f.write(reg_report)
print("Modelo de regresión y reporte guardados.")

# --- 3. Modelo de Clasificación (Predecir es_informal) ---
print("\n--- 3. Entrenando Modelo de Clasificación ---")
df_class = master_df[master_df['OCUP300'] == 1].dropna(subset=features + ['es_informal', 'factor_expansion'])
X_class = df_class[features]
y_class = df_class['es_informal']
weights_class = df_class['factor_expansion']
X_train_class, X_test_class, y_train_class, y_test_class, w_train_class, w_test_class = train_test_split(
    X_class, y_class, weights_class, test_size=0.2, random_state=42, stratify=y_class)

class_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced'))
])

class_pipeline.fit(X_train_class, y_train_class, classifier__sample_weight=w_train_class)
y_pred_class = class_pipeline.predict(X_test_class)
y_pred_proba_class = class_pipeline.predict_proba(X_test_class)[:, 1]

# Evaluación
accuracy = accuracy_score(y_test_class, y_pred_class)
roc_auc = roc_auc_score(y_test_class, y_pred_proba_class)
class_rep = classification_report(y_test_class, y_pred_class)

# Guardar modelo y reporte
joblib.dump(class_pipeline, os.path.join(CLASS_MODEL_DIR, 'modelo_clasificacion.joblib'))
class_report = f"""
# Reporte del Modelo de Clasificación
- **Objetivo:** Predecir `es_informal`.
- **Modelo:** RandomForestClassifier.
- **Justificación del `sample_weight`:** Similar al de regresión, para generalizar a la población de Lima.
## Métricas de Evaluación
- **Accuracy:** {accuracy:.4f}
- **ROC AUC Score:** {roc_auc:.4f}
### Reporte de Clasificación:
```
{class_rep}
```
"""
with open(os.path.join(CLASS_MODEL_DIR, 'REPORTE_MODELO.md'), 'w') as f: f.write(class_report)
print("Modelo de clasificación y reporte guardados.")
print("\n--- Proceso de Modelado Completado ---")