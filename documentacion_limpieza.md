# Documentación del Proceso de Limpieza de Datos - EPEN

## 1. Introducción
Este documento detalla el proceso de limpieza y preparación de los datos de la Encuesta Permanente de Empleo Nacional (EPEN) a partir de los 6 archivos CSV trimestrales. El objetivo fue consolidar, limpiar y estructurar la información para facilitar su uso en análisis futuros, utilizando un script de Python (`process_data.py`) y la librería pandas.

## 2. Proceso de Limpieza

### 2.1. Unificación de los 6 Archivos Trimestrales
El primer paso consistió en unificar los seis archivos CSV. Se leyeron todos los archivos del directorio `Empleabilidad/` y se añadió una columna `periodo` a cada uno para identificar el trimestre de origen (e.g., '2024-Q1'). Luego, se concatenaron en un único dataframe maestro.

### 2.2. Consolidación y Ajuste del Factor de Expansión
Cada archivo trimestral contenía su propio factor de expansión (columnas `fa_*`). Para consolidarlos:
1.  Se convirtieron las columnas de factores a tipo numérico.
2.  Se creó una columna `factor_expansion` sumando los valores de estas columnas. Para la población no encuestada en el módulo de empleo (menores de 14 años), este valor es 0, ya que no se les asigna factor de expansión en los datos brutos.
3.  Se creó `factor_ajustado`, dividiendo `factor_expansion` por 6 (el número total de periodos). Este es el factor a usar para análisis poblacionales que combinen trimestres.
4.  Las columnas `fa_*` originales fueron eliminadas.

### 2.3. División de la Data por Edad (C208)
La data se segmentó según la edad (`C208`), siguiendo la documentación de la encuesta:
*   `poblacion_trabajo_df`: Registros con `C208 >= 14`.
*   `poblacion_no_trabajo_df`: Registros con `C208 < 14`.

### 2.4. Limpieza de `poblacion_trabajo_df`
*   **Recodificación de Variables:** Utilizando el diccionario de datos proporcionado, se recodificaron las siguientes variables de códigos numéricos a etiquetas de texto: `REGION`, `C203` (parentesco), `C207` (sexo), `C310` (categoría ocupacional), `C311` (sector empleador), `C312` (registro en SUNAT), `C366` (nivel educativo) y `OCUP300` (condición de actividad).
*   **Manejo de Nulos:** Para las personas no clasificadas como 'Ocupado' en `OCUP300`, todas las columnas del módulo de empleo (de `C308` en adelante) y de ingresos se llenaron con la cadena 'No Aplica', reflejando el branching de la encuesta.
*   **Ingeniería de Características:**
    *   `grupo_edad`: Se creó una columna agrupando la edad (`C208`) en rangos.
    *   `es_informal`: Se creó una bandera binaria. Un trabajador se considera informal si es 'Ocupado' y no está afiliado a EsSalud (`C361_1` == 2). Esta definición se basa en el diccionario de datos y es una práctica común.

### 2.5. Limpieza de `poblacion_no_trabajo_df`
*   **Poda de Columnas:** Se eliminaron las columnas irrelevantes del módulo de empleo. Se conservaron todas las columnas hasta `C300n`, y se añadieron las columnas creadas (`periodo`, `factor_expansion`, `factor_ajustado`).
*   **Recodificación de Variables:** Se recodificaron las variables demográficas (`REGION`, `C203`, `C207`) usando los mismos mapeos que en el dataset de trabajo.

## 3. Descripción de los Datasets Finales

### `datos_limpios_poblacion_trabajo.csv`
Contiene los datos limpios de la población en edad de trabajar (14+ años). Incluye variables demográficas, de empleo, ingresos, y los factores de expansión. Está listo para análisis del mercado laboral.

### `datos_limpios_poblacion_no_trabajo.csv`
Contiene los datos limpios de la población menor de 14 años. Incluye variables demográficas básicas y de hogar. Es útil para análisis demográficos de este grupo.
