import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, classification_report, roc_auc_score

# --- Configuration ---
DATA_PATH = 'lima/02_preparacion_y_limpieza/lima_cleaned_unified.csv'
MODEL_DIR = 'lima/05_modelado'
REG_MODEL_DIR = os.path.join(MODEL_DIR, 'modelo_regresion_lima')
CLASS_MODEL_DIR = os.path.join(MODEL_DIR, 'modelo_clasificacion_lima')
os.makedirs(REG_MODEL_DIR, exist_ok=True)
os.makedirs(CLASS_MODEL_DIR, exist_ok=True)

# --- 1. Data Loading and Preparation ---
print("--- 1. Cargando Datos Unificados para Modelado ---")
try:
    df = pd.read_csv(DATA_PATH, low_memory=False)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo de datos en '{DATA_PATH}'."); exit()

# --- 2. Feature Engineering and Selection ---
df['es_informal'] = np.where((df['ocup300'] == 1) & (df['c361_1'] == 2), 1, 0)

# Using the reduced feature set due to data sparsity
features = ['c208', 'whorat', 'nivel_educativo_agrupado']
numerical_features = ['c208', 'whorat']
categorical_features = ['nivel_educativo_agrupado']

# --- 3. Preprocessing Pipeline ---
# Create a robust preprocessing pipeline that includes imputation
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer(transformers=[
    ('num', numerical_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])

# --- 4. Regression Model (Predicting 'ingtot') ---
print("\n--- 4. Entrenando Modelo de Regresión ---")
df_reg = df[df['ocup300'] == 1].copy()
# Drop rows where the target ('ingtot') is missing, as we can't train on them
df_reg.dropna(subset=['ingtot'], inplace=True)

if len(df_reg) < 10:
    print("ADVERTENCIA: Datos insuficientes para entrenar el modelo de regresión.")
    reg_report = "# Reporte del Modelo de Regresión\n\nNo se pudo entrenar el modelo debido a la falta de datos suficientes."
else:
    X_reg = df_reg[features]
    y_reg = df_reg['ingtot']
    weights_reg = df_reg['factor_expansion'].fillna(1) # Impute missing weights to 1

    X_train_reg, X_test_reg, y_train_reg, y_test_reg, w_train_reg, w_test_reg = train_test_split(
        X_reg, y_reg, weights_reg, test_size=0.25, random_state=42)

    reg_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])

    reg_pipeline.fit(X_train_reg, y_train_reg, regressor__sample_weight=w_train_reg)
    y_pred_reg = reg_pipeline.predict(X_test_reg)

    r2 = r2_score(y_test_reg, y_pred_reg)
    mae = mean_absolute_error(y_test_reg, y_pred_reg)

    joblib.dump(reg_pipeline, os.path.join(REG_MODEL_DIR, 'modelo_regresion.joblib'))
    reg_report = f"""# Reporte del Modelo de Regresión
- **Objetivo:** Predecir `ingtot`.
- **Modelo:** RandomForestRegressor con Imputación (mediana/más frecuente).
- **Características Usadas:** {features}
## Métricas
- **R²:** {r2:.4f}
- **MAE:** S/. {mae:,.2f}
"""
print("Modelo de regresión y reporte guardados.")

# --- 5. Classification Model (Predicting 'es_informal') ---
print("\n--- 5. Entrenando Modelo de Clasificación ---")
df_class = df[df['ocup300'] == 1].copy()
df_class.dropna(subset=['es_informal'], inplace=True)

if len(df_class) < 10:
    print("ADVERTENCIA: Datos insuficientes para entrenar el modelo de clasificación.")
    class_report = "# Reporte del Modelo de Clasificación\n\nNo se pudo entrenar el modelo debido a la falta de datos suficientes."
else:
    X_class = df_class[features]
    y_class = df_class['es_informal']
    weights_class = df_class['factor_expansion'].fillna(1)

    X_train_class, X_test_class, y_train_class, y_test_class, w_train_class, w_test_class = train_test_split(
        X_class, y_class, weights_class, test_size=0.25, random_state=42, stratify=y_class)

    class_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced'))
    ])

    class_pipeline.fit(X_train_class, y_train_class, classifier__sample_weight=w_train_class)
    y_pred_class = class_pipeline.predict(X_test_class)
    y_pred_proba_class = class_pipeline.predict_proba(X_test_class)[:, 1]

    accuracy = accuracy_score(y_test_class, y_pred_class)
    roc_auc = roc_auc_score(y_test_class, y_pred_proba_class)

    joblib.dump(class_pipeline, os.path.join(CLASS_MODEL_DIR, 'modelo_clasificacion.joblib'))
    class_report = f"""# Reporte del Modelo de Clasificación
- **Objetivo:** Predecir `es_informal`.
- **Modelo:** RandomForestClassifier con Imputación.
- **Características Usadas:** {features}
## Métricas
- **Accuracy:** {accuracy:.4f}
- **ROC AUC:** {roc_auc:.4f}
### Reporte de Clasificación:
```
{classification_report(y_test_class, y_pred_class)}
```
"""
print("Modelo de clasificación y reporte guardados.")

# --- 6. Consolidate Documentation ---
print("\n--- 6. Generando Documentación Final del Modelado ---")
final_doc = f"""# Documentación del Proceso de Modelado

Este documento resume el proceso de construcción y evaluación de los modelos de Machine Learning.

## 1. Estrategia General

Debido a la escasez de datos completos en el conjunto de muestra, se adoptó la siguiente estrategia:
- **Conjunto de Características Reducido:** Se utilizaron solo las variables más críticas (`c208`, `whorat`, `nivel_educativo_agrupado`) para maximizar la cantidad de datos disponibles.
- **Imputación de Datos Faltantes:** Se utilizó `SimpleImputer` para rellenar los valores faltantes en las variables predictoras (mediana para numéricas, más frecuente para categóricas), evitando así descartar filas valiosas.
- **Ponderación de Muestras:** Se utilizó el `factor_expansion` como peso de muestra (`sample_weight`) en el entrenamiento para que los modelos aprendan de una distribución representativa de la población de Lima.

---
{reg_report}
---
{class_report}
"""
with open(os.path.join(MODEL_DIR, 'MODELADO.md'), 'w', encoding='utf-8') as f:
    f.write(final_doc)

print("Documentación consolidada del modelado guardada en `lima/05_modelado/MODELADO.md`")
print("\n--- Proceso de Modelado Completado ---")
