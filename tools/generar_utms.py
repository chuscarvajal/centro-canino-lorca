# -*- coding: utf-8 -*-
"""
generar_utms.py — Centro Canino de Lorca (Rank Masters · Chus Carvajal)

Genera los enlaces con parámetros UTM para cada canal que controlamos fuera de
la web (perfil de Google, citaciones/directorios, redes sociales). Al pegar el
enlace etiquetado en el campo "sitio web" de cada ficha, GA4 atribuye la visita
—y el lead— a ese canal concreto. Así sabemos de DÓNDE viene cada llamada,
WhatsApp, email o formulario.

Salida: .tmp/utms_centrocaninodelorca.csv  (Canal | Dónde se pega | URL etiquetada)
"""
import sys, io, os, csv, re, unicodedata
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

BASE = "https://centrocaninodelorca.es/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(ROOT, "directorios-guarderia-canina-murcia.csv")
OUT = os.path.join(ROOT, ".tmp", "utms_centrocaninodelorca.csv")

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)

def url(source, medium, campaign):
    return f"{BASE}?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}"

rows = []  # (canal, donde, url)

# --- Canales fijos principales ---
rows.append(("Perfil de Google (botón Sitio web)", "GBP > Editar > Sitio web",
             url("gbp", "perfil", "google-business")))
rows.append(("Perfil de Google (publicaciones)", "GBP > Novedades/Ofertas (enlace del post)",
             url("gbp", "post", "google-business")))
rows.append(("Instagram (bio)", "Instagram > Editar perfil > Sitio web",
             url("instagram", "social", "bio")))
rows.append(("Facebook (página)", "Facebook > Información > Sitio web",
             url("facebook", "social", "bio")))
rows.append(("WhatsApp / firma", "Mensajes o firma de correo compartiendo la web",
             url("whatsapp", "mensaje", "difusion")))

# --- Citaciones / directorios (desde el CSV) ---
if os.path.exists(CSV_DIR):
    with io.open(CSV_DIR, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            name = (r.get("Directorio") or "").strip()
            if not name or name.lower() == "google business profile":
                continue  # GBP ya está arriba con su propio esquema
            rows.append((f"Directorio: {name}", "Campo 'sitio web' de la ficha",
                         url(slug(name), "citacion", "directorios")))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Canal", "Dónde se pega", "URL etiquetada"])
    w.writerows(rows)

print(f"Generados {len(rows)} enlaces UTM -> {os.path.relpath(OUT, ROOT)}\n")
print("PRINCIPALES:")
for canal, donde, u in rows[:6]:
    print(f"  · {canal}\n      {u}")
