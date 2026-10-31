# Fase 6 · Mitigación, compromisos y recomendación final

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo).

**Partes completadas:** 6.1–6.3, plan de mitigación, trade-offs y evaluación de las cuatro alternativas.

**Estado:** recomendación técnica integrada, pendiente de aprobación del usuario. El nombre del archivo identifica el entregable de la fase; no registra una decisión humana aprobada.

**Recomendación:** **LIMITAR** el sistema a la demostración y auditoría académicas con datos sintéticos, conservando **REVIEW** como estado documental de revisión. Se mantiene una preferencia técnica provisional por logística como referencia experimental y el árbol como comparador. **No se recomienda despliegue real basado en esta evidencia.**

**Jurisdicción:** República Dominicana, confirmada por el usuario en Fase 5. El alcance actual procede de los archivos del proyecto. El mensaje «Continua» autoriza elaborar esta fase; la aceptación de riesgos, las propuestas éticas, la designación de responsables y cualquier adaptación real siguen pendientes de decisiones propias.

## 1. Trabajo realizado y fundamento de la recomendación

### 1.1. Evidencia integrada de LAB11 y LAB12

LAB11 aporta finalidad, alternativa cronológica, seis roles/interesados propuestos y nueve riesgos. LAB12 aporta errores y disparidades descriptivas en un único test sintético. El marco de Fase 5 distingue obligaciones nacionales condicionadas al supuesto, referencias orientativas y propuestas éticas. Esta fase vincula esas evidencias con acciones revisables y opciones de uso.

Se reconstruyeron los conteos desde las predicciones guardadas y se contrastaron con las métricas y metadatos existentes. Los 640 registros se dividieron en 480 para entrenamiento y 160 para prueba; en el test hay 92 positivos y 68 negativos. La reconstrucción no añade una muestra ni nuevas predicciones.

| Modelo | TP | TN | FP | FN | Recall | FPR | Seleccionados | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Logística | 66 | 49 | 19 | 26 | 71.74% | 27.94% | 85/160 | 71.88% |
| Árbol | 66 | 47 | 21 | 26 | 71.74% | 30.88% | 87/160 | 70.63% |

La logística añade dos clasificaciones correctas en 160 casos y evita dos FP respecto al árbol, con igual recall global. Esto sustenta una preferencia descriptiva para continuar el ejercicio; no demuestra superioridad poblacional. Los modelos discrepan en 30 casos: 16 son correctos solo con logística y 14 solo con árbol. Igual número de FN no implica las mismas omisiones.

| Brecha absoluta, en puntos porcentuales | Logística | Árbol |
|---|---:|---:|
| Recall G1/G2 | 13.76 | 18.13 |
| FPR G1/G2 | 12.50 | 16.83 |
| Recall interseccional | 43.75 | 41.67 |
| FPR interseccional | 55.56 | 100.00 |

G1 tiene menor recall y G2 mayor FPR. El árbol reduce los FN de G2 de 9 a 8 y aumenta los de G1 de 17 a 18; también puede mejorar algunas intersecciones. Por ello, una preferencia agregada no determina qué distribución de daño debe aceptarse. Siete de ocho intersecciones tienen menos de 30 casos, con n entre 8 y 35; la FPR 100% del árbol en G2 · 30–44 se basa en 2/2 negativos. Los intervalos individuales conservados son condicionales y no justifican afirmaciones causales, de estabilidad o de ausencia de discriminación.

### 1.2. Proporcionalidad y criterios de decisión

La evidencia permite estudiar evaluación de impacto y equidad. No acredita que priorizar con predicción sea necesario, más oportuno o más justo que revisar todos los casos sintéticos por fecha. Esa alternativa no predictiva sigue siendo una propuesta sin cola implementada ni comparación de tiempos humanos. No se le asigna recall o FPR como si fuera otro clasificador, ni se presume que la revisión manual sea perfecta.

Los valores 0.68 y 0.16 de `configs/governance.yml` permanecen como benchmarks experimentales no aprobados. La prioridad relativa de FN y FP depende de las consecuencias y capacidad de revisión; aquí no se fijan costes, ponderaciones de utilidad ni tolerancias éticas en nombre del usuario. Un eventual `GO` de la función de software no resuelve participación, legalidad, calidad de la etiqueta o aprobación humana. No se ejecutó el gate operativo de LAB13 para esta recomendación.

La referencia jurídica sigue siendo [MARCO_LEGAL_VOLUNTARIO_ETICO.md](MARCO_LEGAL_VOLUNTARIO_ETICO.md) y su matriz: no se atribuye tratamiento de titulares reales al dataset descrito como sintético. Una adaptación exigiría identificar operador, datos, finalidad, sector y flujos y actualizar el análisis. La vigencia específica de la referencia sectorial al Decreto 714-26 conserva el límite de comprobación registrado en Fase 5. El cumplimiento de un indicador del plan tampoco certifica cumplimiento jurídico.

## 2. Archivos modificados y continuidad de los registros

La fase crea documentos y evidencias nuevos. Se conservan dataset, modelos, resultados, configuración, formularios y registros anteriores. El registro LAB11 corresponde a Fase 1 y `student_inputs/lab12_decision.yml` a Fase 2; sus frases sobre trabajo entonces pendiente se leen como antecedentes históricos. Esta es la recomendación integrada actual, respaldada por `evidencias/fase_06/decision_proposal.json`; no se atribuye aprobación retrospectiva a esos antecedentes.

## 3. Archivos generados y plan de mitigación — Parte 6.1

El plan editable completo está en [PLAN_MITIGACION.csv](PLAN_MITIGACION.csv). Cada una de sus nueve filas contiene riesgo, acción propuesta, responsable funcional, prioridad y fundamento, componentes ya realizados, evidencia existente, evidencia esperada, indicador, condición de cumplimiento y estado. Los resultados esperados describen trabajo futuro; no se presentan como archivos ya generados.

Las prioridades alta/media son propuestas de orden de revisión, razonadas por severidad potencial, evidencia y vacíos. No recalculan las probabilidades ordinales ni aceptan el riesgo. R03 recibe prioridad de revisión alta por capacidad desconocida, conservando su residual inicial medio pendiente de revisión. Las actuaciones que impliquen personas o una operación institucional necesitan un alcance y una autorización propios; no son requisitos para impedir la continuación documental del ejercicio.

| Medida / riesgo | Prioridad | Acción propuesta e indicador principal | Componentes realizados y condición de cierre propuesta |
|---|---|---|---|
| M01 / R01 · Disparidades | Alta | Justificar edad/zona y comparar ablaciones o políticas con conteos y soporte por estrato. | Exclusión directa y auditorías realizadas; comparación trazada y criterios revisados antes de aceptar resultados. |
| M02 / R02 · Omisiones | Alta | Diseñar revisión completa de referencia; medir cobertura, descartes por clasificación y demora. | FN medidos y alternativa documentada; ensayo sin descartes automáticos y revisión efectiva antes de afirmar supervisión eficaz. |
| M03 / R03 · Carga | Alta | Comparar capacidad y desplazamientos; medir FP, casos marcados y espera por grupo. | FP/selección medidos; comparación con supuestos explícitos y política revisada antes de aceptar priorización. |
| M04 / R04 · Privacidad | Alta | Revisar procedencia, contenido, accesos y conservación antes de admitir nuevas fuentes. | Rechazo de columnas probado en casos concretos; revisión ampliada y fundamento pertinente antes de incorporar nueva información. |
| M05 / R05 · Calidad | Alta | Acreditar etiqueta/generador y disponibilidad temporal; seguir cobertura de supuestos y estabilidad. | Perfil y preprocesamiento comprobados; resolver supuestos necesarios antes de proponer decisiones operativas. |
| M06 / R06 · Uso indebido | Alta | Proponer autoridad y revisión de alcance; distinguir autorizaciones humanas y banderas del software. | Avisos inspeccionados; cambio de finalidad evaluado y autorizado y barreras verificadas antes de afirmar operación controlada. |
| M07 / R07 · Reproducción | Media | Verificar pruebas y reproducción aislada; seguir discrepancias y procedencia de entradas/salidas. | Entorno y trazabilidad locales disponibles; comandos con resultados reales y diferencias explicadas. |
| M08 / R08 · Reclamación | Alta | Proponer canal y otra persona revisora; medir respuesta, escalado y accesibilidad. | Existe una propuesta documental; solicitud/respuesta sintéticas con autoridad y plazo acordados antes de afirmar que funciona. |
| M09 / R09 · Integridad | Alta | Proponer custodia confiable y revisar accesos/cambios; seguir diferencias y revisiones. | Hashes e historial locales; contraste contra referencia confiable y cambios explicados antes de afirmar integridad. |

Los responsables son roles propuestos: operador de la demostración para M02/M03; responsable académico para M06/M08; equipo de datos/modelos para las demás. No se nombraron personas ni se validó su capacidad o autoridad. La evidencia esperada incluye ensayos y revisión independiente solo si posteriormente se realizan; esta fase no ejecuta consultas ni envía solicitudes a terceros.

### 3.1. Evitar mejoras aparentes y conservar la evaluación

M01 no ordena eliminar automáticamente `age_band` o `zone`: primero hay que justificar su función y comparar efectos. Quitar un atributo sensible o un proxy no demuestra equidad; también podría cambiar los errores o dificultar su diagnóstico. Los atributos usados para auditar se distinguen de los usados para predecir y de su eventual fundamento jurídico si fueran personales.

Una futura búsqueda de variables, pesos o umbrales utilizaría particiones de desarrollo dentro de entrenamiento. El test de 160 casos ya fue examinado para comparar modelos: no debe reutilizarse como evaluación final independiente después de escoger modificaciones a partir de sus resultados. Haría falta un nuevo conjunto final no usado para selección, con procedencia documentada y alcance pertinente; añadir más datos sintéticos por sí solo no demostraría validez real. Ningún experimento de mitigación se ejecuta en esta fase.

Las condiciones de cierre del plan indican qué evidencia se esperaría de cada acción; completarlas documentalmente no equivale a comprobar eficacia ni a aceptar riesgo. Los residuales originales se conservan: **high** en R01/R02/R05/R06/R08 y **medium** en R03/R04/R07/R09. El residual posterior queda **sin reestimar**, porque no se midieron efectos de mitigación.

### 3.2. Compromisos entre dimensiones — Parte 6.2

| Dimensión | Evidencia o compromiso | Implicación para el plan |
|---|---|---|
| Rendimiento predictivo | Mismo recall global; logística tiene dos FP menos. Una política que reduzca omisiones puede incrementar revisiones innecesarias. | M02/M03: comparar ambos tipos de error y consecuencias; no optimizar una métrica aislada ni atribuir utilidad operacional medida. |
| Equidad | Menores brechas G1/G2 con logística; el árbol tiene una brecha interseccional de recall ligeramente menor y otros deterioros. | M01/M03: mostrar efectos por grupo e intersección con denominadores e incertidumbre; criterios de aceptación pendientes. |
| Interpretabilidad | Logística: 11 coeficientes más intercepto. Árbol: profundidad 5, 51 nodos y 26 hojas. Las explicaciones usan variables transformadas. | M01/M08: facilitar interpretación y objeción; legibilidad o importancia de una variable no justifican causalidad ni su uso. Comprensión humana sin validar. |
| Privacidad | El alcance sintético limita la exposición actual; edad/zona y eventuales datos nuevos requieren revisión. Menos información puede alterar capacidad de auditoría o predicción. | M04/M05: justificar necesidad y procedencia y distinguir variables de auditoría y predicción; no suprimir controles para mejorar métricas. |
| Seguridad | Filtros y hashes aportan controles concretos; no prueban control de acceso, autenticación o una aplicación segura. | M04/M09: comprobar accesos y custodia y registrar cambios; no convertir trazabilidad local en garantía de prevención. |
| Complejidad | Cinco predictores se transforman en once columnas; estructura y dependencias requieren explicación y mantenimiento. | M05/M07: conservar transformaciones y versiones; una representación más compacta no elimina supuestos de datos o gobernanza. |
| Costos computacionales | Modelos de 3649 y 8059 bytes. Medianas históricas de ajuste controlado: logística 5.75755 ms y árbol 5.46595 ms, con rangos solapados. | M07: usar mediciones locales como tales; tiempo de fit no es latencia de inferencia. No se midieron pico de RAM, electricidad ni emisiones, ni costes humanos. |
| Supervisión humana | Revisar todos los casos puede reducir dependencia del filtro predictivo y aumentar carga o demora; el procedimiento todavía no está implementado. | M02/M03/M06/M08: asignar autoridad y capacidad y ensayar corrección/reclamación; la presencia nominal de una persona no acredita eficacia. |

Estas dimensiones interactúan: al cambiar la política deben revisarse el conjunto de errores, su distribución y los recursos necesarios. No se demuestra una mejora general mediante un cambio favorable en una sola tasa, en tamaño de archivo o en tiempo de entrenamiento.

### 3.3. Cuatro alternativas — Parte 6.3

La versión editable está en [ALTERNATIVAS_USO.csv](ALTERNATIVAS_USO.csv). Todas las valoraciones siguientes son recomendaciones técnicas pendientes de aprobación.

| Alternativa | Ventaja posible | Desventaja y riesgo principal | Condición y valoración actual |
|---|---|---|---|
| A01 · Desplegar | Un apoyo a priorización podría estudiarse en otro contexto; beneficio todavía no demostrado. | Validez externa, etiqueta, operación y autoridad insuficientes; errores desiguales, sobrecarga y uso indebido. | Requiere nueva evaluación integral e independiente y aprobaciones propias. No recomendado con la evidencia actual. |
| A02 · Modificar | Permite estudiar sensibilidad a variables y políticas en el ejercicio. | Trabajo adicional y riesgo de sobreajuste o traslado de daño entre grupos. | Protocolo de desarrollo y nuevo test final independiente; opción experimental futura, no ejecutada. |
| A03 · Limitar | Conserva el aprendizaje y la trazabilidad del análisis sintético. | Persisten incertidumbre y riesgo de extrapolación; no acredita operación eficaz. | Mantener finalidad, REVIEW, límites y revisión humana pendiente. Recomendación para el alcance actual. |
| A04 · No utilizar | Evita apoyar una decisión en clasificaciones sin validación suficiente; ofrece alternativa cronológica. | La revisión completa también tiene carga y errores potenciales no medidos. | Alternativa para decisiones y retirada si se pierde alcance o integridad; cualquier ensayo manual debe evaluarse. |

La recomendación combina **A03 como límite actual**, **A02 como posible trabajo experimental posterior** y **A04 como alternativa ante fallos o usos fuera de alcance**. Elegir A03 para la finalidad educativa no valida una decisión predictiva sobre personas. A01 no queda autorizado por terminar el expediente ni por aprobar la continuación entre fases.

### 3.4. Condiciones propuestas de suspensión y revisión

Si aparecen datos personales, se pierde el carácter sintético, cambia la finalidad, fallan controles pertinentes o no concuerdan las evidencias, se propone suspender el uso de los resultados afectados y registrar la causa con información mínima. Debe conservarse la evidencia que proceda sin incorporar datos personales a Git o a logs públicos, investigar la discrepancia y solicitar revisión competente antes de reanudar un uso que requiera autorización. No se borran automáticamente los registros previos.

Las disparidades o soportes insuficientes mantienen REVIEW y limitan la interpretación. No impiden documentar sus errores en el ejercicio. Para una decisión de priorización no validada se conserva la alternativa de revisión completa, cuya capacidad y eficacia todavía tendrían que medirse.

## 4. Verificaciones ejecutadas y alcance

`evidencias/fase_06/build_decision_facts.py` reconstruye métricas desde CSV guardados, contrasta las salidas de ambos modelos y sus hashes y genera `decision_facts.json`. El verificador documental revisa medidas, alternativas, cobertura de dimensiones, condiciones de aprobación, vínculos, cifras e integridad de archivos anteriores. Estos controles no miden eficacia de mitigaciones ni constituyen aprobación de las prioridades.

| Comprobación de esta fase | Resultado real | Evidencia de ejecución |
|---|---|---|
| Reconstrucción de hechos guardados con Python 3.12 | Código 0; dos modelos y quince fuentes contrastados; cero ajustes o predicciones nuevos. | `evidencias/fase_06/01_saved_decision_facts.json` |
| Ruff sobre los scripts de esta fase | Código 0; sin observaciones. | `evidencias/fase_06/02_style_check.json` |
| Verificación documental y conservación de archivos anteriores | Código 0; nueve medidas, cuatro alternativas, ocho dimensiones, 60 referencias locales y 168 archivos anteriores intactos. | `evidencias/fase_06/03_decision_verification.json` y `verification.json` |

El cierre del informe se vuelve a contrastar con el mismo verificador; su ejecución se conserva por separado en `evidencias/fase_06/04_final_document_verification.json`.

Los códigos, salida y duración reales se conservan en esos registros y en `execution_log.json`. No hay nuevos entrenamientos, predicciones o ensayos de mitigación. Las pruebas integrales de software y la declaración completa de IA corresponden a Fase 7; no se declaran ejecutadas aquí.

## 5. Problemas y límites

Persisten procedencia y semántica de etiqueta incompletas, ausencia de validez externa, muestra pequeña y test ya inspeccionado. No se evaluaron capacidad de una cola, costes de errores, comprensión humana, consulta a afectados, canal de reclamación o controles de un servicio publicado. Los tiempos históricos son de entrenamiento local; los bytes de modelos no son RAM ni emisiones. El documento no certifica legalidad, equidad o reducción de riesgo.

Las propuestas de mitigación son concretas y verificables en su diseño; su ejecución, eficacia y aceptación siguen pendientes. No se reducen residuales por redactar un plan o por mantener una preferencia técnica. Los criterios de daño y tolerancia requieren revisión del usuario en el contexto pertinente.

## 6. Evidencias y uso de IA

Fuentes locales principales:

- [Evaluación integrada](EVALUACION_INTEGRADA.md): relación de nueve riesgos con controles, resultados y límites.
- [Comparación de modelos](COMPARACION_MODELOS.md): resultados globales, por grupos/intersecciones, estructura y benchmark.
- [Marco legal, voluntario y ético](MARCO_LEGAL_VOLUNTARIO_ETICO.md): jurisdicción y clasificación de referencias, con citas oficiales verificadas en Fase 5.
- `student_inputs/risk_register.csv`, `student_inputs/lab11_impact.yml` y `student_inputs/stakeholders.csv`: escenarios, alcance y roles de origen.
- `reports/lab12/logistic/` y `reports/lab12/tree/`: predicciones, soporte, métricas y metadatos conservados.
- `reports/lab12/comparison/`: comparación emparejada, estructura y mediciones previas.
- `evidencias/fase_06/initial_state.json`, `decision_facts.json`, `decision_proposal.json`, registros y manifiesto: procedencia, propuesta estructurada y verificaciones de esta fase.

La asistencia de IA consistió en leer evidencias locales, reconstruir conteos, redactar propuestas y verificarlas documentalmente. El usuario autorizó esta fase con «Continua»; no se recibió aprobación de la recomendación, aceptación de riesgo, nombramiento de responsables ni revisión independiente del contenido. La declaración integral de prompts y verificaciones se elaborará en Fase 7.

## 7. Pendientes

Revisar la recomendación y las prioridades propuestas; ejecutar las verificaciones integrales y documentar reproducibilidad y asistencia de IA en Fase 7; preparar síntesis PDF/editables en Fase 8; auditar la rúbrica en Fase 9. La implementación y evaluación de mitigaciones futuras no se presentan como realizadas ni como requisito satisfecho para un despliegue.

## 8. Próximo paso y autorización

**Fase 6 completada documentalmente; recomendación y aceptación pendientes.** El siguiente paso del plan acordado es **Fase 7: pruebas, reproducibilidad y evidencias**, después de autorización para continuar. Esta fase no inicia LAB13, publicación en GitHub ni despliegue real.
