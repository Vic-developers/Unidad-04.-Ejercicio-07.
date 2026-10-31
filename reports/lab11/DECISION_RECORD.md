# LAB11 · Registro de decisión

**Fecha:** 31 de octubre de 2026.

**Sistema:** Territorial Review DSS - Synthetic.

**Estado del registro:** recomendación técnica para revisión; aprobación humana pendiente.

**Recomendación:** REVIEW. Mantener el ejercicio como demostración sintética y someter la continuación a revisión de esta fase. No autoriza despliegue real.

## Sistema y finalidad

La configuración declara priorización de casos sintéticos para revisión humana. El código implementa clasificación binaria, métricas y una interfaz demostrativa; no implementa una cola institucional ni decisiones sobre personas. Los 640 casos no representan poblaciones, territorios ni tasas reales.

La finalidad de esta entrega es aprender a evaluar impacto y equidad. La semántica operacional de `target` y la utilidad de priorizar frente a una alternativa manual no se han demostrado. Los límites y nueve campos de impacto están documentados en `student_inputs/lab11_impact.yml`.

## Interesados y autoridad

Se distinguen grupos sintéticos, operador previsto, responsable académico propuesto, equipo de datos/modelos propuesto, persona evaluadora prevista y personas de una hipotética adaptación real fuera del alcance actual. Sus beneficios, daños, influencia y mecanismos están en `stakeholders.csv`; sus intereses se explican en `IMPACT_ASSESSMENT.md`.

El rol de responsable académico está pendiente de designación nominal. No se ha recibido aceptación de riesgos, revisión docente ni aprobación institucional. No se realizaron consultas a personas afectadas.

## Riesgos prioritarios

Las valoraciones son juicios ordinales propuestos, no frecuencias observadas. R01, desigualdad entre grupos o intersecciones, tiene prioridad propuesta 12. R03, carga por falsos positivos; R05, calidad/semántica/temporalidad; y R07, trazabilidad, tienen prioridad propuesta 9. Los nueve escenarios y su puntuación reproducible constan en `risk_register_scored.csv`.

R02, falsos negativos; R04, identificadores directos; y R06, extrapolación indebida tienen severidad potencial 4, por lo que deben revisarse aunque su producto sea 8. R08, falta de canal de objeción; y R09, alteraciones de evidencias tienen producto 6. Estos productos no equivalen a riesgos calibrados o aceptados.

## Controles aplicados y limitaciones

- Avisos de datos sintéticos y prohibiciones en README, configuración y código de la aplicación: inspeccionados; no se inició la aplicación en esta fase.
- Rechazo de identificadores directos por nombres de columnas y exclusión de `protected_group` del conjunto de predictores: implementados en el código. Las pruebas ejecutadas y el alcance exacto se documentan en el informe de Fase 1.
- Validación del formulario y registros, cálculo de prioridades y resumen de funciones NIST: salidas reproducibles de LAB11.
- Corrección de sintaxis y preservación del registro de decisión al repetir LAB11: cambio de código con pruebas de regresión.
- Entorno preparado con `uv sync --frozen`, comandos registrados e integridad de entradas/salidas trazada mediante hashes.

La revisión humana efectiva, canal de apelación, supervisión institucional y barreras contra reutilización real son propuestas documentadas, no mecanismos operativos implementados. La exclusión de `protected_group` no prueba equidad, dado que se utilizan edad y zona. El rechazo de cuatro nombres de columnas no garantiza por sí solo privacidad.

## Riesgos residuales e incertidumbre

R01, R02, R05, R06 y R08 conservan residual cualitativo alto por falta de auditoría o controles institucionales efectivos. R03, R04, R07 y R09 conservan residual medio dentro del alcance educativo. No se ha demostrado una reducción cuantitativa ni una aceptabilidad del riesgo para un uso real.

No hay métricas de modelo ejecutadas en Fase 1. Se desconocen recall, FPR, precisión, selección y diferencias de grupo de esta entrega. No se atribuyen daños o beneficios reales a los casos sintéticos.

## Alternativas consideradas

1. **Revisión cronológica sin modelo:** propuesta sencilla para revisar todos los casos; no se ha implementado ni evaluado una cola de trabajo.
2. **Continuar la evaluación predictiva solo en la demo:** permitiría medir errores y brechas en LAB12 después de autorizar esa fase; utilidad y equidad todavía desconocidas.
3. **Suspender interpretación o reutilización de resultados:** apropiado si aparecen datos reales, pruebas fallidas, entradas fuera de contrato o pérdida de trazabilidad, hasta investigar y corregir.

La evidencia actual permite documentar y comprobar LAB11. No permite seleccionar un modelo, aceptar riesgos de despliegue o justificar una intervención real. La evaluación comparada y la decisión final corresponden a fases posteriores.

## Condiciones propuestas para revisar la continuación

Revisar los resultados de LAB11 y sus pruebas, confirmar o corregir los supuestos y roles propuestos, y autorizar expresamente LAB12. Mantener datos sintéticos y exclusión de identificadores directos; medir desempeño y equidad antes de cualquier conclusión sobre el modelo.

**Aprobación del usuario:** pendiente.

**Aprobación institucional o docente:** no documentada.

**Despliegue autorizado:** no.

**Evidencias:** `reports/ejercicio_07/FASE_01_LAB11.md`, `reports/ejercicio_07/evidencias/fase_01/execution_log.json`, `risk_register_scored.csv`, `rmf_summary.json` e `IMPACT_ASSESSMENT.md`.
