# -*- coding: utf-8 -*-
"""
mejorar_titulos_metas_ctr.py — Centro Canino de Lorca (Chus Carvajal)

Mejora los TÍTULOS SEO (title + og:title) de las páginas comerciales con frases
gancho + un emoji relevante para subir el CTR, y añade un emoji temático al inicio
de la meta descripción y og:description (que ya llevan el 📞 + teléfono).

- Título (<title>): keyword delante + emoji separador + gancho. SEO.
- og:title: versión orientada a beneficio + emoji (redes/WhatsApp lo muestran siempre).
- Las páginas legales NO se tocan (emoji en legales queda poco profesional).

Uso:  python tools/mejorar_titulos_metas_ctr.py
"""
import sys, os, re
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PUBLIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")

M = {
 "index.html": {
   "title":   "Centro Canino de Lorca 🐾 Adiestramiento y Residencia · 5,0★",
   "ogtitle": "Centro Canino de Lorca 🐾 Todo para tu perro en un solo sitio",
   "demoji":  "🐾",
 },
 "adiestramiento-canino-lorca.html": {
   "title":   "Adiestramiento Canino en Lorca 🐕 100% de casos resueltos",
   "ogtitle": "Adiestramiento Canino en Lorca 🐕 el 100% de los casos, resueltos",
   "demoji":  "🐕",
 },
 "adiestramiento-canino-online.html": {
   "title":   "Adiestramiento Canino Online 💻 Consulta 1:1 · 45 años",
   "ogtitle": "Adiestramiento Canino Online 💻 una consulta 1:1, no un curso",
   "demoji":  "💻",
 },
 "residencia-canina-lorca.html": {
   "title":   "Residencia y Guardería Canina en Lorca 🏡 45 años · 5,0★",
   "ogtitle": "Residencia Canina en Lorca 🏡 donde los perros no quieren irse",
   "demoji":  "🏡",
 },
 "cachorros-lorca.html": {
   "title":   "Cachorros y Criadero de Perros en Lorca 🐶 Cría selectiva",
   "ogtitle": "Cachorros en Lorca 🐶 criadero con cría selectiva, no en cadena",
   "demoji":  "🐶",
 },
 "cachorros-pastor-aleman-de-trabajo.html": {
   "title":   "Cachorros de Pastor Alemán de Trabajo en Lorca 🦮 Salud certificada",
   "ogtitle": "Cachorros de Pastor Alemán de Trabajo 🦮 línea de trabajo, no belleza",
   "demoji":  "🦮",
 },
 "cachorros-caniche-gigante.html": {
   "title":   "Cachorros de Caniche Gigante en Lorca 🐩 Referente en Murcia",
   "ogtitle": "Caniche Gigante en Lorca 🐩 inteligente, hipoalergénico y familiar",
   "demoji":  "🐩",
 },
 "peluqueria-canina-lorca.html": {
   "title":   "Peluquería Canina en Lorca ✂️ Corte a tijera de exposición",
   "ogtitle": "Peluquería Canina en Lorca ✂️ corte a tijera, 3º de Europa",
   "demoji":  "✂️",
 },
}


def process(path):
    fn = os.path.basename(path)
    if fn not in M:
        return None
    m = M[fn]
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html

    html = re.sub(r'(<title>).*?(</title>)',
                  lambda x: x.group(1) + m["title"] + x.group(2), html, count=1)
    html = re.sub(r'(<meta property="og:title" content=").*?(")',
                  lambda x: x.group(1) + m["ogtitle"] + x.group(2), html, count=1)

    def prep(x):
        pre, content, post = x.group(1), x.group(2), x.group(3)
        if not content.lstrip().startswith(m["demoji"]):
            content = m["demoji"] + " " + content
        return pre + content + post

    html = re.sub(r'(<meta name="description" content=")(.*?)(")', prep, html, count=1)
    html = re.sub(r'(<meta property="og:description" content=")(.*?)(")', prep, html, count=1)

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    changed = 0
    for fn in M:
        path = os.path.join(PUBLIC, fn)
        r = process(path)
        if r:
            changed += 1
            print("  ✔", fn, "→", M[fn]["title"], f"({len(M[fn]['title'])} car.)")
    print(f"\n{changed} páginas actualizadas.")


if __name__ == "__main__":
    main()
