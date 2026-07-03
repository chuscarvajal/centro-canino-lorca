# -*- coding: utf-8 -*-
"""
optimizar_imagenes_seo.py — Centro Canino de Lorca (Rank Masters · Chus Carvajal)

Estampa en cada imagen SERVIDA por la web:
  - ImageDescription  -> descripción SEO (leída por Google/Bing en Image Search)
  - XPTitle / XPSubject / XPKeywords -> título, asunto y keywords (campos Windows/Explorer)
  - Artist / Copyright / Software -> autoría
  - GPS (lat/lon) -> geolocalización EN LORCA (MURCIA) para señales locales

Estrategia sin pérdida:
  - JPEG y WebP  -> piexif.insert()  (inyecta metadatos SIN recodificar la imagen)
  - PNG          -> Pillow save(exif=...) (PNG es lossless, no hay pérdida)

Uso:  python tools/optimizar_imagenes_seo.py            (aplica)
      python tools/optimizar_imagenes_seo.py --check    (solo lee y muestra EXIF)
"""
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import piexif
from PIL import Image

PUBLIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")

# Ubicación EXACTA del Centro Canino de Lorca (Camino de los Valencianos, Lorca, Murcia)
LAT, LON = 37.6014375, -1.6675633

ARTIST    = "Centro Canino de Lorca — Juan Miguel Marín"
COPYRIGHT = "© Centro Canino de Lorca · Lorca (Murcia) · centrocaninodelorca.es"
SOFTWARE  = "Rank Masters — Chus Carvajal (SEO local)"
GEO_TAIL  = "Centro Canino de Lorca, Lorca, Murcia, España"

# file: (título, descripción SEO, keywords extra)
MANIFEST = {
 "logo-centro-canino-lorca.jpeg": (
    "Logo del Centro Canino de Lorca",
    "Logotipo del Centro Canino de Lorca, adiestramiento, residencia, cría y peluquería canina en Lorca (Murcia).",
    "logo, centro canino"),
 "juan-miguel.jpg": (
    "Juan Miguel Marín, adiestrador y etólogo canino en Lorca",
    "Juan Miguel Marín, adiestrador, etólogo y criador canino con 45 años de experiencia en el Centro Canino de Lorca (Murcia).",
    "adiestrador canino, etólogo, Juan Miguel Marín"),
 "el-adiestrador.webp": (
    "Adiestrador canino observando el comportamiento de un perro en Lorca",
    "Juan Miguel observando la conducta de un perro durante el diagnóstico de comportamiento en el Centro Canino de Lorca (Murcia).",
    "adiestrador canino Lorca, comportamiento canino"),
 "clases-adiestramiento-canino-lorca.webp": (
    "Clase de adiestramiento canino en Lorca",
    "Clase de adiestramiento canino en el Centro Canino de Lorca: programa de obediencia y modificación de conducta en Lorca (Murcia).",
    "clases de adiestramiento canino, obediencia"),
 "servicio-adiestramiento-canino.webp": (
    "Modificación de conducta de un perro adulto en Lorca",
    "Sesión de educación canina y modificación de conducta con un perro adulto en el Centro Canino de Lorca (Murcia).",
    "modificación de conducta, educación canina"),
 "cluster-adiestramiento-canino.webp": (
    "Adiestramiento canino en Lorca",
    "Adiestramiento canino en Lorca con método propio y 45 años de experiencia en el Centro Canino de Lorca (Murcia).",
    "adiestramiento canino Lorca"),
 "videollamada-1a1.webp": (
    "Adiestramiento canino online por videollamada 1:1",
    "Consulta de adiestramiento canino online uno a uno por videollamada con Juan Miguel, del Centro Canino de Lorca (Murcia).",
    "adiestramiento canino online, videollamada"),
 "como-funciona-online.webp": (
    "Asesoría canina online por videollamada",
    "Juan Miguel toma notas mientras observa a un perro por videollamada en una asesoría canina online del Centro Canino de Lorca (Murcia).",
    "asesoría canina online, educador canino online"),
 "adiestramiento-online.webp": (
    "Adiestramiento canino online — consulta por videollamada",
    "Servicio de adiestramiento canino online por videollamada del Centro Canino de Lorca (Murcia), para toda España.",
    "adiestramiento canino online, comportamiento canino online"),
 "diferencia-trabajo-belleza.webp": (
    "Pastor alemán de línea de trabajo frente a línea de belleza",
    "Diferencia entre un pastor alemán de línea de trabajo y uno de belleza, criados en el Centro Canino de Lorca (Murcia).",
    "pastor alemán de trabajo, línea de trabajo"),
 "reproductor-macho.webp": (
    "Reproductor macho de pastor alemán de trabajo en Lorca",
    "Reproductor macho de pastor alemán de línea de trabajo del criadero del Centro Canino de Lorca (Murcia).",
    "reproductor pastor alemán, criadero Lorca"),
 "reproductora-hembra.webp": (
    "Reproductora hembra de pastor alemán de trabajo en Lorca",
    "Reproductora hembra de pastor alemán de línea de trabajo del criadero del Centro Canino de Lorca (Murcia).",
    "reproductora pastor alemán, criadero Lorca"),
 "cluster-cachorros-pastor-aleman.png": (
    "Cachorro de pastor alemán de trabajo junto a un adulto",
    "Cachorro de pastor alemán de trabajo con un adulto; formación temprana desde las 6 semanas en el Centro Canino de Lorca (Murcia).",
    "cachorros pastor alemán, adiestramiento de cachorros"),
 "cachorros-pastor-aleman-hero.webp": (
    "Cachorros de pastor alemán de trabajo en Lorca",
    "Cachorros de pastor alemán de línea de trabajo con protocolo sanitario completo, criados en el Centro Canino de Lorca (Murcia).",
    "cachorros pastor alemán de trabajo Lorca"),
 "caniche-gigante-talla-real.webp": (
    "Tamaño real del caniche gigante frente al mediano, enano y toy",
    "Comparativa del tamaño real de un caniche gigante frente a las tallas mediana, enana y toy; cría en el Centro Canino de Lorca (Murcia).",
    "caniche gigante, poodle gigante, talla"),
 "caniche-gigante-familia.webp": (
    "Caniche gigante adulto, inteligente e hipoalergénico para familias",
    "Caniche gigante adulto, perro inteligente e hipoalergénico ideal para familias, criado en el Centro Canino de Lorca (Murcia).",
    "caniche gigante hipoalergénico, perro para familias"),
 "reproductor-macho-caniche.webp": (
    "Reproductor macho de caniche gigante en Lorca",
    "Reproductor macho de caniche gigante del criadero del Centro Canino de Lorca (Murcia).",
    "reproductor caniche gigante, criadero Lorca"),
 "reproductora-hembra-caniche.webp": (
    "Reproductora hembra de caniche gigante en Lorca",
    "Reproductora hembra de caniche gigante del criadero del Centro Canino de Lorca (Murcia).",
    "reproductora caniche gigante, criadero Lorca"),
 "cachorro-caniche-gigante.webp": (
    "Cachorro de caniche gigante en Lorca",
    "Cachorro de caniche gigante con protocolo sanitario completo, criado en el Centro Canino de Lorca (Murcia). Envíos a toda España.",
    "cachorros caniche gigante Lorca"),
 "corte-caniche-peluqueria-canina-profesional.png": (
    "Peluquería canina: corte de caniche gigante en Lorca",
    "Corte de exposición a tijera de un caniche gigante en la peluquería canina del Centro Canino de Lorca (Murcia).",
    "peluquería canina Lorca, corte a tijera, stripping"),
 "hero-peluqueria.webp": (
    "Peluquería canina de exposición en Lorca",
    "Peluquería canina artesanal en Lorca (Murcia): cortes de exposición a tijera y stripping en el Centro Canino de Lorca.",
    "peluquería canina Lorca, cortes de exposición"),
 "hero-homepage.webp": (
    "Instalaciones de la residencia canina en Lorca",
    "Instalaciones de la residencia canina del Centro Canino de Lorca (Murcia), con supervisión real 24 h y 45 años de experiencia.",
    "residencia canina Lorca, instalaciones"),
 "la-estancia.webp": (
    "Perro cuidado en la residencia canina de Lorca",
    "Perro atendido en la residencia canina del Centro Canino de Lorca (Murcia), con pocas plazas y supervisión constante.",
    "residencia canina Lorca, estancia perros"),
 "guarderia-canina-lorca-zona-verde-cesped.webp": (
    "Zona verde de la guardería y residencia canina en Lorca",
    "Zona verde con césped de la guardería y residencia canina del Centro Canino de Lorca (Murcia).",
    "guardería canina Lorca, zona verde, residencia canina"),
 "hero-home-1.webp": (
    "Instalaciones del Centro Canino de Lorca",
    "Instalaciones del Centro Canino de Lorca (Murcia): adiestramiento, residencia, cría y peluquería canina con 45 años de experiencia.",
    "centro canino Lorca, instalaciones, boxes"),
 "hero-home-2.webp": (
    "Centro Canino de Lorca — servicios caninos en Lorca",
    "Centro Canino de Lorca (Murcia): adiestramiento, residencia canina, cría selectiva y peluquería con Juan Miguel Marín.",
    "centro canino Lorca, servicios caninos"),
 "hero-home-3.webp": (
    "Zona verde de la residencia del Centro Canino de Lorca",
    "Zona verde de la residencia canina del Centro Canino de Lorca (Murcia), amplio espacio al aire libre para los perros.",
    "residencia canina Lorca, zona verde"),
}

def dms(value):
    v = abs(value)
    d = int(v); m = int((v - d) * 60); s = round((v - d - m/60) * 3600 * 10000)
    return ((d, 1), (m, 1), (s, 10000))

def build_exif(title, desc, kw):
    keywords = f"{kw}, {GEO_TAIL}"
    zeroth = {
        piexif.ImageIFD.ImageDescription: desc.encode("utf-8"),
        piexif.ImageIFD.Artist: ARTIST.encode("utf-8"),
        piexif.ImageIFD.Copyright: COPYRIGHT.encode("utf-8"),
        piexif.ImageIFD.Software: SOFTWARE.encode("utf-8"),
        piexif.ImageIFD.XPTitle:    (title + "\x00").encode("utf-16le"),
        piexif.ImageIFD.XPSubject:  (desc + "\x00").encode("utf-16le"),
        piexif.ImageIFD.XPKeywords: (keywords + "\x00").encode("utf-16le"),
        piexif.ImageIFD.XPComment:  (COPYRIGHT + "\x00").encode("utf-16le"),
    }
    gps = {
        piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef: b"N" if LAT >= 0 else b"S",
        piexif.GPSIFD.GPSLatitude: dms(LAT),
        piexif.GPSIFD.GPSLongitudeRef: b"E" if LON >= 0 else b"W",
        piexif.GPSIFD.GPSLongitude: dms(LON),
        piexif.GPSIFD.GPSMapDatum: b"WGS-84",
    }
    return piexif.dump({"0th": zeroth, "Exif": {}, "GPS": gps, "1st": {}, "thumbnail": None})

def stamp(path, exif_bytes):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".jpg", ".jpeg", ".webp"):
        try:
            piexif.insert(exif_bytes, path)
            return "insert (sin pérdida)"
        except Exception as e:
            im = Image.open(path)
            params = {"exif": exif_bytes}
            if ext == ".webp":
                params.update(quality=92, method=6)
            im.save(path, **params)
            return f"pillow-fallback ({e.__class__.__name__})"
    else:  # png
        im = Image.open(path)
        im.save(path, exif=exif_bytes)
        return "pillow-png (lossless)"

def gps_to_deg(dms_t, ref):
    d = dms_t[0][0]/dms_t[0][1]; m = dms_t[1][0]/dms_t[1][1]; s = dms_t[2][0]/dms_t[2][1]
    val = d + m/60 + s/3600
    return -val if ref in (b"S", b"W") else val

def check(path):
    try:
        ex = piexif.load(path)
    except Exception as e:
        return f"  (sin EXIF legible: {e})"
    desc = ex["0th"].get(piexif.ImageIFD.ImageDescription, b"").decode("utf-8", "ignore")
    g = ex.get("GPS", {})
    if piexif.GPSIFD.GPSLatitude in g:
        lat = gps_to_deg(g[piexif.GPSIFD.GPSLatitude], g[piexif.GPSIFD.GPSLatitudeRef])
        lon = gps_to_deg(g[piexif.GPSIFD.GPSLongitude], g[piexif.GPSIFD.GPSLongitudeRef])
        geo = f"GPS {lat:.5f},{lon:.5f}"
    else:
        geo = "SIN GPS"
    return f"  {geo} | desc: {desc[:70]}"

def main():
    only_check = "--check" in sys.argv
    ok = miss = 0
    for fname, (title, desc, kw) in MANIFEST.items():
        path = os.path.join(PUBLIC, fname)
        if not os.path.exists(path):
            print(f"[FALTA] {fname}"); miss += 1; continue
        if only_check:
            print(f"[{fname}]"); print(check(path)); ok += 1; continue
        exif_bytes = build_exif(title, desc, kw)
        how = stamp(path, exif_bytes)
        print(f"[OK] {fname:52} {how}")
        print(check(path))
        ok += 1
    print(f"\nTotal: {ok} procesadas, {miss} no encontradas. Coordenadas: {LAT},{LON} (Lorca, Murcia)")

if __name__ == "__main__":
    main()
