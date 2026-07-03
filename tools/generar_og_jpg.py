# -*- coding: utf-8 -*-
"""
generar_og_jpg.py — Centro Canino de Lorca (Rank Masters · Chus Carvajal)

Crea una copia JPG de cada imagen usada como og:image (para que la vista previa
al compartir en WhatsApp/Facebook, que no renderizan WebP, funcione siempre).
Mantiene el WebP en la web para velocidad. Conserva el EXIF (geolocalización).
"""
import sys, os, io
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from PIL import Image
import piexif

PUBLIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")

OG_IMAGES = [
    "adiestramiento-online.webp",
    "cachorro-caniche-gigante.webp",
    "cachorros-pastor-aleman-hero.webp",
    "cluster-adiestramiento-canino.webp",
    "hero-home-1.webp",
    "hero-peluqueria.webp",
]

for name in OG_IMAGES:
    src = os.path.join(PUBLIC, name)
    dst = os.path.join(PUBLIC, os.path.splitext(name)[0] + ".jpg")
    if not os.path.exists(src):
        print(f"[FALTA] {name}"); continue
    im = Image.open(src).convert("RGB")
    # conservar EXIF (geolocalización + descripción) si el webp lo tiene
    exif_bytes = b""
    try:
        exif_bytes = piexif.dump(piexif.load(src))
    except Exception:
        exif_bytes = im.info.get("exif", b"")
    params = dict(quality=85, optimize=True, progressive=True)
    if exif_bytes:
        params["exif"] = exif_bytes
    im.save(dst, "JPEG", **params)
    kb = os.path.getsize(dst) / 1024
    print(f"[OK] {os.path.basename(dst):40} {im.size[0]}x{im.size[1]}  {kb:.0f} KB")
print("\nHecho. Ahora hay que apuntar og:image/twitter:image a los .jpg en el HTML.")
