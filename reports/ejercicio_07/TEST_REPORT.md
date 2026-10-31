# Fase 7 · Informe de pruebas, reproducibilidad y evidencias

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo). **Partes:** 7.1–7.5.

**Estado:** pruebas y reproducción local completadas. **15 pruebas únicas aprobadas:** LAB11 3, LAB12 4, complementarias sin interfaz 7 y AppTest 1. No hay fallos, errores o pruebas omitidas en esos resultados finales. Se conservan los intentos inconclusos y fallidos por separado.

La reproducción usa una copia de 42 archivos de código/entradas y salidas separadas con el mismo entorno y máquina. LAB11 y ambos modelos reproducen los resultados comprobados. Esto acredita reproducción local de esta entrega, sin demostrar validez externa, eficacia de mitigaciones, revisión humana independiente ni autorización de uso real.

## 1. Trabajo realizado y resultados — Parte 7.1

Los cuatro grupos siguientes cubren todos los tests disponibles. El encabezado Comando muestra su núcleo legible; cada JSON conserva el array exacto con intérprete, directorio, `--basetemp`, salida JUnit y opciones adicionales. Todas las pruebas se ejecutaron sobre la copia aislada, incluyendo el código base y el cambio de sintaxis indicado en la sección 2.

| Prueba | Comando | Resultado | Evidencia en `evidencias/fase_07/` | Observaciones |
|---|---|---|---|---|
| LAB11: valoración y privacidad | `python -B -m pytest -q tests/test_impact.py tests/test_privacy.py` | **3 passed in 1.13s** | `reproduction/commands/02_lab11_tests.json`; `reproduction/02_lab11_tests.xml` | Rechazo de placeholder, producto de riesgo y columna name; cobertura concreta, no privacidad integral. |
| LAB12: métricas y predicciones | `python -B -m pytest -q tests/test_fairness.py tests/test_model.py` | **4 passed in 2.95s** | `reproduction/commands/03_lab12_tests.json`; `reproduction/03_lab12_tests.xml` | Dos tests parametrizados para logística/árbol. Acotan recall-gap y salida binaria; no prueban equidad o utilidad real. |
| Datos, preservación LAB11 y gobernanza | `python -B -m pytest -q tests/test_data.py tests/test_lab11_script.py tests/test_governance.py` | **7 passed in 1.38s** | `reproduction/commands/04a_non_ui_tests.json`; `reproduction/04a_non_ui_tests.xml` | Contrato/identificador email; preservación byte a byte, borrador no aprobado, interesado incompleto; gate fallido y RACI sin accountable. |
| Arranque y aviso de aplicación | `python -B -m pytest -q tests/test_app.py` | **1 passed in 4.52s** | `reproduction/commands/04c_app_test_loopback.json`; `reproduction/04c_app_test_loopback.xml` | AppTest sin excepción y advertencia sintética. Ejecutado con conexión local permitida tras bloqueo del bucle de eventos en el entorno predeterminado. |
| Compatibilidad de dependencias | `uv --cache-dir reports/ejercicio_07/evidencias/fase_07/.runtime/uv-cache pip check --python .venv/Scripts/python.exe` | Código 0; **55 paquetes compatibles** | `04_dependency_check_workspace_cache.json` | No instala ni actualiza dependencias. |
| Correspondencia del entorno | `python -B reports/ejercicio_07/evidencias/fase_07/capture_environment.py` | Código 0; 55 distribuciones y once requisitos comprobados; sin versiones discrepantes o paquetes extra respecto al lock. | `05_environment.json`; `environment.json` | Entorno existente; no instalación limpia. |
| Reproducción de LAB11 | `python -B scripts/lab11_impact.py` | Código 0; tres salidas reproducidas byte a byte y registro de decisión conservado. | `reproduction/commands/05_lab11_reproduction.json`; `reproduction/reproduction_result.json` | Salidas en la copia; nueve riesgos y seis interesados, sin aprobación humana. |
| Reproducción logística | `python -B scripts/lab12_audit.py --model logistic`; `python -B scripts/lab12_supporting_evidence.py --model logistic` | Ambos códigos 0; 160 predicciones/probabilidades y métricas iguales; hash del modelo igual. | `reproduction/commands/06_logistic_audit.json`; `07_logistic_support.json` | Ajuste nuevo para reproducción; conserva tiempos nuevos aparte. |
| Reproducción árbol | `python -B scripts/lab12_audit.py --model tree`; `python -B scripts/lab12_supporting_evidence.py --model tree` | Ambos códigos 0; 160 predicciones/probabilidades y métricas iguales; hash del modelo igual. | `reproduction/commands/08_tree_audit.json`; `09_tree_support.json` | Ajuste nuevo para reproducción; no nuevo holdout. |
| Sintaxis del código | `python -B reports/ejercicio_07/evidencias/fase_07/check_syntax.py` | Código 0; 46 archivos sin errores de sintaxis en el cierre. | `14_syntax_final.json`; `syntax_result.json`; `03_initial_syntax.json` | `ast.parse`, sin ejecutar las plantillas ni generar bytecode. |
| Estilo y verificación del expediente | Ruff y `verify_phase.py` de esta fase | Ruff código 0 tras corregir el alias UTC; verificación de cierre en su registro. | `11_style_check.json`; `13_style_final.json`; `15_phase_verification.json`; `verification.json` | Verifican código modificado/nuevo, vínculos e integridad; no aceptación ética. |

Son quince tests únicos finales, no una suma de todos los intentos ni de pruebas de fases anteriores. Al reanudar se reutilizaron los resultados aprobados cuya copia de fuentes permaneció idéntica; no se repitieron LAB11/LAB12 sin necesidad. La primera ejecución complementaria inconclusa no se suma como prueba aprobada.

## 2. Archivos modificados

El único archivo anterior modificado en esta fase es `scripts/simulate_incident.py`. Su cadena `f"...` abarcaba varias líneas y no era sintácticamente válida. Se delimitó con triple comilla y se separaron las operaciones de escritura en líneas legibles. El control de estilo pidió utilizar el alias UTC en lugar de timezone.utc; se aplicó esa sustitución equivalente. Se conservan sus campos `REPLACE`; no se completó ni ejecutó la plantilla LAB13.

El original está en `evidencias/fase_07/simulate_incident_original.py.txt`, vinculado al hash inicial. Se preservan los otros **184 archivos anteriores**, incluidos los modelos canónicos y todos los informes de Fases 0–6. La corrección de sintaxis no genera un incidente real, no ejecuta LAB13 y no cambia la recomendación de limitar el sistema.

## 3. Archivos generados — Partes 7.3–7.4

- Este informe y [AI_USAGE_DECLARATION.md](AI_USAGE_DECLARATION.md).
- [PROMPTS_RELEVANTES.md](PROMPTS_RELEVANTES.md), copia del adjunto y procedencia/hash.
- `evidencias/fase_07/`: estado inicial, entorno, registrador, scripts de sintaxis/reproducción/verificación, logs y manifiesto.
- `evidencias/fase_07/reproduction/`: manifiesto de la copia, comandos con salidas, cuatro JUnit XML, resultado estructurado y salidas LAB11/LAB12 reproducidas.
- `.runtime/`: copia de trabajo, caché y nuevos modelos disponibles localmente y excluidos de Git por el ignore de esta fase. Las salidas tabulares, metadatos y hashes relevantes sí se conservan como evidencia editable.

La declaración distingue aportación humana, redacción/correcciones asistidas y hechos realmente comprobados. La autorización de esta fase no se registra como aprobación de recomendaciones o aceptación del riesgo.

## 4. Reproducibilidad — Parte 7.2

### 4.1. Entorno y parámetros

El entorno comprobado usa **Python 3.12.13**, **uv 0.11.22**, scikit-learn 1.9.1, Fairlearn 0.12.0, pandas 2.3.3, NumPy 2.5.3, SciPy 1.18.1, joblib 1.6.0, pytest 8.4.2, Ruff 0.16.8 y Streamlit 1.64.0. `environment.json` conserva la lista completa, plataforma, ejecutable, Git y hash de `uv.lock`. El proyecto exige Python >=3.12,<3.13 y el lock ==3.12.*.

Los modelos comparten cinco predictores, transformados en once columnas. Se excluyen case_id, received_date, protected_group y target de los predictores. Se ordenan fechas antes del corte temporal 480/160. One-hot encoding y StandardScaler se ajustan con entrenamiento; los metadatos reproducidos comprueban categorías y estadísticas de train.

Parámetros explícitos: ambos estimadores usan `class_weight="balanced"` y `random_state=42`; logística `max_iter=1200`, solver lbfgs, C=1.0 y tol=0.0001; árbol `max_depth=5`, criterio gini, `min_samples_split=2` y `min_samples_leaf=1`. Los metadatos guardan los valores efectivos. El generador/semilla del dataset sigue sin evidencia completa; la semilla del estimador no lo sustituye.

El archivo contiene 640 casos sintéticos. Las fechas del test son 25-09-2026 a 27-12-2026; las posteriores a la fecha de este trabajo forman parte de la simulación y no son observaciones reales del futuro. Los ocho estratos interseccionales tienen n=8–35 y siete n<30. La reproducción no añade personas, muestras independientes o validación externa.

### 4.2. Entradas y correspondencia de resultados

`reproduction/source_manifest.json` registra los 42 archivos copiados y sus hashes. Se comprobó que los módulos importados procedían de esa copia; se reutilizó el mismo intérprete instalado y no se creó un entorno limpio. Los inputs principales son dataset, YAML/CSV de student_inputs, configuración, código, lock y el registro LAB11 existente. La copia precede al ajuste final de estilo UTC en la plantilla de incidente no ejecutada: esa es la única diferencia posterior con los archivos copiados. Se conservó el snapshot y se verificó que todo el código ejecutado y los tests permanecen idénticos.

El hash del dataset permanece `2af1858fe874f3914b0f9bfe068fd876cb716186694a6ece9a16e8c929128a01`.

| Resultado | Correspondencia observada |
|---|---|
| LAB11 | risk_register_scored.csv, stakeholders.csv y rmf_summary.json idénticos en bytes; DECISION_RECORD.md preservado. |
| Logística | 160 predicciones binarias iguales; diferencia absoluta máxima de probabilidades 0.0 con tolerancia prevista 1e-12; métricas/gaps iguales. Modelo SHA-256 `9fc217d3fed0cfb74093c95d40012c386c0e1172e71d0f30f594cd2da177eb2a`, igual al canónico. |
| Árbol | 160 predicciones binarias iguales; diferencia absoluta máxima de probabilidades 0.0 con tolerancia prevista 1e-12; métricas/gaps iguales. Modelo SHA-256 `e778bdfdbd0c2f02f14ac869046cab6dad79f54e6aac1c7c44e3a925fc611a87`, igual al canónico. |
| Soportes y corte | Tablas por grupo/intersección, audit_support y gap_analysis iguales en bytes para ambos modelos; dataset_profile y temporal_split también coinciden. |
| Recursos | Tiempos de ajuste nuevos: logística 0.0649023 s y árbol 0.0494662 s. Se conservan junto a los originales, sin sustituirlos. No son un nuevo benchmark controlado ni mediciones de energía. |

Las auditorías de reproducción realizan dos ajustes nuevos. Las pruebas de modelos y de aplicación también entrenan; su número de llamadas a fit no se instrumentó. AppTest escribe `models/model.joblib` únicamente en la copia y calcula la bandera técnica del pipeline. Se trata de verificación de software: no se aprueba despliegue, operación institucional ni decisión sobre personas. El CLI de LAB13 y la plantilla de incidente no se ejecutaron.

### 4.3. Repetir en otra copia

Los commits de la entrega son locales: el enlace remoto por sí solo no acredita que estos cambios estén publicados. Los pasos siguientes requieren una copia entregada con el código, inputs, resultados canónicos de referencia e historial Git; para instalar dependencias se necesita acceso a los paquetes o una caché adecuada. La instalación limpia siguiente es una receta, no una operación realizada en Fase 7:

```powershell
uv sync --frozen
```

Después, desde la raíz de esa copia, elegir una etiqueta nueva para conservar los resultados previos:

```powershell
.\.venv\Scripts\python.exe -B reports\ejercicio_07\evidencias\fase_07\reproduce.py --run-id revision_02
```

La ejecución crea nuevas rutas de trabajo y evidencia para esa etiqueta. El script comprueba que la ruta quede dentro del proyecto y evita sobrescribir una ejecución previa. Si se reanuda una ejecución inconclusa, `--resume-existing --run-id revision_02` verifica las fuentes y reutiliza solo comandos aprobados idénticos. Un comando fallido conservado requiere otra etiqueta para repetirlo sin sustituir su registro. Una prueba de interfaz necesita que el entorno permita la conexión local usada por asyncio/Streamlit; una restricción debe registrarse como tal y no contarse como éxito.

La receta fue implementada para la reproducción Windows local documentada. La coincidencia binaria observada no garantiza bytes, tiempos o comportamiento idénticos en otras plataformas, versiones o máquinas. La distribución de entradas/salidas y la correspondencia semántica deben revisarse ante esas diferencias.

## 5. Problemas, intentos fallidos y correcciones

1. **uv y temporales:** `01_dependency_check.json` terminó con código 2 por acceso denegado al persistir una consulta del intérprete en un temporal. La caché dentro del workspace permitió `04_dependency_check_workspace_cache.json`, código 0, sin instalar paquetes ni pedir acceso global a la caché.
2. **Sintaxis original:** `03_initial_syntax.json` identificó una cadena sin terminar en simulate_incident.py, entre 44 archivos entonces presentes. El original y `syntax_result_initial.json` se conservaron; la revisión final cubre también los scripts nuevos de esta fase. No se ejecutó la plantilla para probar la corrección.
3. **Complementarias inconclusas:** la primera ejecución se interrumpió manualmente al quedar sin terminar; `06_interruption_record.json` conserva ese hecho. Las siete complementarias sin interfaz se ejecutaron separadas y pasaron. Los resultados ya aprobados de LAB11/LAB12 se conservaron.
4. **AppTest y bucle local:** el intento `reproduction/commands/04b_app_test.json` fue detenido por el padre tras 45 s, código 124. La traza sitúa la espera en socketpair/accept al crear el bucle de eventos, antes de correr la app. Tras autorización de ejecución fuera del aislamiento de red predeterminado, `08_app_test_with_loopback.json` y el hijo 04c registran el test aprobado. El intento fallido sigue en `07_reproduction_resume.json`.
5. **Estilo del simulador:** `11_style_check.json` registró UP017 por timezone.utc. `13_style_final.json` corrigió el alias a UTC y terminó con código 0. La plantilla se comprobó por sintaxis sin ejecución; no se repiten pruebas de modelos por ese cambio no usado en ellas.

No se modificaron las pruebas para omitir la interfaz ni se redujeron las comprobaciones que fallaban. La recuperación cambió el contexto de ejecución del test local y añadió límite de tiempo y registros al orquestador. Persisten las limitaciones de datos, mitigación y aprobación descritas en [DECISION_FINAL.md](DECISION_FINAL.md).

## 6. Evidencias y alcance de las verificaciones

El resultado agregado está en `evidencias/fase_07/reproduction/reproduction_result.json`; los JUnit permiten contar pruebas sin sumar reintentos. Los JSON de comandos conservan stdout/stderr y tiempo UTC. `verification.json` verifica cobertura, fuentes, salidas, declaración/prompts y conservación de archivos. El manifiesto final registra los bytes del árbol de trabajo e incluye los dos modelos canónicos locales ignorados; excluye su propio archivo y el scratch `.runtime/`.

Los verificadores de fases anteriores registran restricciones del momento en que se ejecutaron. Por ejemplo, la ausencia de DECISION_FINAL en una fase previa era una condición histórica; no deben confundirse esos snapshots con una obligación de borrar entregables posteriores. El cierre actual se contrasta con el estado inicial de Fase 7 y el cambio de sintaxis expresamente documentado.

La copia íntegra del prompt conserva espacios finales de Markdown del original. El primer control de blancos de Git los señaló; se preservó el contenido y su hash y se excluyó únicamente esa referencia de dicho control. Las dos copias originales de evidencia se marcan con `-text` en el .gitattributes local para conservar sus bytes en Git. Esta excepción no afecta a las comprobaciones de código, sintaxis o estilo.

## 7. Pendientes

Quedan la revisión y aprobación del usuario, síntesis PDF/editables en Fase 8 y auditoría final de rúbrica en Fase 9. No se completó una instalación limpia, una reproducción en otra máquina o una revisión independiente por otra persona. La eficacia de mitigaciones, consulta a afectados, autoridad operativa y validación real siguen sin acreditarse; estas pruebas no resuelven esos vacíos.

## 8. Próximo paso

**Fase 8: expediente final de síntesis**, después de autorización conforme al plan acordado. Esta fase entrega pruebas y declaración de IA y conserva la recomendación académica limitada, pendiente de aprobación. No genera todavía el PDF ni publica cambios en GitHub.
