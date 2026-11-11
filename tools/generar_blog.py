# -*- coding: utf-8 -*-
"""
generar_blog.py — Blog del Centro Canino de Lorca (Chus Carvajal)

Genera public/blog/index.html y un HTML por artículo a partir de la lista ARTICULOS,
con el mismo diseño que el resto de la web (nav, pie, tipografías, colores) y con
schema BlogPosting + BreadcrumbList + FAQPage. Copia y redimensiona las fotos a
public/blog/img/ en WebP. Cada artículo lleva una llamada a la consulta online
(toda España) y otra al servicio presencial relacionado.

Uso : python tools/generar_blog.py
Sale: public/blog/index.html, public/blog/<slug>.html, public/blog/img/*.webp
Después: añadir las URL nuevas al sitemap y ejecutar el script del menú.
"""
import sys, os, re, html
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
BLOG = os.path.join(PUBLIC, "blog")
IMG = os.path.join(BLOG, "img")
BASE = "https://centrocaninodelorca.es/"
FECHA = "2026-11-11"
WA = "https://wa.me/34670360676?text="

# (destino webp, origen relativo a ROOT, alt)
FOTOS = {
    "perro-ladra-solo":      ("public/hero-home-2.webp", "Zona exterior con sombra del Centro Canino de Lorca"),
    "ansiedad-separacion":   ("public/juan-miguel.jpg", "Juan Miguel, adiestrador y etólogo canino en Lorca"),
    "no-hace-caso":          ("public/clases-adiestramiento-canino-lorca.webp", "Clase de adiestramiento con varias familias en el Centro Canino de Lorca"),
    "tira-de-la-correa":     ("public/clases-adiestramiento-canino-lorca.webp", "Familias practicando el paseo con correa en una clase en Lorca"),
    "caniche-ninos":         ("Centro canino de lorca/FOTOS POSTS GBP/03-caniche-gigante-dcopo.jpg", "Caniche gigante blanco criado en el Centro Canino de Lorca"),
    "perro-proteccion":      ("Centro canino de lorca/FOTOS POSTS GBP/05-pastor-aleman-trabajo.jpg", "Pastor alemán de línea de trabajo del Centro Canino de Lorca"),
    "peluqueria-cada-cuanto":("Centro canino de lorca/FOTOS POSTS GBP/02-peluqueria-corte-exposicion.jpg", "Caniche gigante con corte de exposición hecho por Juanmi en Lorca"),
    "residencia-elegir":     ("public/hero-home-1.webp", "Boxes cubiertos de la residencia canina del Centro Canino de Lorca"),
}

ONLINE = "../adiestramiento-canino-online.html"
LORCA = "../adiestramiento-canino-lorca.html"
MURCIA = "../adiestramiento-canino-murcia.html"
GUARDERIA = "../guarderia-canina-lorca.html"
RESIDENCIA = "../residencia-canina-lorca.html"
PELU = "../peluqueria-canina-lorca.html"
CANICHE = "../cachorros-caniche-gigante.html"
PASTOR = "../cachorros-pastor-aleman-de-trabajo.html"

def L(href, txt):
    return f'<a href="{href}">{txt}</a>'

# ---------------------------------------------------------------------------
# ARTÍCULOS. Cada uno: slug, foto, categoria, title (SEO), meta, h1, entradilla,
# cuerpo (HTML con h2/p/ul), hoy (lista "qué hacer hoy"), cta (titulo, texto,
# servicio local href + label), faq [(p, r)], relacionados [slugs]
# ---------------------------------------------------------------------------
ARTICULOS = [
 dict(
  slug="mi-perro-ladra-cuando-se-queda-solo", foto="perro-ladra-solo", categoria="Conducta",
  title="Mi perro ladra cuando se queda solo: por qué lo hace y qué hacer",
  meta="¿Tu perro ladra o llora cuando se queda solo y los vecinos se quejan? Te explico por qué lo hace, lo que no funciona y qué puedes hacer desde hoy. Juan Miguel, 45 años con perros.",
  h1="Mi perro ladra cuando se queda solo: por qué lo hace y qué puedes hacer desde hoy",
  entradilla="Sales a trabajar, cierras la puerta y empieza el concierto. Al volver tienes una nota del vecino, o peor, una queja en la comunidad. No es un perro malo ni un perro «desobediente»: es un perro que lo pasa mal solo. Te explico lo que hay detrás y por dónde empezar.",
  cuerpo=f"""
<h2>Por qué ladra: no es rabieta, es angustia</h2>
<p>Un perro es un animal social. Que se quede solo en una casa cerrada, sin saber cuándo vuelves, no es algo que venga de serie en su naturaleza: es algo que tiene que aprender. Cuando no lo ha aprendido, ladra, llora, araña la puerta o rompe lo que pilla. No lo hace para fastidiarte ni «por venganza»; lo hace porque no sabe gestionar la situación.</p>
<p>En 45 años he visto muchas versiones del mismo caso, y casi siempre hay una de estas tres cosas detrás:</p>
<ul>
<li><strong>Nunca aprendió a estar solo.</strong> Llegó de cachorro y siempre hubo alguien en casa. El día que la rutina cambia, se le viene el mundo encima.</li>
<li><strong>Está sobrado de energía.</strong> Un perro que no ha corrido, no ha olido y no ha jugado tiene la cabeza llena de nervio. Solo en casa, ese nervio sale por la boca.</li>
<li><strong>Tú le estás diciendo que algo pasa.</strong> Las despedidas largas, el «ahora vuelvo, portate bien» con voz de pena, el recibimiento como si volvieras de la guerra. Todo eso le confirma que irte es un drama.</li>
</ul>
<h2>Lo que no funciona (y empeora el problema)</h2>
<p>Castigarlo al volver no sirve de nada: el perro no relaciona la bronca con lo que hizo hace tres horas, solo aprende que tu llegada es mala. Los collares que dan descargas o rocían citronela tapan el síntoma y suben la angustia. Y dejarle la tele puesta o un hueso no resuelve que no sepa estar solo. Son parches.</p>
<h2>Qué hay que cambiar de verdad</h2>
<p>Lo digo siempre: para cambiar la conducta tienes que entrar en su mundo y saber cómo funciona él. Y en este caso, casi siempre, lo que hay que cambiar es el manejo. Tres cosas:</p>
<p><strong>Gasta la energía antes de irte.</strong> Un paseo de verdad, con olfateo y algo de carrera, no cinco minutos para que haga pis. Un perro cansado y satisfecho se echa a dormir cuando te vas.</p>
<p><strong>Quita el drama a la salida y a la llegada.</strong> Sales sin ceremonia. Vuelves y le haces caso cuando está tranquilo, no cuando salta como un loco. Él aprende que irte y volver es lo normal.</p>
<p><strong>Enséñale a estar solo por tramos.</strong> Primero minutos, luego media hora, luego más. Si pasas de cero a ocho horas, fracasas tú y fracasa él.</p>
<h2>Si trabajas fuera todo el día</h2>
<p>Hay casos en los que el perro, simplemente, no puede pasar ocho o diez horas solo todavía. Para eso abrimos en Lorca la {L(GUARDERIA, "guardería canina de día")}: lo traes de camino al trabajo, pasa el día en espacios exteriores con otros perros y lo recoges a la vuelta. No es la solución al problema de fondo, pero te quita los ladridos y las quejas de los vecinos mientras lo trabajamos.</p>
""",
  hoy=["Paseo largo con olfateo antes de salir de casa, todos los días.",
       "Salidas y llegadas sin ceremonias: ni despedidas largas ni fiestas al volver.",
       "Practica ausencias cortas de 5-10 minutos varias veces al día y ve subiendo.",
       "Deja algo para masticar que solo tenga cuando estás fuera.",
       "Apunta cuánto tarda en empezar a ladrar y cuánto dura: ese dato me sirve si me escribes."],
  cta=("¿Llevas semanas así y no mejora?",
       "Cada perro ladra por un motivo, y el truco que le funcionó a tu cuñado puede no servir para el tuyo. Cuéntame tu caso por videollamada: te veo a ti y al perro en vuestra casa, que es donde pasa, y te digo qué está fallando.",
       GUARDERIA, "Guardería de día en Lorca"),
  faq=[("¿Cuánto tiempo puede estar solo un perro?", "Depende de la edad y de lo que haya aprendido. Un cachorro, muy poco; un adulto acostumbrado, varias horas sin problema. Pero ningún perro debería pasar la jornada entera solo todos los días sin un paseo serio antes y compañía después. Si es tu situación, una guardería de día o alguien que lo saque a mediodía cambian mucho las cosas."),
       ("¿Se le pasará solo con la edad?", "Normalmente no. Lo que hace un perro cada día lo refuerza. Si ladra solo durante meses, aprende que ladrar es lo que se hace cuando te vas. Cuanto antes cambies el manejo, más fácil es."),
       ("¿Es ansiedad por separación o solo aburrimiento?", "El aburrimiento se arregla cansándolo y dándole algo que hacer. La ansiedad por separación es más seria: el perro lo pasa realmente mal, puede hacerse daño o destrozar puertas. Si ves babeo, temblores o destrozos en las salidas, lee el artículo sobre ansiedad por separación y pide ayuda.")],
  relacionados=["ansiedad-por-separacion-en-perros", "mi-perro-no-hace-caso", "mi-perro-tira-de-la-correa"],
 ),
 dict(
  slug="ansiedad-por-separacion-en-perros", foto="ansiedad-separacion", categoria="Conducta",
  title="Ansiedad por separación en perros: señales y cómo tratarla",
  meta="Ansiedad por separación en perros: cómo distinguirla del aburrimiento, por qué aparece y cómo se trata de verdad, sin trucos ni collares. Juan Miguel, adiestrador con 45 años de experiencia.",
  h1="Ansiedad por separación en perros: señales, causas y cómo se trata de verdad",
  entradilla="Destrozos en la puerta, pis en casa aunque acabe de salir, babeo, ladridos que no paran. Si tu perro hace esto solo cuando te vas, no es que sea «malo»: es que lo pasa mal de verdad. Y eso tiene nombre, causa y solución.",
  cuerpo=f"""
<h2>Cómo saber si es ansiedad por separación</h2>
<p>Mucha gente llama ansiedad a cualquier perro que ladra un rato. No es lo mismo. Un perro aburrido se entretiene rompiendo un cojín; un perro con ansiedad por separación lo pasa mal, y se nota:</p>
<ul>
<li>Empieza a ponerse nervioso <strong>antes</strong> de que salgas: cuando coges las llaves, cuando te pones los zapatos.</li>
<li>Ladra o llora de forma continua, no a ratos, y puede durar horas.</li>
<li>Destroza sobre todo puertas, ventanas y lo que esté cerca de la salida: está intentando ir contigo.</li>
<li>Se hace pis o caca en casa aunque acabe de salir, babea mucho o tiembla.</li>
<li>Te sigue por toda la casa y no se queda tranquilo en ninguna habitación sin ti.</li>
</ul>
<p>Si reconoces tres o cuatro de estas, no estamos hablando de aburrimiento.</p>
<h2>De dónde sale</h2>
<p>Casi nunca es «de nacimiento». Lo normal es que lo hayamos construido entre todos sin darnos cuenta: un cachorro que nunca se quedó solo, un perro adoptado que vivió un abandono, una familia que pasó meses en casa y de repente vuelve a la oficina, o un dueño que, con toda su buena intención, convierte al perro en el centro absoluto de su vida. El perro aprende que estar contigo es lo único seguro, y estar sin ti, un peligro.</p>
<h2>Lo que no es la solución</h2>
<p>Ni el castigo, ni el collar antiladridos, ni «dejarlo que llore hasta que se canse». Con un perro que lo está pasando mal, todo eso suma angustia. Tampoco sirve encerrarlo en una jaula sin más: un perro con ansiedad en una jaula puede hacerse daño intentando salir.</p>
<h2>Cómo se trata</h2>
<p>Primero, el diagnóstico: hay que saber si el problema es del perro o del manejo, y en mi experiencia casi siempre es del manejo. Después, un plan por pasos, que es trabajo tuyo más que mío:</p>
<p><strong>Romper la dependencia en casa.</strong> El perro tiene que aprender a estar en otra habitación mientras tú estás en casa, a tener su sitio y a no seguirte a todas partes. Sin esto, nada de lo demás funciona.</p>
<p><strong>Desactivar las señales de salida.</strong> Coger las llaves y no salir. Ponerte los zapatos y sentarte en el sofá. Que las señales dejen de anunciar un drama.</p>
<p><strong>Ausencias graduales.</strong> Segundos, minutos, cuartos de hora. Cada paso solo cuando el anterior está tranquilo. Es lento y es lo único que fija el aprendizaje.</p>
<p><strong>Ejercicio y cabeza.</strong> Un perro cansado y con estímulos tiene mucha menos angustia que uno que vive entre cuatro paredes.</p>
<p>En los casos más serios, en Lorca lo trabajamos con el {L(LORCA, "diagnóstico previo")}: una semana con nosotros, lejos de tus rutinas, para ver cómo es el perro de verdad y decirte exactamente qué tienes que cambiar tú.</p>
""",
  hoy=["Anota qué hace el perro cuando sales: cuándo empieza, cuánto dura, qué rompe. Un vídeo de los primeros 10 minutos vale oro.",
       "Empieza a practicar en casa que se quede en otra habitación sin ti, con la puerta abierta.",
       "Coge las llaves y el abrigo varias veces al día sin salir.",
       "Sube el ejercicio diario: olfateo, paseo largo, juego.",
       "No lo castigues al volver, aunque haya destrozos. No lo relaciona y solo le añade miedo."],
  cta=("La ansiedad por separación no se arregla con un vídeo de YouTube",
       "Necesita un diagnóstico y un plan para tu perro, no uno genérico. Por videollamada veo a tu perro en su casa, que es donde aparece el problema, y salimos con pautas concretas y seguimiento.",
       LORCA, "Diagnóstico previo en Lorca"),
  faq=[("¿La ansiedad por separación se cura?", "Se trata y en la mayoría de los casos se resuelve, pero no en una semana ni con un truco. Hace falta cambiar el manejo y trabajar las ausencias paso a paso durante semanas. Lo que no cambia solo es la conducta: cada día que el perro lo pasa mal, se refuerza."),
       ("¿Sirve tener otro perro para que no esté solo?", "Casi nunca. La ansiedad es por separarse de ti, no por estar sin perros. Lo habitual es acabar con dos perros nerviosos en vez de uno. Primero se trabaja el problema; después, si quieres otro perro, que sea por otras razones."),
       ("¿Hay que medicarlo?", "Eso lo decide el veterinario, y solo en casos muy graves y siempre acompañado de trabajo de conducta. La medicación sola no enseña nada al perro. Mi trabajo empieza por el diagnóstico: si veo señales de que hace falta un veterinario, te lo digo.")],
  relacionados=["mi-perro-ladra-cuando-se-queda-solo", "mi-perro-no-hace-caso", "residencia-canina-que-tener-en-cuenta"],
 ),
 dict(
  slug="mi-perro-no-hace-caso", foto="no-hace-caso", categoria="Conducta",
  title="Mi perro no hace caso: los problemas de conducta más comunes",
  meta="Tira de la correa, no viene cuando lo llamas, ladra a otros perros, marca en casa. Te explico por qué tu perro no hace caso y cómo se educa de verdad. Juan Miguel, 45 años adiestrando en Lorca.",
  h1="Mi perro no hace caso: cómo resolver los problemas de conducta más comunes",
  entradilla="«No me hace caso» es la frase con la que empiezan la mitad de las llamadas que recibo. Detrás hay siempre un problema concreto: tira de la correa, no viene cuando lo llamas, se pone como loco con otros perros, marca en casa. Casi todos tienen explicación, y casi todos tienen solución. La clave es por dónde empiezas.",
  cuerpo=f"""
<h2>Primero: tu perro no es desobediente, es un perro</h2>
<p>Cuando alguien me dice que su perro «no hace caso», lo primero que pregunto es: ¿caso a qué? Un perro no viene con el castellano instalado. Si nunca ha aprendido qué significa «ven», no está desobedeciendo: no sabe lo que le pides. Y si lo sabe pero no lo hace, es porque en ese momento hay algo que le importa más que tú. Las dos cosas se trabajan, pero no igual.</p>
<h2>Los cuatro problemas que más veo</h2>
<p><strong>Tira de la correa.</strong> El paseo es un tira y afloja y llegas a casa con el brazo dolorido. El perro ha aprendido que tirando llega antes a donde quiere. Se resuelve enseñándole a caminar contigo, no delante de ti, y para eso hay que cambiar lo que haces tú con la correa.</p>
<p><strong>No viene cuando lo llamas.</strong> Lo llamas en el parque y hace como que no te oye. Normalmente es porque «ven» ha significado muchas veces «se acabó lo bueno»: fin del juego, correa y a casa. Hay que volver a construir la llamada para que venir sea siempre buena noticia.</p>
<p><strong>Ladra o se lanza a otros perros.</strong> Reactividad. Puede ser miedo, puede ser frustración, puede ser que nunca aprendió a relacionarse. Aquí no hay receta universal: hay que ver por qué reacciona ese perro, y ahí es donde el diagnóstico lo es todo.</p>
<p><strong>Marca o hace sus cosas en casa.</strong> En un cachorro es aprendizaje pendiente. En un adulto que antes no lo hacía, suele ser un cambio en casa, estrés o un problema de manejo. Y en algunos casos, un tema médico que debe descartar el veterinario.</p>
<h2>Educar no es imponer</h2>
<p>Un buen proceso de educación no consiste en forzar al perro, sino en entender qué cuestiones hacen que se comporte de una u otra manera y, a partir de ahí, establecer las pautas que deben marcar vuestra relación. Cuando el dueño comprende a su perro, la mayoría de los problemas se previenen antes de aparecer. Yo trabajo con etología, cómo funciona el perro desde su naturaleza, y con conductismo, cómo se forman y se cambian las conductas. El «refuerzo positivo» genérico corrige el síntoma; esto va a la causa.</p>
<h2>Lo que pasa en una clase</h2>
<p>En Lorca el programa son {L(LORCA, "5 clases de 2 horas")} en las que no solo educo al perro: te enseño a ti a hacerlo. No pasas a la siguiente clase hasta que dominas la anterior, y entre clase y clase trabajas en casa. Así los resultados se mantienen cuando yo no estoy. Si vives lejos, el mismo trabajo lo hacemos {L(ONLINE, "por videollamada")}, viendo al perro en su entorno.</p>
""",
  hoy=["Elige un solo problema para empezar. Querer arreglarlo todo a la vez es no arreglar nada.",
       "Observa cuándo pasa exactamente: con qué perros, en qué calle, a qué hora. El patrón te dice la causa.",
       "Deja de repetir la orden diez veces. Si la dices una vez y no funciona, el problema no es el volumen.",
       "Premia lo que quieres ver, en el momento en que lo ves, no cinco segundos después.",
       "Sube el ejercicio y el olfateo: muchos «no me hace caso» son perros con energía sin gastar."],
  cta=("¿No sabes cuál de las cinco causas es la de tu perro?",
       "Ese es justo mi trabajo. Cuéntame el caso por videollamada: analizo a tu perro y a ti, y te digo qué está pasando de verdad y por dónde empezar. Sin curso enlatado.",
       LORCA, "Adiestramiento en Lorca: 5 clases, 250 €"),
  faq=[("¿Mi perro es demasiado mayor para aprender?", "No. Eso es un mito. El perro adulto que nunca fue educado y el que arrastra un problema desde hace años tienen los dos solución con el método correcto. En cuanto tú haces lo que tienes que hacer, el perro se comporta de otra forma. La edad no es el problema; el método sí importa."),
       ("¿Cuántas clases hacen falta?", "En Lorca el programa son 5 clases de 2 horas, y para la mayoría de los casos es suficiente, con seguimiento después sin coste. No vamos por calendario: pasamos de clase cuando lo anterior está dominado."),
       ("¿Puede ser un problema de salud?", "A veces. Un perro que de repente no hace caso, se vuelve irritable o hace sus cosas en casa puede tener dolor o un problema médico. Si el cambio es brusco, pasa antes por el veterinario y después hablamos de conducta.")],
  relacionados=["mi-perro-tira-de-la-correa", "mi-perro-ladra-cuando-se-queda-solo", "ansiedad-por-separacion-en-perros"],
 ),
 dict(
  slug="mi-perro-tira-de-la-correa", foto="tira-de-la-correa", categoria="Conducta",
  title="Mi perro tira de la correa: cómo enseñarle a pasear a tu lado",
  meta="¿Tu perro tira de la correa y el paseo es una pelea? Te explico por qué tira, qué collares y arneses no resuelven nada y cómo enseñarle a caminar contigo. Juan Miguel, adiestrador con 45 años de experiencia.",
  h1="Mi perro tira de la correa: por qué lo hace y cómo enseñarle a pasear a tu lado",
  entradilla="Abres la puerta y ya vas colgado de la correa. En cada esquina, en cada perro, en cada farola. Pasear se ha convertido en un trabajo y el perro vuelve a casa igual de nervioso que salió. Te explico qué está pasando y cómo se cambia, sin tirones ni aparatos.",
  cuerpo=f"""
<h2>Por qué tira: porque funciona</h2>
<p>Tu perro tira por una razón muy simple: tirando llega antes adonde quiere ir. Cada vez que tira y tú sigues andando, él aprende que tirar es la forma de avanzar. No es dominancia, no es que «quiera ser el líder», ni ninguna de esas cosas que se leen por ahí. Es aprendizaje, y lo has reforzado tú sin querer, paseo a paseo.</p>
<p>A eso súmale que el paseo es el momento más emocionante de su día. Olores, perros, gente. Un perro que pasa veintidós horas en casa sale a la calle con una energía que no cabe en una correa de un metro.</p>
<h2>Lo que no lo soluciona</h2>
<p>El collar de pinchos, el de ahogo y los tirones secos consiguen un perro que tira igual pero con miedo. El arnés antitirones ayuda a que no te lleve en volandas, pero no le enseña nada: el día que se lo quitas, vuelve a tirar. El «flexi» de ocho metros directamente le enseña a tirar, porque tirar siempre da más cuerda.</p>
<h2>Cómo se enseña a caminar contigo</h2>
<p>Lo que hay que cambiar es, otra vez, el manejo. Tres ideas:</p>
<p><strong>Tirar no avanza.</strong> En el momento en que la correa se tensa, tú te paras. Sin tirón, sin bronca: simplemente dejas de andar. Cuando la correa se afloja, seguís. Al principio tardas veinte minutos en recorrer una calle; a la semana, el perro ha entendido que la correa floja es la que mueve el paseo.</p>
<p><strong>Tú eres más interesante que la farola.</strong> Si durante el paseo no le hablas, no le miras y vas con el móvil, el perro busca estímulos en otro sitio. Cambia de dirección sin avisar, prémialo cuando esté a tu lado, haz que mirarte merezca la pena.</p>
<p><strong>Gasta la energía antes de pedirle calma.</strong> Un perro que ya ha corrido y olfateado en una zona tranquila pasea después mucho mejor. Pedirle a un perro con las pilas cargadas que ande despacio a tu lado es pedir demasiado.</p>
<h2>Si tu perro además ladra o se lanza a otros perros</h2>
<p>Entonces el tirón es solo la punta del iceberg. Ahí hablamos de reactividad, y la causa puede ser miedo, frustración o falta de aprendizaje. Lo explico en {L("mi-perro-no-hace-caso.html", "los problemas de conducta más comunes")}, y es un caso para verlo con calma, porque la receta equivocada lo empeora.</p>
""",
  hoy=["Correa corta de 1,5-2 metros y arnés o collar plano normal. Guarda el extensible.",
       "Regla de hoy: correa tensa, te paras; correa floja, seguís. Sin excepciones.",
       "Empieza en un sitio aburrido (tu calle a una hora tranquila), no en el parque lleno de perros.",
       "Cambia de dirección sin avisar cuando se adelante, y prémialo cuando vuelva a tu lado.",
       "Paseos más cortos pero bien hechos valen más que una hora de tirones."],
  cta=("¿Lo has intentado todo y sigue tirando?",
       "Entonces hay algo en el manejo que no estás viendo, y es normal: desde dentro no se ve. Por videollamada te veo pasear con él y te digo qué cambiar. Suele ser una o dos cosas concretas.",
       LORCA, "Clases de adiestramiento en Lorca"),
  faq=[("¿Arnés o collar para un perro que tira?", "Para enseñarle, un collar plano o un arnés normal con la correa en la espalda. Lo importante no es el aparato, es lo que haces tú con la correa. Los arneses antitirones pueden ayudar mientras aprende, pero no sustituyen el trabajo."),
       ("¿Cuánto se tarda en que deje de tirar?", "Si eres constante, en una o dos semanas se nota mucho. Lo que lo retrasa es la incoherencia: un día te paras y otro día, con prisa, le dejas tirar. El perro aprende lo que haces la mayoría de las veces."),
       ("¿A partir de qué edad se puede enseñar?", "Desde cachorro. De hecho, es mucho más fácil enseñar a un cachorro a pasear con correa floja que corregir a un adulto que lleva años tirando. Pero un adulto también aprende; solo tarda un poco más.")],
  relacionados=["mi-perro-no-hace-caso", "mi-perro-ladra-cuando-se-queda-solo", "como-elegir-un-perro-de-proteccion"],
 ),
 dict(
  slug="caniche-gigante-familias-con-ninos", foto="caniche-ninos", categoria="Razas",
  title="Caniche gigante con niños: por qué es ideal para tu familia",
  meta="El caniche gigante es tranquilo, muy inteligente, no suelta pelo y se lleva de maravilla con los niños. Te explico cómo es de verdad y qué mirar al elegir un cachorro. Criador en Lorca con 45 años.",
  h1="Por qué el caniche gigante es un perro ideal para familias con niños",
  entradilla="Cuando una familia busca su primer perro, el temperamento importa tanto o más que la estética. Y el caniche gigante destaca precisamente por ahí: equilibrado, sociable, listísimo y sin pelo por el sofá. Llevo 45 años criando esta raza en Lorca y te cuento cómo es de verdad, sin postal.",
  cuerpo=f"""
<h2>Un carácter tranquilo y sociable</h2>
<p>El caniche gigante es un perro de carácter equilibrado, tranquilo y enormemente sociable, que crea un apego fuerte con su gente y entiende e interpreta las situaciones del hogar como muy pocas razas. Esa sensibilidad lo hace especialmente bueno con los niños: no es un perro que se altere con facilidad; al contrario, se integra en la dinámica familiar y se convierte en un compañero de juegos paciente y atento.</p>
<p>Eso sí: es un perro grande, de 45 a 60 centímetros a la cruz, y con un cachorro de cualquier raza y un niño pequeño siempre hace falta un adulto delante. La diferencia es que con un caniche gigante bien criado, la supervisión es por sentido común, no por miedo.</p>
<h2>Inteligencia y aprendizaje rápido</h2>
<p>Es una de las razas más inteligentes que existen, y se nota en el día a día: asimila las normas de casa con facilidad, aprende el nombre, el sitio y las rutinas en pocos días, y responde de maravilla a una educación basada en el vínculo, no en la imposición. Para una familia esto significa una convivencia más sencilla desde el primer día. La otra cara: un perro tan listo se aburre si no tiene qué hacer, así que necesita paseo, juego y cabeza.</p>
<h2>No suelta pelo</h2>
<p>El caniche no muda como otras razas: su pelo crece de forma continua y no se cae por casa. Por eso es la elección de muchas familias con alergia o que, sencillamente, no quieren vivir entre pelos. A cambio, necesita peluquería regular, cada seis u ocho semanas, y cepillado en casa entre visita y visita. En Lorca lo tenemos resuelto: Juanmi, el peluquero del centro, es especialista en la raza y quedó {L(PELU, "tercero en el Campeonato de Europa")}.</p>
<h2>Cría y selección: la clave de un buen cachorro</h2>
<p>No todos los cachorros llegan igual a casa. El carácter del caniche gigante que te he descrito no es automático: es fruto de una selección responsable de los padres por carácter, salud y conformación, y de una socialización desde los primeros días de vida. En el Centro Canino de Lorca criamos y seleccionamos a mano buscando ese carácter equilibrado y sensible, y cada cachorro pasa un protocolo sanitario completo antes de la entrega. Ese trabajo previo es lo que marca la diferencia en la adaptación a tu hogar.</p>
<h2>Qué mirar antes de elegir</h2>
<ul>
<li><strong>Los padres.</strong> Pide verlos. El carácter se hereda y se aprende de la madre las primeras semanas.</li>
<li><strong>Criador registrado.</strong> Núcleo zoológico, factura con IVA e informe veterinario antes de la entrega. Si falta alguno, desconfía.</li>
<li><strong>Edad de entrega.</strong> Nunca antes de las ocho semanas. Un cachorro separado antes de tiempo arrastra problemas de conducta toda la vida.</li>
<li><strong>El precio.</strong> En esta raza, el «chollo» se paga después en el veterinario.</li>
</ul>
<p>Si quieres conocer a nuestros caniches gigantes, te invitamos a pasar por el centro en Lorca a verlos. Toda la información está en la página de {L(CANICHE, "cachorros de caniche gigante")}.</p>
""",
  hoy=["Piensa en el tiempo real que tenéis para pasear y jugar con él: es un perro grande y listo.",
       "Reserva presupuesto para la peluquería: cada 6-8 semanas, toda su vida.",
       "Pide ver a los padres y el informe veterinario antes de decidir.",
       "Prepara una zona tranquila en casa para el cachorro antes de que llegue.",
       "Desde el primer día, los niños aprenden a dejarlo en paz cuando come y cuando duerme."],
  cta=("¿Dudas sobre si el caniche gigante encaja en tu familia?",
       "Cuéntame cómo es tu casa, tu horario y la edad de los niños. Te digo con sinceridad si es vuestra raza y, si lo es, cuándo tenemos camada. Sin reservas, sin presión.",
       CANICHE, "Cachorros de caniche gigante en Lorca"),
  faq=[("¿El caniche gigante es bueno con niños pequeños?", "Sí, es de las razas más recomendables: tranquilo, paciente y muy apegado a su familia. Como con cualquier perro grande, con niños pequeños siempre debe haber un adulto presente y los niños deben aprender a respetar al perro cuando come o duerme."),
       ("¿Es verdad que no da alergia?", "Ninguna raza es cien por cien hipoalergénica, pero el caniche no suelta pelo y produce mucha menos caspa que otras razas, por lo que la mayoría de las personas alérgicas lo toleran bien. Si en casa hay alergia, lo mejor es pasar un rato con un caniche adulto antes de decidir."),
       ("¿Cuánto ejercicio necesita?", "Un paseo largo diario con juego y olfateo, y algo que le haga pensar. Es un perro activo pero no hiperactivo: en casa es tranquilo si fuera ha gastado la energía.")],
  relacionados=["cada-cuanto-llevar-al-perro-a-la-peluqueria", "como-elegir-un-perro-de-proteccion", "mi-perro-no-hace-caso"],
 ),
 dict(
  slug="como-elegir-un-perro-de-proteccion", foto="perro-proteccion", categoria="Razas",
  title="Cómo elegir un perro de protección sin equivocarte",
  meta="No todos los perros sirven para proteger, ni criándolos bien. Qué tener en cuenta (carácter, físico, vínculo) antes de elegir un pastor alemán o malinois para tu familia. Criador de pastor alemán de trabajo en Lorca.",
  h1="Cómo elegir un perro de protección sin equivocarte",
  entradilla="Existe la idea de que, criando bien a un perro, todos salen estupendos y valen para cualquier función. No es así. La cría y selección de perros de utilidad es una labor compleja, y ahí reside precisamente su atractivo. Elegir un perro que proteja a tu familia no debe dejarse al azar.",
  cuerpo=f"""
<h2>Criar bien no basta</h2>
<p>Un perro de protección de verdad no se improvisa con cariño y buena comida. Hace falta genética: padres seleccionados durante generaciones por carácter y por capacidad de trabajo, no por bonitos. Es la diferencia entre un pastor alemán de línea de trabajo y uno de belleza, y es una diferencia de estructura, de carácter y de salud. Lo explico con detalle en la página de {L(PASTOR, "cachorros de pastor alemán de trabajo")}.</p>
<h2>Qué hace a un buen perro de protección</h2>
<p>Un sistema nervioso equilibrado, un carácter más o menos instintivo, un físico saludable y libre de taras genéticas, una fuerte tendencia a vincularse con su guía, una conciencia clara de su entorno y la capacidad de afrontar con valor situaciones difíciles. Estas son las cualidades que diferencian a un perro de protección real de uno que simplemente parece serlo.</p>
<p>Fíjate en que la primera es el equilibrio. Un perro nervioso, miedoso o que ladra a todo no protege: reacciona. Y un perro que reacciona sin criterio es un problema en casa, no una seguridad.</p>
<h2>«Solo lo quiero para casa»</h2>
<p>Incluso quien dice «lo quiero solo para casa» debería ser exigente en la elección, porque la protección familiar es una de las funciones donde más conviene acertar. Un perro de protección vive con niños, con visitas, con el cartero. Tiene que saber distinguir, y eso exige nervio templado y mucha socialización desde cachorro. No busques el perro «más fiero»: busca el más equilibrado.</p>
<h2>Lo que tienes que poner tú</h2>
<p>Además de hacerse necesaria la suficiente formación de la persona que se va a encargar de su manejo, hay que entender que un perro de trabajo necesita trabajo: ejercicio, tareas, educación desde las primeras semanas. Un malinois o un pastor alemán de línea de trabajo en un piso, sin actividad y sin guía, es un perro frustrado. Si no vas a poder darle eso, elige otra raza; prefiero decírtelo antes que venderte un cachorro que va a ser un problema.</p>
<h2>Razas que seleccionamos en Lorca</h2>
<p>En el Centro Canino de Lorca seleccionamos y criamos pastor alemán de línea de trabajo y, en algunas camadas, cruces con malinois: perros instintivos, fuertes, muy entrenables y, a la vez, aptos para la vida familiar. Cada cachorro se evalúa de temperamento antes de asignarlo, pasa un protocolo sanitario completo y, si no está en condiciones, la venta no se formaliza. Y antes de nada, te asesoramos para que la elección encaje con tu estilo de vida, aunque eso signifique recomendarte que no lo compres.</p>
""",
  hoy=["Sé honesto con el tiempo y la actividad que puedes darle: un perro de trabajo necesita trabajo.",
       "Pide ver a los padres y pregunta por su carácter, no solo por su pedigrí.",
       "Huye del perro «fiero»: lo que proteges con un perro nervioso es un problema.",
       "Pregunta qué evaluación de temperamento se hace a los cachorros antes de asignarlos.",
       "Planifica la educación desde las 8 semanas: en estos perros no hay tiempo que perder."],
  cta=("¿No sabes si un perro de protección encaja en tu casa?",
       "Cuéntame cómo vivís, quién lo va a manejar y para qué lo quieres. Te digo con sinceridad si es buena idea y qué raza o línea te conviene. A veces la respuesta es «mejor otro perro», y también te lo diré.",
       PASTOR, "Pastor alemán de trabajo en Lorca"),
  faq=[("¿Pastor alemán o malinois para una familia?", "Depende de la experiencia y la actividad de la familia. El malinois es más intenso y necesita más trabajo y más guía; el pastor alemán de línea de trabajo suele ser más llevadero en casa manteniendo la capacidad de protección. Lo vemos caso por caso."),
       ("¿Un perro de protección es peligroso con los niños?", "Un perro de protección bien seleccionado y bien educado es equilibrado, y eso es lo contrario de peligroso. El peligro está en el perro nervioso o mal socializado, sea de la raza que sea. Por eso insisto tanto en el carácter de los padres y en la educación desde cachorro."),
       ("¿Hacéis adiestramiento de guardia y defensa?", "No. No hago guardia, defensa, ataque ni deporte canino, y lo digo claro. Lo mío es seleccionar perros equilibrados y enseñar a las familias a manejarlos para convivir bien. La protección natural de un buen perro sale de su carácter, no de enseñarle a morder.")],
  relacionados=["caniche-gigante-familias-con-ninos", "mi-perro-no-hace-caso", "mi-perro-tira-de-la-correa"],
 ),
 dict(
  slug="cada-cuanto-llevar-al-perro-a-la-peluqueria", foto="peluqueria-cada-cuanto", categoria="Cuidados",
  title="Peluquería canina: cada cuánto llevar a tu perro y por qué",
  meta="La peluquería canina no es solo estética: es piel, higiene y salud. Cada cuánto llevar a tu perro según su tipo de pelo, qué incluye una buena sesión y por qué el stripping importa. Peluquería canina en Lorca, 3º de Europa.",
  h1="Peluquería canina: cada cuánto llevar a tu perro y por qué cuidar el pelo es cuidar su salud",
  entradilla="Un buen corte y un cepillado regular mantienen a tu perro guapo, sí, pero sobre todo sano. Nudos que tiran de la piel, humedad que no se seca, orejas y almohadillas que nadie revisa. Te cuento cada cuánto hay que ir según el pelo de tu perro y qué diferencia a una peluquería de verdad de un repaso rápido.",
  cuerpo=f"""
<h2>Más que estética</h2>
<p>El pelo de un perro es su abrigo y su piel la ve poca gente. Los nudos no son solo feos: tiran de la piel, esconden humedad y acaban en irritaciones y hongos. Un manto sin cuidar en verano da calor y en invierno no abriga. Y una sesión de peluquería bien hecha es, además, una revisión: orejas, uñas, almohadillas, bultos que aparecen y que en casa no se ven bajo el pelo.</p>
<h2>Cada cuánto, según el tipo de pelo</h2>
<ul>
<li><strong>Pelo rizado que no muda (caniche, bichón, perro de agua).</strong> Es el que más cuidado pide: una sesión cada seis u ocho semanas y cepillado en casa dos o tres veces por semana. Si se deja, el nudo llega a la piel y ya no hay cepillo que lo saque.</li>
<li><strong>Pelo largo (yorkshire, maltés, shih tzu).</strong> Cada seis u ocho semanas también, y cepillado diario si lo llevas largo.</li>
<li><strong>Pelo duro (schnauzer, westy, teckel de pelo duro).</strong> Aquí la clave no es cortar: es el stripping, arrancar a mano el pelo muerto para que el manto conserve su textura y su color. Cada tres o cuatro meses, y nunca con máquina.</li>
<li><strong>Pelo corto (beagle, bulldog, labrador).</strong> No necesitan corte, pero sí baño y cepillado cada uno o dos meses para quitar pelo muerto y revisar la piel.</li>
</ul>
<h2>Lo que incluye una sesión de verdad</h2>
<p>Primero se valora cómo está el pelaje. Luego baño con el producto que pide su tipo de pelo, secado a mano, corte o stripping según la raza y una revisión final. En nuestra {L(PELU, "peluquería canina en Lorca")} una sesión dura entre dos y cuatro horas, no cuarenta y cinco minutos como en un salón de volumen, y por eso solo entran uno o dos perros al día. Al tuyo le toca el tiempo que necesita.</p>
<h2>Máquina o tijera: la diferencia que se ve</h2>
<p>La máquina da un resultado igual para todos y, en las razas de pelo duro, estropea la textura y el color. La tijera respeta el estándar de cada raza y deja un acabado que la máquina no consigue. Lleva más tiempo y más oficio, por eso no lo hace cualquiera. Juanmi, el peluquero del centro, quedó tercero en el Campeonato de Europa, especializado en caniche gigante y cortes de exposición. Ese nivel de tijera es el que recibe tu perro, aunque venga solo para el corte de todos los días.</p>
<h2>Si tu perro lo pasa mal en la peluquería</h2>
<p>Hay perros que nunca han ido, perros nerviosos y perros a los que han rechazado en otros sitios. Trabajamos en un centro de adiestramiento y conducta, así que entendemos el lenguaje del perro antes de tocarlo: sin sedación y sin atarlo a la fuerza, con manejo y con paciencia. Si es tu caso, cuéntanoslo al pedir cita.</p>
""",
  hoy=["Cepilla a tu perro hoy mismo, despacio, y comprueba si el cepillo llega a la piel o se queda en la capa de arriba.",
       "Revisa orejas y almohadillas: olor fuerte, rojez o pelo apelmazado entre los dedos son avisos.",
       "Apunta la fecha de la última peluquería y calcula la siguiente según su tipo de pelo.",
       "Seca bien al perro después de cada baño, sobre todo en razas de pelo rizado.",
       "Si tiene pelo duro, pregunta por stripping, no por «corte a máquina»."],
  cta=("Pide cita en la peluquería canina de Lorca",
       "Cuéntanos la raza, la edad y cuándo fue su última peluquería. Solo con cita previa, máximo dos perros al día, trabajo a tijera y stripping a mano.",
       PELU, "Peluquería canina en Lorca"),
  faq=[("¿Cada cuánto hay que bañar a un perro?", "Depende del pelo y de la vida que haga, pero como norma cada cuatro u ocho semanas, con un champú para perros, nunca de personas. Bañarlo cada semana reseca la piel; no bañarlo en meses acumula suciedad y olor. Entre baños, el cepillado hace más que el agua."),
       ("¿Es malo cortar el pelo a un perro en verano?", "Depende de la raza. A un caniche o un yorkshire, un corte más corto en verano le viene bien. A las razas de doble capa (pastor alemán, husky, golden) no se les rapa: su manto les protege del calor y del sol, y rapado no vuelve a crecer igual. Pregunta antes de pedir «que le quiten todo»."),
       ("¿Cuánto cuesta la peluquería canina?", "En Lorca nuestras tarifas van de 30 € a 150 € por animal según la raza, el estado del pelo y el tipo de trabajo. Un corte de exposición a tijera no cuesta lo que un repaso de máquina. Escríbenos con la raza y te damos el precio de tu caso.")],
  relacionados=["caniche-gigante-familias-con-ninos", "residencia-canina-que-tener-en-cuenta", "mi-perro-no-hace-caso"],
 ),
 dict(
  slug="residencia-canina-que-tener-en-cuenta", foto="residencia-elegir", categoria="Cuidados",
  title="Residencia canina: qué tener en cuenta antes de dejar a tu perro",
  meta="¿Te vas de viaje? Qué mirar al elegir una residencia canina: quién cuida de los perros, cuántos hay a la vez, requisitos, visita previa y qué llevar. Consejos de un centro con 45 años en Lorca.",
  h1="Residencia canina: qué tener en cuenta antes de dejar a tu perro",
  entradilla="Ausentarse unos días es más llevadero cuando sabes que tu perro está bien. Pero no todas las residencias son iguales, y lo que más importa no sale en las fotos. Te cuento en qué fijarte, qué preguntar y cómo preparar a tu perro para su primera estancia.",
  cuerpo=f"""
<h2>Quién cuida de los perros, de verdad</h2>
<p>Una buena residencia canina no es un sitio donde «aparcar» al animal: es un entorno donde está supervisado, acompañado y atendido por personas que entienden el mundo del perro. Pregunta quién está con ellos y cuánto tiempo. No es lo mismo un empleado que ficha a las ocho y se va a las seis que una familia que vive en la misma parcela y oye toser a un perro a las tres de la mañana.</p>
<h2>Cuántos perros hay a la vez</h2>
<p>Es la pregunta que casi nadie hace y la que más dice. Una nave con sesenta perros no puede dar a cada uno paseo, atención y descanso de verdad. En nuestra {L(RESIDENCIA, "residencia canina en Lorca")} tenemos más de cien plazas y, por decisión propia, nunca pasamos de diez o quince perros a la vez. Un perro no es un número en una jaula: si entran demasiados, ninguno recibe lo que necesita.</p>
<h2>Instalaciones y rutina</h2>
<p>Fíjate en el espacio, la limpieza y si hay zonas separadas según el tamaño y el carácter de cada perro. Pregunta por la rutina: cuántos paseos, dónde, si hay zonas de césped, cómo gestionan las comidas y la convivencia entre perros. Y pregunta qué pasa si tu perro deja de comer o se pone malo: la respuesta tiene que ser «te llamamos», no «ya veremos».</p>
<h2>Requisitos: lo que piden, lo piden por algo</h2>
<p>Cartilla de vacunación al día y antiparasitario en vigor, por dentro y por fuera. No es burocracia: en una residencia conviven varios perros y lo que protege al tuyo protege a todos. Si una residencia no te pide nada, piensa qué perros van a estar con el tuyo.</p>
<h2>La visita previa</h2>
<p>Ve a verlo antes de decidir, y lleva al perro. Si el tuyo es nervioso, miedoso o no se fía de los desconocidos, una visita corta en la que conoce el sitio y a las personas sin quedarse cambia por completo la primera estancia. En Lorca esa visita no cuesta nada y la recomendamos siempre.</p>
<h2>Cómo preparar la estancia</h2>
<ul>
<li>Lleva su pienso de siempre y las instrucciones si toma medicación.</li>
<li>Algo con tu olor, una manta o una camiseta, le ayuda las primeras noches.</li>
<li>Reserva con tiempo: en julio, agosto, puentes y Navidad las plazas vuelan.</li>
<li>Despídete sin dramas. Si tú te vas angustiado, él se queda angustiado.</li>
</ul>
<p>Y si lo que necesitas no es una estancia con noche sino dejarlo unas horas mientras trabajas, para eso está la {L(GUARDERIA, "guardería canina de día")}, por horas y sin pernoctar.</p>
""",
  hoy=["Haz tres preguntas a cualquier residencia: ¿quién está con los perros por la noche?, ¿cuántos perros tenéis a la vez? y ¿qué hacéis si el mío no come?",
       "Comprueba que te piden cartilla y antiparasitario: si no lo hacen, mala señal.",
       "Pide una visita previa con tu perro antes de la primera estancia.",
       "Reserva ya si tienes fechas de vacaciones o puente.",
       "Prepara pienso, medicación con instrucciones y algo con tu olor."],
  cta=("Dinos tus fechas y te confirmamos plaza",
       "Residencia canina en Lorca con 45 años de experiencia, solo 10-15 perros a la vez y supervisión real: vivimos en la misma parcela. Recogida sin cargo hasta 20-25 km.",
       RESIDENCIA, "Residencia canina en Lorca"),
  faq=[("¿Cuánto cuesta una residencia canina?", "En Lorca el precio es de 18 € + IVA por perro y día, e incluye la estancia, los paseos, la supervisión y el descanso, sin extras escondidos. Para estancias largas, de semanas o meses, el precio por día baja."),
       ("¿Mi perro lo pasará mal los primeros días?", "Algunos tardan uno o dos días en adaptarse, y dejar de comer del todo al principio es normal. Lo vigilamos de cerca y te avisamos si algo no va bien. La visita previa y una despedida sin dramas reducen mucho ese periodo."),
       ("¿Puedo dejar dos perros juntos?", "Sí, si conviven bien entre ellos. Cuéntanoslo al reservar para organizar el espacio. Cada perro es diferente y antes de la primera estancia nos gusta conocerlos para saber cómo tratarlos.")],
  relacionados=["mi-perro-ladra-cuando-se-queda-solo", "ansiedad-por-separacion-en-perros", "cada-cuanto-llevar-al-perro-a-la-peluqueria"],
 ),
]

# ---------------------------------------------------------------------------
# Plantilla
# ---------------------------------------------------------------------------
HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <!-- Google tag (gtag.js) con Consent Mode -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','wait_for_update':500});
    gtag('js', new Date());
    gtag('config','G-7N81DQBRL0');
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-7N81DQBRL0"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__</title>
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="description" content="__META__">
  <meta property="og:type" content="__OGTYPE__">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Centro Canino de Lorca">
  <meta property="og:url" content="__CANON__">
  <meta property="og:title" content="__TITLE__">
  <meta property="og:description" content="__META__">
  <meta property="og:image" content="__OGIMG__">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="__TITLE__">
  <meta name="twitter:description" content="__META__">
  <meta name="twitter:image" content="__OGIMG__">
  <link rel="icon" type="image/jpeg" href="../logo-centro-canino-lorca.jpeg">
  <link rel="canonical" href="__CANON__">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <script>
    tailwind.config = {
      theme: { extend: {
        colors: {
          primary:'#059669','on-primary':'#ffffff','primary-fixed-dim':'#a7f3d0','surface-tint':'#047857',
          'secondary-container':'#fea619','on-secondary-container':'#3b1f00','on-primary-container':'#d1fae5',
          background:'#f9f7f2',surface:'#ffffff','on-surface':'#1a1a1a','on-surface-variant':'#4a4a4a',
          secondary:'#fea619','secondary-fixed-dim':'#fbbf24',
        },
        fontFamily:{ sans:['Inter','sans-serif'], display:['Epilogue','sans-serif'] },
        maxWidth:{ 'container-max-width':'1200px' },
        spacing:{ 'margin-mobile':'1.25rem','margin-desktop':'2.5rem',gutter:'1.5rem' },
      } }
    }
  </script>
  <style>
    .font-headline-lg { font-family:'Epilogue',sans-serif; font-size:clamp(1.5rem,4.6vw,2.5rem); font-weight:700; line-height:1.15; letter-spacing:-0.03em; }
    .font-headline-md { font-family:'Epilogue',sans-serif; font-size:1.375rem; font-weight:700; line-height:1.2; letter-spacing:-0.02em; }
    .font-body-md     { font-family:'Inter',sans-serif; font-size:1rem; font-weight:400; line-height:1.7; }
    .font-label-md    { font-family:'Inter',sans-serif; font-size:0.9375rem; font-weight:600; }
    .font-label-sm    { font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:600; }
    .tonal-shadow       { box-shadow:0 4px 8px rgba(5,150,105,0.04),0 1px 3px rgba(5,150,105,0.06); }
    .tonal-shadow-hover { box-shadow:0 8px 16px rgba(5,150,105,0.08),0 2px 6px rgba(5,150,105,0.08); }
    .anim { opacity:0; transform:translateY(16px); transition:opacity .55s ease, transform .55s ease; }
    .anim.visible { opacity:1; transform:none; }
    .delay-1{transition-delay:.1s;}.delay-2{transition-delay:.2s;}.delay-3{transition-delay:.3s;}
    /* Cuerpo del artículo */
    .prose { font-family:'Inter',sans-serif; font-size:1.0625rem; line-height:1.8; color:#2f2f2f; }
    .prose p { margin:0 0 1.25rem; }
    .prose h2 { font-family:'Epilogue',sans-serif; font-size:clamp(1.3rem,2.6vw,1.65rem); font-weight:700; line-height:1.2; letter-spacing:-0.02em; color:#059669; margin:2.4rem 0 0.9rem; }
    .prose ul { margin:0 0 1.25rem; padding-left:1.25rem; }
    .prose li { margin:0 0 0.6rem; padding-left:0.25rem; }
    .prose li::marker { color:#059669; }
    .prose strong { color:#1a1a1a; }
    .prose a { color:#059669; font-weight:600; text-decoration:underline; text-decoration-color:rgba(5,150,105,0.3); text-underline-offset:3px; transition:text-decoration-color .2s; }
    .prose a:hover { text-decoration-color:#059669; }
    .caja-hoy { background:rgba(5,150,105,0.06); border-left:4px solid #059669; border-radius:0 16px 16px 0; }
    .caja-hoy li::marker { color:#059669; font-weight:700; }
    .drop::first-letter { font-family:'Epilogue',sans-serif; font-size:3.2em; font-weight:700; float:left; line-height:0.85; padding:0.08em 0.12em 0 0; color:#059669; }
  </style>
</head>
<body class="bg-surface text-on-surface antialiased">
"""

NAV = """
<!-- NAV -->
<header class="sticky top-0 z-50 w-full bg-background/95 backdrop-blur border-b border-[#E9E5D9]" style="box-shadow:0 1px 8px rgba(5,150,105,0.06);">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop h-16 flex items-center justify-between gap-4">
    <a href="../index.html" class="flex items-center gap-2 flex-shrink-0">
      <img src="../logo-centro-canino-lorca.jpeg" alt="Centro Canino de Lorca" class="w-9 h-9 rounded-full object-cover flex-shrink-0">
      <span style="font-family:'Epilogue',sans-serif;font-weight:700;font-size:1.2rem;color:#059669;letter-spacing:-0.01em;">Centro Canino de Lorca</span>
    </a>
    <nav class="hidden md:flex items-center gap-6">
      <a href="../index.html" class="font-label-md text-on-surface-variant hover:text-primary transition-colors">Inicio</a>
      <div class="relative group">
        <a href="../index.html#servicios" class="font-label-md text-on-surface-variant hover:text-primary transition-colors inline-flex items-center gap-1 cursor-pointer">Servicios<span class="material-symbols-outlined text-[16px]">expand_more</span></a>
        <div class="absolute left-1/2 -translate-x-1/2 top-full pt-3 hidden group-hover:block z-50">
          <div class="bg-surface rounded-xl border border-[#E9E5D9] shadow-[0_8px_24px_rgba(5,150,105,0.14)] py-2 w-72">
            <a href="../residencia-canina-lorca.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">home</span><span class="font-label-md text-on-surface">Residencia canina</span></a>
            <a href="../guarderia-canina-lorca.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">sunny</span><span class="font-label-md text-on-surface">Guardería de día</span></a>
            <a href="../adiestramiento-canino-lorca.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">school</span><span class="font-label-md text-on-surface">Adiestramiento canino en Lorca</span></a>
            <a href="../adiestramiento-canino-online.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">videocam</span><span class="font-label-md text-on-surface">Adiestramiento online</span></a>
            <a href="../adiestramiento-canino-murcia.html" class="flex items-center gap-3 px-4 py-2.5 pl-9 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[18px]">arrow_right</span><span class="font-label-md text-on-surface">Adiestramiento en Murcia</span></a>
            <a href="../cachorros-lorca.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">pets</span><span class="font-label-md text-on-surface">Cachorros en Lorca</span></a>
            <a href="../cachorros-pastor-aleman-de-trabajo.html" class="flex items-center gap-3 px-4 py-2.5 pl-9 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[18px]">arrow_right</span><span class="font-label-md text-on-surface">Cachorros Pastor Alemán</span></a>
            <a href="../cachorros-caniche-gigante.html" class="flex items-center gap-3 px-4 py-2.5 pl-9 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[18px]">arrow_right</span><span class="font-label-md text-on-surface">Cachorros Caniche Gigante</span></a>
            <a href="../cachorros-en-murcia.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">map</span><span class="font-label-md text-on-surface">Cachorros en Murcia</span></a>
            <a href="../peluqueria-canina-lorca.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors"><span class="material-symbols-outlined text-primary text-[20px]" style="font-variation-settings:'FILL' 1;">content_cut</span><span class="font-label-md text-on-surface">Peluquería canina</span></a>
          </div>
        </div>
      </div>
      <a href="../index.html#nosotros" class="font-label-md text-on-surface-variant hover:text-primary transition-colors">Nosotros</a>
      <a href="../index.html#resenas" class="font-label-md text-on-surface-variant hover:text-primary transition-colors">Reseñas</a>
      <a href="./" class="font-label-md text-primary transition-colors">Blog</a>
      <a href="../index.html#contacto" class="font-label-md text-on-surface-variant hover:text-primary transition-colors">Contacto</a>
      <a href="tel:+34670360676" class="inline-flex items-center gap-2 bg-primary text-on-primary font-label-md px-5 py-2.5 rounded-lg font-bold hover:bg-surface-tint transition-colors tonal-shadow tonal-shadow-hover">
        <span class="material-symbols-outlined text-[18px]" style="font-variation-settings:'FILL' 1;">phone</span>670 36 06 76
      </a>
    </nav>
    <button id="menuBtn" class="md:hidden flex flex-col gap-1.5 p-2" aria-label="Abrir menú">
      <span class="w-5 h-0.5 bg-on-surface block"></span><span class="w-5 h-0.5 bg-on-surface block"></span><span class="w-5 h-0.5 bg-on-surface block"></span>
    </button>
  </div>
  <div id="mobileMenu" class="hidden md:hidden bg-background border-t border-[#E9E5D9] px-margin-mobile py-4 flex flex-col gap-4">
    <a href="../index.html" class="font-label-md text-on-surface-variant">Inicio</a>
    <p class="font-label-sm text-on-surface-variant/60 uppercase tracking-wider pt-1">Servicios</p>
    <a href="../residencia-canina-lorca.html" class="font-label-md text-on-surface-variant pl-3">Residencia canina</a>
    <a href="../guarderia-canina-lorca.html" class="font-label-md text-on-surface-variant pl-3">Guardería de día</a>
    <a href="../adiestramiento-canino-lorca.html" class="font-label-md text-on-surface-variant pl-3">Adiestramiento canino en Lorca</a>
    <a href="../adiestramiento-canino-online.html" class="font-label-md text-on-surface-variant pl-3">Adiestramiento online</a>
    <a href="../adiestramiento-canino-murcia.html" class="font-label-md text-on-surface-variant pl-6">· Adiestramiento en Murcia</a>
    <a href="../cachorros-lorca.html" class="font-label-md text-on-surface-variant pl-3">Cachorros en Lorca</a>
    <a href="../cachorros-pastor-aleman-de-trabajo.html" class="font-label-md text-on-surface-variant pl-6">· Pastor Alemán</a>
    <a href="../cachorros-caniche-gigante.html" class="font-label-md text-on-surface-variant pl-6">· Caniche Gigante</a>
    <a href="../cachorros-en-murcia.html" class="font-label-md text-on-surface-variant pl-3">Cachorros en Murcia</a>
    <a href="../peluqueria-canina-lorca.html" class="font-label-md text-on-surface-variant pl-3">Peluquería canina</a>
    <a href="../index.html#nosotros" class="font-label-md text-on-surface-variant pt-1">Nosotros</a>
    <a href="../index.html#resenas" class="font-label-md text-on-surface-variant">Reseñas</a>
    <a href="./" class="font-label-md text-primary">Blog</a>
    <a href="../index.html#contacto" class="font-label-md text-on-surface-variant">Contacto</a>
    <a href="tel:+34670360676" class="inline-flex items-center gap-2 bg-primary text-on-primary font-label-md px-5 py-3 rounded-lg font-bold w-fit"><span class="material-symbols-outlined text-[18px]" style="font-variation-settings:'FILL' 1;">phone</span>670 36 06 76</a>
  </div>
</header>
"""

FOOTER = """
<!-- FOOTER -->
<footer class="w-full bg-primary pt-12 pb-8">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <div class="flex flex-col md:flex-row md:justify-between gap-10 pb-8 border-b border-white/15">
      <div class="flex flex-col gap-3 max-w-xs">
        <div class="flex items-center gap-2">
          <img src="../logo-centro-canino-lorca.jpeg" alt="Centro Canino de Lorca" class="w-10 h-10 rounded-full object-cover flex-shrink-0">
          <span style="font-family:'Epilogue',sans-serif;font-weight:700;font-size:1.1rem;color:#ffffff;">Centro Canino de Lorca</span>
        </div>
        <span class="font-label-sm text-on-primary opacity-70 leading-relaxed">45 años cuidando, adiestrando y mimando a los perros de Lorca y su comarca.</span>
        <div class="flex items-center gap-3 mt-1">
          <a href="https://www.facebook.com/centrocaninolorca/" target="_blank" rel="noopener" aria-label="Facebook" class="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-colors"><svg viewBox="0 0 24 24" fill="currentColor" class="w-[18px] h-[18px]"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07c0 6.03 4.39 11.03 10.13 11.93v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.95.93-1.95 1.88v2.26h3.32l-.53 3.49h-2.79V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a>
          <a href="https://www.instagram.com/centrocaninodelorca/" target="_blank" rel="noopener" aria-label="Instagram" class="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-colors"><svg viewBox="0 0 24 24" fill="currentColor" class="w-[18px] h-[18px]"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.43.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.43.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.43-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.43-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.31-1.46.72-2.12 1.38C1.36 2.67.95 3.34.63 4.14.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.8.72 1.47 1.38 2.13.66.66 1.33 1.07 2.12 1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56.8-.31 1.47-.72 2.13-1.38.66-.66 1.07-1.33 1.38-2.13.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91-.31-.8-.72-1.47-1.38-2.12-.66-.66-1.33-1.07-2.13-1.38-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1018.16 12 6.16 6.16 0 0012 5.84zM12 16a4 4 0 110-8 4 4 0 010 8zm6.41-10.85a1.44 1.44 0 11-1.44-1.44 1.44 1.44 0 011.44 1.44z"/></svg></a>
        </div>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-8 md:gap-12">
        <nav class="flex flex-col gap-2.5">
          <p class="font-label-sm text-on-primary opacity-50 uppercase tracking-wider mb-2">Navegación</p>
          <a href="../index.html" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Inicio</a>
          <a href="../index.html#servicios" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Servicios</a>
          <a href="./" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Blog</a>
          <a href="../index.html#resenas" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Reseñas</a>
          <a href="../index.html#contacto" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Contacto</a>
        </nav>
        <nav class="flex flex-col gap-2.5">
          <p class="font-label-sm text-on-primary opacity-50 uppercase tracking-wider mb-2">Legal</p>
          <a href="../aviso-legal.html" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Aviso legal</a>
          <a href="../politica-privacidad.html" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Política de privacidad</a>
          <a href="../politica-cookies.html" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">Política de cookies</a>
        </nav>
        <nav class="flex flex-col gap-2.5">
          <p class="font-label-sm text-on-primary opacity-50 uppercase tracking-wider mb-2">Contacto</p>
          <a href="tel:+34670360676" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">670 36 06 76</a>
          <a href="https://wa.me/34670360676" target="_blank" rel="noopener" class="font-label-sm text-on-primary opacity-80 hover:opacity-100 transition-opacity">WhatsApp</a>
          <span class="font-label-sm text-on-primary opacity-70 leading-relaxed">Cam. de los Valencianos, 24<br>30813 Lorca, Murcia</span>
        </nav>
      </div>
    </div>
    <div class="pt-6 border-t border-white/15">
      <p class="font-label-sm text-on-primary opacity-50 uppercase tracking-wider mb-2">Zona de servicio</p>
      <p class="font-label-sm text-on-primary opacity-75 leading-relaxed">Damos servicio en Lorca, Totana, Alhama, La Hoya, Puerto Lumbreras, Águilas y toda la comarca. Para cría de cachorros y consulta de conducta online llegamos a toda la Región de Murcia —incluidas Murcia capital, Cartagena y Molina de Segura— y a toda España.</p>
    </div>
    <div class="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3">
      <p class="font-body-md text-sm text-on-primary opacity-60">© 2025 Centro Canino de Lorca · Lorca, Murcia · Núcleo zoológico ES300240540715</p>
      <p class="font-label-sm text-on-primary opacity-50">5,0 ★ · 16 reseñas en Google</p>
    </div>
  </div>
</footer>

<a href="https://wa.me/34670360676?text=Hola%20Juan%20Miguel%2C%20he%20le%C3%ADdo%20un%20art%C3%ADculo%20del%20blog%20y%20quiero%20contarte%20mi%20caso" target="_blank" rel="noopener" aria-label="Contactar por WhatsApp" class="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-[#25D366] text-white flex items-center justify-center shadow-[0_4px_16px_rgba(0,0,0,0.2)] hover:scale-110 transition-transform">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-7 h-7"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.116 1.527 5.845L.057 23.5l5.773-1.517A11.944 11.944 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.808 9.808 0 01-5.031-1.385l-.361-.214-3.427.9.915-3.332-.235-.373A9.818 9.818 0 012.182 12C2.182 6.57 6.57 2.182 12 2.182S21.818 6.57 21.818 12 17.43 21.818 12 21.818z"/></svg>
</a>

<script>
  document.getElementById('menuBtn').addEventListener('click', function(){ document.getElementById('mobileMenu').classList.toggle('hidden'); });
  document.querySelectorAll('#mobileMenu a').forEach(function(a){ a.addEventListener('click', function(){ document.getElementById('mobileMenu').classList.add('hidden'); }); });
  var observer = new IntersectionObserver(function(entries){ entries.forEach(function(e){ if(e.isIntersecting) e.target.classList.add('visible'); }); }, { threshold:0.12 });
  document.querySelectorAll('.anim').forEach(function(el){ observer.observe(el); });
</script>
__SCHEMA__
  <script src="../cookies-analytics.js" defer></script>
</body>
</html>
"""

WA_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.116 1.527 5.845L.057 23.5l5.773-1.517A11.944 11.944 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.808 9.808 0 01-5.031-1.385l-.361-.214-3.427.9.915-3.332-.235-.373A9.818 9.818 0 012.182 12C2.182 6.57 6.57 2.182 12 2.182S21.818 6.57 21.818 12 17.43 21.818 12 21.818z"/></svg>'

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def fecha_es(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {y}"

def texto_plano(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

def palabras(a):
    return len(texto_plano(a["entradilla"] + a["cuerpo"] + " ".join(a["hoy"])).split())

def jsonstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def exportar_fotos():
    os.makedirs(IMG, exist_ok=True)
    for key, (src, _) in FOTOS.items():
        dst = os.path.join(IMG, key + ".webp")
        im = Image.open(os.path.join(ROOT, src)).convert("RGB")
        w, h = im.size
        if w > 1400:
            im = im.resize((1400, round(h * 1400 / w)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=82)
        print("  foto:", os.path.relpath(dst, ROOT), im.size)

def head(title, meta, canon, ogimg, ogtype="article"):
    return (HEAD.replace("__TITLE__", html.escape(title, quote=True)).replace("__META__", html.escape(meta, quote=True))
                .replace("__CANON__", canon).replace("__OGIMG__", ogimg).replace("__OGTYPE__", ogtype))

def tarjeta(a):
    foto, alt = a["foto"], FOTOS[a["foto"]][1]
    return f"""
      <a href="{a['slug']}.html" class="anim group bg-surface rounded-2xl border border-[#E9E5D9] tonal-shadow overflow-hidden flex flex-col hover:-translate-y-1 transition-transform duration-300">
        <div class="relative overflow-hidden" style="aspect-ratio:16/10;">
          <img src="img/{foto}.webp" alt="{html.escape(alt, quote=True)}" loading="lazy" class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
          <span class="absolute top-3 left-3 font-label-sm text-[11px] uppercase tracking-widest px-2.5 py-1 rounded-full" style="background:rgba(249,247,242,0.92);color:#059669;letter-spacing:0.12em;">{a['categoria']}</span>
        </div>
        <div class="p-6 flex flex-col gap-3 flex-1">
          <h2 class="font-headline-md text-[1.1rem] text-on-surface group-hover:text-primary transition-colors">{a['h1']}</h2>
          <p class="font-body-md text-[0.9rem] text-on-surface-variant leading-relaxed">{a['entradilla'][:150].rsplit(' ', 1)[0]}…</p>
          <div class="mt-auto pt-3 flex items-center justify-between border-t border-[#E9E5D9]">
            <span class="font-label-sm text-on-surface-variant text-xs">{fecha_es(FECHA)} · {max(3, round(palabras(a) / 200))} min de lectura</span>
            <span class="inline-flex items-center gap-1 font-label-md text-[13px] text-primary">Leer <span class="material-symbols-outlined text-[16px] transition-transform group-hover:translate-x-1">arrow_forward</span></span>
          </div>
        </div>
      </a>"""

def pagina_articulo(a):
    por = {x["slug"]: x for x in ARTICULOS}
    foto, alt = a["foto"], FOTOS[a["foto"]][1]
    canon = f"{BASE}blog/{a['slug']}"
    ogimg = f"{BASE}blog/img/{foto}.webp"
    minutos = max(3, round(palabras(a) / 200))
    cta_t, cta_p, cta_href, cta_label = a["cta"]
    wa = WA + "Hola%20Juan%20Miguel%2C%20he%20le%C3%ADdo%20el%20art%C3%ADculo%20%22" + html.escape(a["h1"][:60]).replace(" ", "%20") + "%22%20y%20quiero%20contarte%20mi%20caso"
    hoy = "".join(f"<li>{x}</li>" for x in a["hoy"])
    faq_html = "".join(f"""
      <details class="group rounded-2xl border border-[#E9E5D9] bg-background overflow-hidden">
        <summary class="flex items-center justify-between p-5 cursor-pointer font-label-md text-on-surface select-none">{p}<span class="material-symbols-outlined text-primary transition-transform group-open:rotate-180">expand_more</span></summary>
        <div class="px-5 pb-5 font-body-md text-on-surface-variant">{r}</div>
      </details>""" for p, r in a["faq"])
    rel_html = "".join(tarjeta(por[s]) for s in a["relacionados"] if s in por)
    faq_json = ",\n    ".join(f'{{ "@type": "Question", "name": {jsonstr(p)}, "acceptedAnswer": {{ "@type": "Answer", "text": {jsonstr(r)} }} }}' for p, r in a["faq"])
    schema = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {jsonstr(a['h1'])},
  "description": {jsonstr(a['meta'])},
  "image": "{ogimg}",
  "datePublished": "{FECHA}",
  "dateModified": "{FECHA}",
  "inLanguage": "es",
  "mainEntityOfPage": "{canon}",
  "author": {{ "@type": "Person", "name": "Juan Miguel Marín", "jobTitle": "Adiestrador y etólogo canino", "url": "{BASE}adiestramiento-canino-lorca" }},
  "publisher": {{ "@type": "Organization", "name": "Centro Canino de Lorca", "url": "{BASE}", "logo": {{ "@type": "ImageObject", "url": "{BASE}logo-centro-canino-lorca.jpeg" }} }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Centro Canino de Lorca", "item": "{BASE}" }},
    {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{BASE}blog/" }},
    {{ "@type": "ListItem", "position": 3, "name": {jsonstr(a['h1'])}, "item": "{canon}" }}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faq_json}
  ]
}}
</script>"""
    cuerpo = a["cuerpo"].strip()
    body = f"""
<!-- CABECERA DEL ARTÍCULO -->
<section class="w-full bg-background pt-8 pb-10">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <nav class="flex items-center gap-2 text-on-surface-variant/70 font-label-sm text-xs mb-6">
      <a href="../index.html" class="hover:text-primary transition-colors">Centro Canino de Lorca</a>
      <span class="material-symbols-outlined text-[14px]">chevron_right</span>
      <a href="./" class="hover:text-primary transition-colors">Blog</a>
      <span class="material-symbols-outlined text-[14px]">chevron_right</span>
      <span class="text-on-surface">{a['categoria']}</span>
    </nav>
    <div class="max-w-3xl">
      <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-widest mb-4" style="background:rgba(5,150,105,0.10);color:#059669;letter-spacing:0.12em;">{a['categoria']}</span>
      <h1 class="font-headline-lg text-primary mb-5">{a['h1']}</h1>
      <p class="font-body-md text-[1.125rem] text-on-surface-variant leading-relaxed mb-6">{a['entradilla']}</p>
      <div class="flex items-center gap-3">
        <img src="../logo-centro-canino-lorca.jpeg" alt="" class="w-10 h-10 rounded-full object-cover">
        <div class="leading-tight">
          <p class="font-label-md text-on-surface text-sm">Juan Miguel Marín · adiestrador y etólogo canino</p>
          <p class="font-label-sm text-on-surface-variant text-xs">{fecha_es(FECHA)} · {minutos} min de lectura</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="w-full bg-surface py-10">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <img src="img/{foto}.webp" alt="{html.escape(alt, quote=True)}" class="w-full rounded-2xl object-cover shadow-[0_4px_24px_rgba(5,150,105,0.10)] border border-[#E9E5D9]" style="max-height:520px;">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 mt-12">
      <article class="lg:col-span-8">
        <div class="prose max-w-3xl">
          {cuerpo}
        </div>
        <aside class="caja-hoy max-w-3xl p-6 md:p-8 mt-10">
          <h2 class="font-headline-md text-[1.15rem] text-primary mb-3">Qué puedes hacer hoy</h2>
          <ol class="font-body-md text-on-surface-variant leading-relaxed list-decimal pl-5 flex flex-col gap-2">{hoy}</ol>
        </aside>
        <div class="max-w-3xl mt-10 rounded-2xl p-7 md:p-8 flex flex-col gap-4" style="background:#1c1c1c;">
          <span class="inline-block w-fit px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-widest" style="background:rgba(165,208,185,0.15);color:#d1fae5;letter-spacing:0.12em;">Cuándo pedir ayuda</span>
          <h2 class="font-headline-md text-white">{cta_t}</h2>
          <p class="font-body-md text-[0.95rem] leading-relaxed" style="color:rgba(255,255,255,0.7);">{cta_p}</p>
          <div class="flex flex-col sm:flex-row gap-3 mt-1">
            <a href="{wa}" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 bg-[#25D366] text-white font-label-md font-bold px-5 py-3 rounded-lg hover:opacity-90 transition-opacity">{WA_SVG}Cuéntame tu caso por WhatsApp</a>
            <a href="{ONLINE}" class="inline-flex items-center justify-center gap-2 font-label-md font-bold px-5 py-3 rounded-lg transition-colors" style="background:rgba(255,255,255,0.10);color:#fff;border:1px solid rgba(255,255,255,0.2);">Consulta online para toda España</a>
          </div>
          <a href="{cta_href}" class="font-label-md text-[0.875rem] text-secondary-container underline underline-offset-4 decoration-secondary-container/40 hover:decoration-secondary-container transition-colors w-fit">{cta_label} →</a>
        </div>
        <div class="max-w-3xl mt-12">
          <h2 class="font-headline-md text-primary mb-5">Preguntas frecuentes</h2>
          <div class="flex flex-col gap-4">{faq_html}
          </div>
        </div>
        <div class="max-w-3xl mt-12 rounded-2xl border border-[#E9E5D9] bg-background p-6 md:p-7 flex gap-5 items-start">
          <img src="../juan-miguel.jpg" alt="Juan Miguel, adiestrador canino del Centro Canino de Lorca" class="w-16 h-16 md:w-20 md:h-20 rounded-full object-cover flex-shrink-0 border border-[#E9E5D9]">
          <div>
            <p class="font-label-sm text-on-surface-variant/70 uppercase tracking-wider text-[11px] mb-1">Quién escribe</p>
            <p class="font-headline-md text-[1.05rem] text-on-surface mb-2">Juan Miguel Marín</p>
            <p class="font-body-md text-[0.9rem] text-on-surface-variant leading-relaxed">Adiestrador y etólogo canino, 45 años con perros en el <a href="../index.html" class="text-primary font-semibold underline decoration-primary/30 hover:decoration-primary">Centro Canino de Lorca</a>. Trabaja con familias, no con deportistas ni instituciones, en Lorca, en toda la Región de Murcia y <a href="{ONLINE}" class="text-primary font-semibold underline decoration-primary/30 hover:decoration-primary">por videollamada para toda España</a>.</p>
          </div>
        </div>
      </article>
      <aside class="lg:col-span-4">
        <div class="lg:sticky lg:top-24 flex flex-col gap-6">
          <div class="rounded-2xl p-6 bg-primary text-on-primary flex flex-col gap-3">
            <span class="material-symbols-outlined text-secondary-container text-[28px]" style="font-variation-settings:'FILL' 1;">videocam</span>
            <h3 class="font-headline-md text-[1.1rem]">¿Tu perro tiene este problema?</h3>
            <p class="font-body-md text-[0.9rem] opacity-85 leading-relaxed">Consulta 1:1 por videollamada con Juan Miguel, desde cualquier punto de España. No es un curso grabado: es tu caso y tu perro.</p>
            <a href="{wa}" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 bg-[#25D366] text-white font-label-md font-bold px-5 py-3 rounded-lg hover:opacity-90 transition-opacity mt-1">{WA_SVG}Cuéntame tu caso</a>
            <a href="{ONLINE}" class="font-label-sm text-primary-fixed-dim underline underline-offset-4 text-center">Cómo funciona la consulta online</a>
          </div>
          <div class="rounded-2xl p-6 bg-background border border-[#E9E5D9] flex flex-col gap-3">
            <h3 class="font-headline-md text-[1rem] text-on-surface">En Lorca y la Región de Murcia</h3>
            <a href="{LORCA}" class="font-label-md text-[0.9rem] text-primary hover:underline">Adiestramiento canino en Lorca: 5 clases, 250 €</a>
            <a href="{MURCIA}" class="font-label-md text-[0.9rem] text-primary hover:underline">Adiestramiento para toda la Región de Murcia</a>
            <a href="{GUARDERIA}" class="font-label-md text-[0.9rem] text-primary hover:underline">Guardería canina de día, 1,50 € la hora</a>
            <a href="{RESIDENCIA}" class="font-label-md text-[0.9rem] text-primary hover:underline">Residencia canina</a>
            <a href="{PELU}" class="font-label-md text-[0.9rem] text-primary hover:underline">Peluquería canina, 3º de Europa</a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="w-full bg-background py-16">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <h2 class="font-headline-lg text-primary mb-8">Sigue leyendo</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{rel_html}
    </div>
  </div>
</section>
"""
    return head(a["title"], a["meta"], canon, ogimg) + NAV + body + FOOTER.replace("__SCHEMA__", schema)

def pagina_indice():
    canon = BASE + "blog/"
    ogimg = BASE + "blog/img/no-hace-caso.webp"
    title = "Blog del Centro Canino de Lorca 🐕 conducta, razas y cuidados"
    meta = "Artículos de Juan Miguel, adiestrador con 45 años de experiencia: por qué tu perro ladra solo, tira de la correa o no hace caso, cómo elegir un cachorro y cómo cuidarlo. Sin humo."
    cards = "".join(tarjeta(a) for a in ARTICULOS)
    schema = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "Blog del Centro Canino de Lorca",
  "url": "{canon}",
  "description": {jsonstr(meta)},
  "publisher": {{ "@type": "Organization", "name": "Centro Canino de Lorca", "url": "{BASE}" }},
  "blogPost": [
    {",".join(f'{{ "@type": "BlogPosting", "headline": {jsonstr(a["h1"])}, "url": "{BASE}blog/{a["slug"]}", "datePublished": "{FECHA}" }}' for a in ARTICULOS)}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Centro Canino de Lorca", "item": "{BASE}" }},
    {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{canon}" }}
  ]
}}
</script>"""
    body = f"""
<section class="w-full bg-background pt-10 pb-12">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <nav class="flex items-center gap-2 text-on-surface-variant/70 font-label-sm text-xs mb-6">
      <a href="../index.html" class="hover:text-primary transition-colors">Centro Canino de Lorca</a>
      <span class="material-symbols-outlined text-[14px]">chevron_right</span>
      <span class="text-on-surface">Blog</span>
    </nav>
    <div class="max-w-3xl">
      <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-widest mb-4" style="background:rgba(5,150,105,0.10);color:#059669;letter-spacing:0.12em;">Blog</span>
      <h1 class="font-headline-lg text-primary mb-5">45 años de perros, contados sin humo</h1>
      <p class="font-body-md text-[1.125rem] text-on-surface-variant leading-relaxed">Lo que Juan Miguel explica cada día por teléfono, por escrito: por qué tu perro hace lo que hace, qué funciona y qué no, y cómo elegir y cuidar un perro con cabeza. Si después de leer quieres contarle tu caso, está a un WhatsApp.</p>
    </div>
  </div>
</section>
<section class="w-full bg-surface py-14">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{cards}
    </div>
  </div>
</section>
<section class="w-full bg-background py-16">
  <div class="max-w-container-max-width mx-auto px-margin-mobile md:px-margin-desktop">
    <div class="rounded-2xl p-8 md:p-10 flex flex-col md:flex-row md:items-center gap-6" style="background:#1c1c1c;">
      <div class="flex-1">
        <h2 class="font-headline-lg text-white mb-3">¿Tu perro tiene un problema que no está aquí?</h2>
        <p class="font-body-md" style="color:rgba(255,255,255,0.7);">Cuéntaselo a Juan Miguel por WhatsApp. Si vives en Lorca o la Región de Murcia, lo vemos en el centro; si estás en cualquier otro punto de España, por videollamada.</p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <a href="{WA}Hola%20Juan%20Miguel%2C%20vengo%20del%20blog%20y%20quiero%20contarte%20el%20caso%20de%20mi%20perro" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 bg-[#25D366] text-white font-label-md font-bold px-6 py-3.5 rounded-lg hover:opacity-90 transition-opacity">{WA_SVG}Cuéntame tu caso</a>
        <a href="{ONLINE}" class="inline-flex items-center justify-center gap-2 font-label-md font-bold px-6 py-3.5 rounded-lg" style="background:rgba(255,255,255,0.10);color:#fff;border:1px solid rgba(255,255,255,0.2);">Consulta online</a>
      </div>
    </div>
  </div>
</section>
"""
    return head(title, meta, canon, ogimg, ogtype="website") + NAV + body + FOOTER.replace("__SCHEMA__", schema)

def main():
    os.makedirs(BLOG, exist_ok=True)
    exportar_fotos()
    for a in ARTICULOS:
        out = os.path.join(BLOG, a["slug"] + ".html")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(pagina_articulo(a))
        print(f"  {a['slug']}.html  ({palabras(a)} palabras)")
    with open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina_indice())
    print("  index.html")
    print(f"OK: {len(ARTICULOS)} artículos en public/blog/")

if __name__ == "__main__":
    main()
