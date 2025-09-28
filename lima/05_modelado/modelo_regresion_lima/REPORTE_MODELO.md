
# Reporte del Modelo de Regresión
- **Objetivo:** Predecir `INGTOT` (Ingreso Total).
- **Modelo:** RandomForestRegressor.
- **Justificación del `sample_weight`:** Se usó `factor_expansion` para que el modelo aprenda de una distribución que represente a la población de Lima, no solo a la muestra.
## Métricas de Evaluación
- **R-cuadrado (R²):** 0.5377
- **Error Absoluto Medio (MAE):** S/. 1,379.00
