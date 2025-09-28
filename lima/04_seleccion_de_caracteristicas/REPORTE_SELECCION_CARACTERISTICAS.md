# Reporte de Selección de Características

Este documento justifica la selección de variables para los modelos de clasificación y regresión.

## 1. Para Modelo de Regresión (Objetivo: INGTOT)

### a) Correlación con Variables Numéricas
|        |    INGTOT |
|:-------|----------:|
| INGTOT | 1         |
| C208   | 0.219936  |
| whoraT | 0.0856152 |

### b) Relación con Variables Categóricas (ANOVA)
- **C207**: F-statistic = 12.89, p-value = 0.0004
  - *Conclusión: Significativo. La media de INGTOT varía según esta categoría.*
- **C366**: F-statistic = 33.11, p-value = 0.0000
  - *Conclusión: Significativo. La media de INGTOT varía según esta categoría.*
- **periodo**: F-statistic = 132.01, p-value = 0.0000
  - *Conclusión: Significativo. La media de INGTOT varía según esta categoría.*

## 2. Para Modelo de Clasificación (Objetivo: es_informal)

### a) Relación con Variables Categóricas (Chi-Cuadrado)
- **C207**: Chi2 = 0.11, p-value = 0.7387
  - *Conclusión: No significativo.*
- **C366**: Chi2 = 180.90, p-value = 0.0000
  - *Conclusión: Significativo. Hay una asociación entre la variable y la informalidad.*
- **periodo**: Chi2 = 99.03, p-value = 0.0000
  - *Conclusión: Significativo. Hay una asociación entre la variable y la informalidad.*

## 3. Conclusión de Selección

Basado en los p-values, la mayoría de las variables analizadas, **incluyendo 'periodo'**, muestran una relación estadísticamente significativa con los objetivos de ingreso e informalidad. Por lo tanto, se recomienda su inclusión como predictores en los modelos iniciales. La relevancia final se determinará durante el entrenamiento y la evaluación del modelo.
