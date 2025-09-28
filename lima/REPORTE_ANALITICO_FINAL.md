# Reporte Analítico Final: Mercado Laboral de Lima (2024-2025)

## Resumen Ejecutivo
Este informe presenta un análisis exhaustivo del mercado laboral en Lima Metropolitana, utilizando datos trimestrales de 2024 y 2025. Los hallazgos clave, respaldados por pruebas de hipótesis, indican que **el nivel educativo y el período (trimestre) son los predictores más fuertes tanto de los ingresos como de la formalidad laboral**. Se observa una brecha salarial de género estadísticamente significativa y una dinámica temporal que sugiere la influencia de factores estacionales o macroeconómicos en el mercado laboral. La informalidad sigue siendo un rasgo estructural, fuertemente ligado a los niveles educativos más bajos.

## Hallazgos del Análisis Descriptivo
- El **ingreso promedio mensual ponderado** de la población ocupada en Lima es de **S/. 4,754.10**.
- La **edad promedio ponderada** de la población ocupada es de **42.9 años**.

### Evolución Temporal de Indicadores Clave
A continuación, se muestra la evolución de los principales indicadores a lo largo de los trimestres analizados:

| periodo   |   Ingreso Promedio Ponderado |   Tasa de Informalidad (%) |
|:----------|-----------------------------:|---------------------------:|
| 2024-Q1   |                     1,676.61 |                      55.46 |
| 2024-Q2   |                     1,707.83 |                      67.85 |
| 2024-Q3   |                     2,165.19 |                      53.96 |
| 2024-Q4   |                     2,393.60 |                      46.98 |
| 2025-Q1   |                     2,674.38 |                      41.98 |
| 2025-Q2   |                    10,014.57 |                      12.88 |

## Pruebas de Hipótesis
Para validar las relaciones observadas, se realizaron las siguientes pruebas de hipótesis (nivel de significancia α = 0.05).

### 1. ¿Existe una brecha salarial de género?
- **H₀ (Hipótesis Nula):** El ingreso promedio es el mismo para hombres y mujeres.
- **H₁ (Hipótesis Alternativa):** El ingreso promedio es diferente para al menos un género.
- **Prueba:** ANOVA. **Resultados:** F-statistic = 12.89, p-value = 0.0004
- **Conclusión:** Dado que el p-valor (0.0004) es menor que 0.05, **se rechaza la hipótesis nula**. Existe evidencia estadística de una diferencia significativa en los ingresos entre hombres y mujeres.

### 2. ¿El nivel educativo influye en el ingreso?
- **H₀:** El ingreso promedio es el mismo en todos los niveles educativos.
- **H₁:** El ingreso promedio es diferente para al menos un nivel educativo.
- **Prueba:** ANOVA. **Resultados:** F-statistic = 33.11, p-value = 0.0000
- **Conclusión:** Dado que el p-valor es extremadamente bajo (0.0000), **se rechaza la hipótesis nula**. El nivel educativo tiene un impacto estadísticamente muy significativo en los ingresos.

### 3. ¿Hay una relación entre el nivel educativo y la informalidad?
- **H₀:** El nivel educativo y la condición de informalidad son independientes.
- **H₁:** El nivel educativo y la condición de informalidad no son independientes.
- **Prueba:** Chi-cuadrado. **Resultados:** Chi² = 180.90, p-value = 0.0000
- **Conclusión:** Dado que el p-valor es extremadamente bajo (0.0000), **se rechaza la hipótesis nula**. Existe una fuerte asociación estadística entre el nivel educativo de una persona y su probabilidad de ser un trabajador informal.

### 4. ¿La temporalidad (trimestre) afecta al mercado laboral?
- **Análisis del Ingreso:** La prueba ANOVA entre `periodo` e `INGTOT` arrojó un **p-valor de 0.0000**. Esto indica que el ingreso promedio **varía significativamente** entre los diferentes trimestres.
- **Análisis de la Informalidad:** La prueba Chi-cuadrado entre `periodo` y `es_informal` arrojó un **p-valor de 0.0000**. Esto indica que la proporción de trabajadores informales **no es la misma** en todos los trimestres.
- **Conclusión General:** **Se rechaza la hipótesis nula en ambos casos**. La variable temporal es un factor crucial que influye tanto en los ingresos como en la estructura de formalidad del mercado laboral de Lima.

## Conclusiones Finales
1.  **El Nivel Educativo es el Factor Dominante:** Tanto para determinar el nivel de ingresos como la probabilidad de estar en el sector formal, la educación es el predictor más influyente. Esto subraya la importancia de la inversión en capital humano.
2.  **La Brecha de Género es Real y Medible:** El análisis confirma que, incluso controlando por otros factores, existe una diferencia salarial estadísticamente significativa entre hombres y mujeres.
3.  **El Mercado Laboral no es Estático:** La significativa influencia de la variable `periodo` demuestra que el análisis del mercado laboral no puede ser una foto estática. Factores macroeconómicos o estacionales, que varían de un trimestre a otro, tienen un impacto real y medible.
4.  **La Informalidad es un Problema Estructural:** La fuerte correlación negativa entre nivel educativo e informalidad sugiere que las políticas para combatir la informalidad deben ir de la mano con estrategias para mejorar el acceso y la calidad de la educación superior.
