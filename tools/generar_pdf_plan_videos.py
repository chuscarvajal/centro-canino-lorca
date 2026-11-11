# -*- coding: utf-8 -*-
"""generar_pdf_plan_videos.py — Plan de vídeos cortos para el adiestramiento online. Chus Carvajal.

Para Juan Miguel (habla) y Juanmi (graba): cómo grabar, dónde publicar, calendario de 8 semanas
y los guiones de los 9 vídeos (1 de presentación + 8 temas, uno por artículo del blog).
Cada guion va en una ficha con foto; los textos van en celdas de tabla (los párrafos con fondo
de ReportLab se pisaban con la línea anterior).

Uso : python tools/generar_pdf_plan_videos.py
Sale: Centro canino de lorca/Plan_videos_adiestramiento_online_2026-11-11.pdf
"""
import sys, os, tempfile
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Centro canino de lorca", "Plan_videos_adiestramiento_online_2026-11-11.pdf")
WEB = "https://centrocaninodelorca.es/"
TMP = os.path.join(tempfile.gettempdir(), "plan_videos_fotos")

EMERALD = colors.HexColor("#059669"); DARK = colors.HexColor("#1c1c1c"); GREY = colors.HexColor("#6b7280")
LINEC = colors.HexColor("#E9E5D9"); LIGHT = colors.HexColor("#f1f5f4"); PALE = colors.HexColor("#f9f7f2"); AMBER = colors.HexColor("#fea619")
ss = getSampleStyleSheet()
def stl(n, **k): return ParagraphStyle(n, parent=ss["Normal"], **k)
H1  = stl("H1", fontName="Helvetica-Bold", fontSize=18, textColor=DARK, leading=21)
SUB = stl("SUB", fontName="Helvetica", fontSize=10, textColor=EMERALD, leading=13)
H2  = stl("H2", fontName="Helvetica-Bold", fontSize=12.5, textColor=EMERALD, leading=15, spaceBefore=10, spaceAfter=4)
BODY= stl("BODY", fontName="Helvetica", fontSize=9.5, textColor=DARK, leading=13.5, spaceAfter=3)
SMALL=stl("SMALL", fontName="Helvetica-Oblique", fontSize=8.5, textColor=GREY, leading=11, spaceAfter=3)
LBL = stl("LBL", fontName="Helvetica-Bold", fontSize=8, textColor=EMERALD, leading=10)
TXT = stl("TXT", fontName="Helvetica", fontSize=9.5, textColor=DARK, leading=13.5)
TIT = stl("TIT", fontName="Helvetica-Bold", fontSize=12, textColor=DARK, leading=15)
NUM = stl("NUM", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white, leading=10)
def hr(c=LINEC, w=0.8): return HRFlowable(width="100%", thickness=w, color=c, spaceBefore=5, spaceAfter=5)
def P(t, s=BODY): return Paragraph(t, s)

# (n, titulo, enlace, foto relativa a ROOT, gancho, desarrollo, cierre)
VIDEOS = [
 (0, "Quién soy y cómo funciona la consulta por videollamada", "adiestramiento-canino-online", "public/juan-miguel.jpg",
  "«Me llamo Juan Miguel, tengo 67 años y los 67 los he pasado con perros.»",
  ["Llevo 45 años resolviendo problemas de conducta en Lorca: perros que ladran, que tiran, que no hacen caso, que lo destrozan todo cuando se quedan solos.",
   "Ahora lo hago también por videollamada, para familias de toda España. No es un curso grabado: es una conversación contigo y con tu perro, en tu casa, que es donde pasa el problema.",
   "Me cuentas qué hace, te hago preguntas, te pido que me lo enseñes por cámara, y salimos con un diagnóstico y pautas concretas. Y con seguimiento para las dudas."],
  "«Si tu perro tiene un problema, escríbeme por WhatsApp. El número está en la web. Te respondo yo.»"),
 (1, "Mi perro ladra cuando se queda solo", "blog/mi-perro-ladra-cuando-se-queda-solo", "Centro canino de lorca/FOTOS POSTS GBP/L3-07-adiestramiento-se-queda-solo.jpg",
  "«¿Tu perro ladra cuando te vas y los vecinos ya se quejan? No es un perro malo. Es un perro que lo pasa mal solo.»",
  ["Casi siempre es una de tres cosas: nunca aprendió a estar solo, le sobra energía, o tú le estás diciendo que irte es un drama con despedidas y recibimientos de película.",
   "Lo que no sirve: la bronca al volver (no la relaciona) y los collares antiladridos (tapan el síntoma y suben la angustia).",
   "Lo que sí: paseo de verdad antes de salir, salir y entrar sin ceremonias, y enseñarle a estar solo por tramos cortos, no de cero a ocho horas."],
  "«Si llevas semanas así y no mejora, cuéntamelo. Lo vemos por videollamada.»"),
 (2, "Ansiedad por separación: cómo saber si es eso", "blog/ansiedad-por-separacion-en-perros", "public/hero-home-3.webp",
  "«Hay perros que ladran un rato cuando te vas y hay perros que lo pasan mal de verdad. No es lo mismo.»",
  ["Señales de ansiedad: se pone nervioso antes de que salgas, cuando coges las llaves; ladra o llora sin parar durante horas; destroza la puerta o la ventana; se hace pis aunque acabe de salir; babea, tiembla; te sigue por toda la casa.",
   "Si ves tres o cuatro de estas, no es aburrimiento. Y no se arregla con un truco ni con una jaula.",
   "Se arregla con diagnóstico (casi siempre es de manejo) y un plan por pasos: que aprenda a estar en otra habitación contigo en casa, que las llaves dejen de ser una amenaza, ausencias de segundos, luego minutos."],
  "«Grábale los primeros diez minutos cuando te vas y mándamelo. Con eso ya te digo mucho.»"),
 (3, "Mi perro no viene cuando lo llamo", "blog/mi-perro-no-hace-caso", "public/clases-adiestramiento-canino-lorca.webp",
  "«Lo llamas en el parque y hace como que no te oye. Te voy a decir por qué.»",
  ["Porque «ven» ha significado muchas veces «se acabó lo bueno»: fin del juego, correa y a casa. El perro no es tonto.",
   "Y porque lo has repetido diez veces: si lo dices una vez y no funciona, el problema no es el volumen.",
   "Hay que volver a construir la llamada: que venir sea siempre buena noticia, premiar en el momento, y practicar donde no hay distracciones antes de pedirlo en el parque lleno de perros."],
  "«Elige un solo problema y empieza por ahí. Si quieres que lo veamos juntos, escríbeme.»"),
 (4, "Mi perro tira de la correa", "blog/mi-perro-tira-de-la-correa", "Centro canino de lorca/FOTOS POSTS GBP/04-adiestramiento-diagnostico.jpg",
  "«¿Vuelves del paseo con el brazo dolorido? Tu perro tira por una razón muy simple: porque funciona.»",
  ["Cada vez que tira y tú sigues andando, aprende que tirar es la forma de avanzar. No es dominancia ni quiere ser el líder. Es aprendizaje, y lo has reforzado tú sin querer.",
   "Lo que no lo arregla: el collar de pinchos, los tirones y el extensible, que le enseña a tirar.",
   "Lo que sí: correa tensa, te paras; correa floja, seguís. Sin bronca. Y gastarle la energía antes de pedirle calma."],
  "«En una o dos semanas se nota, si eres constante. Si no lo consigues, lo miramos por videollamada.»"),
 (5, "¿El problema es tu perro o eres tú?", "adiestramiento-canino-lorca", "public/hero-home-1.webp",
  "«Te voy a decir algo que casi nadie te dice: muchas veces el perro no tiene ningún problema. El problema es cómo se le maneja.»",
  ["En 45 años he visto miles de casos y casi siempre es de manejo. Y eso es buena noticia, porque lo que haces tú se puede cambiar.",
   "Por eso lo primero que hago es el diagnóstico. En Lorca, el perro se queda una semana conmigo, normalizo el trato, y te digo qué pasa de verdad. Por videollamada, lo veo en tu casa.",
   "Para cambiar la conducta tienes que entrar en su mundo y saber cómo funcionan ellos. Lo demás es suerte."],
  "«Cuéntame qué hace tu perro y te digo con sinceridad si puedo ayudarte.»"),
 (6, "Un perro mayor sí aprende", "adiestramiento-canino-lorca", "Centro canino de lorca/FOTOS POSTS GBP/L3-05-pastor-aleman-adulto.jpg",
  "«Mi perro ya es mayor, ya no cambia. Eso es mentira.»",
  ["El perro adulto que nunca fue educado y el que lleva años con una maña tienen los dos solución con el método correcto.",
   "En cuanto tú cambias lo que tienes que cambiar, el perro se comporta de otra forma. La edad no es el problema; el método sí importa.",
   "Lo que sí es verdad: cuanto más tiempo lleve haciéndolo, más lo tiene aprendido. Así que cuanto antes empieces, mejor."],
  "«Si tienes un perro de ocho años que tira, ladra o no hace caso, escríbeme. Se puede.»"),
 (7, "Caniche gigante con niños", "blog/caniche-gigante-familias-con-ninos", "Centro canino de lorca/FOTOS POSTS GBP/03-caniche-gigante-dcopo.jpg",
  "«¿Buscas un perro para una familia con niños y no quieres pelos por casa? Te presento al caniche gigante.»",
  ["Tranquilo, muy sociable, listísimo: aprende las normas de casa en días. Y no suelta pelo, por eso lo eligen familias con alergia.",
   "Es grande, de 45 a 60 centímetros, y como cualquier perro grande, con niños pequeños siempre con un adulto delante. Pero con un caniche bien criado la supervisión es por sentido común, no por miedo.",
   "El carácter no es automático: sale de seleccionar a los padres y de socializar a los cachorros desde el primer día. Pide ver a los padres y el informe veterinario antes de decidir."],
  "«Si quieres conocerlos, estamos en Lorca. Y si tienes dudas de si es vuestra raza, pregúntame.»"),
 (8, "Cómo elegir un perro de protección", "blog/como-elegir-un-perro-de-proteccion", "Centro canino de lorca/FOTOS POSTS GBP/05-pastor-aleman-trabajo.jpg",
  "«Criar bien a un perro no garantiza que sirva para proteger. Te lo dice alguien que lleva 45 años criándolos.»",
  ["Un perro de protección de verdad necesita: sistema nervioso equilibrado, un físico sano, vínculo fuerte con su guía y valor para afrontar situaciones difíciles. Lo primero es el equilibrio: un perro nervioso no protege, reacciona.",
   "Incluso si lo quieres «solo para casa», sé exigente: va a vivir con niños, visitas y el cartero. Tiene que saber distinguir.",
   "Y lo que pones tú: un perro de trabajo necesita trabajo. Si no vas a poder dárselo, elige otra raza. Prefiero decírtelo antes que venderte un cachorro."],
  "«Cuéntame cómo vivís y para qué lo quieres. A veces la respuesta es «mejor otro perro», y también te lo diré.»"),
]

CALENDARIO = [("Semana 1", "Vídeo 0 (presentación) + vídeo 1", "La presentación va a la página de la consulta online; el 1 a YouTube, Instagram y Google Business"),
              ("Semana 2", "Vídeo 2", "Ansiedad por separación"), ("Semana 3", "Vídeo 3", "No viene cuando lo llamo"),
              ("Semana 4", "Vídeo 4", "Tira de la correa"), ("Semana 5", "Vídeo 5", "¿El problema es tu perro o eres tú?"),
              ("Semana 6", "Vídeo 6", "Un perro mayor sí aprende"), ("Semana 7", "Vídeo 7", "Caniche gigante con niños"),
              ("Semana 8", "Vídeo 8", "Cómo elegir un perro de protección")]

def foto_jpg(rel, ancho_px=520):
    """Copia la foto a JPG (recorte 4:3) para ReportLab."""
    os.makedirs(TMP, exist_ok=True)
    dst = os.path.join(TMP, os.path.splitext(os.path.basename(rel))[0] + ".jpg")
    im = PILImage.open(os.path.join(ROOT, rel)).convert("RGB")
    w, h = im.size
    objetivo = 4 / 3
    if w / h > objetivo:
        nw = int(h * objetivo); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / objetivo); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((ancho_px, int(ancho_px * 3 / 4)), PILImage.LANCZOS)
    im.save(dst, "JPEG", quality=85)
    return dst

def tabla(filas, anchos, cabecera=True):
    t = Table(filas, colWidths=[cm * a for a in anchos])
    estilo = [("GRID", (0, 0), (-1, -1), 0.4, LINEC), ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 6)]
    if cabecera:
        estilo += [("BACKGROUND", (0, 0), (-1, 0), EMERALD), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(estilo))
    return t

def ficha(n, titulo, enlace, foto, gancho, ideas, cierre):
    """Ficha de un vídeo: foto a la izquierda, guion en celdas a la derecha."""
    img = Image(foto_jpg(foto), width=4.6 * cm, height=3.45 * cm)
    num = Table([[Paragraph(f"VÍDEO {n} · 60-90 s", NUM)]], colWidths=[4.6 * cm])
    num.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), EMERALD), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    izquierda = [img, Spacer(1, 4), num]
    filas = [[Paragraph("GANCHO · 3 primeros segundos", LBL), Paragraph(gancho, TXT)],
             [Paragraph("DESARROLLO · 40-60 s", LBL), [Paragraph("• " + i, TXT) for i in ideas]],
             [Paragraph("CIERRE · 10 s", LBL), Paragraph(cierre, TXT)]]
    guion = Table(filas, colWidths=[3.2 * cm, 9.1 * cm])
    guion.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BACKGROUND", (0, 1), (-1, 1), PALE),
                               ("LINEBELOW", (0, 0), (-1, -2), 0.6, colors.white), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                               ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7)]))
    derecha = [Paragraph(titulo, TIT), Spacer(1, 5), guion, Spacer(1, 3),
               Paragraph(f"Enlace que pongo en la descripción: {WEB}{enlace}", SMALL)]
    ficha_t = Table([[izquierda, derecha]], colWidths=[4.9 * cm, 12.5 * cm])
    ficha_t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), 8),
                                 ("LINEBELOW", (0, 0), (-1, -1), 0.6, LINEC), ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 6)]))
    return KeepTogether([ficha_t, Spacer(1, 6)])

s = [P("Plan de vídeos cortos para el adiestramiento online", H1),
     P("Centro Canino de Lorca · 9 guiones de 60-90 segundos · Chus Carvajal · 11 de noviembre de 2026", SUB), hr(EMERALD, 1.3),
     P("<b>Para qué sirve esto.</b> Hoy la página de adiestramiento online no la encuentra nadie fuera de Lorca: en Google la búsqueda la ocupan "
       "academias que venden cursos para hacerse adiestrador. Los vídeos cortos son la forma más rápida de que te vea gente de toda España, porque "
       "YouTube e Instagram los enseñan a quien tiene un perro con ese problema aunque no te conozca. Un vídeo a la semana, 60-90 segundos, tú "
       "hablando como hablas por teléfono. Juanmi graba, yo publico y pongo los enlaces.", BODY),
     P("Cómo grabar", H2)]
for t in ["<b>Móvil en vertical</b>, a la altura de los ojos, apoyado o en la mano de Juanmi. Nada de trípode profesional.",
          "<b>Luz de frente</b>: en el exterior del centro a media mañana o media tarde, con el sol de cara o en sombra abierta. Nunca con el sol detrás.",
          "<b>Sin ruido</b>: lejos de los perros que ladran. Si hay viento, de espaldas al viento o dentro.",
          "<b>Mirar a la cámara</b> (al puntito, no a la pantalla) y hablar como hablas por teléfono. Los guiones son ideas, no texto para memorizar.",
          "<b>Primera frase en los 3 primeros segundos</b>: es la que decide si la gente sigue viendo. Está marcada como «gancho».",
          "<b>Última frase siempre la misma</b>: «escríbeme por WhatsApp, el número está en la web». Es lo que convierte el vídeo en llamadas.",
          "<b>Una toma seguida</b>. Si te equivocas, paras un segundo y repites la frase: yo lo corto. No hace falta que salga perfecto; hace falta que salga tú.",
          "<b>Si sale un perro en el vídeo, mejor</b>: contigo al lado, atado, tranquilo. Vende más que cualquier palabra."]:
    s.append(P("• " + t, BODY))
s += [P("Dónde se publica cada vídeo", H2),
      tabla([[P("<b>Sitio</b>", BODY), P("<b>Qué hacemos</b>", BODY), P("<b>Quién</b>", BODY)],
             [P("YouTube (canal del centro)", BODY), P("Cada vídeo como Short y, los más largos, como vídeo normal. Título con el problema, descripción con el enlace a la web.", BODY), P("Chus", BODY)],
             [P("Instagram @juanmi_marin._ y @centrocaninodelorca", BODY), P("Reel con el mismo vídeo. Enlace a la web en la biografía.", BODY), P("Juanmi", BODY)],
             [P("Facebook del centro", BODY), P("El mismo vídeo con el enlace en el primer comentario.", BODY), P("Chus", BODY)],
             [P("Página de adiestramiento online", BODY), P("El vídeo 0 (presentación) incrustado en la página, para que quien llega vea a Juan Miguel antes de escribir.", BODY), P("Chus", BODY)],
             [P("Google Business", BODY), P("Un post con el vídeo cada dos semanas, enlazando al artículo del blog correspondiente.", BODY), P("Chus", BODY)]],
            [4.2, 10.0, 2.6]),
      P("Calendario de 8 semanas", H2),
      tabla([[P("<b>Semana</b>", BODY), P("<b>Vídeo</b>", BODY), P("<b>Tema</b>", BODY)]] + [[P(a, BODY), P(b, BODY), P(c, BODY)] for a, b, c in CALENDARIO], [2.4, 5.0, 9.4]),
      P("Si se graban varios el mismo día (recomendado: una mañana, cuatro o cinco vídeos), yo los voy publicando uno por semana.", SMALL),
      Spacer(1, 10), hr(EMERALD, 1.3), P("Los guiones", H1),
      P("Ideas para contar, no texto para leer. Gancho en los 3 primeros segundos, cierre siempre con el WhatsApp. La foto es orientativa: la que mejor pega con el tema.", SUB), Spacer(1, 6)]
for v in VIDEOS:
    s.append(ficha(*v))
s += [P("Lo que necesito de vosotros", H2),
      P("1. Una mañana de grabación con Juanmi: con los 9 guiones delante se hacen en una hora. 2. Que me mandéis los vídeos por WhatsApp o Drive tal cual, sin editar. "
        "3. El precio de la consulta online, para ponerlo en la web y decirlo en el vídeo 0 si queréis.", BODY),
      Spacer(1, 8), hr(EMERALD, 1.1), P("Chus Carvajal", stl("F", fontName="Helvetica-Bold", fontSize=10.5, textColor=DARK))]

SimpleDocTemplate(OUT, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.5 * cm, bottomMargin=1.4 * cm,
                  title="Plan de vídeos — adiestramiento online — Centro Canino de Lorca", author="Chus Carvajal").build(s)
print("PDF generado:", os.path.relpath(OUT, ROOT), "|", round(os.path.getsize(OUT) / 1024, 1), "KB")
