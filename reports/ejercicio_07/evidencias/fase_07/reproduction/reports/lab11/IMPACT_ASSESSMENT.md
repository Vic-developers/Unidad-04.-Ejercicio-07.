# LAB11 · Evaluación de impacto del DSS sintético

**Fecha:** 31 de octubre de 2026.

**Alcance:** demostración académica de Territorial Review DSS - Synthetic.

**Naturaleza:** análisis técnico asistido por IA; responsabilidades, valoraciones y procedimientos organizativos son propuestas pendientes de revisión humana. No se documenta una aprobación institucional ni un despliegue real.

## 1. Finalidad, decisión y límites del sistema

La configuración describe una herramienta para priorizar casos sintéticos para revisión humana. El código implementa clasificadores binarios y una aplicación que muestra métricas y puertas de calidad. No existe una cola operacional de casos, un proceso de intervención ni una asignación efectiva de personal revisor. En consecuencia, priorizar es la finalidad declarada y no una capacidad de gestión de expedientes ya demostrada.

Los 640 registros recibidos no representan personas, territorios ni tasas reales. `G1` y `G2` son etiquetas sintéticas sin equivalencia demográfica acreditada. Los posibles daños a personas se analizan como escenarios de reutilización indebida o futura adaptación. No son incidentes observados ni resultados medidos sobre personas.

Las fuentes locales de este análisis son `README.md`, `configs/governance.yml`, `docs/DATASET_CARD.md`, `src/inf8239_u04/data.py`, `model.py`, `fairness.py`, `governance.py` y `app.py`. Los requisitos académicos proceden del texto adjunto; todavía falta la consigna docente original para contrastarlos.

El formulario `student_inputs/lab11_impact.yml` documenta finalidad, usuarios previstos, población, responsable propuesto, alternativa, límites, suspensión y apelación. No se nombra un propietario real ni se asigna autoridad institucional al estudiante, al docente o a terceros.

## 2. Proporcionalidad y alternativa no predictiva

**Necesidad educativa:** usar un modelo es pertinente para practicar auditoría, identificar supuestos y comparar errores de grupo. Ello no demuestra necesidad operacional ni que el modelo mejore una revisión manual.

**Idoneidad pendiente:** aún no se han ejecutado las auditorías de LAB12. Se desconoce el rendimiento del modelo en esta entrega y no se ha comparado el efecto de priorizar sobre una cola real o simulada con capacidad limitada. Tampoco está definida de forma operacional la semántica de `target` más allá de su carácter binario sintético.

**Alternativa propuesta:** revisar todos los casos sintéticos por fecha de recepción sin asignar prioridad predictiva ni excluir casos. Esta alternativa reduce dependencia del modelo, pero su carga de trabajo y desempeño no han sido medidos. Es una referencia de análisis, no un componente implementado.

**Balance preliminar:** el ejercicio resulta justificable dentro de una demostración sintética y supervisada. No hay evidencia para afirmar proporcionalidad de una intervención real. El beneficio comprobable de esta fase es producir documentación y comprobaciones técnicas; la mejora de la atención, la reducción de daños y la equidad son objetivos pendientes de evaluación.

## 3. Interesados e intereses

El CSV conserva sus cinco columnas originales. Esta tabla añade los intereses para evitar alterar el contrato de entrada. Beneficios, daños potenciales, influencia y mecanismos de participación están en `student_inputs/stakeholders.csv` y en la copia generada `reports/lab11/stakeholders.csv`.

| Interesado del CSV | Interés principal | Situación de participación |
|---|---|---|
| Grupos y casos sintéticos G1/G2 y franjas de edad | Ser representados correctamente en el análisis y evitar inferencias sobre colectivos reales. | No son personas participantes; la revisión por subgrupo se realizará técnicamente en LAB12. |
| Operador revisor de la demostración | Comprender errores y conservar autoridad de revisión sin depender de una predicción. | Rol previsto; no se realizaron entrevistas, pruebas de usabilidad ni revisión de casos con operadores. |
| Responsable académico (rol propuesto) | Mantener coherencia entre alcance, evidencias y decisiones. | Designación nominal pendiente; no se presupone aceptación de responsabilidades. |
| Equipo de datos y modelos (rol propuesto) | Reproducir la evaluación y detectar fallos sin ocultar incertidumbre. | Se registra trabajo técnico asistido por IA; no se acredita participación de un equipo humano constituido. |
| Persona evaluadora del ejercicio (rol propuesto) | Verificar trazabilidad y correspondencia con la consigna. | No se ha recibido revisión docente ni aprobación de este informe. |
| Personas de una eventual adaptación real (fuera de alcance) | Participación, protección de datos y posibilidad de impugnar decisiones. | No hay personas reales evaluadas ni consultas efectuadas; una adaptación exigiría una nueva evaluación. |

La influencia `low`, `medium` o `high` es una caracterización cualitativa propuesta de los roles, no una encuesta o un dato observado. Los mecanismos pendientes no se presentan como participación ya realizada.

## 4. Método de valoración de riesgos

Se documentan nueve escenarios vinculados al código y a su posible interpretación o reutilización. Los identificadores R01–R08 de la plantilla se conservan y se añade R09 para integridad de las evidencias.

Las escalas siguientes son una convención exploratoria para este ejercicio, propuesta para revisión. No proceden de un estudio de frecuencias, no son umbrales oficiales de NIST y no representan tolerancias aprobadas por el usuario. El horizonte es la preparación, ejecución y posible reutilización de la demostración; los daños reales son condicionales a una adaptación o uso fuera de alcance.

| Valor | Plausibilidad ordinal del escenario | Severidad potencial si ocurre |
|---|---|---|
| 1 | Requiere circunstancias adicionales excepcionales o un cambio sustancial de alcance. | Error documental localizado, corregible sin afectar la interpretación principal. |
| 2 | Plausible ante cambios de entradas, reutilización o interpretación sin controles suficientes. | Retrabajo acotado o retraso reversible de revisión. |
| 3 | Plausible en el flujo de desarrollo o interpretación por limitaciones visibles del prototipo. | Conclusiones engañosas, carga de revisión importante o pérdida de trazabilidad. |
| 4 | Escenario directamente reproducible y recurrente sin control dentro del flujo considerado. | Potencial afectación grave de derechos o decisiones sobre personas si se extrapola indebidamente. |

La columna `likelihood_1_4` expresa plausibilidad cualitativa, no probabilidad numérica. La severidad 4 no significa que se haya producido daño real. La prioridad inicial es el producto exacto `likelihood_1_4 * impact_1_4`, calculado por el código docente. Para ordenar revisión se propone 9–16 como alta, 4–8 como media y 1–3 como baja; esta convención no convierte el producto en una medida calibrada de riesgo.

`residual` es un juicio cualitativo conservador sobre las limitaciones que quedan con los controles actualmente disponibles. No asume eficacia de medidas pendientes ni una reducción numérica demostrada. Puede seguir siendo alto aunque la prioridad inicial sea media, por ejemplo R02, mientras no se mida recall y la severidad potencial siga siendo alta. Para un uso real no se ha estimado ni aceptado riesgo residual.

| Riesgo | Síntesis | Plausibilidad | Impacto | Prioridad calculable | Residual propuesto y motivo |
|---|---|---:|---:|---:|---|
| R01 | Diferencias de error o selección por grupo/intersección. | 3 | 4 | 12 | high: auditoría y justificación de predictores pendientes. |
| R02 | Falsos negativos si se filtran casos por el modelo. | 2 | 4 | 8 | high: recall desconocido; revisión de todos los casos solo propuesta. |
| R03 | Falsos positivos y desplazamiento de carga de revisión. | 3 | 3 | 9 | medium: alcance sintético acota exposición actual; carga y FPR pendientes. |
| R04 | Identificadores directos en nuevas entradas. | 2 | 4 | 8 | medium: rechazo por nombre de columna; no garantiza privacidad semántica. |
| R05 | Calidad, etiqueta o temporalidad insuficientes. | 3 | 3 | 9 | high: contrato básico sin demostrar validez de etiqueta o estabilidad. |
| R06 | Extrapolación o automatización indebida. | 2 | 4 | 8 | high: advertencias no impiden reutilización por terceros. |
| R07 | Pérdida del registro o irreproducibilidad. | 3 | 3 | 9 | medium: preservación y entorno trazado; modelos y revisión independiente pendientes. |
| R08 | Objeción sin canal o autoridad de revisión. | 2 | 3 | 6 | high: procedimiento documentado sin canal técnico ni prueba con usuarios. |
| R09 | Alteración de entradas o reportes sin trazabilidad confiable. | 2 | 3 | 6 | medium: Git y hashes ayudan a detectar cambios; no son control de acceso ni autenticación. |

Los escenarios, afectados, controles, roles responsables y rutas de evidencia constan en `student_inputs/risk_register.csv`. Las prioridades y ordenación reproducibles se encuentran en `reports/lab11/risk_register_scored.csv`.

## 5. Controles existentes y límites de su verificación

| Control | Evidencia verificable en esta fase | Estado y límite |
|---|---|---|
| C01 · Declaración de datos sintéticos y usos prohibidos. | README, ficha de datos, configuración y aviso de `app.py`. | Implementado en documentación y código inspeccionado; la interfaz no se ejecutó en Fase 1 porque inicia entrenamiento. No constituye bloqueo técnico de usos externos. |
| C02 · Rechazo de identificadores directos por columnas. | `validate_schema`, `tests/test_privacy.py`, `tests/test_data.py` y sus registros de ejecución. | Implementado; las pruebas cubren `name` y `email`. No demuestra ausencia de identificadores indirectos o campos mal rotulados. |
| C03 · Separación de atributos y procedimiento temporal. | `features`, `load_data`, `temporal_split` y verificación de artefactos. | `protected_group` se excluye de predictores; la carga ordena fechas. `age_band` sigue siendo predictor; prevenir toda fuga o sesgo exige LAB12. |
| C04 · Validación y cálculo de impacto. | LAB11 ejecutado, CSV puntuado y resumen RMF. | Valida los campos esperados y calcula prioridades propuestas. No prueba validez empírica de las valoraciones. |
| C05 · Preservación del registro existente. | Apertura exclusiva del registro y pruebas en `tests/test_lab11_script.py`. | Implementado: repetir el script no sustituye el registro. Las salidas calculadas CSV/JSON sí se regeneran de sus entradas. |
| C06 · Entorno y procedencia de artefactos. | `uv sync --frozen`, `uv.lock`, manifiesto de hashes, historial Git y logs. | Implementado para esta fase; depende de preservar una copia confiable de las evidencias. No acredita autenticidad institucional. |
| C07 · Retirada, revisión humana y apelación. | Formulario de impacto y registro de decisión. | Procedimientos propuestos y documentados. No existe un canal implementado, asignación nominal ni validación con personas. |

Los resultados de cada comando están en `reports/ejercicio_07/evidencias/fase_01/execution_log.json`; su interpretación y limitaciones se resumen en `reports/ejercicio_07/FASE_01_LAB11.md`. Una ruta de código demuestra existencia de un control; una prueba solo acredita el comportamiento y casos que ejecutó.

## 6. Aplicación de NIST AI RMF

Se usa AI RMF 1.0 como referencia voluntaria. La fuente oficial lo distingue de una obligación jurídica; este ejercicio no constituye certificación ni declaración de cumplimiento legal. [NIST: AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), consulta: 31 de octubre de 2026.

Las cuatro funciones ayudan a ordenar el análisis: **GOVERN**, responsabilidades y criterios; **MAP**, contexto y afectados; **MEASURE**, evaluación e incertidumbre; **MANAGE**, priorización y respuesta. GOVERN se aplica de forma transversal. La tabla siguiente es un mapeo elaborado para este proyecto, no una lista oficial de conformidad. [NIST: AI RMF Core, secciones 5.1–5.4](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), consulta: 31 de octubre de 2026.

| Riesgo | Funciones relacionadas | Control y responsable propuesto | Evidencia de aplicación actual | Pendiente y residual |
|---|---|---|---|---|
| R01 | MAP, MEASURE, GOVERN | C03; equipo de datos/modelos. | Exclusión de `protected_group` en `data.py`; identificación de intersecciones en `fairness.py`. | Medir brechas y soporte, justificar edad y zona. high. |
| R02 | MAP, MEASURE, MANAGE | C07 propuesto; operador revisor. | Finalidad y alternativa documentadas en el YAML; recall definido en código. | Ejecutar auditoría; acordar respuesta a falsos negativos. high. |
| R03 | MAP, MEASURE, MANAGE | C07 propuesto; operador revisor. | FPR y selección definidos en `fairness.py`; alternativa documentada. | Medir errores y evaluar carga sin presuponer una capacidad operativa. medium. |
| R04 | GOVERN, MEASURE, MANAGE | C02; equipo de datos/modelos. | Rechazo por esquema y pruebas de privacidad/datos. | Ampliar revisión semántica y controles de acceso ante nuevos datos. medium. |
| R05 | MAP, MEASURE | C03 y C04; equipo de datos/modelos. | Contrato básico y fechas del CSV verificadas; limitaciones de etiqueta registradas. | Analizar calidad y validez en LAB12; no hay validación externa. high. |
| R06 | GOVERN, MAP, MANAGE | C01 y C07; responsable académico. | Avisos y prohibiciones existentes; recomendación REVIEW documentada. | Asignación de autoridad, supervisión y barreras institucionales. high. |
| R07 | GOVERN, MEASURE, MANAGE | C05 y C06; equipo de datos/modelos. | Código corregido, pruebas de preservación, entorno bloqueado y logs. | Auditorías reproducibles y revisión independiente. medium. |
| R08 | GOVERN, MAP, MANAGE | C07 propuesto; responsable académico. | Propuesta de objeción por case_id y registro de respuesta. | Canal accesible, plazos, autoridad y consulta a afectados si se cambia el alcance. high. |
| R09 | GOVERN, MEASURE, MANAGE | C06; equipo de datos/modelos. | Historial local, hashes de entradas/salidas y trazas de ejecución. | Acceso controlado y contraste con una copia confiable independiente. medium. |

`rmf_summary.json` resume las cuatro funciones y remite a este documento. Distingue las valoraciones ordinales de métricas observadas y no registra por su cuenta aprobación humana ni autoriza despliegue. La aplicación completa del marco requiere seguimiento; este expediente evidencia solo las actividades expresamente realizadas.

## 7. Retirada, objeción y responsabilidades propuestas

Ante entradas con identificadores directos, pérdida de trazabilidad, fallo de pruebas o cambio del carácter sintético, se propone suspender la interpretación de resultados, preservar archivos y acudir a revisión cronológica. La auditoría pendiente deberá informar el tratamiento de brechas e incertidumbre; los límites de `configs/governance.yml` no se adoptan aquí como tolerancias éticas aprobadas.

Una objeción se podría registrar con el case_id sintético, motivo, evidencia, persona revisora distinta, respuesta y corrección. Este esquema todavía no tiene canal técnico, plazos acordados ni responsables nominales. Su incorporación al YAML es documentación de una propuesta, no prueba de que una reclamación haya sido recibida o atendida.

La responsabilidad final y aceptación de las propuestas quedan en revisión por el usuario. Este análisis no designa personas ni sustituye una decisión ética, académica o institucional.

## 8. Resultado preliminar y referencias locales

Se recomienda **REVIEW**, mantener el alcance educativo y completar la auditoría después de la autorización de la fase siguiente. El resultado no es una decisión final del Ejercicio 07 ni un GO generado por las puertas de LAB13. No se recomienda despliegue real a partir de datos sintéticos.

Artefactos: `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv`, `student_inputs/risk_register.csv`, `reports/lab11/risk_register_scored.csv`, `reports/lab11/stakeholders.csv`, `reports/lab11/rmf_summary.json`, `reports/lab11/DECISION_RECORD.md` y las evidencias de Fase 1. Las conclusiones sobre rendimiento, brechas, mitigaciones comparadas y legislación aplicable siguen pendientes de sus fases correspondientes.
