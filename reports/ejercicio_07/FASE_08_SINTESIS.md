# Fase 8 Elaboración del expediente de síntesis

**Fecha:** 31 de octubre de 2026. **Estado:** completada y verificada para el alcance académico documentado. La recomendación y aceptación de riesgos siguen pendientes de aprobación humana.

## 1. Trabajo realizado

Se integraron las 28 secciones solicitadas en una síntesis de 16 páginas A4, con portada, índice enlazado, numeración, 15 tablas, dos figuras vectoriales y once referencias institucionales con enlaces. El contenido mantiene separados hechos medidos, controles comprobados, recomendaciones propuestas y limitaciones.

El PDF y Markdown se generan desde la misma estructura de secciones y bloques. Se conserva esa estructura en `evidencias/fase_08/synthesis_content.json`. La fuente editable, los SVG y los CSV/YAML previos permiten revisar contenido y cifras; el PDF es la versión de presentación.

## 2. Archivos modificados

Ningún archivo anterior a la fase: los 264 archivos de partida, incluidos dataset, configuración, modelos y evidencias de Fases 0-7, mantienen sus bytes. Los ajustes se limitaron al generador y artefactos nuevos de Fase 8.

## 3. Archivos generados

- [Expediente PDF](Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad.pdf).
- [Versión editable Markdown](Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad.md).
- `figuras/resultados_globales.svg` y `figuras/equidad_por_grupo.svg`, calculados con los resultados guardados.
- `evidencias/fase_08/build_report.py`, `verify_report.py`, estructura de contenido, entorno de autoría, estado inicial, logs, revisión visual y manifiesto.

Los renders PNG y la primera versión se conservan localmente en `.runtime/`, excluida de Git. No se incluyen como entregables de presentación.

## 4. Verificaciones ejecutadas

| Comprobación | Resultado real | Evidencia en `evidencias/fase_08/` |
|---|---|---|
| Primer generador de síntesis | Código 0; 28 secciones, 15 tablas y dos figuras. | `01_build_synthesis.json` |
| Render inicial con Poppler a 150 dpi | Código 0; primera versión de 17 páginas inspeccionada. | `02_render_pdf.json` |
| Ajustes de anchos y flujo de tablas | Código 0; versión revisada de 16 páginas. | `03_build_layout_revision.json` |
| Render revisado con Poppler | Código 0; 16 imágenes de página. Todas inspeccionadas a resolución completa. | `04_render_layout_revision.json`; `visual_review.json` |
| Correspondencia de contenido y geometría | Código 0; 69 párrafos, 345 celdas en 17 fragmentos de tablas, 27 destinos de índice y 12 URLs externas comprobados; cero desbordamientos geométricos. | `05_document_verification.json`; `verification.json` |
| Ruff sobre los tres scripts de fase | Código 0; tres observaciones corregidas, sin pendientes. | `06_style_check.json` |
| Verificación final tras ajustes de estilo | Resultado final de cierre preservado por separado. | `07_final_document_verification.json` |
| Tratamiento binario y control Git | Control de formato final preservado; PDF marcado como binario para conservar sus bytes. | `08_git_binary_check.json`; `git_binary_note.json` |

La comparación de las 15 tablas extraídas del PDF incluye sus encabezados repetidos y todas sus celdas; no se limita a buscar números aislados. La tabla de métricas se contrasta además con los hechos guardados y el registro de riesgos conserva productos y residuales. Las URLs del PDF coinciden con el registro de once fuentes y el enlace del repositorio; esta comprobación de destinos no equivale a una nueva consulta web de su contenido.

No se ejecutan nuevos entrenamientos, predicciones o pytest. Se sintetizan las 15 pruebas únicas aprobadas en Fase 7 y se conservan sus límites. La revisión de imágenes fue realizada por el asistente; no se declara revisión humana independiente.

## 5. Problemas y correcciones

La primera maqueta partía códigos R01/E01 y palabras de la columna Poder por falta de ancho. Se ampliaron esas columnas y se centraron valores breves. Se permitió la continuación de tablas con encabezados repetidos y se ajustó el flujo del catálogo para evitar espacio excesivo. Se corrigieron puntuación y una concordancia de redacción sin cambiar métricas o conclusiones.

Una sospecha inicial sobre el índice se contrastó con coordenadas extraídas: el texto no invadía el pie de página. El índice permanece dentro de márgenes. En la versión final no se observan recortes, superposiciones, glifos ausentes o tablas ilegibles.

El primer control de blancos de Git interpretó el PDF como texto y señaló espacios de su sintaxis interna. Se declaró `*.pdf binary` en el .gitattributes local y se comprobó que los bytes del índice coincidan con el PDF revisado. No se alteró el contenido del documento para corregir esa clasificación.

El entorno de autoría se mantuvo separado del entorno científico: Python empaquetado 3.12.14, ReportLab 4.4.9, pypdf 6.10.0, pdfplumber 0.11.9 y Pillow 12.3.0. Los resultados del proyecto proceden de su entorno Python 3.12.13 documentado en Fase 7; no se modificó uv.lock ni se instalaron dependencias en él.

## 6. Evidencias y regeneración

Los hashes de partida están en `initial_state.json`. `authoring_environment.json` registra el runtime y el inicio de creación PDF; `visual_review.json` vincula las 16 imágenes revisadas con el hash del PDF final; `verification.json` guarda la correspondencia de contenido. Los registros conservan stdout, stderr y códigos reales. El manifiesto incluye los archivos finales y los dos modelos canónicos locales ignorados, excluyendo su propio archivo, `.gitkeep` y `.runtime/`.

Para regenerar la síntesis, ejecutar `build_report.py` desde la raíz con el runtime de autoría registrado; requiere ReportLab y fuentes Arial de Windows. El generador reconstruye las cifras desde los hechos guardados y el texto desde sus secciones redactadas. Las modificaciones editoriales deben trasladarse al contenido del generador y comprobarse de nuevo: editar el Markdown por sí solo no actualiza automáticamente el PDF. Después se renderiza con Poppler y se verifican contenido e imágenes de la nueva versión.

La asistencia de IA cubrió síntesis, código de composición, revisión visual y comprobación documental. No se inventó nombre de autor, matrícula, institución, consulta a afectados o aprobación. El mensaje de continuación autoriza elaborar la fase; no convierte la recomendación en una decisión humana aceptada.

## 7. Pendientes

Auditoría final de la rúbrica y de la entrega en Fase 9. Persisten las limitaciones científicas, operativas y de aprobación recogidas en el PDF. No se asignó una calificación ni se publicó la entrega en GitHub en esta fase.

## 8. Próximo paso

**Fase 9 Auditoría final y cumplimiento de la rúbrica**, después de la autorización correspondiente al plan acordado. La Fase 8 concluye con PDF y fuente editable revisados; no inicia la auditoría final ni autoriza despliegue real.
