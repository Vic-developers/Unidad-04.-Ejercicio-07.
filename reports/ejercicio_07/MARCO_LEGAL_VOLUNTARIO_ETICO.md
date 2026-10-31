# Fase 5 · Marco legal, marcos voluntarios y recomendaciones éticas

**Fecha de consulta:** 31 de octubre de 2026 (America/Santo_Domingo).

**Estado:** completada para el alcance académico documentado. Jurisdicción confirmada por el usuario: **República Dominicana**. Se identifican normas nacionales, condiciones de aplicación, marcos orientativos y nueve recomendaciones éticas. Este cierre documental no certifica cumplimiento jurídico ni aprueba las recomendaciones.

**Sistema:** Territorial Review DSS - Synthetic, demostración académica con datos sintéticos. El mensaje «Republica Dominicana» confirma el país. El alcance procede de README, DATASET_CARD y formulario de impacto; no se atribuye al usuario una confirmación adicional de uso futuro ni una autorización de despliegue real.

## 1. Trabajo realizado y criterio de clasificación

Se revisaron fuentes institucionales dominicanas y de NIST, OCDE y UNESCO y se relacionaron con los riesgos y controles del proyecto. La clasificación distingue:

| Categoría | Qué acredita | Estado en el expediente |
|---|---|---|
| Obligación legal aplicable | Una fuente jurídica vinculante pertinente al país, sujeto, datos, finalidad y actividad evaluados. | Constitución y Ley 172-13 identificadas; matriz con condiciones y límites de evidencia. La referencia sectorial al Decreto 714-26 se registra por separado. |
| Marco o instrumento orientativo | Una referencia de gestión o recomendación intergubernamental cuya naturaleza debe identificarse. | NIST AI RMF y recomendaciones de OCDE/UNESCO examinados. |
| Recomendación ética del proyecto | Una propuesta razonada para este sistema y sus afectados potenciales, diferenciada de lo implementado. | Nueve temas desarrollados; aprobación e implementación pendientes según cada caso. |

La evidencia técnica y la preferencia provisional por logística no prueban cumplimiento jurídico. Los valores 0.68 y 0.16 de `configs/governance.yml` son benchmarks experimentales del proyecto; no se clasifican como límites legales o tolerancias éticas aprobadas.

### 1.1. Parte legal: República Dominicana y alcance de la determinación

**Contexto acreditado.** El proyecto contiene 640 casos descritos como sintéticos y no autoriza decisiones automáticas sobre personas. No se documenta una institución operadora, una contratación pública, personas afectadas reales ni un servicio publicado. Esa delimitación permite completar esta fase sin inventar un despliegue. El mensaje del usuario y su procedencia se conservan en `evidencias/fase_05/legal_context.json`.

**Base constitucional.** Se utiliza el texto proclamado el 27-10-2024, cuya disposición final prevé vigencia desde la proclamación. Los arts. 6, 39, 44.2 y 70 sustentan la sujeción constitucional, la igualdad, la privacidad y el hábeas data. [L01: Constitución 2024, copia del Tribunal Constitucional](https://tribunalsitestorage.blob.core.windows.net/media/61583/constitucion-6-x-9-de-lujo-web-portad-nea.pdf).

**Protección de datos.** La ficha oficial consultada presenta la Ley 172-13 como vigente. [L03: Superintendencia de Bancos](https://www.sb.gob.do/regulacion/leyes/ley-no-172-13-proteccion-de-los-datos/). Se examinaron ámbito, principios, derechos, deberes del responsable y categorías especialmente protegidas en los artículos indicados en la matriz. [L02: texto de la Ley 172-13](https://sb.gob.do/media/4i1ploou/ley17213.pdf).

La interpretación aplicada al proyecto es condicional: el dataset, tal como está documentado, no acredita tratamiento de personas identificadas o identificables. Esto no declara exenta toda actividad académica, ni prueba por sí solo la procedencia sintética. El generador completo y su semilla siguen sin evidencia suficiente. Cuentas, autoría, correos o registros técnicos que pudieran acompañar una publicación requieren un inventario separado. Un filtro de columnas no resuelve la identificabilidad indirecta.

La matriz editable [MATRIZ_APLICABILIDAD_LEGAL.csv](MATRIZ_APLICABILIDAD_LEGAL.csv) contiene diez comprobaciones:

| Filas | Materia y fuente | Lectura del expediente |
|---|---|---|
| RD01–RD03 | Constitución: igualdad, privacidad y hábeas data · L01 | Marco vinculante; las métricas sintéticas no acreditan cumplimiento en decisiones sobre personas. |
| RD04–RD09 | Ley 172-13: alcance y condiciones de tratamiento · L02/L03 | El supuesto personal no se acredita en el CSV. Ante nueva información debe reevaluarse cada condición y conservar evidencia. |
| RD10 | Infraestructura digital estatal · L05 | No se acredita el supuesto sectorial ni una inversión estatal en esta práctica. La vigencia específica necesita comprobarse si ese supuesto llega a existir. |

Cada fila conserva artículos, fuente, regla breve, condición de aplicación, evidencia local, limitaciones y riesgos relacionados. `not_certified` significa que no se emite una certificación de cumplimiento; no equivale a afirmar una infracción.

**Vigilancia normativa y selección de fuentes.** El acta de la Cámara de Diputados del 24-03-2026 registra la remisión a comisiones de los proyectos 05389-2024-2028-CD sobre IA y 05407-2024-2028-CD sobre datos. Ese antecedente no acredita promulgación ni determina por sí solo su estado posterior. No se utilizan esos proyectos como obligaciones vigentes. [L04: acta oficial, puntos 10.59 y 10.68](https://camaradediputados.gob.do/download/1936/2026-plo-ordenes-del-dia-conocidos-por-el-pleno/27776/sesion-08-del-martes-24-de-marzo-de-2026.pdf).

Se examinó también el Decreto 714-26, dado el 09-10-2026: su ámbito sectorial y la condición de publicación en Gaceta Oficial se registran en RD10; la fecha de esa publicación no quedó verificada. No se le atribuyen deberes actuales a este ejercicio. [L05: PDF oficial, arts. 3, 9–13 y 15](https://map.gob.do/transparencia/download/105/decretos/22808/decreto-714-26-reglamento-de-coordinacion-e-interes-estrategico-de-la-infraestructura-digital-del-estado.pdf).

La noticia del MAP etiqueta el enlace como «716-26», aunque el PDF enlazado dice 714-26; sus afirmaciones sobre supervisión de algoritmos y evaluación previa universal tampoco se trasladan automáticamente al texto normativo. Se priorizó el PDF efectivamente leído. [L06: noticia contrastada del MAP](https://map.gob.do/2026/10/12/gobierno-emite-por-decreto-reglamento-de-coordinacion-e-interes-estrategico-de-la-infraestructura-digital-del-estado/).

No se declara una ausencia exhaustiva de regulación de IA. Tampoco se acredita un vínculo que haga aplicables el RGPD o el Reglamento de IA europeo. Una adaptación real exige identificar operador, sector, personas, procedencia, finalidad y circulación de datos y actualizar este análisis. Las condiciones hipotéticas quedan descritas para revisión futura; no son autorización para ejecutarlas.

### 1.2. NIST AI RMF: referencia voluntaria

NIST caracteriza el AI RMF como voluntario. Se mantiene la edición 1.0 publicada el 26 de enero de 2023; la página consultada informa una revisión en curso. No se presenta un borrador como sustituto de la edición utilizada. [Fuente F01: NIST](https://www.nist.gov/itl/ai-risk-management-framework).

Las funciones GOVERN, MAP, MEASURE y MANAGE organizan el trabajo de contexto, evaluación y respuesta. Su uso debe adaptarse al caso. [Fuente F02: AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).

El mapeo del proyecto es una elaboración técnica: roles y límites propuestos en GOVERN; nueve escenarios e interesados en MAP; métricas/conteos en MEASURE; controles concretos y propuestas pendientes en MANAGE. La existencia de esa documentación no acredita una certificación ni una incorporación legal o contractual del marco, que no se ha documentado aquí.

### 1.3. OCDE: recomendación intergubernamental

OECD/LEGAL/0449 fue adoptada en 2019 y revisada en 2023 y mayo de 2024. Sus principios abarcan derechos/equidad, transparencia, robustez y responsabilidad. El documento oficial distingue las recomendaciones no vinculantes de otros instrumentos jurídicos. [Fuente F03: recomendación y nota sobre naturaleza de instrumentos](https://legalinstruments.oecd.org/api/print?ids=648), sección 1 y última página del PDF.

Para este expediente se utiliza como orientación: explicar las salidas, permitir cuestionarlas, conservar trazabilidad y responder al uso fuera de finalidad. Es un mapeo propuesto al proyecto; no se afirma una obligación doméstica directa ni se necesita atribuir adhesión nacional para usarlo como referencia.

### 1.4. UNESCO: principios éticos y naturaleza del instrumento

La recomendación de ética de IA adoptada en noviembre de 2021 reúne principios de proporcionalidad, privacidad, equidad, transparencia, supervisión y responsabilidad. [Fuente F04: UNESCO](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics).

La oficina jurídica de UNESCO explica que sus recomendaciones no tienen el carácter vinculante internacional de las convenciones; distingue, además, los compromisos procedimentales de los Estados miembros. No corresponde convertir cada recomendación en una ley local aplicable automáticamente a este prototipo. [Fuente F05: naturaleza de los instrumentos UNESCO](https://www.unesco.org/en/legal-affairs/standard-setting/overview?hub=66535).

El vínculo con el proyecto es una propuesta ética: mantener la finalidad limitada, evitar inferencias sobre personas reales a partir de datos sintéticos y diseñar participación y revisión efectivas si cambia el alcance. Ninguna consulta a afectados o autoridad institucional se da por realizada.

### 1.5. Comparación de las referencias

| Referencia | Naturaleza utilizada | Aporte al proyecto | Límite de la conclusión |
|---|---|---|---|
| NIST AI RMF 1.0 | Marco voluntario de gestión de riesgos | Ordena contexto, medición, responsabilidades y respuesta. | Mapeo no equivale a certificación o aceptación de riesgos. |
| OCDE, OECD/LEGAL/0449 | Recomendación intergubernamental no vinculante | Orienta información comprensible, trazabilidad y posibilidad de cuestionar resultados. | No se afirma adhesión del país ni obligación doméstica sin análisis. |
| UNESCO, recomendación de ética de IA | Instrumento de principios y orientación ética internacional | Apoya proporcionalidad, participación y supervisión. | No se confunde recomendación con convención o ley nacional. |

## 2. Archivos modificados

Se actualizan este informe, el contexto legal y el registro de fuentes de Fase 5. Se conserva el CSV ético y se añaden matriz legal y verificador de cierre. Los formularios, modelos, datos y resultados de Fases 0–4 se conservan; ninguna decisión previa recibe aprobación normativa por esta documentación.

## 3. Recomendaciones éticas del proyecto y archivos generados

La versión editable es [RECOMENDACIONES_ETICAS.csv](RECOMENDACIONES_ETICAS.csv). Sus nueve filas relacionan tema, riesgos, propuesta, evidencia existente, estado y fuentes. El contenido siguiente es elaboración aplicada a este proyecto, apoyada en las referencias; no es transcripción de obligaciones legales.

| ID y tema | Propuesta para el sistema | Evidencia y límite actual |
|---|---|---|
| ET01 · Transparencia | Comunicar finalidad, carácter sintético, límites y revisión pendiente al presentar resultados. | README y reportes disponibles; comprensión por usuarios sin validar. |
| ET02 · Explicabilidad | Explicar factores y errores con lenguaje comprensible; aclarar transformaciones y distinguir asociación de causalidad. | Coeficientes y reglas exportados; no se probó comprensión humana. |
| ET03 · Equidad | Acordar daños y criterios en contexto, considerando soportes, intersecciones e incertidumbre. | Auditorías realizadas; no se aceptaron tolerancias ni mitigaciones operativas. |
| ET04 · Supervisión humana | Acordar competencia, autoridad y capacidad efectiva para revisar, corregir y suspender. | Roles y procedimiento propuestos; operación humana no acreditada. |
| ET05 · Protección de datos | Mantener el alcance sintético y revisar necesidad/procedencia/accesos ante nuevos datos. | Rechazo de columnas probado en ejemplos; privacidad integral no evaluada. |
| ET06 · Responsabilidad | Designar responsable, preservar versiones y declarar asistencia de IA y límites de verificación. | Logs y hashes disponibles; autoridad nominal y revisión independiente pendientes. |
| ET07 · Participación | Si se adapta a personas, incorporar participación accesible para acordar daños y revisión. | CSV de interesados describe propuestas; no hubo consultas reales. |
| ET08 · Gestión de errores | Conservar evidencia, registrar correcciones y acordar suspensión/alternativa manual. | Incidencias técnicas registradas; proceso operativo sin validar. |
| ET09 · Reclamación | Proponer canal accesible y seguro, plazos por acordar y revisión por otra persona. | Mecanismo documentado como propuesta, sin canal técnico acreditado. |

Ninguna recomendación se registra como decisión ética personal adoptada por el usuario. La Fase 6 deberá concretar un plan de mitigación y comparar alternativas después de cerrar y revisar esta fase. Los tiempos o bytes de modelos medidos anteriormente no se convierten en electricidad o emisiones.

Archivos de esta parte: este informe, ambos CSV, `sources.json`, `legal_context.json`, estado inicial y registros bajo `evidencias/fase_05/`. La carpeta `draft_snapshot/` conserva siete archivos del borrador parcial y su índice de hashes. No se genera PDF ni decisión final en esta fase.

## 4. Verificaciones y método de consulta

Se consultaron páginas y un PDF oficiales; se contrastó la naturaleza de los instrumentos en sus propias instituciones. La interfaz HTML principal de la recomendación OCDE exigió JavaScript y una copia PDF alternativa agotó el tiempo; se accedió al PDF oficial mediante la API de impresión del Compendio. No se trata un enlace inaccesible como texto revisado: la fuente final citada sí fue leída.

La verificación local comprueba clasificación de fuentes, diez filas legales, cobertura de los nueve temas, relación con riesgos, existencia de evidencias, correspondencia de citas y conservación de archivos previos. No se ejecutan nuevos entrenamientos o pruebas de modelo para este trabajo documental. Los comandos y resultados reales de cierre se guardan en registros nuevos, sin sustituir los dos del borrador.

| Comprobación realizada | Resultado real | Evidencia en `evidencias/fase_05/` |
|---|---|---|
| Ruff sobre registrador y verificador, con `check --fix` | Código 0; un orden de importación corregido, sin observaciones restantes. | `01_style_check.json` |
| Python 3.12: `verify_draft.py` (borrador histórico) | Código 0 en el borrador de cinco fuentes, nueve temas y 24 referencias locales. Aquel resultado conservaba el estado parcial. | `02_draft_verification.json` y `draft_snapshot/verification.json` |
| Ruff sobre `verify_framework.py` | Código 0; sin observaciones. | `03_framework_style.json` |
| Primera verificación de cierre | Código 1: el verificador esperaba «no determina», mientras el informe dice «ni determina». Se corrigió esa coincidencia de texto; no cambió el análisis legal. | `04_framework_verification.json` |
| Python 3.12: `verify_framework.py`, tras corregir la comprobación | Código 0: once fuentes, diez filas legales, nueve temas éticos, 49 referencias locales, siete archivos históricos preservados y 144 archivos anteriores intactos. | `05_framework_verification_final.json` y `verification.json` |

La investigación de fuentes y la interpretación contextual sustentan la clasificación jurídica. El verificador comprueba estructura, rutas, hashes y coherencia de lo registrado; no decide si una interpretación legal es correcta. Un resultado técnico favorable no certifica cumplimiento jurídico.

## 5. Problemas y límites

La jurisdicción quedó resuelta con la respuesta del usuario. La consulta encontró un enlace 404 de Consultoría Jurídica y un PDF de JCE demasiado grande para la herramienta; se utilizó la copia accesible del Tribunal Constitucional. El portal SIL mostró una pantalla de carga; el antecedente parlamentario citado se leyó en un PDF oficial. La discrepancia de la noticia del MAP se conserva como límite de fuente y se contrasta con el decreto enlazado. La primera validación local falló por una expectativa literal del verificador; el registro se conserva y la comprobación se corrigió.

Los controles organizativos permanecen mayormente propuestos. Las referencias y su mapeo no convierten el dataset en evidencia sobre personas ni demuestran ausencia de discriminación. No se ha recibido revisión humana independiente de este análisis. La cobertura es la del supuesto académico acreditado, sin certificar un régimen sectorial o institucional que todavía no se ha definido.

## 6. Referencias verificadas y evidencia

Todas las referencias se consultaron el **31 de octubre de 2026**. El registro estructurado contiene título, organización, versión, URL, ubicación y afirmación respaldada.

- **F01. NIST.** AI Risk Management Framework, edición 1.0 (2023) y estado de revisión informado. [Página oficial](https://www.nist.gov/itl/ai-risk-management-framework).
- **F02. NIST AIRC.** AI RMF Core, sección 5 de AI RMF 1.0. [Funciones del marco](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).
- **F03. OECD.** Recommendation of the Council on Artificial Intelligence, OECD/LEGAL/0449, con revisiones hasta 03-05-2024 identificadas en la copia consultada. [PDF oficial del Compendio](https://legalinstruments.oecd.org/api/print?ids=648).
- **F04. UNESCO.** Recommendation on the Ethics of Artificial Intelligence, adoptada en 2021. [Síntesis institucional](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics).
- **F05. UNESCO, Legal Affairs.** UNESCO’s standard-setting. An Overview, actualización indicada 19-06-2024, apartado Recommendations. [Explicación jurídica institucional](https://www.unesco.org/en/legal-affairs/standard-setting/overview?hub=66535).

Las seis fuentes nacionales L01–L06 están enlazadas junto a sus afirmaciones en 1.1. `evidencias/fase_05/sources.json` contiene los once registros, su naturaleza y ubicaciones concretas. `initial_state.json` registra la base de partida; `legal_context.json` identifica la confirmación directa del país y el alcance de la determinación.

La asistencia de IA consistió en consultar y comparar fuentes y redactar propuestas y verificaciones. La aportación humana acreditada en esta reanudación fue confirmar República Dominicana. No se declaran consultas a afectados, aprobación ética, validación jurídica independiente ni correcciones humanas que no consten.

## 7. Pendientes

No queda pendiente un dato necesario para esta fase dentro del alcance actual. Quedan para las siguientes fases el plan de mitigación, evaluación de las cuatro alternativas, recomendación final, pruebas integrales, declaración de IA, PDF y auditoría de rúbrica. Las propuestas éticas y cualquier aceptación de riesgos siguen sujetas a aprobación humana.

## 8. Próximo paso

**Fase 6: mitigación y recomendación final**, cuando el usuario autorice continuar conforme al orden por fases acordado. La Fase 5 se cierra para la demostración académica documentada. No se inicia la Fase 6 ni se realiza push como parte de este cierre.
