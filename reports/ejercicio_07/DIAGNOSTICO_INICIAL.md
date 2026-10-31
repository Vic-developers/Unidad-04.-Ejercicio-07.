# Ejercicio 07 · Diagnóstico inicial

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo).  
**Fase:** 0 · Recepción, inspección y diagnóstico, partes 0.1–0.4.  
**Estado:** diagnóstico completado; desarrollo de LAB11 y LAB12 pendiente.  
**Repositorio indicado:** [Vic-developers/Unidad-04.-Ejercicio-07.](https://github.com/Vic-developers/Unidad-04.-Ejercicio-07.).

## 1. Alcance y procedencia de los requisitos

Se inspeccionaron los materiales entregados y se preparó este diagnóstico. Los requisitos de fases, entregables y rúbrica se toman del texto adjunto «PROMPT MAESTRO PARA OPENCODE». Ese texto es material de trabajo aportado; no constituye por sí mismo una consigna original del docente ni evidencia de haber ejecutado actividades. No se recibió una consigna docente independiente con la que contrastar su transcripción.

Se examinó el código sin importarlo ni ejecutar los laboratorios. Se generaron únicamente archivos nuevos de diagnóstico en el clon local. La base de Descargas conserva sus archivos originales. No se completaron formularios, no se entrenaron modelos, no se ejecutó pytest, no se produjo el PDF y no se realizaron commits ni push.

## 2. Materiales recibidos y acceso

| Material | Ubicación o identificación | Resultado |
|---|---|---|
| URL de GitHub | `https://github.com/Vic-developers/Unidad-04.-Ejercicio-07..git` | Accesible mediante Git; no devuelve referencias. La clonación terminó correctamente e informó un repositorio vacío. |
| Texto adjunto | `C:/Users/reyti/.codex/attachments/fc6675f6-da6a-4a4e-a69d-565c850eb06f/Texto pegado.txt` | Leído; contiene el plan por fases y los requisitos propuestos del Ejercicio 07. |
| Carpeta entregada | `C:/Users/reyti/Downloads/INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv/` | Contiene otra carpeta con el mismo nombre; la raíz real del proyecto es la carpeta interior. |
| Raíz real de la base | `C:/Users/reyti/Downloads/INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv/INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv/` | 42 archivos; sin directorio `.git` ni entorno `.venv`. |
| Clon de trabajo | `C:/Users/reyti/OneDrive/Documentos/ChatGPT/Tareas/Unidad-04.-Ejercicio-07/` | Se creó una carpeta nueva con el remoto indicado; contiene los archivos nuevos de esta fase. La base docente todavía no se ha incorporado al clon. |

Los intentos iniciales de acceso web no permitieron leer la página. La verificación efectiva del remoto se realizó mediante `git ls-remote` y `git clone`. El primer intento de Git dentro del entorno restringido falló por resolución de red; el acceso de lectura autorizado fuera de esa restricción terminó correctamente. No debe confundirse ese fallo inicial con un repositorio inexistente.

### Materiales que faltan o deberán confirmarse

- Consigna original, instrucciones de LAB11/LAB12 y rúbrica del docente, si existen como documentos separados. Su ausencia limita la verificación académica frente a la fuente original, pero no impide este diagnóstico.
- No se recibieron informes previos, métricas, modelos entrenados ni evidencias de ejecución.
- No se identificó una jurisdicción aplicable a un despliegue real. La mención de República Dominicana en la ficha aclara que los datos no son estadísticas dominicanas; no determina obligaciones legales. Se deberá confirmar el contexto en la Fase 5.
- Responsable real, datos académicos de portada y aprobación de decisiones deberán confirmarse cuando corresponda. El código permite describir un caso educativo; no acredita un propietario institucional real.

## 3. Estructura encontrada en la base local

```text
INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
├── app.py
├── configs/
│   └── governance.yml
├── data/
│   └── territorial_risk_synthetic.csv
├── docs/
│   ├── AI_USE_DECLARATION.md
│   ├── DATASET_CARD.md
│   ├── MODEL_CARD.md
│   └── RUNBOOK.md
├── models/
│   └── .gitkeep
├── reports/
│   ├── lab11/.gitkeep
│   ├── lab12/.gitkeep
│   └── lab13/.gitkeep
├── scripts/
│   ├── check_environment.py
│   ├── describe_dataset.py
│   ├── lab11_impact.py
│   ├── lab12_audit.py
│   ├── lab13_governance.py
│   ├── simulate_incident.py
│   └── validate_lab12_decision.py
├── src/inf8239_u04/
│   ├── __init__.py
│   ├── data.py
│   ├── fairness.py
│   ├── governance.py
│   ├── impact.py
│   ├── model.py
│   └── pipeline.py
├── student_inputs/
│   ├── lab11_impact.yml
│   ├── lab12_decision.yml
│   ├── raci.csv
│   ├── risk_register.csv
│   └── stakeholders.csv
└── tests/
    ├── test_app.py
    ├── test_data.py
    ├── test_fairness.py
    ├── test_governance.py
    ├── test_impact.py
    ├── test_model.py
    └── test_privacy.py
```

No se encontraron archivos `AGENTS.md` aplicables en las rutas revisadas ni dentro de la base. El inventario completo con tamaños y hashes está en `evidencias/fase_00/diagnostico_estatico.json`.

## 4. Sistema identificado

`configs/governance.yml` denomina el sistema **Territorial Review DSS - Synthetic** y define su propósito como priorizar casos sintéticos para revisión humana. Prohíbe intervención automática, decisiones de elegibilidad y declaraciones de emergencia. El README y la aplicación limitan el sistema a una demostración educativa.

`src/inf8239_u04/model.py` implementa regresión logística y árbol de decisión. Ambos utilizan un pipeline de transformación de variables; los estimadores fijan `random_state=42` y `class_weight="balanced"`. El árbol limita su profundidad a 5 y la regresión logística fija 1200 iteraciones máximas. Estos parámetros se observaron en el código; no constituyen resultados de un entrenamiento realizado.

No se ha identificado una definición operacional detallada de la etiqueta `target`, ni una entidad territorial real, ni una finalidad de despliegue real. La documentación posterior deberá respetar ese carácter sintético y distinguir los roles propuestos de personas o instituciones existentes.

## 5. Estado de LAB11

| Archivo o salida | Estado observado | Trabajo pendiente |
|---|---|---|
| `student_inputs/lab11_impact.yml` | Existen las 9 claves, todas con `REPLACE`. | Documentar finalidad, decisión asistida, usuarios, afectados, responsable, alternativa, usos excluidos, retirada y apelación. |
| `student_inputs/stakeholders.csv` | 4 filas de roles; beneficios, daños y participación pendientes. | Justificar interesados e incorporar intereses de forma compatible con el esquema. |
| `student_inputs/risk_register.csv` | 8 filas de ejemplo con escenarios y controles pendientes. | Sustentar cada riesgo; revisar puntuaciones y riesgo residual, sin tratar los valores de plantilla como una valoración aprobada. |
| `scripts/lab11_impact.py` | Error de sintaxis en la línea 11: cadena sin terminar. | Corregir al iniciar la Fase 1 y validar de nuevo. |
| `src/inf8239_u04/impact.py` | Valida campos y calcula `likelihood_1_4 * impact_1_4`. | Ejecutar con entradas completas y revisar la coherencia de las puntuaciones. |
| `tests/test_impact.py`, `tests/test_privacy.py` | Existen 3 pruebas en total, identificadas por análisis del código. | Ejecutarlas en el entorno del proyecto durante la Fase 1. |
| `reports/lab11/` | Solo `.gitkeep`. | Generar resultados y registro de decisión sustentado. |

**Salidas ausentes:** `risk_register_scored.csv`, `rmf_summary.json`, `stakeholders.csv` y `DECISION_RECORD.md` dentro de `reports/lab11/`. Su ausencia corresponde al estado inicial; los `.gitkeep` son marcadores de carpeta y no evidencias de laboratorio.

### Precauciones técnicas para la Fase 1

1. La cadena de las líneas 11–14 impide ejecutar el script antes incluso de validar las entradas.
2. Una vez corregida la sintaxis, el script escribirá `DECISION_RECORD.md` incondicionalmente con una plantilla. Debe evitarse que una segunda ejecución sobrescriba un registro ya completado.
3. `rmf_summary.json` contiene etiquetas generales para GOVERN, MAP, MEASURE y MANAGE. No genera una relación por riesgo, control, responsable y evidencia. Esa trazabilidad tendrá que documentarse de forma explícita, diferenciando acciones realizadas de propuestas.
4. El CSV de interesados no tiene una columna independiente de intereses y el registro de riesgos no tiene una columna NIST. Conviene conservar los encabezados originales y completar la explicación y el mapeo en los documentos correspondientes.
5. Las pruebas actuales no acreditan que los archivos reales del estudiante estén completos: prueban funciones con ejemplos. También será necesario ejecutar el laboratorio y revisar sus artefactos.

**Conclusión LAB11:** base disponible, formularios pendientes y ejecución bloqueada por un defecto de sintaxis confirmado. No se ha efectuado ninguna evaluación de impacto.

## 6. Estado de LAB12

| Componente | Estado observado |
|---|---|
| Dataset | Presente: 640 registros y 9 columnas; 640 identificadores únicos; ningún campo vacío en la lectura CSV. No equivale a una validación exhaustiva de calidad. |
| Grupos | `G1`: 396; `G2`: 244. Las etiquetas no identifican grupos demográficos reales documentados. |
| Objetivo | `target=0`: 287; `target=1`: 353. |
| División temporal | La configuración por defecto separa 480 filas de entrenamiento y 160 de prueba tras ordenar por fecha; último día de entrenamiento 2026-09-24, primero de prueba 2026-09-25; sin fechas compartidas. |
| Predictores | `zone`, `age_band`, `previous_incidents`, `infrastructure_score`, `exposure`. |
| Exclusiones observadas | `case_id`, `received_date`, `protected_group` y `target` no son predictores. |
| Auditoría | Métricas implementadas: count, accuracy, selection rate, recall, precision y FPR. La intersección usa `protected_group` y `age_band`. |
| `scripts/lab12_audit.py` | Analiza correctamente con `ast.parse`; su ejecución y dependencias todavía no han sido verificadas. |
| `student_inputs/lab12_decision.yml` | 6 campos con `REPLACE`. |
| Resultados y modelos | No existen; `reports/lab12/` y `models/` contienen solo sus marcadores. |

**Advertencia:** el dataset es sintético. No representa personas, territorios ni tasas reales. Su intervalo de fechas llega a 2026-12-27 y forma parte de la simulación; no acredita observaciones reales futuras.

### Diferencias de rutas respecto del texto adjunto

El script guarda los resultados en subcarpetas por modelo, no directamente en `reports/lab12/`:

```text
reports/lab12/logistic/global_metrics.json
reports/lab12/logistic/fairness_by_group.csv
reports/lab12/logistic/fairness_intersectional.csv
reports/lab12/tree/global_metrics.json
reports/lab12/tree/fairness_by_group.csv
reports/lab12/tree/fairness_intersectional.csv
models/logistic.joblib
models/tree.joblib
```

Estas son rutas esperadas derivadas del código; los archivos todavía no se han generado. `global_metrics.json` utiliza las claves `metrics`, `differences` y `resources`. Las diferencias y los resultados interseccionales deben interpretarse con sus soportes y denominadores; una disparidad no demuestra por sí misma discriminación causal.

### Puntos que requieren revisión posterior

- `protected_group` se reserva a la auditoría, como exige el texto adjunto. `age_band`, también declarado sensible en la configuración, sí es predictor. Se deberá justificar su uso y revisar posibles efectos de variables relacionadas con los grupos.
- Las métricas de grupo incluyen tamaño total, pero no una tabla explícita de positivos y negativos por subgrupo. La interpretación de recall/FPR e incertidumbre necesitará esos denominadores.
- Los tests de equidad comprueban límites y presencia de grupos; no establecen que el sistema cumpla criterios de aceptación ni prueban equidad interseccional.
- `scripts/validate_lab12_decision.py` es independiente y no se invoca desde el script de auditoría. Se deberá ejecutar por separado tras completar el YAML.
- El código usa el mismo procedimiento temporal y semillas para comparar modelos. No se entrenó ninguno para este diagnóstico.
- El tiempo de entrenamiento y tamaño serializado están implementados como medidas de recursos. No se mide energía ni emisiones de carbono.
- La ficha menciona una semilla educativa fija para generar los datos, pero no incluye su valor ni un generador. El CSV recibido se puede preservar mediante su hash; no se ha demostrado cómo regenerarlo desde cero.

**SHA-256 del dataset recibido:** `2af1858fe874f3914b0f9bfe068fd876cb716186694a6ece9a16e8c929128a01`.

**Conclusión LAB12:** implementación y datos disponibles; auditorías, comparación y decisión pendientes. No hay métricas de modelos que puedan informarse como resultados obtenidos.

## 7. Dependencias y entorno

El proyecto exige Python `>=3.12,<3.13`, `.python-version` indica `3.12` y `uv.lock` declara `==3.12.*`. Se confirmó que **Python 3.12.13 ya está instalado**. El comando genérico `python` apunta a Python 3.13.5, por lo que no debe usarse para ejecutar el proyecto fuera de su entorno sin seleccionar el intérprete correcto.

No existe `.venv` en la base. La consulta del intérprete 3.12 usado para la inspección no encontró pandas, numpy, sklearn, fairlearn, yaml, joblib, streamlit ni pytest en ese intérprete. Esto describe su disponibilidad actual; no es un fallo de instalación, pues todavía no se ha ejecutado la sincronización.

| Dependencia | Rango de `pyproject.toml` | Versión registrada en `uv.lock` |
|---|---|---|
| fairlearn | `>=0.12,<0.13` | 0.12.0 |
| joblib | `>=1.5,<2` | 1.6.0 |
| numpy | `>=2.0,<3` | 2.5.3 |
| pandas | `>=2.2,<3` | 2.3.3 |
| plotly | `>=6,<7` | 6.9.0 |
| pyyaml | `>=6,<7` | 6.0.3 |
| scikit-learn | `>=1.7,<2` | 1.9.1 |
| streamlit | `>=1.49,<2` | 1.64.0 |
| pytest (dev) | `>=8.4,<9` | 8.4.2 |
| pytest-cov (dev) | `>=6,<7` | 6.3.0 |
| ruff (dev) | `>=0.13,<1` | 0.16.8 |

El backend de construcción es `hatchling`. Ambos archivos TOML pudieron analizarse; no se verificó todavía la descarga ni instalación de las dependencias bloqueadas. Herramientas observadas: uv 0.11.22, Git 2.49.0.windows.1 y GitHub CLI 2.97.0.

Los intentos de inventariar Python desde el entorno restringido fallaron al persistir archivos de caché de uv. La consulta local autorizada fuera de esa restricción terminó con código 0 y confirmó los intérpretes instalados. No se instaló software para este diagnóstico.

## 8. Pruebas disponibles y verificaciones realizadas

### Inventario estático de pruebas, sin ejecución de pytest

| Archivo | Cantidad | Lo que comprueba su código |
|---|---:|---|
| `tests/test_impact.py` | 2 | Puntuación de un riesgo de ejemplo y rechazo de un placeholder. |
| `tests/test_privacy.py` | 1 | Rechazo de una columna de identificador directo. |
| `tests/test_fairness.py` | 1 | Rango del gap de recall y etiquetas de grupo presentes. |
| `tests/test_model.py` | 1 | Predicciones binarias de un modelo. |
| `tests/test_data.py` | 2 | Tamaño/identificadores y rechazo de email. |
| `tests/test_governance.py` | 2 | Puerta fallida exige revisión y validación de RACI. |
| `tests/test_app.py` | 1 | Inicio de Streamlit y aviso de datos sintéticos. |
| **Total** | **10** | **Identificadas; no ejecutadas.** |

### Comprobaciones efectivamente realizadas

| Comprobación | Comando o procedimiento | Resultado real |
|---|---|---|
| Referencias de GitHub | `git ls-remote https://github.com/Vic-developers/Unidad-04.-Ejercicio-07..git` | Código 0; salida vacía, sin referencias. |
| Clonación | `git clone -- <URL indicada> <carpeta nueva de trabajo>` | Código 0; advertencia de repositorio vacío. |
| Estado Git local | `git status --short --branch`, `git remote -v`, `git show-ref`, `git ls-files` | Rama local inicial `main`, sin commits ni archivos versionados; remoto correcto; sin referencias. `git show-ref` devuelve 1 al no existir referencias. |
| Inventario de Python | `uv --no-cache python list --only-installed --offline` | Código 0 fuera de la restricción de caché; Python 3.12.13 disponible. |
| Análisis estático reproducible | Script de diagnóstico adjunto ejecutado con Python 3.12.13 | 42 archivos inventariados, 22 Python analizados, 2 errores de sintaxis y 10 pruebas identificadas. |
| Revisión CSV y TOML | Biblioteca estándar: csv, tomllib, hashlib y ast | Dimensiones, conteos, partición temporal, hashes y metadatos obtenidos sin entrenar modelos. |
| Integridad de la base | Comparación con los 42 hashes recogidos antes de generar el diagnóstico | Resultado documentado en `evidencias/fase_00/integridad_fuente.json`. |

El análisis estático terminó con código 0 porque completó la inspección y generó el JSON. Ese código **no significa que el proyecto pase sus pruebas**: el JSON registra expresamente dos errores y `pytest_executed: false`.

### Reproducir la inspección

Desde la raíz del clon local, en PowerShell:

```powershell
& 'C:\Users\reyti\AppData\Roaming\uv\python\cpython-3.12.13-windows-x86_64-none\python.exe' -B `
  'reports\ejercicio_07\evidencias\fase_00\diagnostico_estatico.py' `
  'C:\Users\reyti\Downloads\INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv\INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv' `
  --output 'reports\ejercicio_07\evidencias\fase_00\diagnostico_estatico.json'
```

El script solo lee la base indicada y escribe el JSON de salida. No importa el paquete docente, no completa YAML/CSV y no ejecuta pruebas ni modelos. Las rutas locales deberán adaptarse en otro equipo.

## 9. Problemas y riesgos técnicos priorizados

| ID | Hallazgo y evidencia | Consecuencia | Acción propuesta |
|---|---|---|---|
| D01 | GitHub sin referencias; clon vacío. | El enlace aún no contiene el proyecto ni sus evidencias. | Incorporar la base al clon al iniciar el desarrollo; publicar únicamente cuando se autorice. |
| D02 | `scripts/lab11_impact.py:11` no analiza sintácticamente. | LAB11 no puede ejecutarse. | Corrección mínima en Fase 1 y nueva verificación. |
| D03 | 9 claves de impacto, 6 de decisión y filas CSV incompletas. | No existen evaluaciones o decisiones sustentadas. | Completar cada artefacto en su fase. |
| D04 | No hay `.venv`; el Python genérico es 3.13.5. | Ejecución con dependencias ausentes o intérprete incompatible. | Usar Python 3.12 y `uv sync --frozen` en el clon cuando se incorpore la base. |
| D05 | Escritura incondicional de `DECISION_RECORD.md`. | Riesgo de perder el texto completado al repetir LAB11. | Proteger un registro existente antes de generar resultados definitivos. |
| D06 | Rutas de salida de LAB12 diferentes de las propuestas en el adjunto. | Referencias rotas o resultados de modelos mezclados. | Conservar `reports/lab12/logistic/` y `reports/lab12/tree/`. |
| D07 | Resumen NIST genérico y pruebas de alcance limitado. | Un test aprobado podría confundirse con cumplimiento académico o equidad. | Revisar artefactos reales y añadir trazabilidad documental e interpretación. |
| D08 | `age_band` sensible y predictor; faltan denominadores explícitos en las tablas. | Conclusiones de equidad insuficientemente justificadas. | Examinar diseño, soporte e incertidumbre en Fase 2. |
| D09 | Falta consigna original y jurisdicción concreta. | No puede afirmarse cumplimiento íntegro del docente ni legislación aplicable. | Contrastar la fuente original y confirmar jurisdicción cuando corresponda. |
| D10 | `scripts/simulate_incident.py:3` contiene una f-string sin terminar. | La simulación de incidentes de LAB13 no puede ejecutarse. | Registrar el defecto; LAB13 está fuera del alcance principal de este ejercicio y no se corrige en Fase 0. |

`docs/MODEL_CARD.md`, `docs/RUNBOOK.md` y `docs/AI_USE_DECLARATION.md` son plantillas con `REPLACE`. Las dos primeras se identifican con LAB13; se documentan como contexto sin ampliar el alcance actual. La declaración de IA del Ejercicio 07 sí será necesaria y deberá reflejar verificaciones realmente efectuadas.

## 10. Plan de trabajo propuesto

Cada fase producirá sus evidencias y se cerrará con un informe antes de pasar a la siguiente, conforme al flujo descrito en el adjunto.

| Fase | Trabajo y validación previstos | Entregable principal |
|---|---|---|
| 0 | Recepción, acceso, revisión estática y diagnóstico. | Este documento y evidencias de inspección. |
| 1 | Incorporar la base preservando rutas; preparar Python 3.12 con `uv sync --frozen`; corregir el bloqueo de LAB11 y proteger el registro de decisión; completar impacto, interesados y riesgos. Ejecutar LAB11 y `uv run pytest -q tests/test_impact.py tests/test_privacy.py`. | Artefactos LAB11 y `FASE_01_LAB11.md`. |
| 2 | Examinar calidad, temporalidad y predictores; ejecutar auditoría logística; revisar grupos e intersecciones; completar y validar el YAML de decisión. Ejecutar `uv run pytest -q tests/test_fairness.py tests/test_model.py` y las verificaciones de datos pertinentes. | Resultados bajo `reports/lab12/logistic/` y `FASE_02_LAB12.md`. |
| 3 | Auditar árbol bajo las mismas condiciones; comparar utilidad, brechas, interpretación, tiempo y tamaño medidos. | `COMPARACION_MODELOS.md`. |
| 4 | Relacionar riesgos, grupos, hallazgos, controles y riesgo residual mediante una matriz de trazabilidad. | `EVALUACION_INTEGRADA.md`. |
| 5 | Confirmar jurisdicción; consultar fuentes oficiales vigentes; separar obligaciones, marcos voluntarios y recomendaciones. | `MARCO_LEGAL_VOLUNTARIO_ETICO.md`. |
| 6 | Formular mitigaciones y comparar desplegar, modificar, limitar o no usar; recomendación técnica pendiente de aprobación. Los datos sintéticos no respaldan despliegue real. | `DECISION_FINAL.md`. |
| 7 | Verificar reproducibilidad, pruebas y evidencias; declarar asistencia de IA, prompts y correcciones reales. | `TEST_REPORT.md` y `AI_USAGE_DECLARATION.md`. |
| 8 | Integrar los resultados aprobados en una síntesis PDF, con editables y revisión visual. | `Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad.pdf`. |
| 9 | Contrastar expediente, artefactos, enlaces y rúbrica; corregir deficiencias dentro del alcance aprobado. | `AUDITORIA_FINAL.md`. |

## 11. Control provisional de la rúbrica aportada

| Criterio | Puntuación máxima indicada | Estado a la recepción |
|---|---:|---|
| Finalidad, interesados y proporcionalidad | 0.75 | Pendiente; formularios sin completar. |
| Registro de riesgos y NIST AI RMF | 1.00 | Pendiente; ocho filas de plantilla, sin evaluación sustentada. |
| Auditoría global, por grupos e interseccional | 1.25 | Pendiente; no hay resultados ejecutados. |
| Mitigación, trade-offs y decisión final | 1.25 | Pendiente; no existen comparación ni decisión. |
| Pruebas, referencias y declaración de IA | 0.75 | Hay código de pruebas; ejecución, referencias finales y declaración pendientes. |
| **Total máximo indicado** | **5.00** | **No se asigna nota; falta evidencia para evaluar los criterios.** |

## 12. Archivos nuevos, evidencias y cierre

- `reports/ejercicio_07/DIAGNOSTICO_INICIAL.md`: diagnóstico, discrepancias y plan.
- `reports/ejercicio_07/evidencias/fase_00/diagnostico_estatico.py`: procedimiento reproducible de inspección.
- `reports/ejercicio_07/evidencias/fase_00/diagnostico_estatico.json`: inventario de 42 archivos con hashes, hallazgos sintácticos y comprobaciones básicas de datos y metadatos.
- `reports/ejercicio_07/evidencias/fase_00/acceso_y_entorno.json`: salidas reales de consultas del remoto y de intérpretes locales.
- `reports/ejercicio_07/evidencias/fase_00/integridad_fuente.json`: comparación de hashes de los materiales originales.
- `reports/ejercicio_07/evidencias/fase_00/estado_git.txt`: estado local y remoto tras generar el diagnóstico.

La asistencia de IA en esta fase consistió en inspeccionar materiales, preparar el procedimiento estático y redactar el diagnóstico. No se han recibido correcciones ni una revisión humana de sus conclusiones; la declaración integrada se elaborará en su fase correspondiente.

**Criterio de cierre de Fase 0:** materiales identificados, repositorio comprobado, LAB11/LAB12 inspeccionados, problemas documentados y plan definido. El diagnóstico está completado; el proyecto aún requiere desarrollo y validación.

**Siguiente fase propuesta:** Fase 1 · LAB11.  
**Estado de avance:** en espera de `CONTINUAR`, según la secuencia del texto adjunto.
