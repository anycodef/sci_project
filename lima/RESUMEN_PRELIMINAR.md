# Resumen Preliminar del Análisis del Mercado Laboral en Lima

## 1. Principales Insights Iniciales

A partir del análisis exploratorio de los datos de la Encuesta Permanente de Empleo Nacional (EPEN) para Lima, se han identificado los siguientes insights preliminares:

- **Brecha de Género Persistente:** Se observa una diferencia salarial constante entre hombres y mujeres en la mayoría de los sectores económicos analizados. Además, la participación laboral femenina sigue siendo inferior a la masculina, aunque con una ligera tendencia al alza en los últimos trimestres.
- **Impacto del Nivel Educativo:** Existe una correlación positiva fuerte entre el nivel educativo alcanzado y el ingreso promedio. Los individuos con educación superior universitaria perciben ingresos significativamente mayores que aquellos con solo educación básica.
- **Sector Informal Dominante:** Una proporción considerable de la fuerza laboral en Lima se encuentra en el sector informal, caracterizado por una mayor inestabilidad laboral, menores ingresos y falta de acceso a beneficios sociales.
- **Juventud y Desempleo:** La tasa de desempleo es notablemente más alta en el segmento de la población joven (18-29 años) en comparación con otros grupos de edad, señalando dificultades en la transición de la educación al mercado laboral.

## 2. Preguntas para el Análisis Posterior

Este análisis inicial abre nuevas preguntas que guiarán las siguientes fases del proyecto:

- ¿Qué variables (sector, nivel educativo, experiencia) explican en mayor medida la brecha salarial de género?
- ¿Cómo ha evolucionado la informalidad laboral en Lima a lo largo de los diferentes trimestres disponibles en la encuesta? ¿Existen patrones estacionales?
- ¿El retorno de la inversión en educación es homogéneo en todos los sectores económicos o hay áreas donde es más rentable tener un título universitario?
- ¿Qué factores específicos están asociados a la alta tasa de desempleo juvenil? ¿La falta de experiencia es el principal impedimento?

## 3. Principales Retos en el Manejo de la Base de Datos

Durante la fase de preparación y limpieza de los datos, se han encontrado los siguientes desafíos:

- **Homogeneización de Variables:** La codificación de algunas variables categóricas (como ocupación o sector económico) ha cambiado ligeramente entre diferentes trimestres de la encuesta, lo que ha requerido un esfuerzo considerable de armonización para permitir un análisis longitudinal consistente.
- **Manejo de Datos Faltantes:** Se ha detectado una cantidad significativa de valores ausentes en variables clave como `ingreso_total` y `horas_trabajadas`. Se está evaluando la implementación de técnicas de imputación para tratar estos datos sin introducir sesgos en el análisis.
- **Interpretación de Ponderadores:** El uso correcto de los factores de ponderación de la encuesta es crucial para obtener estimaciones representativas de la población total. Asegurar su correcta aplicación en todas las etapas del análisis es un reto metodológico importante.
