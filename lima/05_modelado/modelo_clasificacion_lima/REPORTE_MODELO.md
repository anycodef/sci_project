
# Reporte del Modelo de Clasificación
- **Objetivo:** Predecir `es_informal`.
- **Modelo:** RandomForestClassifier.
- **Justificación del `sample_weight`:** Similar al de regresión, para generalizar a la población de Lima.
## Métricas de Evaluación
- **Accuracy:** 0.7626
- **ROC AUC Score:** 0.8032
### Reporte de Clasificación:
```
              precision    recall  f1-score   support

           0       0.76      0.88      0.81        82
           1       0.77      0.60      0.67        57

    accuracy                           0.76       139
   macro avg       0.77      0.74      0.74       139
weighted avg       0.76      0.76      0.76       139

```
