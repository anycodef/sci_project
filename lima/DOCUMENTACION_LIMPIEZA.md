# Documentación del Proceso de Limpieza y Preprocesamiento de Datos

Este documento detalla los pasos realizados en el script `data_cleaning_script.py` para limpiar, transformar y unificar los datos trimestrales de la encuesta.

---

### 1. Unificación de Archivos Trimestrales

El primer paso consistió en consolidar los datos de los seis archivos CSV trimestrales en un único DataFrame. Este enfoque centraliza el preprocesamiento y facilita el análisis de series temporales.

- **Creación de la Columna `trimestre`:** Para mantener la dimensión temporal, se extrajo el trimestre y el año del nombre de cada archivo y se creó una columna `trimestre` (e.g., `2024_EneFebMar`).

---

### 2. Estandarización y Limpieza General

Se aplicaron varias transformaciones para asegurar la consistencia y calidad de los datos.

- **Nombres de Columnas:** Todos los nombres de las columnas se convirtieron a minúsculas para facilitar el acceso (e.g., `C208` a `c208`).
- **Factor de Expansión:** La columna de factor de expansión (e.g., `fa_efm24`) fue renombrada a `factor_expansion` y convertida a tipo numérico.
- **Manejo de Códigos Especiales:** Se reemplazaron los códigos que indican valores perdidos (e.g., `99`, `9999`) con `NaN` de NumPy, basándose en el diccionario de variables. Esto es crucial para realizar cálculos y modelos precisos.

---

### 3. Corrección de Tipos de Datos

Para optimizar el uso de memoria y asegurar la correcta interpretación de las variables, se realizó una conversión de tipos:

- **Variables Numéricas:** Las columnas que contenían representaciones numéricas como texto se convirtieron a tipos numéricos (`int` o `float`).
- **Variables Categóricas:** Las columnas que no pudieron convertirse a numéricas se transformaron en tipo `category` de Pandas, que es más eficiente para variables con un número limitado de valores.

---

### 4. Ingeniería de Características (Feature Engineering)

Para enriquecer el dataset y facilitar el modelado, se crearon nuevas variables a partir de las existentes:

- **`grupo_edad`:** Se agrupó la variable `c208` (edad) en categorías (`0-14`, `15-24`, `25-39`, `40-59`, `60+`) para facilitar análisis demográficos.
- **`tiene_seguro`:** Se creó una variable binaria (`1` o `0`) que indica si una persona está afiliada a *cualquier* tipo de seguro de salud, consolidando la información de múltiples columnas (`c361_1` a `c361_8`).
- **`nivel_educativo_agrupado`:** Se reagrupó la variable `c366` (nivel educativo) en categorías más amplias (`Sin Nivel`, `Primaria`, `Secundaria`, `Superior No Univ.`, `Superior Univ.`, `Postgrado`) para simplificar el análisis y el modelado.

---

### 5. Resultado Final

El resultado de este proceso es un único archivo CSV, `lima_cleaned_unified.csv`, que contiene los datos limpios y enriquecidos de todos los trimestres, listo para las etapas de análisis exploratorio, selección de características y modelado. Los archivos intermedios (`lima_filtered_*.csv`) fueron eliminados para mantener el directorio de trabajo organizado.
