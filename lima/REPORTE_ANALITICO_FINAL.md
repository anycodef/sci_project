# Reporte Analítico Final: Mercado Laboral de Lima (2024-2025)

## 1. Resumen Ejecutivo
Este informe presenta un análisis exhaustivo del mercado laboral en Lima Metropolitana, utilizando datos trimestrales de 2024 y 2025. Se detalla un pipeline de datos robusto, desde la limpieza y preprocesamiento hasta la construcción de un modelo de datos conceptual y el desarrollo de un flujo de trabajo para modelos de machine learning.

Los hallazgos clave, respaldados por un análisis estadístico riguroso, confirman que **el nivel educativo, la edad y las horas trabajadas** son predictores potencialmente fuertes de los ingresos y la formalidad laboral. Sin embargo, el análisis también reveló una **severa escasez de datos completos** en la muestra proporcionada, lo que impidió el entrenamiento exitoso de modelos predictivos.

A pesar de las limitaciones de los datos, el proyecto establece una base metodológica sólida para futuros análisis con conjuntos de datos más completos.

## 2. Metodología y Procesamiento de Datos

Se implementó un proceso automatizado para garantizar la reproducibilidad y la calidad de los datos.

### a) Limpieza y Preprocesamiento de Datos
Se desarrolló un script que unifica los datos trimestrales, estandariza columnas, maneja valores faltantes y crea nuevas características para enriquecer el análisis.

**Para más detalles, consulte:** [`DOCUMENTACION_LIMPIEZA.md`](./DOCUMENTACION_LIMPIEZA.md)

### b) Modelo Conceptual de Datos
Se diseñó un modelo de datos para estructurar la información en entidades lógicas como `Persona`, `Situación Laboral` e `Ingresos`, facilitando la comprensión de las relaciones en los datos.

**Para más detalles, consulte:** [`MODELO_DE_DATOS.md`](./MODELO_DE_DATOS.md)

## 3. Análisis Exploratorio y Dashboard
Se enriqueció un dashboard interactivo que permite explorar los datos de forma dinámica. El dashboard ahora incluye nuevas visualizaciones sobre la distribución demográfica, el nivel educativo y la evolución temporal de indicadores clave como el desempleo y la informalidad.

*(Nota: El dashboard se encuentra en la carpeta `06_dashboard`)*

## 4. Selección de Características y Modelado
Se realizó un análisis estadístico para identificar las variables más relevantes para predecir el ingreso y la informalidad.

### a) Selección de Características
Las pruebas de ANOVA y Chi-cuadrado confirmaron que variables como `c208` (edad), `whorat` (horas trabajadas) y `nivel_educativo_agrupado` tienen una relación estadísticamente significativa con las variables objetivo.

**Para más detalles, consulte:** [`../04_seleccion_de_caracteristicas/SELECCION_DE_CARACTERISTICAS.md`](../04_seleccion_de_caracteristicas/SELECCION_DE_CARACTERISTICAS.md)

### b) Flujo de Trabajo de Machine Learning
Se construyó un pipeline de modelado robusto que incluye preprocesamiento, imputación de datos faltantes y entrenamiento de modelos. Sin embargo, el proceso se vio detenido por la falta de datos.

- **Problema Identificado:** Después de filtrar por trabajadores ocupados y eliminar filas con datos faltantes en las variables clave (incluso en un conjunto reducido), no quedaron registros suficientes para entrenar los modelos de regresión y clasificación.
- **Consecuencia:** Los modelos no pudieron ser entrenados, y por lo tanto, no se pueden generar predicciones válidas con la data actual.

**Para más detalles sobre el pipeline, consulte:** [`../05_modelado/MODELADO.md`](../05_modelado/MODELADO.md)

## 5. Conclusiones y Próximos Pasos

### Conclusiones
1.  **Base Metodológica Sólida:** El proyecto ha producido un conjunto de scripts y una metodología documentada que conforman un pipeline de análisis de datos robusto y reproducible.
2.  **Limitación Crítica de Datos:** La principal conclusión del análisis es que la muestra de datos actual es insuficiente para la construcción de modelos predictivos. La escasez de registros completos impide derivar insights cuantitativos fiables a nivel de modelado.
3.  **Potencial Analítico Confirmado:** El análisis de selección de características sugiere que, con datos adecuados, las variables seleccionadas serían excelentes predictores, validando las hipótesis iniciales del proyecto.

### Recomendaciones y Próximos Pasos
- **Adquisición de Datos Más Completos:** La prioridad absoluta es obtener un conjunto de datos más grande y con menos valores faltantes. Un dataset de mayor tamaño es esencial para poder entrenar y validar los modelos de machine learning.
- **Re-ejecución del Pipeline:** Una vez se disponga de mejores datos, el pipeline de scripts desarrollado en este proyecto (desde la limpieza hasta el modelado) puede ser re-ejecutado para obtener los resultados predictivos originalmente planteados.
- **Exploración de Técnicas de Imputación Avanzadas:** Si la adquisición de datos no es posible, se podría investigar el uso de técnicas de imputación más sofisticadas (ej. imputación multivariada) para intentar rescatar más registros, aunque esto debe hacerse con precaución.
