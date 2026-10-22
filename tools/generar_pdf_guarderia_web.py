# -*- coding: utf-8 -*-
"""
Parte de trabajo — Nueva página "Guardería canina de día" en la web del Centro Canino de Lorca.
Documenta lo que pidió Juan Miguel (WhatsApp del 22-oct-2026 con el cartel) y lo que se ha hecho.
Mismo estilo visual que generar_informe_cambios_web.py.

Uso : python tools/generar_pdf_guarderia_web.py
Sale: Centro canino de lorca/Parte_Trabajo_Guarderia_de_dia_2026-10-22.pdf
"""
import sys, os, datetime
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                HRFlowable, KeepTogether, PageBreak)
from reportlab.lib.colors import HexColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Centro canino de lorca", "Parte_Trabajo_Guarderia_de_dia_2026-10-22.pdf")
FECHA = datetime.date(2026, 10, 22)

DARK = HexColor("#1a1a2e"); BRAND = HexColor("#16213e"); ACCENT = HexColor("#0f3460"); GOLD = HexColor("#e94560")
LIGHT_BG = HexColor("#f0f4f8"); MUTED = HexColor("#6b7280"); WHITE = HexColor("#ffffff"); GREEN = HexColor("#10b981")
YELLOW = HexColor("#f59e0b"); TABLE_HDR = HexColor("#0f3460"); ROW_ALT = HexColor("#f8fafc"); BORDER = HexColor("#e2e8f0")
W, H = A4
MARGIN = 18 * mm
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def fecha_es(d=FECHA):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"

def _footer(c, doc):
    c.saveState()
    c.setFillColor(BRAND); c.rect(0, 0, W, 14 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 5 * mm, "Chus Carvajal | Consultor SEO Local")
    c.drawRightString(W - MARGIN, 5 * mm, f"Pág. {doc.page}  ·  {FECHA.strftime('%d/%m/%Y')}")
    c.restoreState()

def build_cover(c, doc):
    c.saveState()
    c.setFillColor(BRAND); c.rect(0, H * 0.35, W, H * 0.65, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H * 0.33, W, 5 * mm, fill=1, stroke=0)
    c.setFillColor(LIGHT_BG); c.rect(0, 0, W, H * 0.33, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 10); c.drawCentredString(W / 2, H * 0.84, "PARTE DE TRABAJO")
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H * 0.75, "Nueva página en la web")
    c.drawCentredString(W / 2, H * 0.69, "Guardería canina de día")
    c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.line(MARGIN * 3, H * 0.66, W - MARGIN * 3, H * 0.66)
    c.setFillColor(WHITE); c.setFont("Helvetica", 14); c.drawCentredString(W / 2, H * 0.61, "Centro Canino de Lorca")
    c.setFont("Helvetica", 11); c.setFillColor(HexColor("#94a3b8")); c.drawCentredString(W / 2, H * 0.57, "Lorca, Murcia, España")
    c.setFillColor(MUTED); c.setFont("Helvetica", 9); c.drawCentredString(W / 2, H * 0.27, "Realizado por")
    c.setFillColor(DARK); c.setFont("Helvetica-Bold", 15); c.drawCentredString(W / 2, H * 0.22, "Chus Carvajal")
    c.setFillColor(MUTED); c.setFont("Helvetica", 9); c.drawCentredString(W / 2, H * 0.18, "Consultor SEO Local")
    c.setFillColor(BORDER); c.setFont("Helvetica", 8); c.drawCentredString(W / 2, H * 0.12, f"Fecha: {fecha_es()}    |    Confidencial")
    c.setFillColor(GOLD); c.rect(0, 0, W, 5 * mm, fill=1, stroke=0)
    c.restoreState()

def get_styles():
    s = {}
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, textColor=ACCENT, spaceAfter=3, spaceBefore=8, leading=16)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=9, textColor=DARK, spaceAfter=4, leading=14, alignment=TA_JUSTIFY)
    s["body_small"] = ParagraphStyle("body_small", fontName="Helvetica", fontSize=8, textColor=MUTED, spaceAfter=3, leading=12)
    s["note"] = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED, spaceAfter=4, leading=12)
    s["caption"] = ParagraphStyle("caption", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER)
    s["tbl_hdr"] = ParagraphStyle("tbl_hdr", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER)
    s["tbl_cell"] = ParagraphStyle("tbl_cell", fontName="Helvetica", fontSize=8, textColor=DARK, leading=11)
    s["tbl_cell_c"] = ParagraphStyle("tbl_cell_c", fontName="Helvetica", fontSize=8, textColor=DARK, leading=11, alignment=TA_CENTER)
    return s

def section_bar(text, st):
    tbl = Table([[Paragraph(text, st["caption"])]], colWidths=[W - 2 * MARGIN])
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT), ("TOPPADDING", (0, 0), (-1, -1), 6),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 10)]))
    return tbl

def tabla(data, widths, st):
    tbl = Table(data, colWidths=[(W - 2 * MARGIN) * x for x in widths], repeatRows=1)
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR), ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ROW_ALT]), ("TOPPADDING", (0, 0), (-1, -1), 5),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return tbl

def estado(txt, color):
    return Paragraph(txt, ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=8, textColor=color, alignment=TA_CENTER))

def bloque_cambio(num, titulo, peticion, solucion, st):
    sol = ParagraphStyle("sol", fontName="Helvetica", fontSize=9, textColor=HexColor("#065f46"), spaceAfter=6, leading=14,
                         leftIndent=8, backColor=HexColor("#ecfdf5"), borderPadding=(4, 6, 4, 6))
    pet = ParagraphStyle("pet", fontName="Helvetica", fontSize=9, textColor=HexColor("#1e40af"), spaceAfter=4, leading=14,
                         leftIndent=8, backColor=HexColor("#eff6ff"), borderPadding=(4, 6, 4, 6))
    return KeepTogether([Paragraph(f"{num}. {titulo}", st["h2"]),
                         Paragraph("<b>Lo que pidió Juan Miguel:</b> " + peticion, pet),
                         Paragraph("<b>Lo que se ha hecho:</b> " + solucion, sol), Spacer(1, 6)])

def build_pdf(output_path):
    st = get_styles()
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=20 * mm,
                            title="Parte de Trabajo — Guardería canina de día — Centro Canino de Lorca", author="Chus Carvajal",
                            subject="Nueva página de guardería de día en la web", creator="Chus Carvajal | Consultor SEO Local")
    story = [PageBreak()]

    story += [section_bar("RESUMEN DEL TRABAJO REALIZADO", st), Spacer(1, 6),
              Paragraph(f"Fecha: <b>{fecha_es()}</b>  |  Negocio: <b>Centro Canino de Lorca</b>  |  "
                        "Página nueva: <b>centrocaninodelorca.es/guarderia-canina-lorca</b>", st["body_small"]), Spacer(1, 6),
              Paragraph("Juan Miguel envió por WhatsApp el cartel del nuevo servicio de <b>guardería de día</b> (1,50 € la hora; a partir "
                        "de 10 horas no se sigue pagando) y preguntó si se podía incorporar a la web. Se ha creado una página propia "
                        "para el servicio, se ha enlazado desde el menú de todas las páginas, desde la portada y desde la página de "
                        "residencia, y se ha publicado en la web real. El objetivo es doble: que quien ya conoce el centro encuentre el "
                        "servicio y su precio sin llamar, y que quien busque en Google «guardería canina Lorca» llegue a una página que "
                        "habla exactamente de eso.", st["body"]), Spacer(1, 8)]
    resumen = [[Paragraph("CAMBIO REALIZADO", st["tbl_hdr"]), Paragraph("ÁMBITO", st["tbl_hdr"]), Paragraph("ESTADO", st["tbl_hdr"])]]
    for cambio, ambito in [
        ("Nueva página «Guardería canina de día en Lorca» con precio, horario por horas y preguntas frecuentes", "Página nueva"),
        ("Enlace «Guardería de día» en el menú de servicios (ordenador y móvil) de las 13 páginas", "Toda la web"),
        ("Tarjeta destacada «Nuevo servicio» en la portada y mención en el texto de «Nosotros»", "Inicio"),
        ("La página de residencia deja de llamarse «residencia y guardería» y enlaza al nuevo servicio", "Residencia"),
        ("Mapa del sitio (sitemap) actualizado para que Google descubra la página", "Google"),
        ("Publicación en producción (Netlify)", "Web en vivo"),
    ]:
        resumen.append([Paragraph(cambio, st["tbl_cell"]), Paragraph(ambito, st["tbl_cell_c"]), estado("HECHO", GREEN)])
    story += [tabla(resumen, [0.58, 0.22, 0.20], st), Spacer(1, 10), HRFlowable(width="100%", thickness=0.5, color=BORDER), Spacer(1, 8)]

    story += [section_bar("DETALLE DE LOS CAMBIOS", st), Spacer(1, 8)]
    story.append(bloque_cambio(1, "Página nueva: guardería canina de día",
        "«Os presentamos nuestro nuevo servicio. Si te vas al trabajo o te ausentas de casa y el perro ladra, tus vecinos se quejan "
        "y esto te supone un problema, no dudes en acudir a nosotros». Cartel con 1,50 €/hora, «a partir de 10 h/día no sigues "
        "pagando», amplios espacios exteriores, agua siempre disponible, actividades y juego y atención profesional.",
        "Se ha creado la página <b>centrocaninodelorca.es/guarderia-canina-lorca</b> con el mismo diseño que el resto de la web. "
        "Arranca con el problema real del cliente (el perro que ladra solo en casa y los vecinos) y explica la solución. Incluye el "
        "<b>precio claro</b> (1,50 € la hora, tope a partir de 10 horas: un día nunca pasa de 15 €), las cuatro ventajas del cartel, "
        "la diferencia entre guardería de día y residencia, los requisitos (vacunas y antiparasitario), nueve preguntas frecuentes, "
        "las reseñas de Google y un formulario que abre WhatsApp con el horario del cliente. Como el centro es también de "
        "adiestramiento, la página enlaza al curso para quien quiera resolver de raíz la ansiedad por separación. Las fotos son "
        "las reales del centro (zona verde, jardín con sombra y boxes).", st))
    story.append(bloque_cambio(2, "Menú y portada",
        "Que el servicio se vea en la web.",
        "El menú de servicios de todas las páginas (ordenador y móvil) tiene ahora la entrada <b>«Guardería de día»</b>, justo "
        "debajo de «Residencia canina». En la portada se ha añadido una tarjeta ancha con la etiqueta <b>«Nuevo servicio»</b> y el "
        "precio, en primer lugar dentro del bloque de servicios, y el texto de «Nosotros» también lo menciona y enlaza.", st))
    story.append(bloque_cambio(3, "Página de residencia",
        "(Ajuste necesario para que Google no confunda los dos servicios.)",
        "Hasta ahora la página de residencia se titulaba «Residencia y guardería canina» porque no existía la guardería de día. "
        "Ahora cada servicio tiene su página: la de residencia habla solo de residencia (vacaciones, puentes, estancias con noche) y "
        "enlaza a la guardería de día en tres sitios (sección de vacaciones y dos preguntas frecuentes). Así, quien busque "
        "«guardería» llega a la guardería y quien busque «residencia» llega a la residencia.", st))
    story.append(bloque_cambio(4, "Google y publicación",
        "Dejarlo publicado y visible.",
        "La página está publicada en la web real y añadida al mapa del sitio que lee Google. Hasta hoy, la búsqueda "
        "«guardería canina lorca» la respondía la página de residencia (posición media 3,6 en los últimos tres meses, 324 "
        "apariciones). Al tener ahora una página propia, es normal que esa posición <b>baile durante dos o cuatro semanas</b> "
        "mientras Google reasigna la búsqueda a la página nueva. Lo revisaré en Search Console a finales de noviembre.", st))
    story += [Spacer(1, 2), HRFlowable(width="100%", thickness=0.5, color=BORDER), Spacer(1, 8)]

    story += [section_bar("DOS DATOS A CONFIRMAR", st), Spacer(1, 6),
              Paragraph("Para dejar la página cerrada necesito que me confirmes dos cosas del cartel:", st["body"])]
    pend = [[Paragraph("DATO", st["tbl_hdr"]), Paragraph("CÓMO ESTÁ EN LA WEB", st["tbl_hdr"]), Paragraph("ESTADO", st["tbl_hdr"])]]
    pend.append([Paragraph("¿El precio de 1,50 € la hora es con IVA incluido? (en la residencia la web indica «18 € + IVA»)", st["tbl_cell"]),
                 Paragraph("Se muestra «1,50 € la hora» tal cual, sin mencionar el IVA", st["tbl_cell_c"]), estado("PENDIENTE", YELLOW)])
    pend.append([Paragraph("El cartel lleva un segundo teléfono (605 79 23 79) que no aparece en ningún sitio de la web ni en la ficha de Google", st["tbl_cell"]),
                 Paragraph("Solo el 670 36 06 76, el mismo que Google y el resto de la web", st["tbl_cell_c"]), estado("PENDIENTE", YELLOW)])
    story += [tabla(pend, [0.50, 0.30, 0.20], st), Spacer(1, 4),
              Paragraph("Nota: mantener un único teléfono en web, Google y directorios ayuda al posicionamiento local. Si el 605 es el "
                        "del servicio de guardería y quieres que aparezca, se puede añadir en la página indicando para qué es.", st["note"]),
              Spacer(1, 8)]

    story += [section_bar("VERIFICACIÓN REALIZADA", st), Spacer(1, 6)]
    verif = [[Paragraph("COMPROBACIÓN", st["tbl_hdr"]), Paragraph("RESULTADO", st["tbl_hdr"])]]
    for txt in ["La página nueva se ve bien en ordenador (1366 px) y en móvil (390 px)",
                "El enlace «Guardería de día» aparece en el menú de las 13 páginas, en ordenador y en móvil",
                "La tarjeta «Nuevo servicio» de la portada enlaza a la página nueva",
                "Los datos estructurados para Google (preguntas frecuentes, servicio y precio) validan sin errores",
                "Los botones de llamada y WhatsApp quedan registrados en el panel de clics de la web",
                "La página responde en la web real y figura en el mapa del sitio"]:
        verif.append([Paragraph(txt, st["tbl_cell"]), estado("Correcto", GREEN)])
    story += [tabla(verif, [0.70, 0.30], st), Spacer(1, 12)]

    story += [HRFlowable(width="100%", thickness=1, color=GOLD), Spacer(1, 6)]
    firma = Table([[Paragraph("<b>Chus Carvajal</b><br/>Consultor SEO Local<br/>carvajalphotos@gmail.com",
                              ParagraphStyle("firma", fontName="Helvetica", fontSize=9, textColor=DARK, leading=14)),
                    Paragraph(f"Parte de trabajo generado el {fecha_es()}<br/>Este documento es de carácter confidencial y está destinado<br/>"
                              "exclusivamente al cliente indicado.",
                              ParagraphStyle("disc", fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED, leading=12, alignment=TA_RIGHT))]],
                  colWidths=[(W - 2 * MARGIN) * 0.5] * 2)
    firma.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4)]))
    story.append(firma)

    def _page(c, d):
        build_cover(c, d) if d.page == 1 else _footer(c, d)
    doc.build(story, onFirstPage=_page, onLaterPages=_page)
    print("PDF generado:", os.path.relpath(output_path, ROOT), "|", round(os.path.getsize(output_path) / 1024, 1), "KB")

if __name__ == "__main__":
    build_pdf(OUT)
