# Declaración de uso de inteligencia artificial

**Actividad:** INF-8239 · Unidad 04 · Ejercicio 07, evaluación de impacto y auditoría de equidad.

**Fecha:** 31 de octubre de 2026. **Alcance de la declaración:** trabajo registrado hasta Fase 7. La síntesis PDF y auditoría final corresponden a fases posteriores.

Se utilizó **Codex, asistente de IA de esta conversación**, para analizar los materiales, modificar código, ejecutar herramientas, organizar evidencias y redactar propuestas. Esta declaración identifica asistencia y verificaciones observadas; no acredita revisión docente, aprobación jurídica, aceptación humana de riesgos ni autoría humana de cada frase.

## 1. Herramientas y finalidad de uso

| Herramienta o medio | Uso acreditado en el expediente |
|---|---|
| Codex en la aplicación de escritorio | Interpretación del encargo y materiales; propuestas de implementación y documentación; ejecución asistida y análisis de resultados. |
| PowerShell, Python y Git mediante herramientas de ejecución | Lectura y edición local, comandos, historial, registros JSON y hashes. Los commits son locales; esta declaración no acredita publicación en GitHub. |
| uv y entorno Python del proyecto | Preparación del entorno en Fase 1 y comprobación de versiones/dependencias; comandos reproducibles registrados por fase. |
| pandas, scikit-learn, Fairlearn, SciPy y joblib | Validación del archivo y evaluación de modelos, conteos, auditorías de grupos/intersecciones e intervalos, exportación y comparación de artefactos. |
| pytest, Ruff y Streamlit AppTest | Pruebas de software, controles de estilo y prueba de arranque de la aplicación; alcance y resultados reales en TEST_REPORT. |
| Herramienta de consulta web | Investigación de fuentes institucionales en las fases documentadas, especialmente el marco jurídico, NIST, OCDE y UNESCO. Registro de URLs, fechas y límites de acceso en Fase 5. |

El título del texto de referencia menciona OpenCode. El registro disponible identifica a Codex como asistente usado. No se conserva una versión exacta del servicio generativo, temperatura o semilla de generación de respuestas. La semilla 42 documentada para los estimadores de LAB12 corresponde al entrenamiento de esos modelos, no al asistente de IA.

## 2. Prompts y procedencia

Los mensajes y materiales relevantes se describen en [PROMPTS_RELEVANTES.md](PROMPTS_RELEVANTES.md). La copia íntegra del texto adjunto se conserva en [prompt_maestro_referencia.txt](evidencias/fase_07/prompt_maestro_referencia.txt), con hash y procedencia en `evidencias/fase_07/prompt_provenance.json`. No se presenta la recopilación como transcripción completa del chat.

La solicitud directa aportó el enlace del repositorio y materiales. Los mensajes de continuación autorizaron avanzar por fases conforme al plan acordado. «Republica Dominicana» confirmó el país. El adjunto sirvió de referencia del trabajo; se distingue de la solicitud directa y no se trata como instrucción del sistema ni como prueba de ejecución.

## 3. Código, análisis y documentos asistidos

| Parte del trabajo | Asistencia realizada y límite |
|---|---|
| Diagnóstico y LAB11 | Inspección, propuesta de finalidad/roles/riesgos, llenado de YAML/CSV y corrección de generación y preservación de registros. Las valoraciones ordinales y roles permanecen propuestos. |
| LAB12 | Entrenamiento/auditoría de logística y árbol sobre el dataset recibido, ampliación de evidencias, exportación de soportes, parámetros y predicciones y comparación de métricas y recursos. No se generaron personas ni se validaron efectos reales. |
| Pruebas y scripts auxiliares | Pruebas de preservación LAB11, parametrización de pruebas de modelos y verificadores de evidencia. En Fase 7 se corrige la sintaxis del simulador LAB13 sin ejecutarlo ni completar su plantilla. |
| Integración y marco legal | Redacción de evaluación integrada, matrices y clasificación de fuentes oficiales. La IA no certifica aplicabilidad o cumplimiento jurídico mediante un test. |
| Mitigación y recomendación | Nueve acciones propuestas, comparación de cuatro opciones y recomendación de limitar la demostración. No se aprueban tolerancias ni se mide eficacia de mitigación por redactar el plan. |
| Fase 7 | Comprobación de dependencias, pruebas, copia aislada de código/entradas, reproducción local y elaboración de informe, declaración y registro de prompts. |

El código y los datos entregados como base tienen procedencia en el paquete recibido. Su inspección o ejecución asistida no establece quién los escribió originalmente. Los cambios y archivos nuevos se distinguen mediante historial Git, estados iniciales y manifiestos por fase. No se atribuye al usuario la escritura manual de código o redacción producidos por el asistente.

## 4. Verificaciones realizadas y evidencia

Las ejecuciones conservan comando, salida, código, fecha y duración. LAB11 dispone de pruebas de riesgo, validación y preservación del registro; LAB12 tiene auditorías de dos modelos y comprobaciones de predicciones, denominadores y transformaciones aprendidas en entrenamiento. Los resultados por fase se conservan, incluidas ejecuciones fallidas y correcciones.

El informe actual [TEST_REPORT.md](TEST_REPORT.md) identifica resultados, cobertura y comandos exactos de Fase 7. La comprobación de versiones contrasta 55 distribuciones instaladas con `uv.lock` y once requisitos directos/de desarrollo. La copia de reproducción utiliza el mismo intérprete y máquina; su aislamiento de archivos no equivale a instalación limpia, réplica en otra máquina o revisión por otra persona.

La prueba de aplicación ejecuta el pipeline y su cálculo de estado técnico dentro de la copia aislada. Una bandera calculada por software no constituye aprobación humana o de despliegue. Los archivos canónicos se contrastan contra sus hashes; las nuevas mediciones de ejecución se conservan aparte. No se convierten tiempo de entrenamiento o tamaño serializado en electricidad, emisiones o RAM total.

## 5. Correcciones y contribución humana

Las siguientes correcciones técnicas fueron efectuadas por el asistente y verificadas según los registros indicados; no se declaran correcciones humanas inexistentes:

| Fase | Corrección o límite conservado | Evidencia |
|---|---|---|
| 1 | Sintaxis y validación de LAB11; preservación del registro al repetir; ajustes de estilo. | FASE_01_LAB11 y sus logs/pruebas. |
| 2 | Ajustes del registro de comandos para capturar resultados fallidos; estilo corregido. | FASE_02_LAB12 y evidencia de Fase 2. |
| 3 | Contadores NumPy convertidos a enteros nativos para exportar JSON del árbol, sin refit para corregir la exportación. | `evidencias/fase_03/02_tree_support.json` y `03_tree_support_final.json`. |
| 4 | Campos de la matriz transferidos con codificación incorrecta restaurados leyendo la fuente UTF-8; fallo inicial conservado. | `evidencias/fase_04/03_integration_verification.json` y `04_integration_verification_final.json`. |
| 5 | Expectativa literal del verificador ajustada de «no determina» a «ni determina»; fuentes contrastadas y límites registrados. | `evidencias/fase_05/04_framework_verification.json` y verificaciones posteriores. |
| 6 | Dos ubicaciones de lectura preliminares corregidas; las cuatro comprobaciones finales registradas terminaron con código 0. | `evidencias/fase_06/execution_log.json`. |
| 7 | Caché de uv redirigida al espacio de trabajo tras acceso denegado; cadena multilínea del simulador reparada; ejecución complementaria inconclusa conservada y separada para diagnóstico. El test de Streamlit pasó al permitir la conexión local fuera del aislamiento de red predeterminado. | Registros Fase 7, original del simulador y TEST_REPORT. |

La contribución humana acreditada consiste en aportar el encargo y materiales, autorizar continuaciones y confirmar República Dominicana. No constan aceptación de riesgos, designación nominal de responsables, comprobación manual de todos los cálculos, revisión docente, consulta a afectados o revisión independiente del análisis. La aprobación para continuar el trabajo no sustituye esas actuaciones.

## 6. Limitaciones y revisión de la entrega

El dataset es declarado sintético por el proyecto; faltan evidencia completa de su generador/semilla y semántica operacional de la etiqueta. Las métricas corresponden a un test pequeño ya examinado. Las referencias consultadas tienen fecha y límites específicos; los enlaces o normas pueden requerir actualización ante un nuevo uso. La asistencia de IA puede producir errores de código, interpretación, citas o redacción, por lo que los artefactos y resultados verificables son necesarios.

La autoría y aprobación de la entrega requieren revisión de quien la presente. Esta declaración hace explícita la asistencia y sus límites; no prueba que esa revisión final se haya realizado ni verifica una política docente sobre uso de IA. La recomendación sigue pendiente de aprobación y no autoriza decisiones sobre personas ni despliegue real.
