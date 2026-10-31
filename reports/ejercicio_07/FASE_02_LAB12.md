# Informe de avance · Fase 2 · LAB12

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo).

**Partes completadas:** 2.1–2.8: dataset, metodología, regresión logística, grupos, intersecciones, pruebas, decisión y artefactos.

**Estado técnico:** completada. Recomendación y prioridades normativas pendientes de aprobación del usuario.

**Advertencia:** el dataset es sintético. No representa personas, territorios ni tasas reales. Las diferencias observadas no acreditan discriminación causal ni autorizan un despliegue real.

## 1. Trabajo realizado y resultados

Se ejecutó la auditoría original de regresión logística sin cambiar su código, el pipeline, la semilla, el dataset ni las condiciones de entrenamiento. Un script complementario documenta calidad, partición temporal, predicciones, matrices de confusión, denominadores e incertidumbre y comprueba su concordancia con los resultados originales. Este complemento reutiliza el modelo guardado; no vuelve a entrenarlo.

### 1.1. Naturaleza, variables y calidad del dataset

El CSV contiene **640 filas, 9 columnas y 640 identificadores únicos**. La documentación docente describe una generación sintética con semilla educativa fija, pero no aporta el generador, el valor de esa semilla ni una definición operacional detallada de la etiqueta. La semilla 42 observada en el modelo no debe confundirse con la semilla desconocida de generación de datos.

| Variable | Tipo observado | Papel y descripción respaldada por los materiales |
|---|---|---|
| `case_id` | Texto | Identificador de caso sintético; excluido del modelo. |
| `received_date` | Fecha | Fecha sintética de recepción; ordena el corte temporal y se excluye de predictores. |
| `zone` | Categórica | Norte, Sur, Este y Oeste; etiquetas sintéticas sin equivalencia territorial real. Predictor. |
| `protected_group` | Categórica | G1/G2; se utiliza exclusivamente para auditoría, nunca como predictor. No se atribuye identidad demográfica real. |
| `age_band` | Categórica | 18–29, 30–44, 45–59 y 60+; predictor y dimensión de auditoría interseccional. Su uso debe justificarse. |
| `previous_incidents` | Entero | Conteo sintético por su nombre y valores; observado entre 0 y 9. La ventana temporal no está documentada. Predictor. |
| `infrastructure_score` | Decimal | Indicador sintético, observado entre 0.0316 y 0.9835; construcción y unidades no aportadas. Predictor. |
| `exposure` | Decimal | Indicador sintético, observado entre 0 y 1; construcción y unidades no aportadas. Predictor. |
| `target` | Entero binario | Objetivo 0/1; 1 se trata como clase positiva para calcular las métricas. No se interpreta como una condición real específica. |

Las comprobaciones ejecutadas no encontraron valores faltantes, valores numéricos no finitos, IDs duplicados, filas completas duplicadas ni combinaciones de predictores exactamente duplicadas. `previous_incidents` contiene enteros no negativos. No aparecieron categorías de zona o edad exclusivas del test ni combinaciones de predictores idénticas entre entrenamiento y prueba.

El CSV original no está ordenado cronológicamente. `load_data()` ordena sus fechas antes del corte. Hay 324 fechas distintas para 640 casos; la repetición de fechas no equivale a duplicación de casos. El rango sintético llega a 2026-12-27: no son observaciones reales futuras.

Estos controles no establecen validez de la etiqueta, ausencia de variables obtenidas después del evento o calidad de una eventual fuente real. La procedencia de los predictores y su disponibilidad previa a la decisión siguen sin documentación suficiente. Los rangos anteriores son observados, no contratos de dominio validados.

### 1.2. Distribución de clases y grupos

| Conjunto | n | Clase 0 | Clase 1 | G1 | G2 | Intervalo de fechas |
|---|---:|---:|---:|---:|---:|---|
| Total | 640 | 287 | 353 | 396 | 244 | 2026-01-01 a 2026-12-27 |
| Entrenamiento | 480 | 219 | 261 | 295 | 185 | 2026-01-01 a 2026-09-24 |
| Prueba | 160 | 68 | 92 | 101 | 59 | 2026-09-25 a 2026-12-27 |

La proporción positiva es 55.16% en el total, 54.38% en entrenamiento y 57.50% en prueba. En el test es **49/101 = 48.51% en G1** y **43/59 = 72.88% en G2**. Esta diferencia de composición importa para interpretar selección y precisión; no explica por sí sola todas las diferencias de error.

El perfil completo está en `reports/lab12/dataset_profile.json`. `reports/lab12/temporal_split.csv` identifica los 480 casos de entrenamiento y 160 de prueba sin modificar el dataset.

### 1.3. Metodología y prevención de fuga

Se usó el 75% inicial y 25% final de las filas ordenadas por fecha. Los IDs de ambos conjuntos son disjuntos y la fecha máxima de entrenamiento es anterior a la mínima de prueba; no se comparten fechas a ambos lados del corte. No se barajaron las filas ni se buscó un corte para mejorar resultados.

Los cinco predictores son zona, franja de edad, incidentes previos, infraestructura y exposición. Se excluyen `case_id`, `received_date`, `protected_group` y `target`. La regresión logística mantiene `random_state=42`, `class_weight="balanced"`, `max_iter=1200`, solver `lbfgs`, C=1 y tolerancia 0.0001. Se usó la regla `predict` predeterminada, sin ajustar un umbral sobre el test.

El pipeline ajusta OneHotEncoder y StandardScaler con el entrenamiento. La verificación del modelo serializado confirmó que las medias y el número de observaciones del escalador corresponden a las 480 filas de entrenamiento y que las categorías del codificador coinciden con las de ese conjunto. Se observan 11 variables transformadas y convergencia del estimador en 9 iteraciones, sin advertencias de convergencia en la ejecución registrada.

Estos controles reducen vías concretas de contaminación entre entrenamiento y prueba; no prueban que todos los indicadores fueran conocidos antes de una decisión real. La documentación de scikit-learn recomienda separar los datos y aprender las transformaciones con entrenamiento dentro de un pipeline. [Fuente oficial sobre fuga de información](https://scikit-learn.org/stable/common_pitfalls.html), consulta: 31 de octubre de 2026.

### 1.4. Resultados globales de la regresión logística

La unidad de evaluación es el caso sintético del test. Se obtuvieron **TP=66, TN=49, FP=19 y FN=26**, con 92 positivos, 68 negativos y 85 predicciones positivas.

| Métrica | Cálculo | Valor |
|---|---|---:|
| Accuracy | (TP+TN)/160 | 71.88% |
| Recall / TPR | TP/92 | 71.74% |
| FPR | FP/68 | 27.94% |
| Selection rate | (TP+FP)/160 | 53.13% |
| Precision | TP/85 | 77.65% |
| F1 | 2TP/(2TP+FP+FN) | 74.58% |
| FNR | FN/92 | 28.26% |

Las seis métricas originales se guardan en `reports/lab12/logistic/global_metrics.json`. F1, FNR, conteos y denominadores adicionales están en `audit_support.csv`. La concordancia entre el recálculo por conteos y las métricas globales y desagregadas originales se comprobó con tolerancia numérica 1e-12.

### 1.5. Auditoría por grupo

| Grupo | n | Positivos / negativos | TP / TN / FP / FN | Accuracy | Recall | FPR | Selección |
|---|---:|---:|---:|---:|---:|---:|---:|
| G1 | 101 | 49 / 52 | 32 / 39 / 13 / 17 | 70.30% | 65.31% | 25.00% | 44.55% |
| G2 | 59 | 43 / 16 | 34 / 10 / 6 / 9 | 74.58% | 79.07% | 37.50% | 67.80% |

La precisión es 71.11% en G1 y 85.00% en G2; FNR es 34.69% y 20.93%, respectivamente. G1 tiene peor resultado respecto a omisiones de positivos. G2 tiene peor resultado respecto a falsos positivos entre sus negativos. No existe un único grupo desfavorecido para todas las métricas.

Las brechas absolutas max–min son **13.76 puntos porcentuales (pp) en recall**, **12.50 pp en FPR** y **23.24 pp en selección**. Las tres tasas son mayores en G2. Comparar solo los 13 FP de G1 con los 6 de G2 ocultaría que sus denominadores negativos son 52 y 16; por eso FPR es mayor en G2.

El campo `differences.count=42` del JSON original es una diferencia de tamaños de grupo, no un indicador de equidad de resultados.

La selección no es un beneficio universal: depende de qué signifique recibir revisión. Su diferencia tampoco demuestra trato causal desigual, particularmente ante las distintas tasas positivas de los grupos. No se ha validado la semántica real de la etiqueta ni una cola de revisión con capacidad limitada.

Fairlearn organiza la evaluación alrededor de daños, grupos pertinentes, métricas e intersecciones. Aquí las etiquetas son sintéticas y la interpretación de daños sigue siendo condicional al uso. [Fairlearn 0.12: Performing a Fairness Assessment](https://fairlearn.org/v0.12/user_guide/assessment/perform_fairness_assessment.html), consulta: 31 de octubre de 2026.

### 1.6. Auditoría interseccional

La intersección disponible combina `protected_group` con `age_band`. Las ocho intersecciones tienen soporte de 8 a 35 casos; siete tienen n<30. Las banderas n<30, positivos<10 o negativos<10 del archivo de apoyo son avisos descriptivos de esta evaluación, no criterios oficiales de suficiencia o tolerancias éticas aprobadas.

| Intersección | n | Positivos / negativos | Recall | FPR | Selección |
|---|---:|---:|---:|---:|---:|
| G1 · 18–29 | 18 | 4 / 14 | 75.00% | 14.29% | 27.78% |
| G1 · 30–44 | 24 | 16 / 8 | 56.25% | 12.50% | 41.67% |
| G1 · 45–59 | 35 | 17 / 18 | 58.82% | 38.89% | 48.57% |
| G1 · 60+ | 24 | 12 / 12 | 83.33% | 25.00% | 54.17% |
| G2 · 18–29 | 11 | 8 / 3 | 87.50% | 0.00% | 63.64% |
| G2 · 30–44 | 14 | 12 / 2 | 66.67% | 50.00% | 64.29% |
| G2 · 45–59 | 8 | 6 / 2 | 100.00% | 0.00% | 75.00% |
| G2 · 60+ | 26 | 17 / 9 | 76.47% | 55.56% | 69.23% |

El recall mínimo observado es 9/16 en G1 · 30–44 y el máximo 6/6 en G2 · 45–59: brecha de **43.75 pp**. La FPR máxima es 5/9 en G2 · 60+ y hay tasas cero en dos intersecciones de G2: brecha de **55.56 pp**. La brecha de selección es **47.22 pp**. Son descripciones del test; los extremos calculados con pocos casos no justifican una clasificación estable de grupos ni conclusiones firmes sobre discriminación.

`fairness_intersectional.csv` conserva todas las métricas originales por intersección. `audit_support.csv` incorpora TP, TN, FP, FN y los denominadores que permiten interpretarlas. `gap_analysis.json` registra extremos; cuando hay empates, el identificador min/max mostrado es uno de los grupos empatados.

### 1.7. Incertidumbre y soporte

Se calcularon intervalos Wilson bilaterales de 95%, sin corrección de continuidad, para recall, FPR y selección. La implementación utiliza `scipy.stats.binomtest(...).proportion_ci(method="wilson")`. El denominador de recall es el número de positivos; el de FPR, los negativos; y el de selección, todos los casos del subconjunto. [Documentación oficial de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html) y [descripción del método en NIST](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm), consultadas el 31 de octubre de 2026.

| Ámbito | Recall: intervalo 95% | FPR: intervalo 95% | Selección: intervalo 95% |
|---|---|---|---|
| Global | 61.81–79.92% | 18.68–39.56% | 45.41–60.69% |
| G1 | 51.31–77.08% | 15.23–38.21% | 35.24–54.27% |
| G2 | 64.79–88.58% | 18.48–61.36% | 55.11–78.31% |

En G2 · 45–59, el recall 6/6 tiene intervalo 60.97–100%, y la FPR 0/2 tiene intervalo 0–65.76%. No observar un error en dos negativos no demuestra ausencia de riesgo. En G2 · 30–44, la FPR 1/2 tiene intervalo 9.45–90.55%; en G2 · 60+, la FPR 5/9 tiene intervalo 26.67–81.12%.

Estos intervalos son condicionales a las predicciones de este modelo y al supuesto binomial; la independencia temporal de los casos no está acreditada por el generador. No incorporan incertidumbre de entrenamiento, sondeos de otros modelos, corrección por múltiples comparaciones ni intervalos simultáneos para brechas. No se ha realizado una prueba causal o de significación del gap. El solapamiento de intervalos individuales tampoco demuestra igualdad de tasas.

### 1.8. Decisión de auditoría propuesta

Se completaron las seis claves de `student_inputs/lab12_decision.yml`. La propuesta prioriza estudiar omisiones mediante recall, acompañándolo por FPR, selección, soportes e intersecciones. Esta elección técnica y su interpretación normativa quedan pendientes de aprobación; no sustituyen preferencias del usuario ni una valoración de afectados.

La configuración trae recall global mínimo 0.68 y gaps por `protected_group` máximos de 0.16 para recall y FPR. Los puntos observados 0.717391, 0.137636 y 0.125 satisfacen esas tres comparaciones. No se ha ejecutado una decisión GO de LAB13 ni adoptado esos números como tolerancias éticas. Los límites no acreditan incertidumbre, selección ni equidad interseccional; los gaps interseccionales observados son mucho mayores y requieren cautela por sus tamaños.

**Recomendación: REVIEW**, mantener el ejercicio sintético, revisar predictores y evidencia y completar las siguientes fases antes de una decisión final. No se aplicaron mitigaciones, ajustes por grupo o cambios de umbral en esta fase. No se recomienda uso real con estos datos.

## 2. Archivos modificados

Únicamente `student_inputs/lab12_decision.yml` cambia respecto del commit de partida `86885b8`. Contiene la prioridad de daño propuesta, métrica, referencia experimental de tolerancia, evidencias, limitaciones y recomendación. Los scripts y módulos docentes de LAB12, las pruebas originales, LAB11, el dataset y el lock conservan sus bytes de partida.

## 3. Archivos generados

| Ruta | Propósito |
|---|---|
| `scripts/lab12_supporting_evidence.py` | Perfil del dataset y explicación verificable de resultados, conteos e intervalos sin reentrenar. |
| `reports/lab12/dataset_profile.json` | Variables, calidad observada, categorías, estadísticos y distribuciones por partición. |
| `reports/lab12/temporal_split.csv` | IDs y etiquetas de las particiones reproducibles de entrenamiento y test. |
| `reports/lab12/logistic/global_metrics.json` | Métricas, diferencias por grupo y recursos medidos por el script original. |
| `reports/lab12/logistic/fairness_by_group.csv` | Auditoría original por G1/G2. |
| `reports/lab12/logistic/fairness_intersectional.csv` | Auditoría original de las ocho intersecciones. |
| `reports/lab12/logistic/test_predictions.csv` | 160 casos del test con etiqueta, predicción y probabilidad de clase 1. |
| `reports/lab12/logistic/audit_support.csv` | Conteos, denominadores, F1/FNR, intervalos Wilson y banderas de soporte. |
| `reports/lab12/logistic/gap_analysis.json` | Brechas max–min y diferencias firmadas G2−G1. |
| `reports/lab12/logistic/model_metadata.json` | Parámetros, versiones, checks del preprocesamiento y hash/tamaño del modelo. |
| `models/logistic.joblib` | Modelo local generado: 3649 bytes, SHA-256 registrado. Se mantiene ignorado por la regla original de Git; puede regenerarse. |
| `reports/ejercicio_07/evidencias/fase_02/` | Estado inicial, comandos y resultados, registrador, integridad y manifiesto final. |
| `reports/ejercicio_07/FASE_02_LAB12.md` | Este informe de validación e interpretación. |

El modelo local tiene SHA-256 `9fc217d3fed0cfb74093c95d40012c386c0e1172e71d0f30f594cd2da177eb2a`. No se subió ni forzó a Git un binario que el proyecto excluye. En un equipo nuevo se debe regenerar antes de ejecutar el análisis complementario. La carga joblib se hizo sobre el modelo generado en esta ejecución local.

## 4. Pruebas y verificaciones ejecutadas

El registrador fija `UV_FROZEN=1` y `UV_OFFLINE=1`, captura stdout/stderr, fecha UTC, duración y código de salida y se niega a sobrescribir un registro previo. No se descargaron dependencias ni se actualizó el lock en esta fase.

| Comando | Resultado real | Registro en `evidencias/fase_02/` |
|---|---|---|
| `uv run python scripts/lab12_supporting_evidence.py --profile-only` | Código 0; perfil y división de 480/160 casos. | `01_dataset_profile.json` |
| `uv run python scripts/lab12_audit.py --model logistic` | Código 0; resultados originales y modelo local generados. | `02_logistic_audit.json` |
| `uv run python scripts/lab12_supporting_evidence.py --model logistic` | Código 0; métricas concordantes, soportes e intervalos calculados. | `03_support_and_uncertainty.json` y `07_final_support_verification.json` |
| `uv run pytest -q tests/test_fairness.py tests/test_model.py` | **2 passed in 2.87s**. | `05_required_tests.json` |
| `uv run ruff check scripts/lab12_supporting_evidence.py reports/ejercicio_07/evidencias/fase_02/record_command.py` | Código 0; `All checks passed!`. | `06_style_final.json` |
| `uv run python scripts/validate_lab12_decision.py` | Código 0; `decision_status: documented`, también tras verificar la ruta final del informe. | `08_decision_yaml_validation.json` y `09_final_decision_validation.json` |
| `uv run python reports/ejercicio_07/evidencias/fase_02/verify_phase.py` | Código 0; 64 archivos previos comprobados, solo cambia el YAML autorizado; ocho intersecciones y 160 predicciones coherentes. | `10_integrity_verification.json` e `integrity_verification.json` |

La primera comprobación de estilo con `--fix` corrigió cinco observaciones y se detuvo por falta de `check=False` explícito en `subprocess.run`. El código se corrigió para capturar y registrar también comandos fallidos. El resultado inicial no exitoso se conserva en `04_code_style.json`; la comprobación final pasó. Tras esos cambios de estilo se volvió a verificar el complemento con el mismo modelo, sin entrenarlo otra vez ni repetir las pruebas ya aprobadas.

Las dos pruebas requeridas entrenan sus propios modelos logísticos dentro del test y comprueban predicciones binarias y propiedades básicas de métricas/grupos. No acreditan cumplimiento normativo, ausencia de sesgo ni validez externa. Además de esas ejecuciones internas de prueba, hubo un entrenamiento de auditoría original; el complemento solo carga y predice. No se ejecutaron el árbol, Streamlit ni LAB13.

## 5. Problemas y limitaciones

La ejecución del laboratorio no presentó errores. Se resolvió el asunto de estilo del registrador. Se mantuvo la estructura real de salidas bajo `reports/lab12/logistic/`, distinta de las rutas planas propuestas en el adjunto.

Los límites principales son etiqueta y generador sin definición completa, carácter sintético, un único holdout temporal, denominadores pequeños y efectos potenciales de predictores sensibles o relacionados. Las métricas describen esta muestra y no una población real. La comparación futura de modelos sobre el mismo test será exploratoria; una validación externa o un holdout independiente seguirían siendo necesarios para generalizar.

No se midió calibración, capacidad de una cola de revisión, efectividad de supervisión humana o mitigación de brechas. Los intervalos no convierten una disparidad en discriminación causal ni un cero observado en seguridad. La jurisdicción, consulta a afectados, roles nominales y aceptación normativa siguen pendientes de sus fases correspondientes.

## 6. Evidencias y reproducción

`evidencias/fase_02/initial_state.json` conserva los hashes de partida. `integrity_verification.json` documenta que los materiales previos permanecen intactos salvo el YAML autorizado. `artifact_manifest.json` registra hashes de entradas, resultados, código nuevo y modelo local, excluyendo el propio manifiesto para evitar circularidad. `estado_git.txt` identifica rama y remoto antes del commit local.

Desde la raíz del proyecto se pueden reproducir las actividades centrales con:

```powershell
uv sync --frozen
uv run --frozen python scripts/lab12_supporting_evidence.py --profile-only
uv run --frozen python scripts/lab12_audit.py --model logistic
uv run --frozen python scripts/lab12_supporting_evidence.py --model logistic
uv run --frozen pytest -q tests/test_fairness.py tests/test_model.py
uv run --frozen python scripts/validate_lab12_decision.py
```

El tiempo de entrenamiento registrado por el laboratorio pertenece a esa ejecución y puede variar al repetirla. Los hashes describen bytes concretos; Git puede transformar saltos de línea de textos al clonar. El archivo de modelo se regenera localmente; su hash y las versiones están registrados para esta ejecución. No se afirma que el tiempo o el hash binario sean invariantes entre plataformas.

**Asistencia de IA:** Codex elaboró el perfil, script de apoyo, análisis y YAML y ejecutó las verificaciones indicadas. El usuario autorizó esta fase con «cONTINUA». No se recibieron correcciones humanas ni aprobación normativa de las propuestas. Los registros conservan la incidencia de estilo y su corrección. La declaración integrada y los prompts finales se recopilarán en la Fase 7.

## 7. Pendientes

Revisión por el usuario de la propuesta de prioridad, tolerancia y recomendación. Siguen pendientes comparación de modelos, integración formal LAB11/LAB12, marco legal, mitigación/decisión final, reproducibilidad final, PDF y auditoría de rúbrica. No se ejecutó ninguna de esas fases en esta entrega.

## 8. Próximo paso y autorización

El siguiente paso será **Fase 3 · Comparación con árbol y análisis de trade-offs**, después de `CONTINUAR`, conforme al flujo del adjunto. La recomendación de auditoría permanece en REVIEW y pendiente de aprobación. Los cambios quedan en la rama local `codex/ejercicio-07`; no se realizó push ni publicación en GitHub.
