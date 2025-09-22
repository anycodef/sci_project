
# Informe Analítico de Empleabilidad y Brecha Salarial
Fecha de Generación: 2025-09-22

## Introducción
Este informe presenta un análisis del mercado laboral basado en datos de encuestas trimestrales. El objetivo es identificar patrones clave en ingresos, demografía y la brecha salarial de género.

## 1. Evidencia de Limpieza de Datos
La siguiente tabla resume el impacto del proceso de limpieza en las variables clave. Se observa la conversión de tipos de dato 'object' a 'float64' y la correcta identificación de valores nulos, lo que permite un análisis numérico preciso.

(El contenido de la tabla de resumen se encuentra en el archivo `resumen_cuantitativo_limpieza.md` en la carpeta `../03_cleaning_evidence/`)

## 2. Análisis de la Distribución de Ingresos
El siguiente gráfico muestra la distribución del ingreso mensual desde cuatro perspectivas para proporcionar un entendimiento completo, incluyendo una vista logarítmica para manejar la asimetría y un diagrama de caja para identificar outliers.

![Análisis de Ingresos](../../03_cleaning_evidence//Analisis_Completo_Ingresos_20250922_000954.png)

## 3. Análisis de Outliers: Perfil de Altos Ingresos

### Análisis de Outliers: Perfil de Altos Ingresos
El perfil de individuos con ingresos superiores a S/. 18,730.00 (outliers) muestra que está predominantemente compuesto por **hombres (62.5%)**.
El nivel educativo más común en este grupo es **'Maestria/Doctorado'** (62.5%), y el grupo de edad más representativo es **'55-64'** (87.5%).


## 4. Prueba de Hipótesis: Brecha Salarial de Género

### Prueba de Hipótesis: Brecha Salarial de Género
Se realizó una prueba T de Student para muestras independientes para comparar los ingresos medios entre hombres y mujeres.
- **Ingreso Promedio Hombres:** S/. 6,641.23
- **Ingreso Promedio Mujeres:** S/. 5,348.10
- **Estadístico T:** 2.13
- **Valor P:** 0.034

**Conclusión de la prueba:** Con un valor p de 0.034, se observa una diferencia estadísticamente significativa en los ingresos entre hombres y mujeres.


## 5. Conclusiones
El análisis revela una brecha salarial de género estadísticamente significativa. Además, los individuos con altos ingresos tienden a ser hombres con educación superior y en grupos de edad con mayor experiencia. Estos hallazgos subrayan la necesidad de políticas enfocadas en la equidad de género y el desarrollo profesional.
