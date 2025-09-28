### **Objetivos del Proyecto de Análisis de Series Temporales para Lima**

Este documento define los objetivos centrales del análisis, con un enfoque en la dimensión temporal y el uso correcto del factor de expansión para obtener resultados estadísticamente representativos de la población de Lima.

---

### **1. Análisis Temporal y Descriptivo (Ponderado)**

El objetivo principal es comprender la dinámica del mercado laboral y las características sociodemográficas de Lima a lo largo del tiempo.

*   **Evolución de Indicadores Clave:** Analizar la evolución de indicadores fundamentales (como empleo, desempleo, ingresos, informalidad) a lo largo de los 6 trimestres disponibles (2024-2025). Todos los cálculos que busquen representar a la población total de Lima se ponderarán utilizando el `factor_expansion` para garantizar la validez de las estimaciones.
*   **Comparación Sociodemográfica:** Comparar las características sociodemográficas de la población (distribución por edad, sexo, nivel educativo, etc.) entre el primer trimestre de 2024 y el último trimestre disponible de 2025 para identificar cambios estructurales o tendencias emergentes.

---

### **2. Modelos Predictivos (Sensibles al Tiempo)**

El segundo gran objetivo es desarrollar modelos predictivos que no solo expliquen las relaciones entre variables, sino que también consideren la temporalidad como un factor potencialmente influyente.

*   **Modelo de Clasificación:**
    *   **Objetivo:** Desarrollar un modelo para clasificar a un individuo en una categoría de interés (ej. riesgo de informalidad laboral, subempleo, etc.).
    *   **Enfoque Temporal:** Investigar explícitamente si la variable "trimestre" (o alguna derivada de esta) es un predictor relevante y mejora la capacidad del modelo.

*   **Modelo de Regresión:**
    *   **Objetivo:** Construir un modelo para predecir una variable numérica clave (ej. ingresos mensuales).
    *   **Enfoque Temporal:** Evaluar el impacto de la temporalidad en la predicción de ingresos, determinando si existen efectos estacionales o tendencias que deban ser incorporados en el modelo.