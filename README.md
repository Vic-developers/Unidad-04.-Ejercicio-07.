# INF-8239 · Unidad 04 · Ejercicio 07

Evaluación de impacto y auditoría de equidad de un DSS territorial con **datos sintéticos**, dos modelos comparables y un análisis de gobernanza para **República Dominicana**. Incluye código, entradas, resultados, pruebas y un informe PDF con su fuente editable.

La recomendación documentada es **LIMITAR el uso a la demostración académica**, pendiente de aprobación humana. Las banderas técnicas de la aplicación no autorizan decisiones sobre personas. Las fases 0–8 están documentadas; la auditoría final de la rúbrica de la Fase 9 sigue pendiente.

## 1. Requisitos

- Git para clonar el repositorio.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) disponible en la terminal.
- Python **3.12**. Los comandos siguientes instalan **3.12.13**, la versión usada para los resultados científicos de esta entrega. `pyproject.toml` admite `>=3.12,<3.13`; Python 3.13 no es compatible con este proyecto.
- Conexión a Internet para la primera descarga de Python y de dependencias.

Los pasos están escritos para **PowerShell en Windows**, desde una carpeta donde tengas permiso de escritura. No es necesario activar manualmente el entorno virtual: `uv run` utiliza `.venv`.

## 2. Clonar e instalar

```powershell
git clone https://github.com/Vic-developers/Unidad-04.-Ejercicio-07..git Unidad-04.-Ejercicio-07
cd Unidad-04.-Ejercicio-07
uv python install 3.12.13
uv sync --frozen --python 3.12.13
```

La carpeta de destino se indica expresamente para evitar el punto final del nombre remoto. `--frozen` conserva las versiones de `uv.lock`; la sincronización incluye las dependencias de desarrollo necesarias para pytest.

Si ya tienes una copia clonada, entra en su raíz antes de ejecutar los demás comandos. Debes ver `app.py`, `pyproject.toml` y `uv.lock` en esa carpeta.

## 3. Comprobar el entorno y las pruebas

```powershell
uv run --frozen python scripts/check_environment.py
uv run --frozen pytest -q
```

La comprobación del dataset debe indicar `dataset_status: valid`, **640 filas y 9 columnas**. La suite contiene **15 pruebas**, incluida una prueba de arranque de la aplicación con AppTest. Las evidencias de la ejecución académica están en [TEST_REPORT.md](reports/ejercicio_07/TEST_REPORT.md).

## 4. Iniciar la aplicación

```powershell
uv run --frozen streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

Abre [http://localhost:8501](http://localhost:8501) en tu navegador y mantén la terminal abierta. Para detener el servidor, pulsa **Ctrl+C**.

La aplicación calcula métricas, muestra resultados por grupo y evalúa puertas técnicas de calidad. Ajusta una regresión logística al arrancar y crea `models/model.joblib` localmente; no necesita descargar un modelo preentrenado. No implementa una cola operativa de revisión ni acredita aprobación humana.

## 5. Leer la entrega

| Archivo o carpeta | Contenido |
|---|---|
| [Informe PDF](reports/ejercicio_07/Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad.pdf) | Síntesis de 16 páginas, 28 secciones, 15 tablas y dos figuras. |
| [Informe editable](reports/ejercicio_07/Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad.md) | Versión Markdown del contenido del PDF. |
| [Decisión final propuesta](reports/ejercicio_07/DECISION_FINAL.md) | Recomendación LIMITAR, condiciones y aprobación pendiente. |
| [Comparación de modelos](reports/ejercicio_07/COMPARACION_MODELOS.md) | Métricas, brechas, incertidumbre y recursos. |
| [Marco legal y ético](reports/ejercicio_07/MARCO_LEGAL_VOLUNTARIO_ETICO.md) | Aplicabilidad en República Dominicana y fuentes institucionales. |
| [Declaración de uso de IA](reports/ejercicio_07/AI_USAGE_DECLARATION.md) | Asistencia utilizada y límites de las verificaciones. |
| `data/`, `student_inputs/`, `configs/` | Dataset sintético, evaluación, riesgos, interesados y configuración. |
| `reports/lab11/`, `reports/lab12/` | Resultados guardados de impacto, logística, árbol y comparación. |
| `reports/ejercicio_07/evidencias/` | Registros, hashes, verificadores y evidencias de las fases. |
| `src/inf8239_u04/`, `scripts/`, `tests/` | Código del proyecto, comandos y pruebas. |

Los resultados tabulares y el PDF ya están incluidos: puedes examinarlos sin volver a entrenar. Los modelos `*.joblib`, `.venv`, cachés y renders temporales se generan localmente y están excluidos de Git.

## 6. Reproducir LAB11 y LAB12

Estos comandos regeneran las salidas de `reports/lab11/` y `reports/lab12/`, incluidos los tiempos y metadatos de la nueva ejecución. Úsalos en una copia de trabajo si quieres conservar intacta la entrega descargada. LAB11 preserva el registro de decisión existente.

Desde la raíz del proyecto, después de instalar las dependencias:

```powershell
uv run --frozen python scripts/lab11_impact.py
uv run --frozen python scripts/lab12_audit.py --model logistic
uv run --frozen python scripts/lab12_supporting_evidence.py --model logistic
uv run --frozen python scripts/lab12_audit.py --model tree
uv run --frozen python scripts/lab12_supporting_evidence.py --model tree
uv run --frozen python scripts/lab12_compare_models.py --repeats 10
```

El orden importa: cada auditoría crea su modelo local; el script de soporte comprueba las métricas y añade predicciones, conteos e intervalos; la comparación requiere ambos modelos y sus soportes. El último comando realiza un calentamiento y diez ajustes medidos por modelo. Los tiempos y los bytes de modelos pueden variar entre equipos; no son medidas de energía o carbono.

Como referencia del test sintético de 160 casos, la logística obtuvo accuracy **0.71875**, recall **0.7173913** y FPR **0.2794118**; el árbol obtuvo accuracy **0.70625**, recall **0.7173913** y FPR **0.3088235**. Estas cifras no demuestran utilidad o equidad en poblaciones reales.

También existe un reproductor que conserva las salidas principales y ejecuta los 15 tests en una copia separada de las fuentes. Usa una etiqueta nueva en cada ejecución:

```powershell
uv run --frozen python -B reports/ejercicio_07/evidencias/fase_07/reproduce.py --run-id revision_01
```

Genera evidencia en `reports/ejercicio_07/evidencias/fase_07/reproduction_revision_01/` y una copia de trabajo local en `.runtime/`. Sus comparaciones estrictas están diseñadas para el entorno Windows documentado; el informe de pruebas explica los límites de versiones, plataforma y reproducción local.

LAB13 y el runbook de incidentes pertenecen al proyecto base y conservan campos pendientes. No forman parte de la ejecución necesaria para el Ejercicio 07.

## 7. Problemas frecuentes

- **`uv` no se reconoce:** instala uv siguiendo su documentación y abre una terminal nueva.
- **Versión de Python incompatible:** ejecuta `uv python install 3.12.13` y repite `uv sync --frozen --python 3.12.13`.
- **No se encuentra el dataset o la configuración:** ejecuta los comandos desde la raíz que contiene `app.py`, no desde `scripts/`.
- **No existe `models/logistic.joblib` o `models/tree.joblib`:** ejecuta primero las auditorías correspondientes de la sección 6. Los binarios no se incluyen en Git.
- **El puerto 8501 está ocupado:** detén el servidor anterior o cambia a `--server.port 8502` y abre `http://localhost:8502`.
- **AppTest o Streamlit no arrancan en un entorno restringido:** necesitan conexiones locales de bucle de retorno. Revisa que el entorno permita ese acceso y conserva el error si la prueba no termina; no lo cuentes como una prueba aprobada.

El PDF se elaboró con un entorno de autoría separado del científico. Su generador y proceso de revisión se documentan en [FASE_08_SINTESIS.md](reports/ejercicio_07/FASE_08_SINTESIS.md); no es necesario regenerarlo para ejecutar la aplicación.
