# Fase 3 · Comparación de modelos y trade-offs

**Fecha:** 31 de octubre de 2026 (America/Santo_Domingo).

**Partes completadas:** 3.1–3.4: árbol, comparación técnica, eficiencia computacional e interpretación.

**Estado técnico:** completada; preferencia técnica propuesta, pendiente de revisión del usuario.

En este test sintético, la regresión logística conserva el mismo recall global que el árbol y obtiene menor FPR, brechas menores entre G1/G2 y un archivo más pequeño. El árbol mejora algunos resultados interseccionales y ofrece reglas por ruta, pero empeora otros. Su pequeña ventaja de mediana de entrenamiento en un benchmark local no demuestra ahorro energético. Se propone mantener la logística como referencia para continuar el estudio; no se adopta una decisión de despliegue.

## 1. Trabajo realizado y comparación

### 1.1. Condiciones metodológicas comunes

Se ejecutó `uv run python scripts/lab12_audit.py --model tree` sin modificar el script docente ni los constructores de modelos. Se conservaron como referencia los ocho artefactos logísticos de Fase 2 y su modelo local; sus bytes se verificaron frente al estado inicial de esta fase.

Ambos modelos usan el mismo CSV sintético, 480 casos de entrenamiento y 160 de prueba, corte 2026-09-24/2026-09-25, cinco predictores originales y once variables transformadas. Comparten OneHotEncoder, StandardScaler, `class_weight="balanced"` y `random_state=42`. `protected_group`, ID, fecha y objetivo quedan excluidos del conjunto de predictores. Edad y zona siguen requiriendo justificación de uso.

La logística conserva solver lbfgs, C=1 y máximo 1200 iteraciones; el árbol conserva criterio gini, profundidad máxima 5, mínimo 2 casos para dividir y mínimo 1 por hoja. Se usó `predict` sin optimizar umbrales con el test. Los metadatos verifican que escaladores y categorías se aprendieron con el entrenamiento. Los IDs, etiquetas, soportes y versiones de dependencias coinciden entre las dos evaluaciones.

El dataset es exclusivamente sintético y no representa personas, territorios o tasas reales. El perfil, la semántica incompleta de `target`, la ausencia del generador y las limitaciones de temporalidad se documentan en Fase 2 y siguen vigentes. La comparación usa un único holdout y tiene carácter exploratorio.

### 1.2. Utilidad global

| Métrica en 160 casos | Logística | Árbol | Árbol − logística |
|---|---:|---:|---:|
| Accuracy | 71.88% | 70.63% | −1.25 pp |
| Recall | 71.74% | 71.74% | 0.00 pp |
| FPR | 27.94% | 30.88% | +2.94 pp |
| Selection rate | 53.13% | 54.38% | +1.25 pp |
| Precision | 77.65% | 75.86% | −1.78 pp |
| F1 | 74.58% | 73.74% | −0.83 pp |
| FNR | 28.26% | 28.26% | 0.00 pp |
| TP / TN / FP / FN | 66 / 49 / 19 / 26 | 66 / 47 / 21 / 26 | 2 FP adicionales |

La ventaja de accuracy de la logística equivale a **dos casos correctos adicionales de 160**, no a una superioridad poblacional demostrada. Los modelos coinciden en 130 predicciones y difieren en 30. Hay 99 casos correctos por ambos, 16 solo por logística, 14 solo por árbol y 31 errados por ambos. Igual recall agregado no significa que omitan exactamente los mismos casos.

`model_comparison.csv` guarda los valores completos sin redondear. Las diferencias de la tabla se calculan antes del redondeo y se expresan en puntos porcentuales (pp).

### 1.3. Resultados por grupo

| Modelo y grupo | n (positivos / negativos) | Recall | FPR | Selección | Accuracy |
|---|---:|---:|---:|---:|---:|
| Logística · G1 | 101 (49 / 52) | 65.31% | 25.00% | 44.55% | 70.30% |
| Árbol · G1 | 101 (49 / 52) | 63.27% | 26.92% | 44.55% | 68.32% |
| Logística · G2 | 59 (43 / 16) | 79.07% | 37.50% | 67.80% | 74.58% |
| Árbol · G2 | 59 (43 / 16) | 81.40% | 43.75% | 71.19% | 74.58% |

El árbol pierde un TP en G1 y gana uno en G2, manteniendo 66 TP globales. Añade un FP en cada grupo; el incremento de FPR es mayor en G2 por su denominador de solo 16 negativos. G1 conserva menor recall y G2 mayor FPR; el criterio de daño importa para interpretar qué grupo queda peor situado.

| Brecha absoluta G1/G2 | Logística | Árbol |
|---|---:|---:|
| Recall | 13.76 pp | 18.13 pp |
| FPR | 12.50 pp | 16.83 pp |
| Selección | 23.24 pp | 26.63 pp |

Como referencia descriptiva, los límites experimentales de 16 pp en recall/FPR de `configs/governance.yml` contienen los puntos logísticos, pero el árbol los supera. No se interpreta esa comparación como tolerancia ética aprobada, equidad demostrada o autorización GO. No se ejecutó LAB13.

### 1.4. Resultados interseccionales

L/A significa logística/árbol. Las tasas están en porcentaje y comparten exactamente los mismos casos y denominadores en ambos modelos.

| Intersección | n (positivos / negativos) | Recall L/A | FPR L/A | Selección L/A |
|---|---:|---:|---:|---:|
| G1 · 18–29 | 18 (4 / 14) | 75.00 / 75.00 | 14.29 / 21.43 | 27.78 / 33.33 |
| G1 · 30–44 | 24 (16 / 8) | 56.25 / 62.50 | 12.50 / 37.50 | 41.67 / 54.17 |
| G1 · 45–59 | 35 (17 / 18) | 58.82 / 64.71 | 38.89 / 27.78 | 48.57 / 45.71 |
| G1 · 60+ | 24 (12 / 12) | 83.33 / 58.33 | 25.00 / 25.00 | 54.17 / 41.67 |
| G2 · 18–29 | 11 (8 / 3) | 87.50 / 100.00 | 0.00 / 0.00 | 63.64 / 72.73 |
| G2 · 30–44 | 14 (12 / 2) | 66.67 / 83.33 | 50.00 / 100.00 | 64.29 / 85.71 |
| G2 · 45–59 | 8 (6 / 2) | 100.00 / 66.67 | 0.00 / 0.00 | 75.00 / 50.00 |
| G2 · 60+ | 26 (17 / 9) | 76.47 / 76.47 | 55.56 / 55.56 | 69.23 / 69.23 |

El árbol mejora simultáneamente recall y FPR en G1 · 45–59, pero el recall cae 25 pp en G1 · 60+. En G2 · 30–44 mejora recall y aumenta FPR de 1/2 a 2/2. La FPR 100% del árbol se basa en dos negativos; su intervalo Wilson 95% es aproximadamente 34.24–100%, no una tasa poblacional conocida.

La brecha interseccional de recall baja ligeramente de 43.75 a 41.67 pp, mientras la de FPR aumenta de 55.56 a 100 pp y la de selección de 47.22 a 52.38 pp. Una mejora en una brecha no equivale a mejora general del sistema.

Siete de las ocho intersecciones tienen menos de 30 casos. Los intervalos Wilson se conservan para ambos modelos en sus archivos `audit_support.csv`; son condicionales, individuales y sin ajuste por comparaciones múltiples. No se ha realizado una prueba causal ni una inferencia simultánea sobre diferencias de modelos o brechas. Las repeticiones de entrenamiento para medir tiempo no aumentan el tamaño del test ni aportan nuevas muestras independientes.

### 1.5. Tamaño, estructura e interpretabilidad

| Aspecto | Logística | Árbol |
|---|---|---|
| Modelo serializado completo | 3649 bytes = 3.5635 KiB | 8059 bytes = 7.8701 KiB |
| Estructura del estimador | 11 coeficientes y un intercepto | Profundidad 5, 51 nodos y 26 hojas |
| Iteraciones observadas | 9 de lbfgs | No aplica el contador iterativo de logística |
| Buffers de parámetros seleccionados | 96 bytes de coeficientes/intercepto | 4080 bytes de arrays de nodos/valores |
| Explicación disponible | Efectos aditivos sobre log-odds en el espacio transformado | Ruta de hasta cinco decisiones y reglas completas |

1 KiB equivale a 1024 bytes. El árbol serializado ocupa aproximadamente 2.21 veces el tamaño de la logística. Los buffers indicados no representan RAM total, memoria del pipeline ni pico de entrenamiento; solo arrays específicos del estimador.

`logistic_coefficients.csv` exporta los coeficientes del modelo conservado. Los efectos numéricos corresponden a variables estandarizadas y las categorías a indicadores one-hot; no son efectos causales ni pruebas de discriminación. `tree_rules.txt` permite inspeccionar las rutas y avisa que los umbrales `num__` están estandarizados. `tree_feature_importances.csv` contiene importancia por impureza, no una justificación normativa de los predictores.

La logística ofrece una representación global compacta, aunque exige explicar log-odds y transformaciones. El árbol ofrece explicaciones locales por ruta, pero 26 hojas requieren revisar múltiples reglas, incluidas condiciones sobre edad y zona. La legibilidad no garantiza equidad, privacidad ni exactitud. La documentación oficial presenta ambos enfoques y sus propiedades predictivas: [regresión logística](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [árboles de decisión](https://scikit-learn.org/stable/modules/tree.html), consultadas el 31 de octubre de 2026.

### 1.6. Tiempo medido y Green AI

Los tiempos originales de `fit_measure` fueron 0.335639 s para logística y 0.049832 s para árbol. Se conservan como trazas de sus auditorías, realizadas en momentos distintos y sin controlar arranque, caché o carga del sistema. Su cociente no se presenta como una ventaja reproducible.

Para mejorar la comparación se ejecutó un experimento local con:

- Un calentamiento por modelo y diez ajustes nuevos medidos por modelo: 22 llamadas a fit en total.
- Orden alternado y balanceado: logística/árbol, después árbol/logística.
- Mismos 480 casos, cinco columnas, preprocesamiento, parámetros y semilla; bibliotecas nativas soportadas limitadas a un hilo y pools observados con `num_threads=1`.
- Cronómetro `time.perf_counter` alrededor de `pipeline.fit`, incluyendo aprendizaje del preprocesamiento y estimador. Se excluyen construcción del objeto, predicción y serialización.
- Predicciones de cada ajuste medido comprobadas frente al modelo canónico; los modelos guardados permanecen intactos.

| Tiempo de fit en el benchmark | Logística | Árbol |
|---|---:|---:|
| Mediana | 5.758 ms | 5.466 ms |
| Percentiles 25–75 | 5.336–6.188 ms | 5.173–5.698 ms |
| Mínimo–máximo | 5.096–7.308 ms | 4.802–6.105 ms |
| Repeticiones medidas | 10 | 10 |

La diferencia de medianas es aproximadamente 0.292 ms; los rangos e intervalos intercuartílicos se superponen. Es una observación de esta máquina y carga pequeña, sin prueba de superioridad general de velocidad. El experimento se realizó en Windows 11, Python 3.12.13, scikit-learn 1.9.1 y threadpoolctl 3.7.0; los detalles están en `fit_benchmark_metadata.json` y las veinte mediciones en `fit_benchmark_trials.csv`. Limitar bibliotecas nativas no equivale a medir utilización total de CPU. [Documentación de threadpoolctl](https://github.com/joblib/threadpoolctl), consulta: 31 de octubre de 2026.

Green AI propone incorporar eficiencia a la evaluación junto al rendimiento. En este ejercicio se reportan tiempo y tamaño como aspectos computacionales observables. **No se midieron electricidad, emisiones de carbono, pico de RAM ni costo monetario**, y no se convierten milisegundos o bytes en esas magnitudes. [Schwartz, Dodge, Smith y Etzioni, Green AI, 2019](https://arxiv.org/abs/1907.10597), consulta: 31 de octubre de 2026.

### 1.7. Complejidad estimada y alternativas de menor costo

Con n=480 y d=11 variables transformadas, la predicción lineal de logística requiere un producto de dimensión d, de orden O(d), más la transformación compartida. Como estimación propia del término de cálculo de objetivo/gradiente, T evaluaciones recorren aproximadamente O(Tnd); las 9 iteraciones registradas no identifican por sí solas T, porque el optimizador puede evaluar varias veces dentro de una iteración. No se midieron FLOPs ni se estima un tiempo absoluto a partir de esa expresión.

En el árbol, la inferencia del estimador sigue una ruta de orden O(profundidad), aquí de hasta cinco decisiones. El entrenamiento depende de la búsqueda de cortes y número de nodos; la documentación describe O(dn log n) para implementaciones con ordenación/cache eficientes bajo sus supuestos. Esa referencia no sustituye una medición de este pipeline ni permite comparar automáticamente consumos energéticos. [Guía oficial: complejidad de árboles](https://scikit-learn.org/stable/modules/tree.html#complexity), consulta: 31 de octubre de 2026.

Como alternativas para un estudio posterior se propone reutilizar modelos y transformaciones ajustados para auditorías adicionales, evitar búsquedas de hiperparámetros sin una pregunta concreta y considerar revisión cronológica sin modelo cuando la finalidad no requiera predicción. La alternativa manual no se ha implementado ni medido; su costo humano y utilidad no pueden darse por inferiores. Reducir complejidad o número de entrenamientos exigiría verificar que no empeoran errores o equidad.

### 1.8. Interpretación y preferencia técnica

La preferencia provisional por la logística para continuar el análisis combina menor FPR global, menor brecha G1/G2 de recall/FPR, menor tamaño y estructura compacta, manteniendo recall global. El árbol tiene una mediana de fit ligeramente menor en este experimento y mejora resultados de algunas intersecciones; también empeora otras, por lo que no se afirma dominancia universal de ningún modelo.

La prioridad de daño, tolerancias y elección final requieren revisión humana. La ventaja global de dos casos y los soportes interseccionales pequeños justifican cautela. La recomendación continúa en **REVIEW para ambos modelos**, limitada al ejercicio sintético y pendiente de aprobación; no es una decisión final ni autorización de uso real.

## 2. Archivos modificados

| Archivo | Cambio justificado por la fase |
|---|---|
| `scripts/lab12_supporting_evidence.py` | Admite árbol y registra sus parámetros/estructura sin asumir atributos de regresión logística; convierte contadores NumPy a enteros JSON. |
| `tests/test_model.py` | Parametriza la prueba de predicciones binarias para logística y árbol. |
| `tests/test_fairness.py` | Parametriza la comprobación de métricas/grupos para ambos modelos. |

Los resultados, modelo y decisión logística de la Fase 2 se conservan como registro de esa evaluación. El análisis comparativo actual se documenta aquí, sin reescribir la aprobación o valoración normativa de las fases anteriores.

## 3. Archivos generados

- `reports/lab12/tree/`: métricas originales, auditorías por grupos e intersecciones, predicciones, soportes/intervalos, brechas y metadatos.
- `models/tree.joblib`: modelo canónico local; permanece ignorado conforme a la regla original de Git, al igual que logística.
- `scripts/lab12_compare_models.py`: comparación y benchmark reproducibles.
- `reports/lab12/comparison/model_comparison.csv`: resumen global, brechas, tamaños y tiempos originales.
- `reports/lab12/comparison/group_and_intersection_comparison.csv`: tasas, errores y soportes para ambos modelos.
- `reports/lab12/comparison/paired_predictions.csv`: comparación de las 160 predicciones por ID.
- `reports/lab12/comparison/fit_benchmark_trials.csv`, `fit_benchmark_summary.csv` y `fit_benchmark_metadata.json`: mediciones, resumen y condiciones.
- `reports/lab12/comparison/complexity_and_interpretability.json`, `logistic_coefficients.csv`, `tree_feature_importances.csv` y `tree_rules.txt`: estructura y evidencias de interpretación.
- `reports/ejercicio_07/evidencias/fase_03/`: estado inicial, comandos, incidencias, verificación y manifiesto de hashes.
- `reports/ejercicio_07/COMPARACION_MODELOS.md`: este informe de cierre.

## 4. Pruebas y verificaciones ejecutadas

Los registros capturan códigos, salida real, fecha UTC y duración con `UV_FROZEN=1` y `UV_OFFLINE=1`.

| Comando | Resultado real | Registro en `evidencias/fase_03/` |
|---|---|---|
| `uv run python scripts/lab12_audit.py --model tree` | Código 0; árbol y tres resultados originales generados. | `01_tree_audit.json` |
| `uv run python scripts/lab12_supporting_evidence.py --model tree` | Ejecución final código 0; métricas, denominadores y modelo concordantes. | `03_tree_support_final.json` |
| `uv run python scripts/lab12_compare_models.py --repeats 10` | Código 0; predicciones comparables, veinte mediciones y modelos preservados. | `04_comparison_and_benchmark.json` |
| `uv run pytest -q tests/test_fairness.py tests/test_model.py` | **4 passed in 2.28s**: dos pruebas por modelo. | `06_both_models_tests.json` |
| `uv run ruff check` sobre scripts, pruebas y verificador de la fase | Código 0; `All checks passed!`. La lista exacta de archivos está en el registro. | `07_style_final.json` |
| `uv run python reports/ejercicio_07/evidencias/fase_03/verify_phase.py` | Código 0; 94 archivos previos comprobados, solo tres cambios autorizados; veinte mediciones y modelos conservados. | `08_integrity_verification.json` |

La primera exportación de apoyo del árbol se detuvo al serializar un contador NumPy `int64` en JSON. Se corrigieron los contadores de profundidad/hojas a enteros nativos y se repitió solo la exportación, sin reentrenar el modelo. El registro fallido se conserva en `02_tree_support.json`; no se presenta como ejecución exitosa. Ruff corrigió además un orden de importación; su comprobación con `--fix` terminó con código 0. Las comprobaciones finales de estilo e integridad se guardan junto a los demás registros.

## 5. Problemas y límites

Se resolvió la incidencia de exportación de metadatos. Persisten el carácter sintético, un test de 160 casos, soportes pequeños, definición incompleta del objetivo y falta de validación externa. Las comparaciones de tasas son descriptivas; el benchmark mide comportamiento computacional local, no validez predictiva adicional ni impacto ambiental.

No se evaluaron mitigaciones, calibración, capacidad operativa, costo de revisión humana o estabilidad ante otras muestras. La preferencia por un modelo depende de criterios revisables y no elimina riesgos residuales o la necesidad de supervisión. La decisión integrada y el marco legal corresponden a fases posteriores.

## 6. Evidencias y reproducción

Las condiciones y hashes iniciales están en `evidencias/fase_03/initial_state.json`. `integrity_verification.json` comprueba conservación de las evidencias previas salvo los tres cambios autorizados, concordancia de casos/métricas y preservación de modelos. `artifact_manifest.json` registra los bytes finales, incluidos los dos modelos locales ignorados; excluye el propio manifiesto y los marcadores `.gitkeep`.

Para reproducir desde una copia que contiene los artefactos de Fase 2 y su modelo local:

```powershell
uv sync --frozen
uv run --frozen python scripts/lab12_audit.py --model tree
uv run --frozen python scripts/lab12_supporting_evidence.py --model tree
uv run --frozen python scripts/lab12_compare_models.py --repeats 10
uv run --frozen pytest -q tests/test_fairness.py tests/test_model.py
```

En un clon sin modelos locales deben generarse primero la logística y sus evidencias con los comandos de Fase 2; ello crea una nueva ejecución, cuyos tiempos y hashes deben registrarse por separado. No se afirma identidad de tiempos o bytes binarios entre máquinas. Las métricas y benchmark de esta entrega conservan su procedencia concreta.

La asistencia de IA consistió en ampliar la exportación, ejecutar comparación/benchmark/pruebas, corregir la incidencia y redactar este informe. El usuario autorizó la Fase 3 con «cONTINUA». No se recibió aprobación normativa ni una revisión humana independiente de las conclusiones. Las fuentes primarias enlazadas se consultaron el 31 de octubre de 2026.

## 7. Pendientes

Revisión por el usuario de la preferencia técnica, integración formal LAB11/LAB12, marco legal, plan de mitigación y decisión final, reproducibilidad final, PDF y auditoría de rúbrica. La comparación no aprueba un despliegue ni modifica la prioridad de daño en nombre del usuario.

## 8. Próximo paso y autorización

El siguiente paso será **Fase 4 · Integración de LAB11 y LAB12**, después de `CONTINUAR`, conforme al flujo del adjunto. La rama local es `codex/ejercicio-07`; no se ha realizado push ni publicado cambios en GitHub.
