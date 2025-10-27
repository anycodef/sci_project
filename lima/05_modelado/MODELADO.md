# Documentación del Proceso de Modelado

Este documento resume el proceso de construcción y evaluación de los modelos de Machine Learning.

## 1. Estrategia General

Debido a la escasez de datos completos en el conjunto de muestra, se adoptó la siguiente estrategia:
- **Conjunto de Características Reducido:** Se utilizaron solo las variables más críticas (`c208`, `whorat`, `nivel_educativo_agrupado`) para maximizar la cantidad de datos disponibles.
- **Imputación de Datos Faltantes:** Se utilizó `SimpleImputer` para rellenar los valores faltantes en las variables predictoras (mediana para numéricas, más frecuente para categóricas), evitando así descartar filas valiosas.
- **Ponderación de Muestras:** Se utilizó el `factor_expansion` como peso de muestra (`sample_weight`) en el entrenamiento para que los modelos aprendan de una distribución representativa de la población de Lima.

---
# Reporte del Modelo de Regresión

No se pudo entrenar el modelo debido a la falta de datos suficientes.
---
# Reporte del Modelo de Clasificación

No se pudo entrenar el modelo debido a la falta de datos suficientes.
