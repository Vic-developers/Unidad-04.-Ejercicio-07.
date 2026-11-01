# Verificación de instalación y ejecución para la publicación

**Fecha:** 31 de octubre de 2026, America/Santo_Domingo. **Resultado:** comprobaciones aprobadas sobre el código del commit `d5765920794aedd24d5ca1295a3640f3229d5f55`.

Se clonó el repositorio local en otra carpeta y se creó un entorno virtual nuevo con `uv sync --frozen --python 3.12.13`: se instalaron 55 distribuciones usando las versiones de `uv.lock`. Se reutilizaron el intérprete Python 3.12.13 y la caché de paquetes disponibles en la misma máquina Windows. No se trata de una verificación en otro equipo ni de una descarga completa desde cero.

| Comprobación | Resultado | Evidencia en `reports/ejercicio_07/evidencias/publicacion/` |
|---|---|---|
| Instalación de Python y sincronización | Python 3.12.13 disponible; entorno nuevo; 55 paquetes instalados. | `python_install.log`, `uv_sync.log` |
| Comprobación del entorno | Código 0; dataset válido, 640 filas y 9 columnas. | `01_environment.json` |
| Suite completa a través del reproductor | 15 pruebas aprobadas: 3 LAB11, 4 LAB12, 7 complementarias y 1 AppTest; sin fallos, errores ni omisiones. | `02_reproduction.json`, `reproduction/*.xml` |
| Reproducción LAB11 | Tres salidas idénticas en bytes y registro de decisión preservado. | `reproduction/reproduction_result.json` |
| Reproducción de logística y árbol | 160 predicciones por modelo iguales a las referencias; diferencia máxima de probabilidades 0; métricas y hashes de modelos iguales. | `reproduction/reproduction_result.json` |
| Comparación de modelos | Código 0; calentamiento y diez ajustes medidos por modelo en la copia de trabajo. | `03_comparison.json` |
| CLI de Streamlit | Código 0; Streamlit 1.64.0. | `04_streamlit_version.json` |
| Servidor local | Endpoint `/_stcore/health` con HTTP 200 y cuerpo `ok`; servidor detenido después de la comprobación. | `05_streamlit_health.json` |

La reproducción ejecutó el comando documentado con `--run-id publicacion_01`. La comparación se realizó dentro de la copia generada por ese reproductor, usando sus modelos y soportes nuevos; las salidas canónicas de la entrega no se sobrescribieron. AppTest ejecutó la aplicación y comprobó su aviso de datos sintéticos. La comprobación HTTP adicional arrancó el mismo módulo Streamlit en modo headless, en el puerto local 18501, con el Python del entorno nuevo. El README utiliza el puerto 8501 para el uso habitual.

Durante la preparación se corrigió `reproduce.py` para crear `.runtime/` antes de crear la carpeta de una ejecución. Esa carpeta está ignorada por Git y puede faltar en una copia recién clonada. La ejecución completa aprobada comprueba ese caso. También se comprobaron los enlaces locales del README y el estilo del script modificado.

Esta verificación posterior a la Fase 8 acompaña la publicación solicitada por el usuario. Los informes anteriores conservan el estado histórico de cada fase, incluidas sus notas sobre commits locales. No se ha realizado la auditoría final de rúbrica de la Fase 9 ni una aprobación de uso real. El PDF, los resultados científicos originales y la recomendación académica LIMITAR permanecen vigentes para el alcance documentado.
