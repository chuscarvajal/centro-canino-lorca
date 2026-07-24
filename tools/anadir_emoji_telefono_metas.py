# -*- coding: utf-8 -*-
"""
anadir_emoji_telefono_metas.py — Centro Canino de Lorca (Chus Carvajal)

Añade el emoji de teléfono (📞) justo delante del número en TODAS las meta
descripciones del proyecto (meta name="description" y og:description) para
subir el CTR en Google. NO toca el <title> ni el teléfono del Schema/JSON-LD.

De paso corrige dos descripciones que superaban el límite recomendado
(~155-160 car.) para que Google no las trunque.

Uso:  python tools/anadir_emoji_telefono_metas.py
"""
import sys, os, re, glob
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PUBLIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
PHONE = "670 36 06 76"
EMOJI = "📞"

# Reescrituras de descripciones demasiado largas (se aplican a description Y og:description).
# El emoji se inserta después por el paso general.
REWRITES = {
    "cachorros-lorca.html":
        "Criadero de perros en Lorca (Murcia): pastor alemán de trabajo y caniche "
        "gigante, cría selectiva con protocolo sanitario completo. Llama al 670 36 06 76.",
    "cachorros-pastor-aleman-de-trabajo.html":
        "Cachorros de pastor alemán de trabajo en Lorca (Murcia): 45 años de selección "
        "y protocolo sanitario completo. Envíos a toda España. Llama al 670 36 06 76.",
}


def add_emoji(text):
    """Inserta 📞 delante del número. Limpia 'Tel. ' redundante. Idempotente."""
    if EMOJI in text:
        return text
    # 'Tel. 670...' -> '📞 670...'  (evita "Tel. 📞")
    text = text.replace("Tel. " + PHONE, EMOJI + " " + PHONE)
    # cualquier otro '670...' que no lleve ya el emoji
    text = re.sub(r"(?<!📞 )" + re.escape(PHONE), EMOJI + " " + PHONE, text)
    return text


def process(path):
    fn = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html

    def repl(m):
        pre, content, post = m.group(1), m.group(2), m.group(3)
        # reescritura por longitud si aplica
        if fn in REWRITES:
            content = REWRITES[fn]
        content = add_emoji(content)
        return pre + content + post

    for attr in (r'name="description"', r'property="og:description"'):
        pat = re.compile(r'(<meta ' + attr + r' content=")(.*?)(")')
        html = pat.sub(repl, html)

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    changed = 0
    for path in sorted(glob.glob(os.path.join(PUBLIC, "*.html"))):
        if process(path):
            changed += 1
            print("  ✔", os.path.basename(path))
    print(f"\n{changed} archivos actualizados.")


if __name__ == "__main__":
    main()
