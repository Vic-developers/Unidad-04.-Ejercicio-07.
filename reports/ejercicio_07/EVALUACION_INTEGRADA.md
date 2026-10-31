# Fase 4 · Evaluación integrada de impacto y equidad

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo).

**Partes:** 4.1–4.3: relación riesgos/resultados, evaluación integral y matriz de trazabilidad.

**Estado técnico:** completada y verificada; recomendaciones pendientes de aprobación del usuario.

**Alcance:** Territorial Review DSS - Synthetic, demostración académica con datos sintéticos. No hay personas reales evaluadas, consulta a afectados o autorización de despliegue acreditadas en este expediente.

LAB11 identificó nueve escenarios y controles propuestos; LAB12 permitió cuantificar algunos de esos escenarios en una muestra sintética. Las auditorías muestran diferencias de error y selección, pero no prueban discriminación causal ni eficacia de una operación de revisión humana. La recomendación integrada permanece en **REVIEW**, pendiente de aprobación. La preferencia técnica provisional por logística no cierra los riesgos de gobernanza.

## 1. Trabajo realizado: conexión entre impacto y resultados

### 1.1. Cadena de evidencia

La finalidad y los interesados delimitan qué podría constituir daño; el registro de riesgos formula escenarios; la auditoría cuantifica errores y diferencias del modelo; los controles y sus límites determinan qué queda pendiente. Cada relación debe especificar qué se observó y qué sigue siendo una hipótesis.

Los datos contienen 640 casos sintéticos; se entrenó con 480 y se evaluó con 160. Ambos modelos usan los mismos casos, cinco predictores, transformaciones y semilla. El conjunto de prueba tiene 92 positivos y 68 negativos. Los resultados y procedimientos anteriores se conservan como registros de sus fases; esta integración no modifica esas entradas ni sus decisiones pendientes.

| Resultado observado | Logística | Árbol | Implicación para LAB11 |
|---|---:|---:|---|
| Recall global | 66/92 = 71.74% | 66/92 = 71.74% | R02: persisten 26 omisiones por modelo; no se demuestra revisión efectiva de esos casos. |
| FPR global | 19/68 = 27.94% | 21/68 = 30.88% | R03: posibles revisiones innecesarias si se usara la clasificación para priorizar. |
| Selección global | 85/160 = 53.13% | 87/160 = 54.38% | R03: volumen hipotético de casos marcados; no es carga humana medida. |
| Brecha G1/G2 de recall | 13.76 pp | 18.13 pp | R01: diferencia de detección de positivos en esta muestra. |
| Brecha G1/G2 de FPR | 12.50 pp | 16.83 pp | R01/R03: errores entre negativos distribuidos de forma distinta. |
| Brecha interseccional de recall | 43.75 pp | 41.67 pp | R01: la ligera mejora de una brecha no acredita mejora general. |
| Brecha interseccional de FPR | 55.56 pp | 100.00 pp | R01/R03: extremos con soportes pequeños; no son tasas poblacionales conocidas. |

pp significa puntos porcentuales. Los scores de riesgo 1–4 de LAB11 son valoraciones ordinales propuestas; las tasas de LAB12 son cocientes observados en el test. No se convierten automáticamente unas en otras ni se recalibra la probabilidad de un riesgo a partir de una tasa de error.

### 1.2. Qué resultados confirman, amplían o dejan sin evaluar

- **R01, diferencias entre grupos:** la hipótesis se concreta en disparidades descriptivas de recall, FPR y selección, incluidas intersecciones. Esto confirma que hay diferencias en la muestra, no que exista discriminación causal o daño real. Excluir `protected_group` de predictores no evitó esas diferencias; edad y zona siguen requiriendo justificación.
- **R02, falsos negativos:** se cuantifican 26 entre 92 positivos en ambos modelos. La identidad y reparto de errores cambia: G1 pasa de 17 FN con logística a 18 con árbol; G2, de 9 a 8. El posible retraso o abandono de un caso dependería de una política de revisión que no se ha implementado ni evaluado.
- **R03, falsos positivos y carga:** se observan 19 y 21 FP. G2 tiene menos FP absolutos que G1, pero mayor FPR por su menor denominador negativo. La auditoría amplía el análisis; no determina capacidad, tiempos de atención o costo del operador.
- **R04, privacidad:** el perfil y los metadatos complementan la identificación de datos y variables. No constituyen auditoría integral de privacidad. Las pruebas de rechazo de columnas `name` y `email` son controles concretos, no una demostración de anonimización o protección frente a nuevas fuentes.
- **R05, calidad y temporalidad:** se verificaron IDs únicos, ausencia de faltantes observados, separación temporal y preprocesamiento ajustado con entrenamiento. Sigue faltando definición operacional de `target`, generador y disponibilidad previa de cada predictor; coherencia del archivo no significa validez externa.
- **R06, usos indebidos:** los resultados refuerzan la necesidad de mantener el alcance sintético. Cumplir tres benchmarks puntuales no confiere autoridad ni evita reutilización. La aplicación tiene advertencias en el código; no se probó una barrera operativa contra usos externos.
- **R07, pérdida de evidencia y reproducibilidad:** se aportan registros, versiones, predicciones y modelos trazados; el registro de decisión se conserva al repetir LAB11. Se fortalece el respaldo técnico local, pero no hay réplica en otro equipo ni revisión humana independiente acreditadas.
- **R08, objeción y participación:** las métricas no añaden evidencia de canal accesible, plazos, autoridad revisora o consulta a personas. La propuesta documental sigue pendiente de implementación y validación.
- **R09, alteración de artefactos:** los hashes y comprobaciones de concordancia permiten detectar cambios frente a una referencia confiable. No prueban autenticación, control de acceso o prevención de alteraciones con sustitución de las evidencias.

### 1.3. Evaluación integral: diez preguntas del ejercicio

| Pregunta | Respuesta sustentada en el proyecto |
|---|---|
| 1. ¿Para qué se utilizaría? | Para practicar evaluación de impacto y auditoría de una priorización sintética para revisión humana. La eficacia educativa u operacional no se ha medido con personas. |
| 2. ¿Qué decisión pretende apoyar? | Qué casos sintéticos podrían recibir revisión prioritaria. El código implementa clasificación y métricas, no una cola institucional ni una intervención efectiva. |
| 3. ¿Quién puede beneficiarse? | Estudiante/analista, persona evaluadora y revisor previsto pueden disponer de evidencia verificable. Un beneficio para una población real es hipotético y exigiría una evaluación distinta. |
| 4. ¿Quién podría verse perjudicado? | Quien interprete el expediente puede extraer conclusiones erróneas; en una adaptación indebida, positivos omitidos, negativos marcados, grupos con errores mayores y operadores sobrecargados. No son daños reales observados aquí. |
| 5. ¿Es proporcional usar predicción? | Existe una justificación didáctica para estudiar modelos. No se ha demostrado necesidad ni proporcionalidad de uso real frente a revisar todos los casos cronológicamente; esa alternativa sigue sin implementación o comparación operativa. |
| 6. ¿Qué riesgos son prioritarios? | La valoración inicial propone R01=12 y R03/R05/R07=9 como productos altos. Las evidencias obligan a revisar errores R01–R03 y vacíos R05/R06/R08. Esas prioridades no son tolerancias aprobadas o probabilidades calibradas. |
| 7. ¿Qué grupos presentan resultados desfavorables? | G1 tiene menor recall y mayor FNR; G2 mayor FPR. Las intersecciones cambian según métrica/modelo y tienen soportes pequeños. No existe un único grupo peor en todas las dimensiones. |
| 8. ¿Qué limita la evaluación? | Datos sintéticos, test de 160 casos, siete intersecciones con n<30, etiqueta/generador incompletos, incertidumbre condicional, ausencia de validación externa y de una operación humana evaluada. |
| 9. ¿Qué controles son necesarios? | Mantener validaciones y trazabilidad existentes, justificar predictores, validar errores y datos de forma independiente y acordar supervisión, límites, retirada y apelación. Los controles organizativos son propuestas pendientes, no resultados de las pruebas. |
| 10. ¿Qué riesgos permanecen? | Diferencias y errores, calidad/validez externa, privacidad no integral, usos indebidos, participación/apelación ausentes y dependencia de una referencia confiable para integridad. No se demuestra riesgo cero ni aceptabilidad para uso real. |

### 1.4. Grupos, soportes e interpretación del daño

| Modelo y grupo | Positivos / negativos | FN y FNR | FP y FPR |
|---|---:|---:|---:|
| Logística · G1 | 49 / 52 | 17; 34.69% | 13; 25.00% |
| Árbol · G1 | 49 / 52 | 18; 36.73% | 14; 26.92% |
| Logística · G2 | 43 / 16 | 9; 20.93% | 6; 37.50% |
| Árbol · G2 | 43 / 16 | 8; 18.60% | 7; 43.75% |

G2 tiene una proporción positiva de 43/59=72.88% y G1 de 49/101=48.51%. La diferencia de selección necesita interpretarse junto a esa composición y a las consecuencias de recibir revisión; no demuestra por sí sola trato causal desigual.

Las ocho intersecciones tienen de 8 a 35 casos. En G2 · 30–44, el árbol alcanza FPR=2/2, cuyo intervalo Wilson 95% es aproximadamente 34.24–100%; en G2 · 45–59, la logística tiene recall=6/6, con intervalo 60.97–100%. Esos extremos no acreditan tasas estables. Los intervalos son individuales, condicionales a las predicciones y no corrigen múltiples comparaciones ni incertidumbre de entrenamiento. No se ha ejecutado una prueba causal o una inferencia simultánea de brechas.

### 1.5. Controles comprobados y propuestas pendientes

Se mantienen los identificadores de controles de `reports/lab11/IMPACT_ASSESSMENT.md`:

| Control | Evidencia disponible y estado integrado |
|---|---|
| C01 · Avisos y usos prohibidos | Implementados en documentación/configuración/código inspeccionado. No se ejecutó la interfaz ni se acreditó prevención de usos externos. |
| C02 · Rechazo de identificadores por columnas | Implementado; pruebas de `name` y `email` aprobadas en Fase 1. Cobertura limitada al contrato y casos comprobados. |
| C03 · Atributos y separación temporal | Exclusiones de predictores, corte 480/160 y aprendizaje de transformaciones con entrenamiento comprobados para ambos modelos. No garantizan ausencia de toda fuga o sesgo. |
| C04 · Validación de impacto y puntuación | Formulario/registros validados y prioridades calculadas correctamente. No valida empíricamente el juicio ordinal de riesgo. |
| C05 · Preservación de decisión | Registro existente conservado y prueba de regresión ejecutada. No equivale a aprobación de su contenido. |
| C06 · Entorno y procedencia | Lock, comandos, versiones, hashes y concordancia de artefactos registrados. Alcance local; no autentica aprobación institucional. |
| C07 · Supervisión, retirada y apelación | Documentados como propuestas. No hay autoridad nominal, canal, plazos acordados o aplicación efectiva acreditados. |

Las auditorías y pruebas de software son evidencia de medición, estructura y comportamiento concreto. No sustituyen consulta a interesados, evaluación de daño, revisión humana de decisiones ni implementación de una mitigación que reduzca los errores. El plan de mitigación con responsables, indicadores y condiciones corresponde a la Fase 6.

### 1.6. NIST AI RMF integrado

Se conserva la referencia voluntaria utilizada en LAB11, sin presentarla como obligación jurídica o certificación. La estructura GOVERN/MAP/MEASURE/MANAGE organiza el expediente; las filas siguientes son la interpretación de este proyecto, no una declaración de conformidad con todas las categorías del marco. Referencia ya consultada: [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), 31 de octubre de 2026.

| Función | Evidencia integrada | Estado y vacío relevante |
|---|---|---|
| GOVERN | Finalidad, límites, roles propuestos, registros de decisión y versiones. | Documentación disponible; aceptación de riesgo, designación de autoridad, consulta y contexto jurídico pendientes. |
| MAP | Seis interesados/roles, nueve escenarios y alcance sintético con alternativa no predictiva. | Contexto definido para el ejercicio; beneficios, carga e impactos reales sin validar. |
| MEASURE | Scores ordinales identificados como propuestas y auditorías de dos modelos con conteos, soportes, intervalos y comparación. | Medición ejecutada en este dataset; no hay validación externa ni evaluación de supervisión o apelación. |
| MANAGE | Corrección técnica de sobrescritura, controles de datos y trazabilidad y recomendación REVIEW. | Hay controles técnicos concretos; mitigaciones organizativas, seguimiento y aceptación siguen siendo propuestas. |

El campo MEASURE del resumen de LAB11 señala que ese script no evalúa el modelo. LAB12 proporciona ahora evidencia adicional en el expediente integrado; no se reescribe el resultado histórico de LAB11 ni se convierte una métrica favorable en aprobación de MANAGE.

## 2. Archivos modificados

La integración crea documentos y evidencias nuevos. Los archivos existentes, modelos, dataset, lock, formularios y resultados de las fases anteriores se conservan y se contrastan con el estado inicial de esta fase. No se recalculan modelos ni se alteran los scores o residuales originales.

## 3. Matriz de trazabilidad y archivos generados

La versión editable completa está en [MATRIZ_TRAZABILIDAD.csv](MATRIZ_TRAZABILIDAD.csv). Incluye los nueve IDs originales, afectados, rutas concretas de evidencia LAB11/LAB12, hallazgo, relación, controles aplicados, propuesta, responsable funcional y residual. Todos los roles siguen propuestos; no se atribuye autoridad a una persona o institución real.

Los códigos A–I de esta síntesis remiten al catálogo de la sección 6. Las referencias a personas/territorios de la matriz describen una adaptación hipotética fuera del alcance actual.

| Riesgo | Grupo afectado | Evidencia LAB11 | Evidencia LAB12 | Mitigación y estado | Residual propuesto |
|---|---|---|---|---|---|
| R01 · Diferencias de error | G1/G2 e intersecciones | A, B: escenario, finalidad y valoración | E, F, H: gaps y soportes cuantificados | Exclusión directa y auditoría realizadas; justificar edad/zona y validar independientemente, pendiente. | high |
| R02 · Falsos negativos | Positivos sintéticos | A, B: omisión y alternativa | E, F, H: 26/92 FN por modelo; reparto distinto | Medición realizada; acordar y probar revisión sin exclusión automática, pendiente. | high |
| R03 · Falsos positivos/carga | Operador y otros casos | A, B: sobrecarga potencial | E, F, H: FP 19/68 y 21/68 | Medición realizada; evaluar capacidad/costos y trade-offs, pendiente. | medium; revisar capacidad |
| R04 · Privacidad en nuevos datos | Personas solo si se introducen datos reales | A, C: contrato y pruebas limitadas | D, G: datos y predictores descritos; sin auditoría integral de privacidad | Rechazo por columnas comprobado; revisión semántica/accesos, pendiente. | medium |
| R05 · Calidad/temporalidad | Analista, operador y grupos | A, B: supuestos y límites | D, G: 640 IDs; corte 480/160 y ajuste con train | Coherencia técnica comprobada; definir etiqueta/procedencia y validez externa, pendiente. | high |
| R06 · Uso indebido | Usuarios y población hipotética | A, B: prohibiciones y REVIEW | E, F, H: métricas no equivalen a autorización | Avisos inspeccionados; autoridad y barreras operativas, pendientes. | high |
| R07 · Irreproducibilidad | Equipo y evaluador | A, C: preservación del registro | G, I: versiones, comandos y modelos trazados | C05/C06 aplicados; réplica y revisión independiente, pendientes. | medium |
| R08 · Objeción sin mecanismo | Revisor y posibles afectados | A, B: procedimiento propuesto | I: límites de auditoría; sin prueba de canal | C07 solo propuesto; asignar y probar canal/autoridad/plazos, pendiente. | high |
| R09 · Integridad de evidencia | Equipo, responsable y evaluador | A, C: control de procedencia | G, I: hashes y concordancia | Integridad local comprobada; custodia/accesos/revisión independiente, pendientes. | medium |

Los residuales son las valoraciones cualitativas de LAB11 conservadas **para revisión**, no una aceptación ni una reducción demostrada. En R03 se hace explícita la necesidad de revisar el nivel una vez se conozcan carga y severidad operativas. Ninguno constituye una estimación suficiente del riesgo de un despliegue real.

Otros archivos nuevos: `evidencias/fase_04/integration_facts.json` extrae métricas/conteos y registros de origen; `build_facts.py` permite reproducir esa extracción; `verify_integration.py` valida correspondencia e integridad; los registros de ejecución y manifiesto guardan las comprobaciones del cierre. No se generó el PDF en esta fase.

## 4. Verificaciones de esta fase y pruebas previas

La extracción se ejecutó con Python 3.12.13 sobre archivos guardados, sin entrenar ni predecir de nuevo. Su registro es `evidencias/fase_04/01_saved_facts.json`. El verificador de cierre contrasta cobertura de riesgos, roles, residuales, referencias existentes, conteos, denominadores, brechas y conservación de todos los archivos previos. El resultado real queda en `verification.json` y el registro del comando.

| Comprobación de Fase 4 | Resultado real | Evidencia en `evidencias/fase_04/` |
|---|---|---|
| Python 3.12: `build_facts.py` | Código 0; dos modelos y nueve riesgos extraídos de artefactos existentes. | `01_saved_facts.json` |
| Ruff sobre los tres scripts nuevos con `check --fix` | Código 0; un orden de importación corregido, sin observaciones restantes. | `02_style_check.json` |
| Python 3.12: `verify_integration.py`, ejecución final | Código 0; nueve riesgos, diez preguntas, 59 referencias a archivos y 129 archivos previos intactos. Conteos/tasas reconstruidos desde predicciones guardadas. | `04_integration_verification_final.json` y `verification.json` |

La primera validación detectó una discrepancia de codificación en campos de afectados/responsables transferidos por consola a la matriz. Se repusieron leyendo directamente el CSV original como UTF-8 y se volvió a validar. El registro fallido se conserva en `03_integration_verification.json`; no se presenta como comprobación aprobada. Ninguna fuente ni métrica cambió durante la corrección.

No se repiten pruebas de modelo para un cambio documental. Las ejecuciones anteriores se citan con su alcance y fecha, sin presentarlas como nuevas pruebas de Fase 4:

| Fase | Pruebas anteriores acreditadas | Alcance |
|---|---|---|
| LAB11 | 3 de impacto/privacidad y 5 de datos/regresión aprobadas | Estructura, ejemplos de rechazo y preservación del registro; no eficacia de una operación humana. |
| LAB12 logística | 2 aprobadas | Predicciones binarias y propiedades básicas de métricas/grupos. |
| Comparación | 4 aprobadas, dos por modelo | Las mismas propiedades para logística y árbol; no certificación de equidad. |

Estas cantidades son ejecuciones por fase, no una suma de pruebas únicas del proyecto. Los fallos de estilo/exportación y sus correcciones se conservan en las evidencias de sus respectivas fases.

## 5. Límites y riesgos no cerrados

La integración no demuestra eficacia de supervisión, canal de apelación, consulta a personas, privacidad integral, validez jurídica, seguridad de acceso o aceptabilidad del riesgo. No se han observado daños reales ni se ha demostrado ausencia de daños potenciales. La comparación descriptiva entre modelos y una revisión documental no sustituyen validación externa.

La logística presenta menor FPR y brechas G1/G2 y ocupa menos bytes; el árbol mejora algunas intersecciones y tiene una mediana local de entrenamiento algo menor. El margen de accuracy es de dos casos de 160 y los rangos de tiempo se superponen. Esas ventajas parciales no autorizan despliegue ni resuelven R06/R08. No se midieron energía o emisiones.

La consigna original y la jurisdicción de una eventual adaptación siguen sin determinarse. El contexto sintético y una mención negativa de estadísticas dominicanas no bastan para afirmar legislación aplicable. Esa identificación corresponde a la Fase 5.

## 6. Catálogo de evidencias y reproducción

| Código | Fuentes locales principales |
|---|---|
| A | `student_inputs/risk_register.csv`, `reports/lab11/risk_register_scored.csv`. |
| B | `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv`, `reports/lab11/IMPACT_ASSESSMENT.md`, `reports/lab11/DECISION_RECORD.md`. |
| C | `src/inf8239_u04/data.py`, `scripts/lab11_impact.py`, `reports/ejercicio_07/evidencias/fase_01/execution_log.json` y manifiesto de esa fase. |
| D | `reports/lab12/dataset_profile.json`, `reports/lab12/temporal_split.csv`. |
| E | `reports/lab12/logistic/global_metrics.json`, `fairness_by_group.csv`, `fairness_intersectional.csv`, `audit_support.csv` y `test_predictions.csv` en la misma carpeta. |
| F | Los mismos archivos de auditoría bajo `reports/lab12/tree/`. |
| G | `reports/lab12/logistic/model_metadata.json` y `reports/lab12/tree/model_metadata.json`. |
| H | `reports/lab12/comparison/model_comparison.csv`, `paired_predictions.csv` y `reports/ejercicio_07/COMPARACION_MODELOS.md`. |
| I | Logs e integridad de `reports/ejercicio_07/evidencias/fase_02/` y `fase_03/`, más `reports/ejercicio_07/FASE_02_LAB12.md`. |

El CSV ofrece rutas completas respecto de la raíz del repositorio para cada fila. Las métricas sin redondeo se conservan en sus fuentes y en `integration_facts.json`; las tablas de este documento usan porcentajes y pp redondeados.

Para reproducir las comprobaciones de integración desde la raíz del proyecto, con los artefactos anteriores presentes:

```powershell
& '.\.venv\Scripts\python.exe' -B 'reports\ejercicio_07\evidencias\fase_04\build_facts.py'
& '.\.venv\Scripts\python.exe' -B 'reports\ejercicio_07\evidencias\fase_04\verify_integration.py'
```

La primera orden regenera una extracción de hechos; la segunda valida el expediente de esta fase. No se ajusta ningún modelo. `initial_state.json` y `artifact_manifest.json` documentan los bytes de partida y cierre; los hashes requieren una referencia confiable y pueden variar por saltos de línea al clonar. Los modelos locales permanecen ignorados por Git y sus hashes se comprueban si están presentes.

La asistencia de IA en esta fase consistió en interpretar y relacionar evidencias, redactar la matriz y el informe y ejecutar las comprobaciones documentadas. El mensaje «cONTINUA» autorizó avanzar a la integración; no constituye aceptación normativa de los residuales. No se recibieron revisiones humanas independientes o consultas a afectados.

## 7. Pendientes del proyecto

Revisar la evaluación integrada, confirmar jurisdicción/contexto para la fase legal, desarrollar el plan de mitigación y decisión final, cerrar reproducibilidad y declaración de IA, producir la síntesis PDF y auditar la rúbrica. Los roles, prioridades y residuales continúan como propuestas.

## 8. Próximo paso y autorización

El siguiente paso será **Fase 5 · Marco legal, marcos voluntarios y recomendaciones éticas**, después de `CONTINUAR`, según el flujo del adjunto. Se deberá confirmar jurisdicción antes de atribuir obligaciones legales. La recomendación vigente es REVIEW; no se ha realizado push ni publicación en GitHub.
