
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
              precision    recall  f1-score   support

           0       0.79      0.84      0.81        57
           1       0.57      0.48      0.52        25

    accuracy                           0.73        82
   macro avg       0.68      0.66      0.67        82
weighted avg       0.72      0.73      0.72        82

```

### Confusion Matrix

```
[[48  9]
 [13 12]]
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
