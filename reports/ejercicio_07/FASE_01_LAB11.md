# Informe de avance · Fase 1 · LAB11

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo).

**Partes completadas:** 1.1–1.6: finalidad, interesados, riesgos, NIST AI RMF, registro de decisión y validación.

**Estado técnico:** completada. Propuestas de roles, escalas y procedimientos pendientes de revisión del usuario.

## 1. Trabajo realizado

Se incorporaron los 42 archivos de la base al clon local, sin sobrescribir el diagnóstico ni modificar la carpeta original de Descargas. Se creó la rama `codex/ejercicio-07`; la recepción y la base original quedaron identificadas por los commits locales `e2d6249` y `6ad4c1a`, respectivamente.

Se preparó `.venv` con **Python 3.12.13** y `uv sync --frozen`. El comando instaló 55 paquetes, incluido el proyecto editable, utilizando el lock recibido; su hash no cambió. Las versiones reales están en `evidencias/fase_01/environment.json`, y las salidas de instalación en `setup_log.json`.

Se completaron los nueve campos del formulario de impacto, seis filas de interesados y nueve escenarios de riesgo. El análisis distingue datos sintéticos, posibles daños condicionales de una reutilización y hechos efectivamente verificados. Se conservan los encabezados de los CSV; los intereses se explican en `reports/lab11/IMPACT_ASSESSMENT.md`.

Se corrigió la cadena sin terminar en `scripts/lab11_impact.py`, se separó su ejecución de la importación mediante `main()` y se protegió `DECISION_RECORD.md` con apertura exclusiva: un archivo existente se conserva. El script también rechaza registros vacíos o incompletos de interesados y exige un mínimo de ocho riesgos antes de generar salidas.

El resumen RMF mantiene las claves GOVERN, MAP, MEASURE y MANAGE, ahora con estados explícitos y referencias a evidencia. No registra aprobación humana ni interpreta las puntuaciones ordinales como frecuencias observadas. El mapeo de cada riesgo a controles, responsables propuestos y residual está en la evaluación de impacto.

El [NIST AI RMF se utiliza como referencia voluntaria](https://www.nist.gov/itl/ai-risk-management-framework); el mapeo del proyecto se apoya en sus [cuatro funciones](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/). No constituye certificación ni valoración jurídica. Fuentes consultadas el 31 de octubre de 2026.

## 2. Archivos modificados respecto de la base

| Ruta | Cambio y propósito |
|---|---|
| `student_inputs/lab11_impact.yml` | Finalidad, decisión asistida, usuarios, afectados, propietario propuesto, alternativa, usos excluidos, suspensión y apelación. |
| `student_inputs/stakeholders.csv` | Seis grupos o roles, con beneficios, daños, influencia y participación; se distingue participación realizada de propuestas. |
| `student_inputs/risk_register.csv` | Nueve escenarios con afectados, valoraciones propuestas, controles, responsables, evidencia y residual. |
| `scripts/lab11_impact.py` | Corrección de sintaxis, validación de interesados/mínimo de riesgos, generación de evidencia y preservación del registro. |

El dataset, `uv.lock`, los módulos de modelado/equidad y el YAML de LAB12 conservan el contenido recibido. El error de `scripts/simulate_incident.py` sigue registrado como asunto de LAB13 fuera de esta fase.

## 3. Archivos generados

| Ruta | Contenido |
|---|---|
| `reports/lab11/IMPACT_ASSESSMENT.md` | Proporcionalidad, intereses, escala propuesta, nueve riesgos, controles y trazabilidad NIST. |
| `reports/lab11/DECISION_RECORD.md` | Recomendación REVIEW, alternativas, controles, incertidumbre, residual y aprobación pendiente. |
| `reports/lab11/risk_register_scored.csv` | Nueve filas puntuadas y ordenadas por prioridad e impacto. |
| `reports/lab11/stakeholders.csv` | Copia generada de los seis interesados. |
| `reports/lab11/rmf_summary.json` | Resumen verificable de las cuatro funciones; despliegue no autorizado. |
| `tests/test_lab11_script.py` | Tres pruebas de preservación del registro, borrador sin aprobación y rechazo de interesado incompleto. |
| `reports/ejercicio_07/FASE_01_LAB11.md` | Este informe de cierre. |
| `reports/ejercicio_07/evidencias/fase_01/` | Instalación, versiones, ejecución final e inicial, scripts de verificación, integridad, manifiesto y estado Git. |

## 4. Pruebas y comandos ejecutados

El registro final contiene stdout, stderr, código de salida, fecha UTC y duración de cada comando. Para las comprobaciones posteriores a la instalación se fijaron `UV_FROZEN=1` y `UV_OFFLINE=1`, de modo que no se actualizara el lock ni se descargaran paquetes durante las pruebas.

| Comando | Resultado real final | Evidencia |
|---|---|---|
| `uv sync --frozen` | Código 0; 55 paquetes instalados. | `setup_log.json` |
| `uv run python scripts/check_environment.py` | Código 0; dataset válido según contrato básico, 640 filas y 9 columnas. | `execution_log.json` |
| `uv run python scripts/lab11_impact.py` | Código 0; nueve riesgos y seis interesados; salidas generadas. | `execution_log.json` y `reports/lab11/` |
| `uv run pytest -q tests/test_impact.py tests/test_privacy.py` | **3 passed in 0.77s**. | `execution_log.json` |
| `uv run pytest -q tests/test_lab11_script.py tests/test_data.py` | **5 passed in 0.88s**. | `execution_log.json` |
| `uv run ruff check scripts/lab11_impact.py tests/test_lab11_script.py` | Código 0; `All checks passed!`. | `execution_log.json` |
| `uv run python reports/ejercicio_07/evidencias/fase_01/verify_artifacts.py` | Código 0; contenido y prioridades coherentes, dataset/lock originales intactos. | `artifact_verification.json` |
| `git diff --check` | Código 0; avisos informativos LF/CRLF de Git, sin errores de espacio en los cambios comprobados. | `execution_log.json` |

**Total: ocho pruebas únicas aprobadas** en el conjunto ejecutado. No se ejecutó toda la suite, no se entrenaron modelos y no se inició Streamlit. Las pruebas de privacidad cubren rechazo de columnas `name` y `email`; no acreditan privacidad completa.

### Incidencia resuelta durante la validación

La primera ejecución pasó las mismas ocho pruebas y se detuvo al encontrar dos observaciones de Ruff en el nuevo archivo de pruebas: orden/formato de imports (`I001`) y argumento UTF-8 innecesario en `encode` (`UP012`). Se corrigieron con `uv run ruff check --fix tests/test_lab11_script.py`. El primer registro se preservó como `execution_log_attempt_01.json`; la validación final se repitió y pasó. No se oculta ni se presenta como exitosa esa comprobación inicial de estilo.

Después se ajustaron únicamente los párrafos de metadatos de los documentos nuevos. Se ejecutaron otra vez LAB11 y el verificador para comprobar la preservación del registro con su formato definitivo, sin repetir las pruebas aprobadas. `decision_record_checks` conserva ambos pares de hashes; los campos de hash de nivel superior corresponden a la última comprobación.

### Contenido comprobado

- Nueve campos de impacto completos; seis interesados completos y copia de salida idéntica.
- Nueve IDs de riesgo únicos, propietarios correspondientes a roles del CSV y valores enteros de 1 a 4.
- Producto de plausibilidad por impacto correcto en las nueve filas y prioridades ordenadas.
- Cuatro funciones RMF con referencias existentes y `deployment_authorized: false`.
- Dataset y lock con los hashes originales; los 42 archivos de Descargas sin cambios.
- Registro de decisión preservado byte por byte durante la ejecución final; la prueba de regresión verifica también dos ejecuciones sucesivas sobre un registro existente.
- Sin modelos `.joblib`, sin resultados LAB12 y sin cambios al YAML de decisión de LAB12.

## 5. Problemas, límites y decisiones pendientes

Se resolvieron el bloqueo de sintaxis, la sobrescritura del registro y la preparación del entorno. No se requirió cambiar dependencias ni el dataset.

Las escalas de plausibilidad e impacto, sus puntos de corte de revisión y los residuales son valoraciones exploratorias propuestas. No son probabilidades estimadas, umbrales oficiales de NIST o tolerancias aprobadas. El código comprueba estructura y aritmética; no demuestra que el juicio de riesgo sea correcto.

Se documentaron roles funcionales sin inventar responsables nominales. La revisión humana, participación de afectados, retirada operativa y apelación siguen siendo procedimientos propuestos; no existe un canal técnico ni una operación institucional validada. No se ha recibido corrección humana, aprobación docente o aceptación de riesgos.

La consigna original y la jurisdicción aplicable a una eventual adaptación real siguen sin determinarse. Las métricas y disparidades del modelo están pendientes de LAB12; excluir `protected_group` no acredita equidad, dado que edad y zona se usan como predictores. No hay medición de energía ni carbono en esta fase.

## 6. Evidencias y trazabilidad

Las rutas de los registros de esta sección son relativas a `reports/ejercicio_07/evidencias/fase_01/`:

- `setup_log.json`: instalación real sin actualizar el lock.
- `environment.json`: versión de Python, ejecutable y paquetes instalados.
- `execution_log_attempt_01.json`: primera ejecución, incluidos el éxito de las pruebas y el fallo inicial de estilo.
- `execution_log.json`: ejecución final completa, con códigos y salidas, más hashes antes/después del registro.
- `artifact_verification.json`: comprobaciones de entradas, resultados y alcance de fase.
- `artifact_manifest.json`: hashes SHA-256 de archivos de esta fase y dependencias relevantes; el propio manifiesto se excluye para evitar una referencia circular.
- `estado_git.txt`: rama, destino remoto y estado preparados para el cierre local.
- `run_validation.py` y `verify_artifacts.py`: procedimientos reproducibles sin entrenamiento.

Para reproducir las comprobaciones centrales desde la raíz del proyecto:

```powershell
uv sync --frozen
uv run --frozen python scripts/check_environment.py
uv run --frozen python scripts/lab11_impact.py
uv run --frozen pytest -q tests/test_impact.py tests/test_privacy.py
uv run --frozen pytest -q tests/test_lab11_script.py tests/test_data.py
uv run --frozen ruff check scripts/lab11_impact.py tests/test_lab11_script.py
uv run --frozen python reports/ejercicio_07/evidencias/fase_01/verify_artifacts.py
```

`run_validation.py` se niega a sobrescribir un registro de ejecución existente: debe conservarse antes de registrar otro intento, como se hizo con el inicial. El verificador puede contrastar los originales de Descargas cuando están disponibles; en otro equipo informa que esa comparación externa no está disponible. Los hashes describen los bytes guardados y deben revisarse si Git transforma saltos de línea al clonar; las salidas se pueden regenerar con los mismos comandos.

**Asistencia de IA en esta fase:** Codex inspeccionó código y materiales, redactó las propuestas, corrigió el script y ejecutó las verificaciones registradas. El mensaje del usuario «cONTINUA» autorizó avanzar a LAB11; el texto adjunto definió las partes 1.1–1.6 y la pausa posterior. La corrección del defecto inicial y los dos ajustes de estilo fueron realizados por el asistente. No se declaran verificaciones humanas ni aprobación de las propuestas. La declaración integrada de IA y recopilación final de prompts corresponden a la Fase 7.

## 7. Pendientes del proyecto

Revisión de este expediente y de los roles y valoraciones propuestas por el usuario. Después: auditoría logística global, por grupos e interseccional (Fase 2), comparación con árbol (Fase 3), integración, marco legal, mitigación/decisión, reproducibilidad final, PDF y auditoría de rúbrica. No se han ejecutado estas fases ni se han creado métricas para anticiparlas.

## 8. Próximo paso y estado de autorización

La recomendación de LAB11 es **REVIEW**, limitada al ejercicio educativo. Su registro permanece pendiente de aprobación humana y no equivale a la decisión final de la Fase 6.

El siguiente paso será **Fase 2 · LAB12**, después de que el usuario escriba `CONTINUAR`, conforme al flujo del adjunto. Los cambios y evidencias quedan en la rama local de trabajo; no se ha realizado push ni se ha publicado el proyecto en GitHub.
