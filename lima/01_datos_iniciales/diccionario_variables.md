# Diccionario de Variables - Encuesta Permanente de Empleo Nacional

A continuación se detalla la descripción de cada variable según el documento "DICCIONARIO DE DATOS (MARZO 2024)".

---

### ANIO
- **Nombre Real (Etiqueta):** Año de la encuesta.
- **Tipo:** Numérica.

---

### MES
- **Nombre Real (Etiqueta):** Mes de la encuesta.
- **Tipo:** Numérica.

---

### CONGLOMERADO
- **Nombre Real (Etiqueta):** Número del conglomerado.
- **Tipo:** Numérica.

---

### MUESTRA
- **Nombre Real (Etiqueta):** Nº de Sub Muestra.
- **Tipo:** Numérica.

---

### SELVIV
- **Nombre Real (Etiqueta):** Número de selección de la vivienda.
- **Tipo:** Categórica (Carácter).

---

### HOGAR
- **Nombre Real (Etiqueta):** Hogar.
- **Tipo:** Numérica.

---

### REGION
- **Nombre Real (Etiqueta):** Región.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Lima Metropolitana.
    - `2`: Resto urbano.
    - `3`: Rural.

---

### LLAVE_PANEL
- **Nombre en Diccionario:** LLAVE PANEL.
- **Nombre Real (Etiqueta):** Código del personal panel.
- **Tipo:** Categórica (Carácter).

---

### ESTRATO
- **Nombre Real (Etiqueta):** ESTRATO (Estrato geográfico).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Conformado por aquellas UPM de 500000 a más habitantes.
    - `2`: Conformado por aquellas UPM de 100000 a 499999 habitantes.
    - `3`: Conformado por aquellas UPM de 50000 a 99999 habitantes.
    - `4`: Conformado por aquellas UPM de 20000 a 49999 habitantes.
    - `5`: Conformado por aquellas UPM de 2000 a 19999 habitantes.
    - `6`: Conformado por aquellas UPM de 500 a 1999 habitantes.
    - `7`: Conformado por el AER Compuesto.
    - `8`: Conformado por el AER Simple.

---

### C201
- **Nombre Real (Etiqueta):** 201. N° de orden (CÓDIGO DE PERSONA).
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 30.

---

### C203
- **Nombre Real (Etiqueta):** ¿CUÁL ES LA RELACIÓN DE PARENTESCO CON EL JEFE DEL HOGAR?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Jefe/a.
    - `2`: Esposo/a o compañero/a.
    - `3`: Hijo/a o hijastro/a.
    - `4`: Yerno o Nuera.
    - `5`: Nieto/a.
    - `6`: Padre / madre / suegro/a.
    - `7`: Hermano/a.
    - `8`: Otro pariente.
    - `9`: Trabajador/a del hogar.
    - `10`: Pensionista.
    - `11`: Otro no pariente.
    - `98`: No residente.

---

### C204
- **Nombre Real (Etiqueta):** ¿MIEMBRO DEL HOGAR?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C205
- **Nombre Real (Etiqueta):** ¿SE ENCUENTRA AUSENTE DEL HOGAR 30 DÍAS O MÁS?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C206
- **Nombre Real (Etiqueta):** ¿ESTA PRESENTE EN EL HOGAR 30 DÍAS O MÁS?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C207
- **Nombre Real (Etiqueta):** 207. SEXO.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Hombre.
    - `2`: Mujer.

---

### C208
- **Nombre Real (Etiqueta):** ¿QUÉ EDAD TIENE EN AÑOS CUMPLIDOS?.
- **Tipo:** Numérica.
- **Restricciones:** Rango de 0 a 98. El valor `99` indica "Missing value".

---

### NROINF
- **Nombre Real (Etiqueta):** CÓDIGO DE INFORMANTE (MODULO EMPLEO).
- **Tipo:** Numérica.
- **Restricciones:** Rango de 0 a 25.

---

### C301_DIA
- **Nombre Real (Etiqueta):** ¿CUÁL ES LA FECHA DE SU NACIMIENTO? - DIA.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C301_MES
- **Nombre Real (Etiqueta):** ¿CUÁL ES LA FECHA DE SU NACIMIENTO? - MES.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C301_ANIO
- **Nombre en Diccionario:** C301 ΑΝΙΟ.
- **Nombre Real (Etiqueta):** ¿CUÁL ES LA FECHA DE SU NACIMIENTO? - AÑO.
- **Tipo:** Numérica.
- **Restricciones:** El valor `9999` indica "Missing value".

---

### C303
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, DEL...AL... TUVO UD. ALGÚN TRABAJO? (Sin contar los quehaceres del hogar).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C304
- **Nombre Real (Etiqueta):** AUNQUE NO TRABAJÓ LA SEMANA PASADA, ¿TIENE ALGÚN EMPLEO FIJO AL QUE PRÓXIMAMENTE VOLVERÁ?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.
- **Notas:** El valor `9` indica "Missing value".

---

### C305
- **Nombre Real (Etiqueta):** AUNQUE NO TRABAJÓ LA SEMANA PASADA, ¿TIENE ALGÚN NEGOCIO PROPIO AL QUE PRÓXIMAMENTE VOLVERÁ?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.
- **Notas:** El valor `9` indica "Missing value".

---

### C306_1
- **Nombre en Diccionario:** C306 1.
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: Trabajando en algún negocio propio o de un familiar?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_2
- **Nombre en Diccionario:** C306 2.
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: Ofreciendo algún servicio?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_3
- **Nombre en Diccionario:** C306 3.
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 3? Haciendo algo en casa para vender.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_4
- **Nombre en Diccionario:** C306 4.
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 4? Vendiendo productos de belleza, ropa, joyas, ¿entre otros?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_5
- **Nombre en Diccionario:** C306 5.
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 5. Realizando alguna labor artesanal.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_6
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: Haciendo prácticas pagadas en un centro de trabajo?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_7
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 7? Trabajando para un hogar particular.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_8
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 8 Fabricando algún producto?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_9
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 9? ¿Realizando labores remuneradas en la chacra o cuidado de animales?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_10
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGuna ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 10 Ayudando a un familiar de su hogar, sin remuneración?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_10A
- **Nombre en Diccionario:** C306 10A.
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, ¿REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, COMO: 10? A. Ayudando con el empleo de algún miembro de su hogar?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C306_11
- **Nombre Real (Etiqueta):** LA SEMANA PASADA, REALIZÓ ALGUNA ACTIVIDAD AL MENOS UNA HORA PARA OBTENER INGRESOS EN DINERO O EN ESPECIE, 11tra?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C300n
- **Nombre Real (Etiqueta):** CÓDIGO DE PERSONA (MODULO DE EMPLEO).
- **Tipo:** Numérica.
- **Restricciones:** Rango de 0 a 25.

---

### C306A
- **Nombre Real (Etiqueta):** ¿EL INFORMANTE ES PRODUCTOR AGRÍCOLA Y/O PECUARIO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C308_COD
- **Nombre Real (Etiqueta):** 308 ¿CUÁL ES LA OCUPACIÓN PRINCIPAL QUE DESEMPEÑÓ? - CODIGO.
- **Tipo:** Numérica.
- **Restricciones:** El valor `9999` indica "Missing value".

---

### C309_COD
- **Nombre en Diccionario:** C309 COD.
- **Nombre Real (Etiqueta):** 309. ¿A QUE SE DEDICA EL NEGOCIO, ORGANISMO O EMPRESA EN LA QUE TRABAJÓ EN SU OCUPACIÓN PRINCIPAL? CODIGO.
- **Tipo:** Numérica.
- **Restricciones:** El valor `9999` indica "Missing value".

---

### C310
- **Nombre Real (Etiqueta):** 310. UD. SE DESEMPEÑÓ EN SU OCUPACIÓN PRINCIPAL O NEGOCIO COMO:.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Empleador o patrono?.
    - `2`: ¿Trabajador independiente?.
    - `3`: ¿Empleado u obrero?.
    - `4`: ¿Ayudante en un negocio de la familia?.
    - `5`: ¿Ayudante en el empleo de un familiar?.
    - `6`: ¿Trabajador del hogar?.
    - `7`: ¿Aprendiz/practicante remunerado?.
    - `8`: ¿Practicante sin remuneración?.
    - `9`: ¿Ayudante en un negocio de la familia de otro hogar.
    - `10`: ¿Ayudante en el empleo de un familiar de otro hogar?.

---

### C311
- **Nombre Real (Etiqueta):** 311. EN SU OCUPACIÓN PRINCIPAL, ¿UD. TRABAJO PARA:.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Fuerzas Armadas, Policía Nacional del Perú (militares)?.
    - `2`: ¿Administración pública?.
    - `3`: ¿Empresa pública?.
    - `4`: ¿Empresas especiales de servicios (SERVICE)?.
    - `5`: ¿Empresa o patrono privado?.
    - `6`: Otra.

---

### C312
- **Nombre Real (Etiqueta):** 312. EL NEGOCIO O EMPRESA DONDE TRABAJA, ¿SE ENCUENTRA REGISTRADO EN LA SUNAT?, COMO:.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Persona jurídica (¿Sociedad Anónima SRL, ¿Sociedad Civil, EIRL o Asociación, etc.?.
    - `2`: ¿Persona Natural con RUC (RUS, RER, u otro régimen)?.
    - `3`: NO ESTA REGISTRADO (¿no tiene RUC?.
    - `4`: NO SABE (solo para dependientes).

---

### C313
- **Nombre Real (Etiqueta):** 313. EL NEGOCIO O EMPRESA DONDE TRABAJA, LLEVA LAS CUENTAS POR MEDIO DE LIBROS CONTABLES EXIGIDOS POR LA SUNAT O SISTEMA DE CONTABILIDAD?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.
    - `3`: No Sabe.

---

### C317
- **Nombre Real (Etiqueta):** 317. EN SU TRABAJO, NEGOCIO O EMPRESA, INCLUYÉNDOSE UD., LABORARON:.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Hasta 20 personas?.
    - `2`: ¿De 21 a 50 personas?.
    - `3`: ¿De 51 a 100 personas?.
    - `4`: ¿De 101 a 500 personas?.
    - `5`: ¿Más de 500 personas?.

---

### C317A
- **Nombre Real (Etiqueta):** 317. EN SU TRABAJO, NEGOCIO O EMPRESA, INCLUYÉNDOSE UD., ¿LABORARON: N° DE PERSONAS.
- **Tipo:** Numérica.
- **Restricciones:** El valor `9999` indica "Missing value".

---

### C318_1
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - Domingo.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_2
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJO LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - lunes.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_3
- **Nombre en Diccionario:** C318 3.
- **Nombre Real (Etiqueta):** ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - martes.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_4
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - miércoles.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_5
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - jueves.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_6
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - viernes.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_7
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - sábado.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C318_T
- **Nombre Real (Etiqueta):** 318. ¿CUÁNTAS HORAS TRABAJÓ LA SEMANA PASADA, EN SU OCUPACIÓN PRINCIPAL? (DÍA POR DÍA) - Total.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C328_T
- **Nombre en Diccionario:** C328 T.
- **Nombre Real (Etiqueta):** 328. ¿CUÁNTO HORA TRABAJÓ LA SEMANA PASADA EN SU(S) OCUPACIONES SECUNDARIAS?.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### whoraT
- **Nombre Real (Etiqueta):** Hora total de los ocupados.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C330
- **Nombre Real (Etiqueta):** 330.EN TOTAL UD. TRABAJÓ HORAS LA SEMANA PASADA. ¿NORMALMENTE TRABAJA ESAS HORAS A LA SEMANA?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C331
- **Nombre Real (Etiqueta):** 331.NORMALMENTE, ¿CUÁNTAS HORAS TRABAJA A LA SEMANA EN TODAS SUS OCUPACIONES?.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C333
- **Nombre Real (Etiqueta):** 333.LA SEMANA PASADA ¿QUERÍA TRABAJAR MÁS HORA DE LAS QUE NORMALMENTE TRABAJADAS?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C334
- **Nombre Real (Etiqueta):** 334.LA SEMANA PASADA ESTUVO DISPONIBLE PARA TRABAJAR MÁS HORA?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### P209H
- **Nombre Real (Etiqueta):** ¿TUVO LA VOLUNTAD DE TRABAJAR MAS HORAS Y ADEMÁS ESTUVO DISPONIBLE PARA HACERLO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C335
- **Nombre Real (Etiqueta):** 335.LA SEMANA PASADA, ¿ESTUVO UD. BUSCANDO OTRO TRABAJO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C338
- **Nombre Real (Etiqueta):** 338 EN SU OCUPACIÓN PRINCIPAL, ¿A UD. LE PAGAN:.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Diario?.
    - `2`: Semanal?.
    - `3`: Quincenal?.
    - `4`: Mensual?.
    - `5`: No recibió pago alguno.

---

### C339_1
- **Nombre Real (Etiqueta):** 339_1 OCUPACIÓN PRINCIPAL ¿CUÁNTO FUE SU INGRESO TOTAL EN EL (LA)...ANTERIOR, INCLUYENDO HORAS EXTRAS, BONIFICACIONES, PAGO POR CONCEPTO DE REFRIGERIO, MOVILIDAD, COMISIONES, ENTRE OTROS? A. Ingreso total - Monto S/..
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C341_T
- **Nombre Real (Etiqueta):** 341_T EN SU OCUPACIÓN PRINCIPAL, ¿CON QUE FRECUENCIA Y EN CUÁNTO ESTIMARÍA UD. EL PAGO EN ESPECIES?: VALOR ESTIMADO TOTAL.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C342
- **Nombre Real (Etiqueta):** 342 EN SU OCUPACIÓN PRINCIPAL, ¿CUÁL FUE LA GANANCIA NETA EN EL MES ANTERIOR?.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C344
- **Nombre Real (Etiqueta):** 344 ¿EN CUÁNTO ESTIMA UD. EL VALOR DE LOS PRODUCTOS UTILIZADOS PARA SU CONSUMO EN EL MES ANTERIOR?.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C345_1
- **Nombre Real (Etiqueta):** 345. ¿CUÁNTO FUE SU INGRESO TOTAL EN EL MES ANTERIOR, INCLUYENDO HORAS EXTRAS, BONIFICACIONES, PAGO POR CONCEPTO DE REFRIGERIO, MOVILIDAD, COMISIONES, ENTRE OTROS ¿EN SU(S) OCUPACIÓN (ES) SECUNDARIA(S)? A. MONTO DEL INGRESO TOTAL.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C347_T
- **Nombre en Diccionario:** C347 T.
- **Nombre Real (Etiqueta):** 347 EN SU OCUPACIÓN SECUNDARIA ¿CON QUE FRECUENCIA Y EN CUÁNTO ESTIMARÍA UD. EL PAGO EN ESPECIES?: VALOR ESTIMADO TOTAL.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C348
- **Nombre Real (Etiqueta):** 348. EN SU(S) OCUPACIÓN (ES) SECUNDARIA(S), ¿CUÁL FUE SU GANANCIA NETA EN EL MES ANTERIOR? Soles.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C350
- **Nombre Real (Etiqueta):** 350 EN SU OCUPACIÓN SECUNDARIA ¿EN CUANTO ESTIMA UD, EL VALOR DE LOS PRODUCTOS UTILIZADOS PARA SU CONSUMO EN EL MES ANTERIOR?: VALOR ESTIMADO TOTAL.
- **Tipo:** Numérica.
- **Restricciones:** El valor `999999` indica "Missing value".

---

### C352
- **Nombre Real (Etiqueta):** 352. LA SEMANA PASADA, ¿HIZO ALGO PARA CONSEGUIR TRABAJO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C353
- **Nombre Real (Etiqueta):** 353. ¿QUÉ ESTUVO HACIENDO LA SEMANA PASADA?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Hizo trámites, buscó local, gestionó préstamos para establecer su propio negocio?.
    - `2`: ¿Reparando sus activos (local, maquina, equipo)?.
    - `3`: Esperando el inicio de un trabajo dependiente (como obrero, empleado o trabajador del hogar)?.
    - `4`: ¿Estudiando?.
    - `5`: ¿Quehaceres del hogar?.
    - `6`: ¿Vivía de su pensión o jubilación u otras rentas?.
    - `7`: ¿Enfermo o incapacitado?.
    - `8`: ¿Otro?.

---

### C354
- **Nombre Real (Etiqueta):** 354. LA SEMANA PASADA, ¿QUERÍA UD. TRABAJAR?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C355
- **Nombre Real (Etiqueta):** 355. LA SEMANA PASADA, ESTUVO DISPONIBLE PARA TRABAJAR?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C356
- **Nombre Real (Etiqueta):** 356. ¿POR QUÉ NO BUSCÓ TRABAJO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: No hay trabajo.
    - `2`: Se cansó de buscar.
    - `3`: Por su edad.
    - `4`: Falta de experiencia.
    - `5`: Sus estudios no le permiten.
    - `6`: Los quehaceres del hogar no le permiten.
    - `7`: Razones de salud.
    - `8`: Falta de capital.
    - `9`: Espera los resultados de una búsqueda anterior.
    - `10`: Por el Covid19 -(para evitar contagio, por ser vulnerable, entre otros).
    - `11`: Otro.
    - `12`: Ya encontró trabajo.
    - `13`: Si buscó trabajo.

---

### C357_I
- **Nombre en Diccionario:** C357_1.
- **Nombre Real (Etiqueta):** 357. LA SEMANA PASADA ¿QUÉ HIZO PARA CONSEGUIR TRABAJO? REGISTRE EL CODIGO DE LA GESTION MAS IMPORTANTE.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Empleador / patrono.
    - `2`: Agencia de empleo.
    - `3`: Bolsa de trabajo de Instituciones públicas.
    - `4`: Bolsa de trabajo de Instituciones privadas.
    - `5`: Amigos y/o parientes.
    - `6`: Diarios, revistas o anuncios.
    - `7`: Envío su curriculum vitae a empresas o instituciones.
    - `8`: Publicó avisos en diarios, revistas o anuncios.
    - `9`: Buscó clientes o pedidos.
    - `10`: Otro.

---

### C358
- **Nombre Real (Etiqueta):** ¿CUÁNTAS SEMANAS HA ESTADO BUSCANDO TRABAJO, SIN INTERRUPCIONES?.
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 998.

---

### C359
- **Nombre Real (Etiqueta):** ¿HA TRABAJADO ANTES?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### SEGURO1
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ES.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ESSALUD (Antes IPSS).
    - `2`: Seguro privado de Salud.
    - `3`: Ambos.
    - `4`: Otro.
    - `5`: Seguro Integral de Salud (SIS).
    - `6`: No está afiliado.

---

### C361_1
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ESSALUD?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_1
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 1. ESSALUD.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.
    - `5`: No paga.

---

### C361_2
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ES. 2¿SEGURO PRIVADO DE SALUD?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_2
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 2.SEGURO PRIVADO DE SALUD.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.

---

### C361_3
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ES 3. ¿ENTIDAD PRESTADORA DE SALUD?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_3
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 3.ENTIDAD PRESTADORA DE SALUD.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.

---

### C361_4
- **Nombre en Diccionario:** C361 4.
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ES. 4. ¿SEGURO DE FF.AA./ POLICIALES?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_4
- **Nombre en Diccionario:** C362 4.
- **Nombre Real (Etiqueta):** 362. QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 4. SEGURO DE FF.AA./POLICIALES.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.

---

### C361_5
- **Nombre en Diccionario:** C361 5.
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ES 5. ¿SEGURO INTEGRAL DE SALUD (SIS)?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_5
- **Nombre en Diccionario:** C362 5.
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 5. SEGURO INTEGRAL DE SALUD (SIS).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `4`: Un familiar.
    - `5`: No paga.

---

### C361_6
- **Nombre en Diccionario:** C361 6.
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO SEGURO UNIVERSITARIO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_6
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 6. SEGURO UNIVERSITARIO.
- **Tipo:** Categórica.
- **Categorías:**
    - `2`: Ud. mismo.
    - `4`: Un familiar.

---

### C361_7
- **Nombre en Diccionario:** C361 7.
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO ES. 7. ¿SEGURO ESCOLAR PRIVADO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_7
- **Nombre en Diccionario:** C362 7.
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 7. SEGURO ESCOLAR PRIVADO.
- **Tipo:** Categórica.
- **Categorías:**
    - `2`: Ud. mismo.
    - `4`: Un familiar.

---

### C361_8
- **Nombre en Diccionario:** C361 8.
- **Nombre Real (Etiqueta):** 361. EL SISTEMA DE SEGURO DE SALUD AL CUAL ESTA AFILIADO OTRO?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C362_8
- **Nombre Real (Etiqueta):** 362.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 8. OTRO.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.
    - `5`: No paga.

---

### C364_1
- **Nombre Real (Etiqueta):** 364. EL SISTEMA DE PENSIONES AL CUAL ESTA AFILIADO ES. 1. SISTEMA PRIVADO DE PENSIONES (AFP).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C365_1
- **Nombre Real (Etiqueta):** 365.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 1. SISTEMA PRIVADO DE PENSIONES (AFP).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.
    - `5`: No paga.

---

### C364_2
- **Nombre en Diccionario:** C364 2.
- **Nombre Real (Etiqueta):** 364. EL SISTEMA DE PENSIONES AL CUAL ESTA AFILIADO ES. 2. SISTEMA NACIONAL DE PENSIONES LEY 19990.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C365_2
- **Nombre en Diccionario:** C365 2.
- **Nombre Real (Etiqueta):** 365.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 2. SISTEMA NACIONAL DE PENSIONES LEY 19990.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.
    - `5`: No paga.

---

### C364_3
- **Nombre Real (Etiqueta):** 364. EL SISTEMA DE PENSIONES AL CUAL ESTA AFILIADO ES. 3. SISTEMA NACIONAL DE PENSIONES LEY 20530 (CÉLULA VIVA).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C365_3
- **Nombre Real (Etiqueta):** 365.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 3. SISTEMA NACIONAL DE PENSIONES LEY 20530 (CÉLULA VIVA).
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `3`: Es jubilado.
    - `4`: Un familiar.

---

### C364_4
- **Nombre en Diccionario:** C364 4.
- **Nombre Real (Etiqueta):** 364. EL SISTEMA DE PENSIONES AL CUAL ESTA AFILIADO ES 4. OTRO.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C365_4
- **Nombre en Diccionario:** C365 4.
- **Nombre Real (Etiqueta):** 365.QUIEN APORTA LOS CUOTAS POR ESTAR AFILIADO. 4. OTRO.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Su centro de trabajo.
    - `2`: Ud. mismo.
    - `3`: Es jubilado.
    - `4`: Un familiar.

---

### C366
- **Nombre Real (Etiqueta):** 366. CUÁL ES EL ÚLTIMO AÑO O GRADO DE ESTUDIOS Y NIVEL QUE APROBÓ.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Sin nivel.
    - `2`: Educación Inicial.
    - `3`: Primaria incompleta.
    - `4`: Primaria completa.
    - `5`: Secundaria incompleta.
    - `6`: Secundaria completa.
    - `7`: Básica especial.
    - `8`: Superior no universitaria incompleta.
    - `9`: Superior no universitaria completa.
    - `10`: Superior universitaria incompleta.
    - `11`: Superior universitaria completa.
    - `12`: Maestria/Doctorado.

---

### C366_1
- **Nombre en Diccionario:** C366 1.
- **Nombre Real (Etiqueta):** 366. ¿CUÁL ES EL ÚLTIMO AÑO O GRADO DE ESTUDIOS Y NIVEL QUE APROBÓ? Año.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C366_2
- **Nombre Real (Etiqueta):** 366. ¿CUÁL ES EL ÚLTIMO AÑO O GRADO DE ESTUDIOS Y NIVEL QUE APROBÓ? Grado.
- **Tipo:** Numérica.
- **Restricciones:** El valor `99` indica "Missing value".

---

### C375_1
- **Nombre Real (Etiqueta):** TIENE UD. LIMITACIONES DE FORMA PERMANENTE, PARA: 1. Moverse o caminar, para usar brazos o piernas?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C375_2
- **Nombre Real (Etiqueta):** TIENE UD. LIMITACIONES DE FORMA PERMANENTE, PARA: 2? Ver, ¿aun usando anteojos?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C375_3
- **Nombre en Diccionario:** C375 3.
- **Nombre Real (Etiqueta):** TIENE UD. LIMITACIONES DE FORMA PERMANENTE, PARA: 3 Hablar o comunicarse, aun usando la lengua de señas u otro.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C375_4
- **Nombre Real (Etiqueta):** 375. TIENE UD. LIMITACIONES DE FORMA PERMANENTE, PARA: 4. Oir, aun usando audífonos?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C375_5
- **Nombre Real (Etiqueta):** TIENE UD. LIMITACIONES DE FORMA PERMANENTE, PARA: 5. Entender o aprender (concentrarse y recordar)?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C375_6
- **Nombre Real (Etiqueta):** 375. TIENE UD. LIMITACIONES DE FORMA PERMANENTE, PARA: 6. Relacionarse con los demás, por sus pensamientos, sentimientos, emociones o conductas?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: Si.
    - `2`: No.

---

### C376
- **Nombre Real (Etiqueta):** ¿CUÁL ES EL IDIOMA O LENGUA MATERNA QUE APRENDIÓ EN SU NIÑEZ?.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Quechua?.
    - `2`: ¿Aimara?.
    - `3`: ¿Ashaninka?.
    - `4`: ¿Awajún/Aguaruna?.
    - `5`: ¿Shipibo - Konibo?.
    - `6`: ¿Shawi / Chayahuita?.
    - `7`: ¿Matigenka / Machiguenga?.
    - `8`: ¿Achuar?.
    - `9`: ¿Otra lengua nativa?.
    - `10`: ¿Castellano?.
    - `11`: ¿Portugués?.
    - `12`: ¿Otra lengua extranjera?.
    - `13`: NO ESCUCHA/NO HABLA.
    - `14`: LENGUA DE SEÑAS PERUANAS.

---

### C377
- **Nombre Real (Etiqueta):** 377. POR SUS COSTUMBRES Y SUS ANTEPASADOS, ¿UD. SE SIENTE O SE CONSIDERA:.
- **Tipo:** Categórica.
- **Categorías:**
    - `1`: ¿Quechua?.
    - `2`: ¿Aymara?.
    - `3`: ¿Nativo o Indigena de la Amazonía?.
    - `4`: ¿Perteneciente o parte de otro Pueblo indígena originario?.
    - `5`: ¿Negro/Moreno/Zambo/Mulato/Pueblo Afro peruano o Afrodescendiente?.
    - `6`: ¿Blanco?.
    - `7`: ¿Mestizo?.
    - `8`: ¿Otro?.
    - `9`: NO SABE/NO RESPONDE.

---

### OCUP300
- **Nombre Real (Etiqueta):** NIVEL DE OCUPACION (Indicador de Condición de Actividad).
- **Tipo:** Categórica.
- **Categorías:**
    - `0`: Sin información.
    - `1`: Ocupado.
    - `2`: Desocupado abierto.
    - `3`: Desocupado oculto.
    - `4`: Inactivo pleno.

---

### I339_1
- **Nombre en Diccionario:** 1339_1.
- **Nombre Real (Etiqueta):** Ingreso mensual monetario de la actividad principal por trabajador dependiente.
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### D341_T
- **Nombre Real (Etiqueta):** Ingreso mensual en especies de la actividad principal por trabajador dependiente (valorizado).
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### I342
- **Nombre en Diccionario:** 1342.
- **Nombre Real (Etiqueta):** Ingreso mensual monetario de la actividad principal por trabajador independiente.
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### D344
- **Nombre Real (Etiqueta):** Ingreso mensual en especies de la actividad principal por trabajador independiente (valorizado).
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### I345_1
- **Nombre en Diccionario:** 1345_1.
- **Nombre Real (Etiqueta):** Ingreso mensual monetario de la actividad secundaria por trabajador dependiente.
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### I348
- **Nombre en Diccionario:** 1348.
- **Nombre Real (Etiqueta):** Ingreso mensual monetario de la actividad secundaria por trabajador independiente.
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### D347_T
- **Nombre en Diccionario:** D347 T.
- **Nombre Real (Etiqueta):** Ingreso mensual en especies de la actividad secundaria por trabajador dependiente (valorizado).
- **Tipo:** Numérica.
- **Restricciones:** Rango de 1 a 999998.

---

### D350
- **Nombre Real (Etiqueta):** Ingreso mensual en especies de la actividad secundaria por trabajador independiente (valorizado).
- **Tipo:** Numérica.

---

### D351_T
- **Nombre Real (Etiqueta):** (Mensual) En los últimos 12 meses, recibió algún dinero: Total.
- **Tipo:** Numérica.

---

### INGTOT
- **Nombre Real (Etiqueta):** Ingresos totales.
- **Tipo:** Numérica.

---

### INGTOTP
- **Nombre Real (Etiqueta):** Ingreso principal mensual.
- **Tipo:** Numérica.

---

### ingtrabw
- **Nombre en Diccionario:** INGTRABW.
- **Nombre Real (Etiqueta):** Ingreso mensual, ocupación principal y secundaria con ingresos extraordinarios.
- **Tipo:** Numérica.

---

### RESIDENT
- **Nombre Real (Etiqueta):** Residente habitual.
- **Tipo:** Categórica.
- **Categorías:**
    - `0`: No.
    - `1`: Si.
    - `9`: Omisión 200.

---

### fa_efm24
- **Nombre en Diccionario:** fa efm24.
- **Nombre Real (Etiqueta):** Factor de expansión Trimestral (enero-febrero-marzo 2024) para el cálculo del empleo.
- **Tipo:** Numérica.

---

### fa_efm25
- **Descripción:** Esta variable no se encontró en el diccionario de datos proporcionado.
