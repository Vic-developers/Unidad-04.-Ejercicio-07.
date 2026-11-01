"""Build a PDF and editable Markdown synthesis from the verified project evidence."""

import csv
import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.graphics import renderSVG
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
OUT = ROOT / "reports/ejercicio_07"
STEM = "Ejercicio_07_Evaluacion_Impacto_Auditoria_Equidad"
NAVY = colors.HexColor("#234B72")
TEAL = colors.HexColor("#287E80")
PALE = colors.HexColor("#F1F5F8")
GRAY = colors.HexColor("#D9D9D9")
PAGE_W, PAGE_H = A4
MARGIN = 2 * cm
WIDTH = PAGE_W - 2 * MARGIN


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def rows(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def percent(value, suffix="%"):
    return str((Decimal(str(value)) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) + suffix


def plain(text):
    return str(text).replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")


def paragraph(text):
    return {"type": "paragraph", "text": plain(text)}


def table(caption, headers, data, widths):
    return {"type": "table", "caption": caption, "headers": headers, "rows": data, "widths": widths}


def subsection(title):
    return {"type": "subheading", "text": title}


def make_charts(facts):
    figures = OUT / "figuras"
    figures.mkdir(exist_ok=True)
    charts = {}
    drawing = Drawing(480, 244)
    x0, y0, chart_w, chart_h = 43, 42, 412, 166
    for tick in range(0, 81, 20):
        y = y0 + chart_h * tick / 80
        drawing.add(Line(x0, y, x0 + chart_w, y, strokeColor=GRAY, strokeWidth=0.5))
        drawing.add(String(x0 - 9, y - 3, str(tick), textAnchor="end", fontName="Arial", fontSize=9))
    for index, key in enumerate(("tp", "tn", "fp", "fn")):
        center = x0 + chart_w * (index + 0.5) / 4
        for offset, name, fill in ((-19, "logistic", NAVY), (3, "tree", TEAL)):
            value = facts["models"][name]["global"][key]
            height = chart_h * value / 80
            drawing.add(Rect(center + offset, y0, 17, height, fillColor=fill, strokeColor=None))
            drawing.add(String(center + offset + 8.5, y0 + height + 5, str(value), textAnchor="middle", fontName="Arial", fontSize=10))
        drawing.add(String(center, y0 - 17, key.upper(), textAnchor="middle", fontName="Arial", fontSize=10))
    drawing.add(String(43, 226, "Casos en el test sintético n = 160", fontName="Arial", fontSize=11))
    for x, label, fill in ((280, "Logística", NAVY), (376, "Árbol", TEAL)):
        drawing.add(Rect(x, 222, 9, 9, fillColor=fill, strokeColor=None))
        drawing.add(String(x + 14, 223, label, fontName="Arial", fontSize=9))
    charts["global"] = drawing
    renderSVG.drawToFile(drawing, str(figures / "resultados_globales.svg"))

    support = {name: {row["group"]: row for row in rows(f"reports/lab12/{name}/audit_support.csv") if row["level"] == "group"} for name in ("logistic", "tree")}
    drawing = Drawing(480, 278)
    x0, y0, chart_w, chart_h = 44, 70, 412, 164
    for tick in range(0, 101, 20):
        y = y0 + chart_h * tick / 100
        drawing.add(Line(x0, y, x0 + chart_w, y, strokeColor=GRAY, strokeWidth=0.5))
        drawing.add(String(x0 - 9, y - 3, str(tick), textAnchor="end", fontName="Arial", fontSize=9))
    for index, (group, metric, denominator) in enumerate((("G1", "recall", 49), ("G2", "recall", 43), ("G1", "fpr", 52), ("G2", "fpr", 16))):
        center = x0 + chart_w * (index + 0.5) / 4
        for offset, name, fill in ((-19, "logistic", NAVY), (3, "tree", TEAL)):
            item = support[name][group]
            value = 100 * float(item[metric])
            height = chart_h * value / 100
            drawing.add(Rect(center + offset, y0, 17, height, fillColor=fill, strokeColor=None))
            x = center + offset + 8.5
            low = y0 + chart_h * float(item[f"{metric}_wilson95_low"])
            high = y0 + chart_h * float(item[f"{metric}_wilson95_high"])
            drawing.add(Line(x, low, x, high, strokeColor=colors.black, strokeWidth=0.8))
            drawing.add(Line(x - 3, low, x + 3, low, strokeColor=colors.black, strokeWidth=0.8))
            drawing.add(Line(x - 3, high, x + 3, high, strokeColor=colors.black, strokeWidth=0.8))
        drawing.add(String(center, y0 - 17, f"{group} {'Recall' if metric == 'recall' else 'FPR'}", textAnchor="middle", fontName="Arial", fontSize=9))
        drawing.add(String(center, y0 - 31, f"denominador {denominator}", textAnchor="middle", fontName="Arial", fontSize=8.5))
    drawing.add(String(44, 256, "Tasas porcentuales e intervalos Wilson del 95%", fontName="Arial", fontSize=11))
    for x, label, fill in ((280, "Logística", NAVY), (376, "Árbol", TEAL)):
        drawing.add(Rect(x, 237, 9, 9, fillColor=fill, strokeColor=None))
        drawing.add(String(x + 14, 238, label, fontName="Arial", fontSize=9))
    drawing.add(String(44, 17, "Intervalos individuales y condicionales sin ajuste por comparaciones múltiples", fontName="Arial", fontSize=8))
    charts["groups"] = drawing
    renderSVG.drawToFile(drawing, str(figures / "equidad_por_grupo.svg"))
    return charts


def content(facts):
    models = facts["models"]
    logistic, tree = models["logistic"], models["tree"]
    risks = rows("student_inputs/risk_register.csv")
    sources = load("reports/ejercicio_07/evidencias/fase_05/sources.json")
    sections = []

    def add(number, title, *blocks):
        sections.append({"number": number, "title": title, "blocks": list(blocks)})

    add(1, "Portada", paragraph("Evaluación de impacto y auditoría de equidad"), paragraph("INF8239 Ciencia de Datos II"), paragraph("Unidad 04 Ejercicio 07"), paragraph("Territorial Review DSS - Synthetic"), paragraph("República Dominicana"), paragraph("31 de octubre de 2026"), paragraph("Recomendación técnica: limitar al ámbito académico con datos sintéticos"), paragraph("Aprobación de la recomendación y aceptación del riesgo pendientes"))
    add(2, "Introducción", paragraph("La recomendación es mantener Territorial Review DSS como demostración académica y conservar REVIEW para la revisión de sus resultados. Los modelos permiten estudiar errores y disparidades descriptivas; la evidencia disponible no sustenta despliegue real ni decisiones sobre personas. Esta síntesis integra la evaluación de impacto de LAB11 con la auditoría de equidad de LAB12 y la evidencia de reproducción local. [E01-E09]"), paragraph("En el test de 160 casos sintéticos, ambos modelos detectan 66 de 92 positivos y omiten 26. La logística produce 19 falsos positivos y el árbol 21. Las diferencias entre grupos y los soportes interseccionales pequeños requieren interpretar el daño y la incertidumbre antes de aceptar una política. Las medidas de mitigación y sus responsables son propuestas pendientes."))
    add(3, "Objetivo del ejercicio", paragraph("Construir un expediente trazable que conecte finalidad, interesados, proporcionalidad, riesgos, controles y métricas. Se evalúan utilidad y equidad global, por grupos e intersecciones; se comparan dos modelos y una alternativa no predictiva; se distinguen normas jurídicas, marcos orientativos y recomendaciones éticas; y se formula una recomendación sustentada en evidencias editables."), paragraph("La calidad del ejercicio se juzga por la correspondencia entre afirmaciones y artefactos, no por obtener una bandera GO o una puntuación de equidad aislada. Las pruebas verifican comportamientos concretos de software y reproducción; no sustituyen evaluación institucional o humana. [E06, E08, E09]"))
    add(4, "Descripción del sistema", paragraph("El proyecto implementa clasificación binaria, métricas, scripts de auditoría y una interfaz demostrativa Streamlit. Su finalidad declarada es explorar qué casos sintéticos recibirían revisión humana prioritaria. El código no implementa una cola institucional de atención ni acredita decisiones efectivas sobre personas."), paragraph("Se utilizan zone, age_band, previous_incidents, infrastructure_score y exposure. Las categorías se codifican con one-hot encoding y las variables numéricas se estandarizan. case_id, received_date, protected_group y target quedan fuera de los predictores. La exclusión directa de protected_group no elimina posibles efectos asociados a edad o zona. [E03-E05]"))
    stakeholder_data = [
        ["Casos G1/G2 y edades simuladas", "Aprender a comparar errores; riesgo de atribuir patrones ficticios a colectivos", "Bajo", "Revisión de escenarios propuesta; no participantes humanos"],
        ["Operador revisor previsto", "Comprender resultados; posible carga o confianza excesiva", "Medio", "Ensayo y revisión manual propuestos"],
        ["Responsable académico propuesto", "Custodiar y revisar alcance; riesgo de aprobar sin evidencia", "Alto", "Designación nominal pendiente"],
        ["Equipo de datos y modelos propuesto", "Reproducir y detectar fallos; riesgo de propagarlos", "Medio", "Asistencia técnica realizada; revisión independiente pendiente"],
        ["Persona evaluadora propuesta", "Contrastar evidencias; riesgo de confundir controles y propuestas", "Medio", "No se acredita revisión docente"],
        ["Personas de una eventual adaptación", "Beneficio hipotético; posibles errores desiguales y usos indebidos", "Bajo", "Fuera de alcance; consulta futura necesaria"],
    ]
    add(5, "Finalidad e interesados", paragraph("La utilidad perseguida es didáctica. En el dataset solo hay 640 casos sintéticos; no existen personas reales sometidas a decisiones en esta evaluación. Los seis roles e interesados se describen con beneficios y daños potenciales, poder y mecanismos de participación. Ningún rol propuesto equivale a autoridad institucional asignada. [E01, E02]"), table("Tabla 1 Interesados y participación", ["Interesado", "Interés y daño potencial", "Poder", "Participación y estado"], stakeholder_data, [3.5, 5.7, 1.8, 6.0]))
    add(6, "Evaluación de proporcionalidad", paragraph("Hay una justificación académica para comparar predicción y errores. No se demostró que una priorización predictiva sea necesaria o mejor que revisar todos los casos por received_date. La alternativa cronológica reduce la dependencia de puntuaciones, pero su carga, demora y eficacia tampoco se midieron."), paragraph("No se asignan recall o FPR a una cola manual no implementada ni se presume que toda revisión humana sea correcta. Antes de proponer uso operativo habría que justificar la finalidad y la disponibilidad de predictores, evaluar capacidad y consecuencias y acordar criterios con los interesados. [E01, E06, E08]"))
    add(7, "Evaluación de impacto", paragraph("LAB11 identificó nueve escenarios relevantes. LAB12 concreta R01-R03 mediante diferencias de error y selección; aporta evidencia de coherencia técnica para R05 y trazabilidad para R07/R09. No verifica eficacia de supervisión, consulta o reclamación R06/R08, ni privacidad integral de nuevas fuentes R04."), paragraph("Los controles comprobados incluyen rechazo de nombres de columnas identificadoras, validación del contrato, separación temporal, transformaciones aprendidas en entrenamiento, preservación del registro LAB11 y trazabilidad local de comandos y hashes. La operación humana, el canal de apelación, la custodia independiente y las barreras institucionales permanecen propuestos. [E02, E04, E06, E09]"))
    risk_summaries = ["Diferencias de error y selección entre grupos e intersecciones", "Omisión de positivos si se usa la clasificación para excluir revisión", "Falsos positivos y desplazamiento de casos con capacidad limitada", "Identificadores o información personal en entradas sustitutas", "Etiqueta y procedencia incompletas y disponibilidad temporal dudosa", "Reutilización indebida o confusión de GO con autorización", "Pérdida de decisiones o dificultad para reconstruir resultados", "Objeción sin canal o autoridad revisora efectiva", "Alteración de entradas o evidencias sin custodia confiable"]
    risk_data = []
    for row, summary in zip(risks, risk_summaries, strict=True):
        score = int(row["likelihood_1_4"]) * int(row["impact_1_4"])
        risk_data.append([row["id"], summary, row["likelihood_1_4"], row["impact_1_4"], str(score), "Alto" if row["residual"] == "high" else "Medio"])
    add(8, "Registro de riesgos", paragraph("Las valoraciones de probabilidad L e impacto I, en escalas de 1 a 4, son juicios ordinales propuestos. Su producto ordena la discusión y no estima una frecuencia observada ni un riesgo aceptado. Los daños a personas son condicionales a una reutilización fuera del alcance sintético. El registro completo conserva afectados, control, responsable funcional, evidencia y residual. [E01, E02]"), table("Tabla 2 Riesgos y valoración inicial propuesta", ["ID", "Escenario", "L", "I", "L x I", "Residual"], risk_data, [1.4, 10.0, 0.75, 0.75, 1.6, 2.5]), paragraph("R01 tiene producto 12; R03/R05/R07, 9; R02/R04/R06, 8; R08/R09, 6. Persisten residuales altos en R01/R02/R05/R06/R08 y medios en los demás. No se ha medido una reducción por las mitigaciones propuestas; el residual posterior no se reestima."))
    add(9, "Aplicación de NIST AI RMF", paragraph("Se utiliza AI RMF 1.0 como referencia voluntaria para organizar la gestión. El mapeo del proyecto no equivale a certificación, obligación jurídica automática o aceptación de riesgos. [F01, F02]"), table("Tabla 3 Funciones y evidencia del proyecto", ["Función", "Aplicación", "Evidencia y vacío"], [["GOVERN", "Finalidad, roles, límites y registros", "Documentados; autoridad nominal y aceptación pendientes"], ["MAP", "Seis interesados y nueve escenarios", "Contexto sintético; beneficios y daños reales sin validar"], ["MEASURE", "Auditorías de dos modelos y soportes", "Medición realizada; sin validación externa o causal"], ["MANAGE", "Controles técnicos y propuestas de respuesta", "Preservación y trazabilidad comprobadas; eficacia operativa pendiente"]], [2.3, 6.2, 8.5]))
    add(10, "Descripción del dataset", paragraph("El CSV contiene 640 filas y nueve columnas, con IDs únicos, sin faltantes observados y valores numéricos finitos. Hay 324 fechas únicas. La carga ordena las fechas porque el archivo original no está ordenado. El control de coherencia no prueba validez de la etiqueta, anonimización o procedencia completa."), table("Tabla 4 Corte temporal y composición", ["Partición", "n", "Fechas sintéticas", "Positivos", "Negativos"], [["Entrenamiento", "480", "01-01-2026 a 24-09-2026", "261", "219"], ["Prueba", "160", "25-09-2026 a 27-12-2026", "92", "68"], ["Total", "640", "01-01-2026 a 27-12-2026", "353", "287"]], [3.4, 1.3, 7.3, 2.5, 2.5]), paragraph("G1 tiene 396 casos y G2 244 en el archivo completo; en prueba son 101 y 59. Las franjas son 18-29, 30-44, 45-59 y 60+. No representan personas, territorios o estadísticas dominicanas. Las fechas posteriores al 31-10-2026 pertenecen a la simulación. Faltan la evidencia completa del generador y su semilla y una definición operacional de target. [E01, E04]"))
    add(11, "Metodología de auditoría", paragraph("Se entrenan regresión logística y árbol sobre los mismos 480 casos y cinco predictores y se evalúan sobre el mismo test de 160. Ambos usan class_weight balanced y random_state 42. La logística fija max_iter 1200; el árbol max_depth 5. Los metadatos confirman que escalador y categorías se aprendieron solo con entrenamiento."), paragraph("Se reconstruyen TP, TN, FP y FN y se calculan accuracy, recall, FPR, selección, precisión, F1 y FNR. Recall es TP dividido entre TP más FN; FPR es FP dividido entre FP más TN. Las brechas son máximo menos mínimo de cada tasa entre estratos. Se auditan protected_group e intersecciones con age_band."), paragraph("Los intervalos Wilson del 95% son individuales y condicionales a las predicciones. No incluyen incertidumbre del entrenamiento, ajuste por comparaciones múltiples ni inferencia causal o simultánea de brechas. El test ya fue examinado; una selección futura de cambios necesita validación de desarrollo y un nuevo test final no usado para seleccionar. [E03-E05, E08]"))
    metric_labels = [("accuracy", "Accuracy"), ("recall", "Recall"), ("fpr", "FPR"), ("selection_rate", "Selección"), ("precision", "Precisión"), ("f1", "F1"), ("fnr", "FNR")]
    metric_data = [[label, percent(logistic["global"][key]), percent(tree["global"][key])] for key, label in metric_labels]
    metric_data.append(["TP / TN / FP / FN", "66 / 49 / 19 / 26", "66 / 47 / 21 / 26"])
    add(12, "Resultados globales", table("Tabla 5 Resultados en los mismos 160 casos", ["Métrica", "Logística", "Árbol"], metric_data, [7, 5, 5]), {"type": "figure", "id": "global", "file": "figuras/resultados_globales.svg", "caption": "Figura 1 Conteos de clasificación sobre el test sintético", "note": "TP y FN suman 92 positivos; TN y FP suman 68 negativos. Fuente E03-E05."}, paragraph("Ambos modelos omiten 26 de 92 positivos. La logística marca 85 casos y el árbol 87. Esa selección no es una carga humana medida: el código no evalúa una cola ni tiempos de atención."))
    group_data = []
    for name, label in (("logistic", "Logística"), ("tree", "Árbol")):
        for group, item in models[name]["by_group"].items():
            group_data.append([f"{label} {group}", str(item["n"]), f"{item['positive_n']} / {item['negative_n']}", percent(item["recall"]), f"{item['fp']}/{item['negative_n']} {percent(item['fpr'])}", percent(item["selection_rate"])])
    add(13, "Resultados por grupos", table("Tabla 6 Soporte y tasas por grupo", ["Modelo y grupo", "n", "P / N", "Recall", "FP / N y FPR", "Selección"], group_data, [3.6, 1, 2, 2.5, 4.1, 3.8]), {"type": "figure", "id": "groups", "file": "figuras/equidad_por_grupo.svg", "caption": "Figura 2 Recall y FPR por grupo con incertidumbre", "note": "Denominadores positivos para recall y negativos para FPR. Las barras negras son IC Wilson individuales del 95%. Fuente E04."}, paragraph("G1 tiene menor recall y mayor FNR; G2 tiene mayor FPR. Con logística son 17 FN de 49 positivos en G1 y 9 de 43 en G2. Los 6 FP de G2 son menos que los 13 de G1, pero su FPR es mayor por tener solo 16 negativos frente a 52. Ningún grupo es el peor en todas las dimensiones."))
    intersection_data = []
    for group, item in logistic["by_intersection"].items():
        other = tree["by_intersection"][group]
        intersection_data.append([group.replace(" | ", " "), f"{item['n']} ({item['positive_n']}/{item['negative_n']})", f"{percent(item['recall'])} / {percent(other['recall'])}", f"{percent(item['fpr'])} / {percent(other['fpr'])}", f"{percent(item['selection_rate'])} / {percent(other['selection_rate'])}"])
    add(14, "Resultados interseccionales", paragraph("L/A significa logística/árbol. P/N identifica positivos y negativos del mismo estrato. Los ocho soportes van de 8 a 35 casos y siete son menores que 30. Las tasas extremas necesitan leerse con esos denominadores. [E04, E05]"), table("Tabla 7 Intersecciones entre grupo y edad simulada", ["Estrato", "n (P/N)", "Recall L / A", "FPR L / A", "Selección L / A"], intersection_data, [2.5, 2.2, 4.1, 4.1, 4.1]), paragraph("El árbol mejora recall y FPR en G1 45-59, pero reduce recall en G1 60+ de 83.33% a 58.33%. En G2 30-44 eleva recall y cambia FPR de 1/2 a 2/2. Ese 100% de FPR se basa en dos negativos; su IC Wilson abarca aproximadamente 34.24%-100%. Un recall 6/6 en logística G2 45-59 tampoco garantiza una tasa estable."))
    add(15, "Comparación de modelos", paragraph("La ventaja de accuracy de la logística equivale a dos casos correctos de 160. Los modelos coinciden en 130 predicciones y discrepan en 30: 16 son correctas solo con logística y 14 solo con árbol. Igual recall agregado no significa omitir los mismos casos. La preferencia logística es técnica y provisional; no demuestra dominancia general."), table("Tabla 8 Complejidad y recursos locales", ["Aspecto", "Logística", "Árbol"], [["Modelo serializado", "3649 bytes", "8059 bytes"], ["Estructura", "11 coeficientes y un intercepto", "Profundidad 5 nodos 51 hojas 26"], ["Iteraciones observadas", "9", "No aplica el contador logístico"], ["Arrays seleccionados", "96 bytes", "4080 bytes"], ["Mediana de ajuste controlado", "5.75755 ms", "5.46595 ms"], ["Ajustes medidos del benchmark", "10", "10"]], [6.2, 5.4, 5.4]), paragraph("El benchmark alternó el orden, incluyó un calentamiento por modelo y limitó bibliotecas nativas a un hilo: 22 ajustes totales. Los rangos se solapan. Los tiempos originales de auditoría, tomados en momentos distintos, no son esa comparación controlada. Los bytes de arrays no representan RAM total; no se midieron electricidad ni emisiones. Las explicaciones de coeficientes y reglas usan variables transformadas, sin demostrar causalidad ni comprensión humana. [E05]"))
    gap_data = []
    for level, metric, label in (("group", "recall", "Recall G1/G2"), ("group", "fpr", "FPR G1/G2"), ("intersection", "recall", "Recall interseccional"), ("intersection", "fpr", "FPR interseccional")):
        gap_data.append([label, percent(logistic["gaps"][level][metric], " pp"), percent(tree["gaps"][level][metric], " pp")])
    add(16, "Interpretación de brechas", table("Tabla 9 Brechas absolutas en puntos porcentuales", ["Comparación", "Logística", "Árbol"], gap_data, [8, 4.5, 4.5]), paragraph("La logística presenta menores brechas G1/G2 en recall y FPR. El árbol reduce ligeramente la brecha interseccional de recall, pero aumenta la de FPR. Una mejora aislada no demuestra mejora general. La prevalencia sintética del test difiere entre G1 49/101 y G2 43/59, por lo que selección, error y consecuencias deben analizarse conjuntamente."), paragraph("Los benchmarks de configuración, recall mínimo 0.68 y brechas máximas 0.16, no son límites legales ni tolerancias éticas aprobadas. Satisfacer esas comparaciones puntuales no prueba equidad ni autoriza GO. Los intervalos condicionales y el test pequeño impiden afirmar discriminación causal o ausencia de daño. [E04, E06, E08, E10]"))
    add(17, "Marco legal aplicable", paragraph("La jurisdicción confirmada es República Dominicana. La Constitución proclamada el 27-10-2024 aporta sujeción constitucional, igualdad, privacidad y hábeas data en los arts. 6, 39, 44.2 y 70. La ficha oficial consultada muestra la Ley 172-13 como vigente. [L01-L03]"), paragraph("Se revisaron ámbito y definiciones, principios, derechos y deberes del responsable y datos especialmente protegidos. La matriz legal distingue cada condición de aplicación. En el CSV declarado sintético no se acreditan titulares identificados o identificables; ello no convierte toda actividad académica en exenta. Una nueva fuente, cuenta o registro personal requiere inventario y análisis propios."), paragraph("Si se incorporaran datos personales habría que determinar fundamento pertinente, información, calidad/finalidad, seguridad/confidencialidad y atención de derechos. Las etiquetas G1/G2 no se equiparan a categorías jurídicas reales. Un filtro de cuatro nombres de columnas no demuestra anonimización ni cumplimiento integral. Las obligaciones crediticias específicas de la ley no se trasladan automáticamente a este prototipo. [L02, E07]"), paragraph("Los antecedentes legislativos de IA y datos registrados el 24-03-2026 no acreditan promulgación o su estado posterior. La referencia al Decreto 714-26 es sectorial y condicional: no se acredita inversión estatal y su publicación en Gaceta Oficial no quedó verificada. Se priorizó el PDF normativo frente a diferencias de una noticia institucional. No se declara ausencia exhaustiva de regulación ni un vínculo para aplicar automáticamente normas europeas. [L04-L06]"))
    add(18, "Marcos voluntarios", table("Tabla 10 Naturaleza de las referencias", ["Referencia", "Naturaleza", "Aporte al ejercicio"], [["NIST AI RMF 1.0", "Marco voluntario", "Organiza contexto medición y respuesta"], ["OCDE OECD LEGAL 0449", "Recomendación no vinculante", "Derechos equidad transparencia robustez responsabilidad"], ["UNESCO ética de IA 2021", "Recomendación internacional", "Proporcionalidad participación supervisión y privacidad"]], [5.1, 5.1, 6.8]), paragraph("La recomendación OCDE, adoptada en 2019 y revisada hasta mayo de 2024 en la copia consultada, orienta la evaluación. UNESCO distingue sus recomendaciones de las convenciones vinculantes y de los compromisos procedimentales estatales. La utilización de estos principios no los convierte en leyes dominicanas aplicables automáticamente ni acredita certificación. [F01-F05]"))
    ethics = ["Transparencia. Comunicar finalidad sintética límites y estado de revisión en toda presentación.", "Explicabilidad. Explicar factores y errores sin confundir asociación y causalidad y comprobar comprensión.", "Equidad. Acordar daños y criterios en contexto y considerar soportes e incertidumbre antes de aceptar tolerancias.", "Supervisión humana. Definir competencia capacidad y autoridad para revisar corregir y suspender.", "Protección de datos. Revisar necesidad procedencia acceso y conservación ante nueva información.", "Responsabilidad. Designar responsable custodiar versiones y declarar asistencia de IA y límites de verificación.", "Participación. Incorporar participación accesible si se plantea una adaptación con personas.", "Gestión de errores. Registrar señales correcciones y condiciones de retirada conservando evidencia pertinente.", "Reclamación. Proponer canal accesible privado y revisión por otra persona con plazos y autoridad acordados."]
    add(19, "Recomendaciones éticas", paragraph("Las nueve recomendaciones se vinculan con los nueve riesgos en el CSV editable. Su estado es propuesto y pendiente de aprobación; no se atribuyen decisiones éticas personales al usuario. [E07, E08]"), *[paragraph(f"ET{index:02} {text}") for index, text in enumerate(ethics, 1)])
    mitigation_rows = [
        ["M01 R01 Alta", "Datos/modelos Justificar edad y zona y comparar ablaciones o umbrales", "Informe de variables y tasas por estrato con soporte", "Desarrollo sin seleccionar sobre el test actual y revisión de criterios"],
        ["M02 R02 Alta", "Operador Diseñar revisión completa de referencia sin excluir por score", "Traza de cobertura descartes y demora", "Ensayo sin descartes automáticos y capacidad/autoridad verificadas"],
        ["M03 R03 Alta", "Operador Comparar capacidad y desplazamientos con supuestos explícitos", "Curvas de carga espera y FP por grupo", "Política revisada antes de aceptar priorización"],
        ["M04 R04 Alta", "Datos/modelos Revisar procedencia contenido accesos y conservación", "Registro de revisión sin contenido personal", "Revisión ampliada antes de admitir nuevas fuentes"],
        ["M05 R05 Alta", "Datos/modelos Acreditar etiqueta generador y disponibilidad temporal", "Ficha y protocolo con supuestos verificables", "Resolver supuestos operativos o mantener explícitos los vacíos"],
        ["M06 R06 Alta", "Responsable académico Definir autoridad y revisión de alcance", "Registro de autorizaciones y revisión de interfaz", "Cambio de finalidad evaluado y autorizado sin equiparar GO a aprobación"],
        ["M07 R07 Media", "Datos/modelos Verificar pruebas y reproducción aislada", "Comandos versiones hashes y discrepancias", "Salidas reales y diferencias explicadas sin atribuir revisión independiente"],
        ["M08 R08 Alta", "Responsable académico Proponer canal y otra persona revisora", "Solicitud y respuesta sintéticas y evaluación de acceso", "Autoridad asignada y plazo acordado antes de afirmar eficacia"],
        ["M09 R09 Alta", "Datos/modelos Proponer custodia confiable y revisión de cambios", "Referencia de confianza y diferencias revisadas", "Cambios explicados sin presentar un hash como firma o control de acceso"],
    ]
    add(20, "Medidas de mitigación", paragraph("El plan completo identifica acción, responsable funcional propuesto, prioridad, evidencia esperada, indicador y condición de cumplimiento para cada riesgo. Las prioridades alta/media ordenan la revisión; no recalculan probabilidades ni aceptan riesgos. Los roles no tienen designación nominal. [E08]"), table("Tabla 11 Plan propuesto y evidencia esperada", ["Medida y prioridad", "Acción y rol propuestos", "Evidencia e indicador", "Condición propuesta"], mitigation_rows, [2.0, 5.4, 4.5, 5.1]), paragraph("Ya se verificaron controles técnicos, auditorías y reproducción local. No se ejecutaron ensayos de mitigación predictiva, de capacidad, de participación o de reclamación. La reproducción de Fase 7 aporta evidencia a M07 sin demostrar revisión humana independiente. Los residuales originales se conservan y su aceptabilidad sigue pendiente."))
    tradeoffs = [["Rendimiento", "Mismo recall global con dos FP menos en logística; una política distinta puede mover ambos errores"], ["Equidad", "Menores brechas G1/G2 no implican mejora de todas las intersecciones"], ["Interpretabilidad", "Coeficientes compactos o rutas de árbol no garantizan comprensión ni justifican variables"], ["Privacidad", "Menos información puede cambiar predicción y auditoría; necesidad y fundamento requieren revisión"], ["Seguridad", "Hashes y filtros no equivalen a autenticación control de acceso o prevención"], ["Complejidad", "Cinco variables y once columnas transformadas requieren mantenimiento y explicación"], ["Cómputo", "Menor tamaño o tiempo local no acredita ahorro energético ni coste humano"], ["Supervisión", "Revisión completa puede aumentar carga; autoridad capacidad y eficacia necesitan evidencia"]]
    add(21, "Trade offs", table("Tabla 12 Compromisos que requieren revisión conjunta", ["Dimensión", "Compromiso"], tradeoffs, [3.5, 13.5]), paragraph("No se fija una ponderación de FN y FP o un nivel aceptable de brecha en nombre del usuario. Una modificación debe mostrar tanto mejoras como deterioros y respetar el conjunto de restricciones. La validación de futuros cambios usaría desarrollo dentro de entrenamiento y un nuevo test final; más datos sintéticos no bastan para acreditar uso real. [E05, E08]"))
    options = [["Desplegar", "Beneficio operacional no demostrado; errores y gobernanza insuficientes", "Nueva evaluación integral y aprobaciones propias", "No recomendado con esta evidencia"], ["Modificar", "Permite estudiar sensibilidad; puede sobreajustar o trasladar daño", "Protocolo y test final independiente", "Opción experimental futura"], ["Limitar", "Conserva aprendizaje; persiste riesgo de extrapolación", "Alcance sintético límites y revisión pendiente", "Recomendación para el alcance actual"], ["No utilizar", "Evita dependencia predictiva; revisión manual también requiere capacidad", "Alternativa cronológica y retirada ante incumplimientos", "Alternativa para decisiones y fallos"]]
    add(22, "Decisión final", paragraph("Se recomienda LIMITAR el sistema a demostración y auditoría académicas con datos sintéticos. La recomendación y la aceptación del riesgo permanecen pendientes de aprobación. Se mantiene REVIEW como estado documental y la preferencia provisional por logística como referencia experimental; el árbol se conserva para comparar. [E08]"), table("Tabla 13 Cuatro alternativas de uso", ["Alternativa", "Ventaja y desventaja", "Condición", "Valoración técnica"], options, [2.4, 6.1, 4.5, 4.0]), paragraph("Limitar el uso actual puede combinarse con futuras modificaciones experimentales y la alternativa de revisión completa. La continuación del expediente no aprueba despliegue real. Ante datos personales no previstos, pérdida de carácter sintético, cambio de finalidad, fallos pertinentes o discrepancias de integridad, se propone suspender el uso de resultados afectados y revisar la causa, conservando evidencia sin difundir información personal."))
    add(23, "Limitaciones", paragraph("La muestra es exclusivamente sintética y el test solo tiene 160 casos. La etiqueta, generador y disponibilidad temporal de predictores no cuentan con documentación suficiente para una aplicación real. Las métricas y sus intervalos son descriptivos y condicionales; el holdout ya se inspeccionó y no permite seleccionar cambios y seguir tratándolo como evaluación final independiente."), paragraph("No se midieron eficacia de una cola, costes de errores, comprensión humana, participación de afectados, apelación, custodia independiente, seguridad integral, RAM máxima, electricidad o emisiones. Las pruebas no acreditan legalidad o equidad ni implementan las mitigaciones propuestas. La reproducción usa la misma máquina y entorno instalado. No hay revisión independiente o aceptación humana registrada. [E01-E09]"))
    add(24, "Pruebas y reproducibilidad", table("Tabla 14 Resultados finales de pruebas únicas", ["Grupo", "Pruebas", "Resultado"], [["LAB11 impacto y privacidad", "3", "Aprobadas"], ["LAB12 logística y árbol", "4", "Aprobadas"], ["Datos preservación y gobernanza", "7", "Aprobadas"], ["Streamlit AppTest", "1", "Aprobada con conexión local permitida"], ["Total único final", "15", "Sin fallos errores u omitidas finales"]], [9, 2.3, 5.7]), paragraph("Se comprobaron 55 distribuciones y once requisitos directos/de desarrollo contra el lock, sin discrepancias, y 46 archivos Python sin errores de sintaxis. Ruff aprobó el código revisado. La copia aislada contiene 42 archivos de código/entradas y conserva outputs separados; se verificó el origen de los módulos importados."), paragraph("LAB11 reprodujo tres salidas byte a byte y preservó el registro de decisión. Dos ajustes nuevos de auditoría reprodujeron las 160 predicciones y probabilidades por modelo, métricas, tablas de soporte y hashes de los modelos en esta máquina. Los tiempos variaron y se guardaron aparte. También se entrenaron modelos dentro de las pruebas; no se instrumentó el total de llamadas a fit."), paragraph("Se conservan los intentos fallidos: caché temporal de uv, sintaxis original del simulador, ejecución complementaria inconclusa, bloqueo de socket local de AppTest y estilo. La caché del workspace y un reintento de AppTest fuera del aislamiento de red predeterminado resolvieron las restricciones. El simulador se corrigió sin ejecutarlo. La plantilla copiada para reproducción precede a un ajuste final equivalente del alias UTC; el código ejecutado y los tests permanecen idénticos. Los comandos exactos, JUnit, hashes y límites están en TEST_REPORT y evidencias de Fase 7. [E09]"))
    add(25, "Declaración de uso de IA", paragraph("Se utilizó Codex para inspeccionar materiales, proponer y modificar código, ejecutar herramientas, consultar fuentes institucionales y redactar análisis y documentos. PowerShell, Python, uv, Git, pytest y Ruff aportaron ejecuciones registradas; pandas, scikit-learn, Fairlearn, SciPy y joblib se usaron en la evaluación. No se conserva una versión exacta del servicio generativo o sus parámetros."), paragraph("La solicitud directa aportó repositorio y materiales; el texto adjunto sirvió como referencia del plan acordado. Los mensajes de continuación autorizaron trabajo por fases y Republica Dominicana confirmó jurisdicción. No equivalen a revisión humana de todos los cálculos, aceptación de riesgos o aprobación institucional. Las correcciones técnicas fueron del asistente y no se declaran como humanas."), paragraph("AI_USAGE_DECLARATION y PROMPTS_RELEVANTES identifican asistencia, límites, verificaciones y correcciones. La copia íntegra del prompt se preserva con su hash. El autor que presente la entrega debe revisar su contenido y su política académica pertinente; esta declaración no acredita que esa revisión final se haya realizado. [E09]"))
    add(26, "Conclusiones", paragraph("La integración muestra por qué unas métricas agregadas aceptables para benchmarks experimentales no bastan para decidir uso. Ambos modelos omiten 26 positivos; la logística tiene menos FP y menores brechas G1/G2, pero existen efectos distintos en intersecciones y mucha incertidumbre. La calidad y el contexto de decisión siguen siendo determinantes."), paragraph("La evidencia de pruebas y reproducción fortalece la trazabilidad del ejercicio. Los controles organizativos, la necesidad de priorizar y la aceptabilidad de errores no se derivan de ella. La recomendación sustentada es limitar el sistema al ámbito académico sintético, conservar revisión y alternativas y evaluar cualquier adaptación real como un nuevo caso. La aprobación humana permanece pendiente."))
    reference_blocks = [paragraph("Fuentes institucionales consultadas el 31 de octubre de 2026. Los identificadores coinciden con el registro de fuentes y permiten distinguir naturaleza y alcance. Las citas del cuerpo remiten a estas entradas y al catálogo local de evidencias.")]
    for source in sources:
        reference_blocks.append({"type": "reference", "id": source["id"], "text": f"{source['organization']}. {source['title']}. {source['version_or_date']}. Ubicación: {source['location']}. Consulta: 31-10-2026.", "url": source["official_url"]})
    catalogue = [
        ["E01", "student_inputs/lab11_impact.yml; stakeholders.csv; risk_register.csv", "Finalidad roles y escenarios"],
        ["E02", "reports/lab11/", "Evaluación registro puntuación y controles"],
        ["E03", "reports/lab12/logistic/ y reports/lab12/tree/", "Métricas predicciones y metadatos"],
        ["E04", "audit_support.csv; dataset_profile.json; temporal_split.csv", "Denominadores intervalos y corte"],
        ["E05", "reports/lab12/comparison/", "Comparación estructura y benchmark"],
        ["E06", "EVALUACION_INTEGRADA.md; MATRIZ_TRAZABILIDAD.csv", "Relación riesgos resultados y controles"],
        ["E07", "MARCO_LEGAL_VOLUNTARIO_ETICO.md; MATRIZ_APLICABILIDAD_LEGAL.csv; RECOMENDACIONES_ETICAS.csv", "Marco normativo y propuestas éticas"],
        ["E08", "DECISION_FINAL.md; PLAN_MITIGACION.csv; ALTERNATIVAS_USO.csv", "Plan compromisos y recomendación"],
        ["E09", "TEST_REPORT.md; AI_USAGE_DECLARATION.md; PROMPTS_RELEVANTES.md; evidencias/fase_07/", "Pruebas reproducción IA y procedencia"],
        ["E10", "configs/governance.yml", "Benchmarks experimentales y usos prohibidos"],
    ]
    reference_blocks.extend([subsection("Catálogo de evidencias editables"), paragraph("Los nombres sin raíz en E06-E09 se ubican en reports/ejercicio_07. En E01, los CSV se ubican en student_inputs. E04 utiliza los archivos de cada carpeta de modelo y los archivos comunes de reports/lab12. Los registros conservan rutas exactas y hashes."), table("Tabla 15 Catálogo local", ["ID", "Archivo o directorio", "Contenido"], catalogue, [1.4, 9.7, 5.9])])
    add(27, "Referencias", *reference_blocks)
    add(28, "Enlace al repositorio", {"type": "reference", "id": "Repositorio", "text": "Vic-developers Unidad 04 Ejercicio 07", "url": "https://github.com/Vic-developers/Unidad-04.-Ejercicio-07..git"}, paragraph("En esta sesión no se ejecutó push. El enlace identifica el remoto indicado por el usuario y no acredita que los archivos actuales estén publicados allí. Los artefactos editables y evidencias se entregan en la copia local. La continuación entre fases y la finalización de este expediente no constituyen autorización de despliegue."))
    assert [item["number"] for item in sections] == list(range(1, 29))
    return sections


class ReportDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "SectionHeading":
            text = flowable.getPlainText()
            key = f"section_{text.split()[0]}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, 0, False)
            self.notify("TOCEntry", (0, text, self.page, key))


def make_pdf(sections, charts):
    styles = getSampleStyleSheet()
    for name in ("Normal", "BodyText"):
        styles[name].fontName = "Arial"
    body = ParagraphStyle("ReportBody", fontName="Arial", fontSize=10.7, leading=14.7, spaceAfter=7, textColor=colors.black, allowWidows=0, allowOrphans=0)
    heading = ParagraphStyle("SectionHeading", parent=body, fontName="ArialBold", fontSize=14.5, leading=18, spaceBefore=14, spaceAfter=8, keepWithNext=True)
    small_heading = ParagraphStyle("SmallHeading", parent=heading, fontSize=12, leading=15)
    caption = ParagraphStyle("ReportCaption", parent=body, fontName="ArialBold", fontSize=9.8, leading=12, spaceBefore=7, spaceAfter=5, keepWithNext=True)
    table_caption = ParagraphStyle("TableCaption", parent=caption, keepWithNext=False)
    note = ParagraphStyle("ReportNote", parent=body, fontSize=8.9, leading=11.5, spaceBefore=4, spaceAfter=9)
    cell = ParagraphStyle("Cell", fontName="Arial", fontSize=9.4, leading=12.5, textColor=colors.black, splitLongWords=True)
    cell_header = ParagraphStyle("CellHeader", parent=cell, fontName="ArialBold", textColor=colors.white, fontSize=9.5)
    cell_center = ParagraphStyle("CellCenter", parent=cell, alignment=TA_CENTER)
    header_center = ParagraphStyle("HeaderCenter", parent=cell_header, alignment=TA_CENTER)
    reference = ParagraphStyle("Reference", parent=body, fontSize=9.3, leading=12.8, spaceAfter=8)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Arial", 8.5)
        canvas.setFillColor(colors.black)
        canvas.drawString(MARGIN, 1.12 * cm, "INF8239 Ejercicio 07")
        canvas.drawRightString(PAGE_W - MARGIN, 1.12 * cm, f"Página {doc.page}")
        canvas.restoreState()

    doc = ReportDoc(str(OUT / f"{STEM}.pdf"), pagesize=A4, rightMargin=MARGIN, leftMargin=MARGIN, topMargin=1.7 * cm, bottomMargin=1.8 * cm, title="Evaluación de impacto y auditoría de equidad", author="", subject="INF8239 Unidad 04 Ejercicio 07", pageCompression=1)
    frame = Frame(MARGIN, 1.8 * cm, WIDTH, PAGE_H - 3.5 * cm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="Report", frames=frame, onPage=footer))
    story = [Spacer(1, 3.2 * cm)]
    title = ParagraphStyle("CoverTitle", parent=body, fontName="ArialBold", fontSize=27, leading=33, spaceAfter=22)
    subtitle = ParagraphStyle("CoverSubtitle", parent=body, fontSize=14, leading=20, spaceAfter=13)
    for index, block in enumerate(sections[0]["blocks"]):
        style = title if index == 0 else subtitle if index <= 2 else body
        if index == 6:
            story.append(Spacer(1, 1.3 * cm))
        story.append(Paragraph(escape(block["text"]), style))
    story.extend([PageBreak(), Paragraph("Contenido", small_heading)])
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("TOCLevel", parent=body, fontSize=9.7, leading=12.8, spaceAfter=3.2, leftIndent=0, firstLineIndent=0)]
    story.extend([toc, PageBreak()])
    for section in sections[1:]:
        story.append(CondPageBreak(130 if section["blocks"][0]["type"] == "table" else 80))
        story.append(Paragraph(f"{section['number']:02} {escape(section['title'])}", heading))
        for block in section["blocks"]:
            kind = block["type"]
            if kind == "paragraph":
                story.append(Paragraph(escape(block["text"]), body))
            elif kind == "subheading":
                story.append(Paragraph(escape(block["text"]), small_heading))
            elif kind == "table":
                centered = {"ID", "L", "I", "L x I", "Residual", "n", "P / N", "Poder", "Pruebas", "Logística", "Árbol", "Recall", "Selección", "FP / N y FPR", "n (P/N)", "Recall L / A", "FPR L / A", "Selección L / A"}
                center_columns = {index for index, title in enumerate(block["headers"]) if title in centered}
                data = [[Paragraph(escape(plain(item)), header_center if index in center_columns else cell_header) for index, item in enumerate(block["headers"])]]
                data.extend([Paragraph(escape(plain(item)), cell_center if index in center_columns else cell) for index, item in enumerate(row)] for row in block["rows"])
                scale = WIDTH / sum(block["widths"])
                item = Table(data, colWidths=[value * scale for value in block["widths"]], repeatRows=1, hAlign="LEFT", splitByRow=1)
                item.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("GRID", (0, 0), (-1, -1), 0.35, GRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
                label = Paragraph(escape(block["caption"]), table_caption)
                label_height = label.wrap(WIDTH, PAGE_H)[1]
                item.wrap(WIDTH, PAGE_H)
                minimum_height = label_height + sum(item._rowHeights[:2]) + 22
                story.extend([CondPageBreak(minimum_height), label, item, Spacer(1, 8)])
            elif kind == "figure":
                story.append(Paragraph(escape(block["caption"]), caption))
                story.append(charts[block["id"]])
                story.append(Paragraph(escape(block["note"]), note))
            elif kind == "reference":
                link = f'<link href="{escape(block["url"], {chr(34): "&quot;"})}" color="#234B72">Fuente oficial</link>'
                story.append(Paragraph(f'<b>[{escape(block["id"])}]</b> {escape(plain(block["text"]))} {link}', reference))
    doc.multiBuild(story)


def make_markdown(sections):
    lines = []
    for section in sections:
        lines.extend([f"# {section['number']:02} {section['title']}", ""])
        for block in section["blocks"]:
            if block["type"] in ("paragraph", "subheading"):
                lines.extend([("## " if block["type"] == "subheading" else "") + block["text"], ""])
            elif block["type"] == "table":
                def line(values):
                    return "| " + " | ".join(plain(value).replace("|", "\\|") for value in values) + " |"
                lines.extend([block["caption"], "", line(block["headers"]), line(["---"] * len(block["headers"]))])
                lines.extend(line(row) for row in block["rows"])
                lines.append("")
            elif block["type"] == "figure":
                lines.extend([f"![{block['caption']}]({block['file']})", "", block["note"], ""])
            elif block["type"] == "reference":
                lines.extend([f"[{block['id']}] {block['text']} [Fuente oficial]({block['url']}).", ""])
    (OUT / f"{STEM}.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont("ArialBold", "C:/Windows/Fonts/arialbd.ttf"))
    facts = load("reports/ejercicio_07/evidencias/fase_06/decision_facts.json")
    assert facts["dataset"]["n"] == 640 and facts["dataset"]["test_n"] == 160
    sections = content(facts)
    charts = make_charts(facts)
    make_markdown(sections)
    (EVIDENCE / "synthesis_content.json").write_text(json.dumps(sections, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    make_pdf(sections, charts)
    outputs = [OUT / f"{STEM}.{suffix}" for suffix in ("pdf", "md")]
    print(json.dumps({"sections": len(sections), "figures": len(charts), "tables": sum(block["type"] == "table" for section in sections for block in section["blocks"]), "outputs": [{"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in outputs], "new_model_fits": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
