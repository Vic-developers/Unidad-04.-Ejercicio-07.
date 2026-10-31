# Fase 5 · Marco legal, marcos voluntarios y recomendaciones éticas

**Fecha de consulta:** 31 de octubre de 2026 (America/Santo_Domingo).

**Estado:** parcial, con borrador documental verificado. Marcos voluntarios, recomendaciones éticas y sus referencias preparados; determinación de obligaciones legales pendiente de confirmar jurisdicción y contexto de uso.

**Sistema:** Territorial Review DSS - Synthetic, demostración académica documentada con datos sintéticos. La autorización para trabajar en esta fase no confirma un país ni autoriza adaptación a personas reales.

## 1. Trabajo realizado y criterio de clasificación

Se revisaron fuentes institucionales de NIST, OCDE y UNESCO y se relacionaron con los riesgos y controles del proyecto. La clasificación distingue:

| Categoría | Qué acredita | Estado en el expediente |
|---|---|---|
| Obligación legal aplicable | Una fuente jurídica vinculante, vigente y pertinente al país, sujeto, datos, finalidad y actividad evaluados. | No determinada todavía: jurisdicción solicitada al usuario. |
| Marco o instrumento orientativo | Una referencia de gestión o recomendación intergubernamental cuya naturaleza debe identificarse. | NIST AI RMF y recomendaciones de OCDE/UNESCO examinados. |
| Recomendación ética del proyecto | Una propuesta razonada para este sistema y sus afectados potenciales, diferenciada de lo implementado. | Nueve temas desarrollados; aprobación e implementación pendientes según cada caso. |

La evidencia técnica y la preferencia provisional por logística no prueban cumplimiento jurídico. Los valores 0.68 y 0.16 de `configs/governance.yml` son benchmarks experimentales del proyecto; no se clasifican como límites legales o tolerancias éticas aprobadas.

### 1.1. Parte legal: identificación pendiente de contexto

La pregunta enviada al usuario solicita país/jurisdicción y confirmación del alcance exclusivamente académico. El repositorio no determina por sí mismo ese contexto. La ficha del dataset aclara que no representa estadísticas dominicanas; esa advertencia no acredita que corresponda aplicar legislación dominicana.

**No se ha concluido que no existan obligaciones legales.** Lo que falta es determinar cuáles resultan aplicables. El carácter sintético del dataset tampoco decide por sí solo el régimen de una institución, una publicación o cualquier información adicional que pudiera tratarse.

| Elemento necesario para la parte 5.1 | Situación actual |
|---|---|
| País o jurisdicción del supuesto | Pendiente de respuesta del usuario. |
| Alcance actual acreditado | Demostración académica con 640 casos sintéticos; no hay despliegue real documentado. |
| Adaptación prevista y sujetos/datos reales | No confirmados; no se presupone que exista esa adaptación. |
| Fuentes nacionales vinculantes y vigencia | Se seleccionarán tras confirmar jurisdicción; todavía no se atribuyen obligaciones domésticas. |
| Artículos, supuesto de aplicación y evidencia de cumplimiento | Pendientes; una afirmación de cumplimiento no se sustituirá por un test del modelo. |

Al confirmar el contexto se revisarán las fuentes oficiales pertinentes y se identificará para cada norma su ámbito y condición de aplicación, la obligación concreta y la evidencia disponible o faltante. Se distinguirá la actividad sintética actual de cualquier adaptación hipotética. La selección de leyes y conclusiones de aplicabilidad no se completan mediante una suposición geográfica.

El estado estructurado está en `evidencias/fase_05/legal_context.json`. La fase no se considera completa y no se avanza a la decisión de Fase 6 mientras falte este dato requerido por la parte 5.1 del adjunto.

### 1.2. NIST AI RMF: referencia voluntaria

NIST caracteriza el AI RMF como voluntario. Se mantiene la edición 1.0 publicada el 26 de enero de 2023; la página consultada informa una revisión en curso. No se presenta un borrador como sustituto de la edición utilizada. [Fuente F01: NIST](https://www.nist.gov/itl/ai-risk-management-framework).

Las funciones GOVERN, MAP, MEASURE y MANAGE organizan el trabajo de contexto, evaluación y respuesta. Su uso debe adaptarse al caso. [Fuente F02: AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).

El mapeo del proyecto es una elaboración técnica: roles y límites propuestos en GOVERN; nueve escenarios e interesados en MAP; métricas/conteos en MEASURE; controles concretos y propuestas pendientes en MANAGE. La existencia de esa documentación no acredita una certificación ni una incorporación legal o contractual del marco, que no se ha documentado aquí.

### 1.3. OCDE: recomendación intergubernamental

OECD/LEGAL/0449 fue adoptada en 2019 y revisada en 2023 y mayo de 2024. Sus principios abarcan derechos/equidad, transparencia, robustez y responsabilidad. El documento oficial distingue las recomendaciones no vinculantes de otros instrumentos jurídicos. [Fuente F03: recomendación y nota sobre naturaleza de instrumentos](https://legalinstruments.oecd.org/api/print?ids=648), sección 1 y última página del PDF.

Para este expediente se utiliza como orientación: explicar las salidas, permitir cuestionarlas, conservar trazabilidad y responder al uso fuera de finalidad. Es un mapeo propuesto al proyecto; no se afirma una obligación doméstica directa ni la adhesión de un país aún no confirmado.

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

Solo se crean borradores y evidencias de Fase 5. Los formularios, modelos, datos y resultados anteriores se conservan. La parte legal queda identificada como pendiente, sin modificar las decisiones previas o atribuirles aprobación normativa.

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

Archivos de esta parte: este borrador, el CSV ético, `sources.json`, `legal_context.json`, estado inicial y registros de verificación bajo `evidencias/fase_05/`. No se genera PDF ni decisión final en esta fase.

## 4. Verificaciones y método de consulta

Se consultaron páginas y un PDF oficiales; se contrastó la naturaleza de los instrumentos en sus propias instituciones. La interfaz HTML principal de la recomendación OCDE exigió JavaScript y una copia PDF alternativa agotó el tiempo; se accedió al PDF oficial mediante la API de impresión del Compendio. No se trata un enlace inaccesible como texto revisado: la fuente final citada sí fue leída.

La verificación local comprueba clasificación de fuentes, cobertura de los nueve temas, relación con riesgos, existencia de evidencias y conservación de los archivos previos. Sus resultados se guardan junto al borrador. No se ejecutan nuevos entrenamientos o pruebas de modelo para este trabajo documental.

| Comprobación realizada | Resultado real | Evidencia en `evidencias/fase_05/` |
|---|---|---|
| Ruff sobre registrador y verificador, con `check --fix` | Código 0; un orden de importación corregido, sin observaciones restantes. | `01_style_check.json` |
| Python 3.12: `verify_draft.py` | Código 0; cinco fuentes registradas, nueve temas, 24 referencias locales y 144 archivos previos intactos. Estado de fase explícitamente parcial. | `02_draft_verification.json` y `verification.json` |

No se interpreta el código 0 del verificador como cierre de la Fase 5: acredita la coherencia del borrador y la conservación de su condición pendiente, no la aplicabilidad de leyes.

Esta verificación no acredita aplicabilidad legal. La parte 5.1 requiere la respuesta del usuario y posterior análisis de normas oficiales vigentes. No se atribuye vigencia a legislación nacional no investigada ni se declara cumplimiento por obtener métricas favorables.

## 5. Problemas y límites

La falta de jurisdicción/contexto impide cerrar la determinación de obligaciones aplicables. La pregunta sigue pendiente; no se interpreta el transcurso del tiempo como respuesta o aprobación. Los marcos examinados no resuelven esa falta de contexto.

Los controles organizativos del proyecto permanecen mayormente propuestos. Las referencias y su mapeo no convierten el dataset en evidencia sobre personas, no demuestran ausencia de discriminación y no autorizan despliegue. No se ha recibido revisión humana independiente de este análisis.

## 6. Referencias verificadas y evidencia

Todas las referencias se consultaron el **31 de octubre de 2026**. El registro estructurado contiene título, organización, versión, URL, ubicación y afirmación respaldada.

- **F01. NIST.** AI Risk Management Framework, edición 1.0 (2023) y estado de revisión informado. [Página oficial](https://www.nist.gov/itl/ai-risk-management-framework).
- **F02. NIST AIRC.** AI RMF Core, sección 5 de AI RMF 1.0. [Funciones del marco](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).
- **F03. OECD.** Recommendation of the Council on Artificial Intelligence, OECD/LEGAL/0449, con revisiones hasta 03-05-2024 identificadas en la copia consultada. [PDF oficial del Compendio](https://legalinstruments.oecd.org/api/print?ids=648).
- **F04. UNESCO.** Recommendation on the Ethics of Artificial Intelligence, adoptada en 2021. [Síntesis institucional](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics).
- **F05. UNESCO, Legal Affairs.** UNESCO’s standard-setting. An Overview, actualización indicada 19-06-2024, apartado Recommendations. [Explicación jurídica institucional](https://www.unesco.org/en/legal-affairs/standard-setting/overview?hub=66535).

`evidencias/fase_05/initial_state.json` registra la base de partida; `sources.json` permite rastrear las afirmaciones sobre los instrumentos; `legal_context.json` documenta el requisito de contexto pendiente. La asistencia de IA consistió en consultar y comparar esas fuentes y redactar propuestas y verificaciones. No se declaran confirmación de jurisdicción, consulta a personas o aprobación normativa inexistentes.

## 7. Pendientes

Confirmar país/jurisdicción y alcance. Después: investigar la legislación pertinente, completar una matriz de aplicabilidad con condiciones y evidencia y verificar el documento completo. Hasta entonces, las partes preparadas no equivalen a una Fase 5 finalizada.

## 8. Próximo paso

**Continuar dentro de la Fase 5 cuando se reciba el contexto solicitado.** La autorización de esta fase ya está dada; lo que falta es información para la parte legal, no una nueva autorización. No se inicia Fase 6 ni se publica el borrador en GitHub.
