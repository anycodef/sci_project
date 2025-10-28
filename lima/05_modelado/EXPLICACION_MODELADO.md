# Explicación del Modelo de Datos del Proyecto

Este documento describe la estructura del modelo de datos utilizado para el análisis del mercado laboral en Lima, basado en la Encuesta Permanente de Empleo Nacional (EPEN). El diseño del modelo se basa en un **esquema de estrella**, una arquitectura probada para el análisis de datos y la inteligencia de negocios, que optimiza la consulta y la agregación de información.

## Estructura del Esquema de Estrella

El modelo se centra en una tabla de hechos principal, `PERSONA`, que contiene los atributos básicos de cada individuo encuestado. Alrededor de esta tabla central orbitan varias tablas dimensionales, cada una de las cuales describe un aspecto específico del individuo o su contexto (ej. su situación laboral, sus ingresos, su educación).

La clave que une todas las tablas es `llave_panel`, que funciona como el identificador único para cada persona a lo largo de los diferentes periodos de la encuesta.

### 1. Tabla de Hechos: `PERSONA`

Es la tabla central del modelo. Contiene los datos demográficos fundamentales de cada individuo.

- **`llave_panel` (PK):** Identificador único de la persona.
- **`c208`:** Edad.
- **`c207`:** Sexo.
- **`grupo_etnia`:** Grupo étnico al que pertenece.
- **`c203`:** Parentesco con el jefe del hogar.

### 2. Tablas Dimensionales

Estas tablas añaden contexto a la tabla `PERSONA` y contienen la mayor parte de las variables de interés para el análisis.

#### `HOGAR`
Contiene información relativa al hogar al que pertenece la persona.
- **Relación:** Una `PERSONA` pertenece a un `HOGAR`.
- **Campos clave:** `conglomerado`, `hogar` (ID de hogar), `estrato` (Estrato socioeconómico), `region`.

#### `SITUACION_LABORAL`
Describe la condición de actividad y las características del empleo de la persona.
- **Relación:** Una `PERSONA` tiene una `SITUACION_LABORAL`.
- **Campos clave:** `ocup350` (Condición de actividad), `c309_cod` (Código de ocupación), `c309_cod_eco` (Código de actividad económica), `c310` (Categoría ocupacional), `whoraT` (Total de horas trabajadas).

#### `INGRESOS`
Detalla las distintas fuentes de ingreso del individuo.
- **Relación:** Una `PERSONA` percibe `INGRESOS`.
- **Campos clave:** `ingtot` (Ingreso total), `ingtdp` (Ingreso principal mensual), `ingtrabw` (Ingreso mensual total por trabajo).

#### `EDUCACION`
Contiene información sobre el nivel educativo alcanzado por la persona.
- **Relación:** Una `PERSONA` tiene un nivel de `EDUCACION`.
- **Campos clave:** `c555` (Nivel educativo detallado), `nivel_educativo_agrupado` (Nivel educativo agrupado para análisis).

#### `SALUD_PENSIONES`
Describe la afiliación del individuo a sistemas de salud y pensiones.
- **Relación:** Una `PERSONA` tiene afiliación a `SALUD_PENSIONES`.
- **Campos clave:** `tiene_seguro` (Si cuenta con seguro de salud), `c364_1` (Afiliado a AFP), `c364_2` (Afiliado a SNP).

#### `CONTEXTO_ENCUESTA`
Proporciona metadatos sobre la encuesta misma, permitiendo análisis temporales y asegurando la correcta ponderación de los resultados.
- **Relación:** Una `PERSONA` es parte de un `CONTEXTO_ENCUESTA`.
- **Campos clave:** `trimestre`, `anio`, `mes`, `factor_expansion` (Ponderador para representatividad estadística).

## Ventajas de este Modelo

Este diseño es ideal para los objetivos del proyecto porque:
- **Simplifica las Consultas:** Permite realizar consultas complejas (ej. "salario promedio de mujeres con educación superior en el sector servicios") de manera eficiente, uniendo la tabla central `PERSONA` con las dimensiones relevantes.
- **Facilita la Agregación:** La estructura es óptima para agregar datos y calcular métricas clave (tasas de desempleo, brechas salariales, etc.) a través de diferentes dimensiones (por estrato, por región, por nivel educativo).
- **Escalabilidad:** Es un modelo flexible que permite añadir nuevas dimensiones en el futuro (ej. información sobre capacitación, uso de tecnología) sin alterar la estructura existente.
