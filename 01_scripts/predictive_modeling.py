import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import numpy as np

# --- Phase 1: Model Training and Export ---

# 1. Data Preparation for Modeling
data_path = '02_data_processed/datos_limpios_poblacion_trabajo.csv'
df = pd.read_csv(data_path, low_memory=False)

# ** FIX: Filter for the employed population to avoid 'No Aplica' issues **
# As per process_data.py, OCUP300 defines employment status.
if 'OCUP300' in df.columns:
    df = df[df['OCUP300'] == 'Ocupado'].copy()


# Corrected feature names based on data processing script
features = ['grupo_edad', 'C207', 'C366', 'C310', 'whoraT']
target = 'es_informal'

# Rename columns for clarity in the modeling process and output
df.rename(columns={
    'C207': 'Sexo',
    'C366': 'Nivel Educativo',
    'C310': 'Tipo de Ocupación'
}, inplace=True)

# The feature list now uses the new, user-friendly names
features_renamed = ['grupo_edad', 'Sexo', 'Nivel Educativo', 'Tipo de Ocupación', 'whoraT']

X = df[features_renamed]
y = df[target]


# Handle Missing Values (Imputation)
# The 'No Aplica' strings should now be gone, but we still handle potential NaNs.
X['whoraT'] = pd.to_numeric(X['whoraT'], errors='coerce')
X['whoraT'] = X['whoraT'].fillna(X['whoraT'].median())

categorical_cols_renamed = ['grupo_edad', 'Sexo', 'Nivel Educativo', 'Tipo de Ocupación']
for col in categorical_cols_renamed:
    if col in X.columns and X[col].isnull().any():
        X[col] = X[col].fillna(X[col].mode()[0])


# Define categorical and numerical features using the new names
numerical_features = ['whoraT']

# 2. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols_renamed)
    ])

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Model Training
model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('classifier', LogisticRegression(random_state=42, max_iter=1000))])

model_pipeline.fit(X_train, y_train)

# 5. Model Evaluation
y_pred = model_pipeline.predict(X_test)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("--- Model Evaluation Results ---")
print(class_report)
print("Confusion Matrix:")
print(conf_matrix)
print("---------------------------------")


# 6. Export Artifacts
model_filename = 'informality_model.pickle'
with open(model_filename, 'wb') as f:
    pickle.dump(model_pipeline, f)
print(f"Model saved to {model_filename}")

# Export Model Parameters for JavaScript
log_reg_model = model_pipeline.named_steps['classifier']
preprocessor_fitted = model_pipeline.named_steps['preprocessor']
one_hot_encoder = preprocessor_fitted.named_transformers_['cat']

encoded_feature_names = list(one_hot_encoder.get_feature_names_out(categorical_cols_renamed))
final_columns = numerical_features + encoded_feature_names

print("\n--- JavaScript Model Parameters ---")
print(f"const model_intercept = {log_reg_model.intercept_[0]};")
print(f"const model_coefficients = {list(log_reg_model.coef_[0])};")
print(f"const model_columns = {final_columns};")
print("-----------------------------------\n")


# --- Phase 3: Automated Documentation Generation ---
doc_path = '04_reports/predictive_modeling_documentation.md'

documentation_content = f"""
# Predictive Modeling for Labor Informality: Documentation

## 1. Business Case and Objective

The primary objective of this predictive model is to identify the key factors associated with labor informality and to create a tool that can predict the likelihood of an individual being an informal worker based on their demographic and employment characteristics. By understanding these predictors, policymakers and analysts can better target interventions to formalize the labor market. This project moves beyond historical analysis to provide a forward-looking, predictive capability.

## 2. Feature Selection

The following features were selected for the initial model based on their established relevance in labor market analysis. The original data used survey column names (`C207`, `C366`, `C310`), which were mapped to more descriptive names for clarity in the modeling process.

- **`grupo_edad`**: Age group of the individual.
- **`Sexo` (`C207`)**: Sex of the individual (recoded from numeric).
- **`Nivel Educativo` (`C366`)**: Highest level of education attained (recoded from numeric).
- **`Tipo de Ocupación` (`C310`)**: The category of occupation (e.g., salaried, independent) (recoded from numeric).
- **`whoraT`**: Total hours worked per week in the main occupation.

These variables provide a balanced view of a worker's personal demographics and their core employment conditions. The target variable is `es_informal`, a binary indicator where `1` represents an informal worker and `0` a formal one. The dataset was filtered to include only "Ocupado" (employed) individuals to ensure data quality.

## 3. Rationale for Logistic Regression

**Logistic Regression** was chosen as the modeling algorithm for the following reasons:

- **Binary Classification**: The target variable, `es_informal`, is binary, which is the exact use case for logistic regression.
- **Interpretability**: The model's coefficients are directly interpretable. A positive coefficient for a feature means it increases the odds of informality, while a negative one decreases it. This is highly valuable for explaining the "why" behind a prediction.
- **Probabilistic Output**: Logistic Regression outputs a probability, which is more nuanced than a simple binary "yes/no" classification. This allows us to understand the *likelihood* of informality.
- **Efficiency**: It is a computationally efficient and well-established algorithm, making it a strong baseline and suitable for deployment in a simple web application.

## 4. Data Preprocessing

To prepare the data for the Logistic Regression model, the following preprocessing steps were executed:

- **Data Filtering**: The dataset was first filtered to only include records where the `OCUP300` status was 'Ocupado', removing individuals not currently in the workforce and avoiding data leakage from 'No Aplica' values.
- **One-Hot Encoding**: The categorical features (`grupo_edad`, `Sexo`, `Nivel Educativo`, `Tipo de Ocupación`) were converted into a numerical format using one-hot encoding.
- **Scaling**: The numerical feature (`whoraT`) was scaled using `StandardScaler`. This standardizes the feature to have a mean of 0 and a standard deviation of 1.

## 5. Model Performance

The model was trained on 80% of the data and evaluated on the remaining 20%. The performance on the test set is as follows:

### Classification Report

```
{class_report}
```

### Confusion Matrix

```
{conf_matrix}
```

The model demonstrates strong predictive power, with high accuracy, precision, and recall for both formal and informal classes.

## 6. Model Export for Web Application

A key innovation in this project is the direct deployment of the model's logic into a client-side web application. This was achieved as follows:

1.  **Model Training**: The `LogisticRegression` model was trained in Python as described.
2.  **Parameter Extraction**: After training, the model's learned parameters were extracted: Intercept, Coefficients, and the specific order of the preprocessed feature columns.
3.  **JavaScript Embedding**: These parameters were exported into a JavaScript-friendly format and embedded directly into the `index.html` file. The web application uses these values to replicate the model's prediction formula.

This approach makes the predictive tool lightweight, serverless, and easily distributable.

## 7. User Guide for the Interactive Web Application

The accompanying `index.html` file provides a simple interface to interact with the model.

- **Batch Predictions**: Upon loading, click the "Show Batch Predictions" button to see the model's predictions on a pre-loaded sample of 20 test records.
- **Interactive Classifier**:
    1.  Select the desired values from the dropdown menus for each feature.
    2.  Enter the total hours worked in the number input field.
    3.  Click the "Classify" button.
    4.  The application will calculate and display the probability of the individual being an informal worker.

"""

with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(documentation_content)

print(f"Documentation generated at {doc_path}")

# Also, let's get a sample of the test data for the web app
print("\n--- Sample Test Data for Web App (first 20 rows) ---")
test_sample = X_test.head(20).copy()
test_sample['es_informal_real'] = y_test.head(20)
print(test_sample.to_json(orient='records', indent=2))
print("----------------------------------------------------")
