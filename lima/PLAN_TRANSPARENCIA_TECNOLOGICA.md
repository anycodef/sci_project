# Plan de Transparencia Tecnológica

## 1. Introducción

Este documento establece el compromiso de este proyecto con la transparencia, la reproducibilidad y la apertura. El objetivo es proporcionar una visión clara de las metodologías, herramientas y procesos utilizados en el análisis del mercado laboral de Lima, permitiendo que cualquier parte interesada pueda entender, evaluar y, si lo desea, replicar nuestros resultados.

## 2. Fuentes de Datos

- **Origen:** Los datos utilizados provienen de la **Encuesta Permanente de Empleo Nacional (EPEN)**, realizada por el Instituto Nacional de Estadística e Informática (INEI) de Perú.
- **Acceso:** Los microdatos de la encuesta son de acceso público y pueden ser descargados desde el portal oficial del INEI. Se ha documentado el trimestre y año específico de los datos utilizados en la carpeta `01_datos_iniciales`.
- **Diccionario de Variables:** Se proporciona un diccionario de variables (`lima/01_datos_iniciales/diccionario_variables.md`) para facilitar la interpretación de los códigos y nombres de las columnas utilizadas en el análisis.

## 3. Metodología de Procesamiento

El análisis sigue un pipeline de datos estructurado y versionado, donde cada etapa reside en una carpeta numerada que indica su secuencia de ejecución:

1.  **`01_datos_iniciales`:** Almacenamiento de los datos brutos.
2.  **`02_preparacion_y_limpieza`:** Scripts para la limpieza, manejo de valores faltantes, homogeneización de variables y filtrado de datos.
3.  **`03_analisis_exploratorio_eda`:** Notebooks y scripts utilizados para generar estadísticas descriptivas y visualizaciones iniciales.
4.  **`04_seleccion_de_caracteristicas`:** Procesos para identificar las variables más relevantes para el modelado.
5.  **`05_modelado`:** Scripts donde se entrenan, validan y evalúan los modelos predictivos.
6.  **`06_dashboard`:** Código fuente de la aplicación de visualización interactiva.

Cada script incluye comentarios que explican la lógica de las transformaciones de datos realizadas.

## 4. Herramientas y Software

Este proyecto se ha desarrollado utilizando exclusivamente software de código abierto para garantizar la máxima accesibilidad y reproducibilidad.

- **Lenguaje de Programación:** Python 3.x
- **Librerías Principales:**
    - **Pandas:** Para la manipulación y análisis de datos.
    - **NumPy:** Para operaciones numéricas.
    - **Scikit-learn:** Para la implementación de modelos de machine learning.
    - **Matplotlib / Seaborn:** Para la generación de gráficos estáticos.
    - **Streamlit:** Para la creación del dashboard interactivo.
- **Gestión de Dependencias:** Los requerimientos de software están listados en el archivo `lima/06_dashboard/requirements.txt`, permitiendo una fácil instalación en un entorno virtual.

## 5. Control de Versiones y Disponibilidad del Código

- **Control de Versiones:** Todo el código fuente del proyecto está gestionado a través de **Git**. El historial de cambios se encuentra disponible en un repositorio de GitHub, lo que permite una trazabilidad completa de cada modificación realizada.
- **Disponibilidad del Código:** El código fuente completo del proyecto es público y está disponible en el repositorio central del proyecto. Se fomenta su revisión, reutilización y mejora por parte de la comunidad.

## 6. Limitaciones del Análisis

En línea con nuestro compromiso de transparencia, reconocemos las siguientes limitaciones:

- **Sesgos de la Muestra:** Aunque la EPEN utiliza factores de ponderación para ser representativa, pueden existir sesgos inherentes al diseño muestral o a la no respuesta.
- **Simplificaciones del Modelo:** Cualquier modelo es una simplificación de la realidad. Las variables seleccionadas y la arquitectura del modelo pueden no capturar toda la complejidad del mercado laboral.
- **Periodo de Tiempo:** Las conclusiones se basan en los datos del periodo analizado y pueden no ser generalizables a otros contextos temporales.
