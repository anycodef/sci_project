# Reporte de Selección de Características (Set Reducido)

Debido a la escasez de datos completos, se utilizó un conjunto reducido de predictores para el análisis.

## 1. Modelo de Regresión (Variable Objetivo: `ingtot`)

### a) Correlación de Pearson con Variables Numéricas

| Variable | Coeficiente de Correlación | P-value |
|---|---|---|
| *Todas* | No se pudo calcular (datos insuficientes) | N/A |

*Conclusión: p-value < 0.05 indica correlación lineal significativa.*

### b) Relación con Variables Categóricas (ANOVA)

| Variable | F-statistic | P-value |
|---|---|---|
| *Todas* | No se pudo calcular (datos insuficientes) | N/A |

*Conclusión: p-value < 0.05 indica que la media del ingreso varía entre categorías.*

## 2. Modelo de Clasificación (Variable Objetivo: `es_informal`)

### a) Relación con Variables Numéricas (ANOVA)

| Variable | F-statistic | P-value |
|---|---|---|
| *Todas* | No se pudo calcular (datos insuficientes) | N/A |

*Conclusión: p-value < 0.05 sugiere que el valor medio de la variable es diferente para formales e informales.*

### b) Asociación con Variables Categóricas (Chi-Cuadrado)

| Variable | Chi2-statistic | P-value |
|---|---|---|
| *Todas* | No se pudo calcular (datos insuficientes) | N/A |

*Conclusión: p-value < 0.05 indica una asociación significativa con la informalidad.*

## 3. Conclusión General

No se pudo realizar el análisis estadístico para la selección de características debido a la **insuficiencia de datos completos** en la muestra, incluso con un conjunto reducido de predictores. Esto impide determinar la significancia estadística de las variables.

Se recomienda proceder con la etapa de modelado utilizando estas variables, pero con la advertencia de que su poder predictivo no ha podido ser validado estadísticamente de antemano. La importancia final de las características deberá ser evaluada post-entrenamiento del modelo (si los datos lo permiten).
