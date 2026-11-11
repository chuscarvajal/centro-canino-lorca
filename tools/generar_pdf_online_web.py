# -*- coding: utf-8 -*-
"""
Parte de trabajo — Adiestramiento online: reenfoque de la página, página para la Región de Murcia,
blog con 8 artículos y plan de vídeos. Lo que pidió Juan Miguel (audio del 11-nov-2026) y lo que se ha hecho.

Uso : python tools/generar_pdf_online_web.py
Sale: Centro canino de lorca/Parte_Trabajo_Adiestramiento_online_2026-11-11.pdf
"""
import sys, os, datetime
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
from reportlab.lib.colors import HexColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Centro canino de lorca", "Parte_Trabajo_Adiestramiento_online_2026-11-11.pdf")
FECHA = datetime.date(2026, 11, 11)
DARK = HexColor("#1a1a2e"); BRAND = HexColor("#16213e"); ACCENT = HexColor("#0f3460"); GOLD = HexColor("#e94560")
LIGHT_BG = HexColor("#f0f4f8"); MUTED = HexColor("#6b7280"); WHITE = HexColor("#ffffff"); GREEN = HexColor("#10b981")
YELLOW = HexColor("#f59e0b"); TABLE_HDR = HexColor("#0f3460"); ROW_ALT = HexColor("#f8fafc"); BORDER = HexColor("#e2e8f0")
W, H = A4; MARGIN = 18 * mm
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
def fecha_es(d=FECHA): return f"{d.day} de {MESES[d.month - 1]} de {d.year}"

def _footer(c, doc):
    c.saveState(); c.setFillColor(BRAND); c.rect(0, 0, W, 14 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 5 * mm, "Chus Carvajal | Consultor SEO Local")
    c.drawRightString(W - MARGIN, 5 * mm, f"Pág. {doc.page}  ·  {FECHA.strftime('%d/%m/%Y')}"); c.restoreState()

def build_cover(c, doc):
    c.saveState()
    c.setFillColor(BRAND); c.rect(0, H * 0.35, W, H * 0.65, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H * 0.33, W, 5 * mm, fill=1, stroke=0)
    c.setFillColor(LIGHT_BG); c.rect(0, 0, W, H * 0.33, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 10); c.drawCentredString(W / 2, H * 0.84, "PARTE DE TRABAJO")
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, H * 0.75, "Adiestramiento online:")
    c.drawCentredString(W / 2, H * 0.69, "web, Murcia, blog y vídeos")
    c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.line(MARGIN * 3, H * 0.66, W - MARGIN * 3, H * 0.66)
    c.setFillColor(WHITE); c.setFont("Helvetica", 14); c.drawCentredString(W / 2, H * 0.61, "Centro Canino de Lorca")
    c.setFont("Helvetica", 11); c.setFillColor(HexColor("#94a3b8")); c.drawCentredString(W / 2, H * 0.57, "Lorca, Murcia, España")
    c.setFillColor(MUTED); c.setFont("Helvetica", 9); c.drawCentredString(W / 2, H * 0.27, "Realizado por")
    c.setFillColor(DARK); c.setFont("Helvetica-Bold", 15); c.drawCentredString(W / 2, H * 0.22, "Chus Carvajal")
    c.setFillColor(MUTED); c.setFont("Helvetica", 9); c.drawCentredString(W / 2, H * 0.18, "Consultor SEO Local")
    c.setFillColor(BORDER); c.setFont("Helvetica", 8); c.drawCentredString(W / 2, H * 0.12, f"Fecha: {fecha_es()}    |    Confidencial")
    c.setFillColor(GOLD); c.rect(0, 0, W, 5 * mm, fill=1, stroke=0); c.restoreState()

st = {
 "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, textColor=ACCENT, spaceAfter=3, spaceBefore=8, leading=16),
 "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9, textColor=DARK, spaceAfter=4, leading=14, alignment=TA_JUSTIFY),
 "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8, textColor=MUTED, spaceAfter=3, leading=12),
 "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED, spaceAfter=4, leading=12),
 "cap": ParagraphStyle("cap", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER),
 "th": ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER),
 "td": ParagraphStyle("td", fontName="Helvetica", fontSize=8, textColor=DARK, leading=11),
 "tdc": ParagraphStyle("tdc", fontName="Helvetica", fontSize=8, textColor=DARK, leading=11, alignment=TA_CENTER),
}
def P(t, k="body"): return Paragraph(t, st[k])
def bar(t):
    tbl = Table([[P(t, "cap")]], colWidths=[W - 2 * MARGIN])
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 10)]))
    return tbl
def tabla(data, widths):
    t = Table(data, colWidths=[(W - 2 * MARGIN) * x for x in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR), ("GRID", (0, 0), (-1, -1), 0.4, BORDER), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ROW_ALT]),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return t
def estado(txt, color): return Paragraph(txt, ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=8, textColor=color, alignment=TA_CENTER))
def bloque(num, titulo, peticion, hecho):
    sol = ParagraphStyle("sol", fontName="Helvetica", fontSize=9, textColor=HexColor("#065f46"), spaceAfter=6, leading=14, leftIndent=8, backColor=HexColor("#ecfdf5"), borderPadding=(4, 6, 4, 6))
    pet = ParagraphStyle("pet", fontName="Helvetica", fontSize=9, textColor=HexColor("#1e40af"), spaceAfter=4, leading=14, leftIndent=8, backColor=HexColor("#eff6ff"), borderPadding=(4, 6, 4, 6))
    return KeepTogether([P(f"{num}. {titulo}", "h2"), Paragraph("<b>Lo que pidió Juan Miguel:</b> " + peticion, pet), Paragraph("<b>Lo que se ha hecho:</b> " + hecho, sol), Spacer(1, 6)])

story = [PageBreak(), bar("RESUMEN DEL TRABAJO REALIZADO"), Spacer(1, 6),
         P(f"Fecha: <b>{fecha_es()}</b>  |  Negocio: <b>Centro Canino de Lorca</b>  |  Servicio: <b>adiestramiento canino online</b>", "small"), Spacer(1, 6),
         P("En el audio del 11 de noviembre Juan Miguel dijo que el adiestramiento online «no está funcionando nada»: le llega gente del pueblo, nadie de fuera, "
           "y es el servicio que quiere potenciar. Los datos lo confirman: la página online ha tenido <b>cero visitas en 90 días</b> (Google Analytics) y <b>un solo clic "
           "en tres meses</b> en Google. La causa principal no es la página, es que nadie llega a ella: la búsqueda «adiestramiento canino online» la ocupan "
           "academias que venden cursos para hacerse adiestrador, no servicios para dueños con un perro con problemas. Se han hecho cuatro cosas: "
           "reenfocar la página, crear una página para toda la Región de Murcia, abrir el blog con 8 artículos y preparar el plan de vídeos.")]
rows = [[P("CAMBIO REALIZADO", "th"), P("ÁMBITO", "th"), P("ESTADO", "th")]]
for c, a, e, col in [
    ("Página online reenfocada a «adiestrador canino online por videollamada» (título, descripción y encabezado)", "Web", "HECHO", GREEN),
    ("Página nueva «Adiestramiento canino en Murcia»: presencial en Lorca, estancia con diagnóstico u online para toda la Región", "Web", "HECHO", GREEN),
    ("Blog con 8 artículos sobre conducta, razas y cuidados, cada uno con llamada a la consulta online", "Web", "HECHO", GREEN),
    ("Enlaces «Adiestramiento en Murcia» y «Blog» en el menú de todas las páginas; sitemap actualizado", "Toda la web", "HECHO", GREEN),
    ("Plan de vídeos: 9 guiones de 60-90 segundos, cómo grabar, dónde publicar y calendario de 8 semanas", "Vídeo", "HECHO", GREEN),
    ("Precio de la consulta online visible en la web", "Web", "PENDIENTE DE JM", YELLOW),
    ("Vídeo de presentación en la página online y vídeos semanales", "Vídeo", "PENDIENTE DE JM", YELLOW),
]:
    rows.append([P(c, "td"), P(a, "tdc"), estado(e, col)])
story += [tabla(rows, [0.58, 0.22, 0.20]), Spacer(1, 10), HRFlowable(width="100%", thickness=0.5, color=BORDER), Spacer(1, 8), bar("DETALLE DE LOS CAMBIOS"), Spacer(1, 8)]
story.append(bloque(1, "Página online: dejar de competir con las academias",
    "«No me está funcionando lo de los cursos online, eso no me está funcionando nada. [...] Eso es lo que tenemos que potenciar si podemos.»",
    "La página se titulaba «Adiestramiento canino online», y en Google esa búsqueda la ocupan 6 academias de cada 10 resultados. Ahora se titula "
    "<b>«Adiestrador canino online por videollamada»</b>, que es lo que busca quien tiene un perro con problemas, y la descripción nombra los casos "
    "concretos: ansiedad por separación, ladridos, miedos y agresividad. Lo que no he podido hacer todavía: poner el <b>precio</b>. Los competidores que "
    "salen en Google lo enseñan (390 € y 490 € en uno de ellos) y la página de Juan Miguel dice «te lo digo cuando me cuentes el caso». Para alguien de "
    "Madrid que compara tres webs, eso es un motivo para no escribir."))
story.append(bloque(2, "Página nueva: adiestramiento canino en Murcia",
    "(Oportunidad detectada en Search Console: la web aparece para «adiestramiento canino murcia», «educador canino murcia», «adiestrador canino murcia», "
    "«escuela de adiestramiento canino en murcia»... unas 150 impresiones en tres meses, en posiciones 23-48, sin página que las recoja.)",
    "Se ha creado <b>centrocaninodelorca.es/adiestramiento-canino-murcia</b>: para familias de Murcia capital, Cartagena, Molina de Segura, Alcantarilla o el Mar "
    "Menor. Explica las tres formas de trabajar (venir a Lorca a las 5 clases por 250 €, dejar al perro una semana para el diagnóstico, o videollamada), "
    "que Lorca está a 45 minutos por la A-7, los casos más frecuentes, el precio y 8 preguntas frecuentes. Es el mismo movimiento que hicimos con «Cachorros en "
    "Murcia», que hoy es la cuarta página con más visitas de la web."))
story.append(bloque(3, "Blog: 8 artículos para que te encuentren desde toda España",
    "Que entre gente de fuera.",
    "La única forma de que alguien de Valladolid llegue a la web es que busque su problema y lo encuentre explicado. Se ha abierto <b>centrocaninodelorca.es/blog/</b> "
    "con 8 artículos escritos con la voz de Juan Miguel: <i>Mi perro ladra cuando se queda solo</i>, <i>Ansiedad por separación</i>, <i>Mi perro no hace caso</i>, "
    "<i>Mi perro tira de la correa</i>, <i>Caniche gigante con niños</i>, <i>Cómo elegir un perro de protección</i>, <i>Cada cuánto llevar al perro a la peluquería</i> y "
    "<i>Residencia canina: qué tener en cuenta</i>. Cada uno termina con «qué puedes hacer hoy», un bloque «cuándo pedir ayuda» con el WhatsApp y la consulta online, "
    "preguntas frecuentes y enlaces al servicio en Lorca. Todo lo que dicen los artículos sale de lo que ya cuenta la web; no hay nada inventado."))
story.append(bloque(4, "Plan de vídeos cortos",
    "«Trato de 2 horas de teléfono aquí dando caña.» Esa facilidad para explicar es lo que hay que grabar.",
    "Documento aparte (<i>Plan de vídeos adiestramiento online</i>) con 9 guiones de 60-90 segundos: uno de presentación para la página online y ocho sobre los "
    "problemas de los artículos. Incluye cómo grabar con el móvil, dónde se publica cada vídeo (YouTube, Instagram, Facebook, Google Business y la web) y un "
    "calendario de 8 semanas. Juanmi graba, Chus publica."))
story += [Spacer(1, 2), HRFlowable(width="100%", thickness=0.5, color=BORDER), Spacer(1, 8), bar("LO QUE NECESITO DE JUAN MIGUEL"), Spacer(1, 6)]
rows = [[P("QUÉ", "th"), P("PARA QUÉ", "th"), P("ESTADO", "th")]]
for q, p in [("El precio de la consulta online y qué incluye (si lleva seguimiento, si hay bono)", "Ponerlo en la página online y en la de Murcia. Sin precio, la gente de fuera no escribe."),
             ("Un vídeo de un minuto hablando a cámara: quién es, qué resuelve, cómo funciona la videollamada", "Incrustarlo en la página online. Quien llega ve a Juan Miguel antes de decidir."),
             ("Una mañana de grabación con Juanmi: los 9 vídeos del plan", "Publicar uno a la semana en YouTube, Instagram, Facebook y Google Business.")]:
    rows.append([P(q, "td"), P(p, "td"), estado("PENDIENTE", YELLOW)])
story += [tabla(rows, [0.42, 0.40, 0.18]), Spacer(1, 4),
          P("Qué esperar: la página de Murcia empieza a notarse en uno o dos meses. Lo nacional (blog y vídeos) tarda de tres a seis meses. "
            "Si se quiere ir más rápido, se puede probar publicidad en Google con 5-10 € al día durante dos semanas.", "note"), Spacer(1, 8),
          bar("VERIFICACIÓN REALIZADA"), Spacer(1, 6)]
rows = [[P("COMPROBACIÓN", "th"), P("RESULTADO", "th")]]
for t in ["Las 24 páginas de la web (incluido el blog) validan los datos estructurados para Google sin errores",
          "Todos los enlaces internos y las imágenes de las páginas nuevas existen (comprobación automática)",
          "Página de Murcia y artículos del blog revisados en ordenador (1366 px) y móvil (390 px)",
          "El menú de todas las páginas muestra «Adiestramiento en Murcia» y «Blog», en ordenador y móvil",
          "Sitemap actualizado con las 10 URL nuevas y las fechas reales de cambio",
          "Publicado en la web real (Netlify) y comprobado en vivo"]:
    rows.append([P(t, "td"), estado("Correcto", GREEN)])
story += [tabla(rows, [0.70, 0.30]), Spacer(1, 12), HRFlowable(width="100%", thickness=1, color=GOLD), Spacer(1, 6)]
firma = Table([[Paragraph("<b>Chus Carvajal</b><br/>Consultor SEO Local<br/>carvajalphotos@gmail.com", ParagraphStyle("f", fontName="Helvetica", fontSize=9, textColor=DARK, leading=14)),
                Paragraph(f"Parte de trabajo generado el {fecha_es()}<br/>Este documento es de carácter confidencial y está destinado<br/>exclusivamente al cliente indicado.",
                          ParagraphStyle("d", fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED, leading=12, alignment=TA_RIGHT))]], colWidths=[(W - 2 * MARGIN) * 0.5] * 2)
firma.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4)]))
story.append(firma)

def _page(c, d): build_cover(c, d) if d.page == 1 else _footer(c, d)
SimpleDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=20 * mm,
                  title="Parte de Trabajo — Adiestramiento online — Centro Canino de Lorca", author="Chus Carvajal").build(story, onFirstPage=_page, onLaterPages=_page)
print("PDF generado:", os.path.relpath(OUT, ROOT), "|", round(os.path.getsize(OUT) / 1024, 1), "KB")
