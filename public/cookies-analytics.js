/* Centro Canino de Lorca — medición sin cookies
   - Analítica propia de clics en CTAs (Netlify Functions + Blobs): llamar, WhatsApp, email,
     mapa y formularios, con fecha, página, sección y ORIGEN de la visita. Panel privado en
     /.netlify/functions/stats?key=...
   - Google Analytics sigue cargado, pero en Consent Mode con todo denegado y sin banner:
     no instala cookies y solo recibe datos anónimos. Por eso ya no hace falta pedir permiso.
   Origen = utm_source[/utm_campaign] del enlace de entrada (p. ej. "gbp/peluqueria" de los
   posts de Google Business); si no hay UTM, el dominio de procedencia; si no, "directo".
   Se guarda en sessionStorage (no es una cookie y se borra al cerrar la pestaña). */
(function () {
  "use strict";

  /* Limpia la elección guardada por el antiguo banner de cookies */
  try { localStorage.removeItem("cc_consent_v1"); } catch (e) {}

  /* ---------- 1) Origen de la visita (primer toque de la sesión) ---------- */
  function origen() {
    try {
      var stored = sessionStorage.getItem("cc_origen");
      if (stored) return stored;
      var p = new URLSearchParams(location.search);
      var s = p.get("utm_source"), c = p.get("utm_campaign"), val;
      if (s) {
        val = c ? s + "/" + c : s;
      } else if (document.referrer) {
        var h = new URL(document.referrer).hostname.replace(/^www\./, "");
        val = (h === location.hostname) ? "directo" : h;
      } else {
        val = "directo";
      }
      sessionStorage.setItem("cc_origen", val);
      return val;
    } catch (e) { return "desconocido"; }
  }
  origen(); // fija el origen en la primera carga, con el UTM aún en la URL

  /* ---------- 2) Clics en CTAs → panel propio en Netlify ----------
     Las secciones solo llevan clases de Tailwind, así que se etiquetan por su titular:
     "hero" si contiene el H1 y, si no, el H2/H3 en slug. */
  function slug(t) { return (t || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 32) || "seccion"; }
  function ctaOf(a) {
    var h = (a.getAttribute("href") || "");
    if (h.indexOf("tel:") === 0) return "llamar";
    if (/wa\.me|whatsapp|api\.whatsapp/i.test(h)) return "whatsapp";
    if (h.indexOf("mailto:") === 0) return "email";
    if (/google\.[a-z.]+\/maps|maps\.app\.goo|maps\.google\.|goo\.gl\/maps/i.test(h)) return "mapa";
    return a.getAttribute("data-cta") || null;
  }
  function sectionOf(el) {
    var d = el.closest("[data-section]"); if (d) return d.getAttribute("data-section");
    if (el.closest("footer")) return "footer";
    if (el.closest("nav")) return "menu";
    if (el.closest("header")) return "cabecera";
    if (el.closest(".fixed")) return "flotante";
    var s = el.closest("section,aside"); if (!s) return "otro";
    if (s.id) return s.id;
    var h = s.querySelector("h1,h2,h3"); if (!h) return "seccion";
    return h.tagName === "H1" ? "hero" : slug(h.textContent);
  }
  function send(cta, section) {
    try {
      var b = JSON.stringify({ cta: cta, section: section, page: location.pathname, origen: origen(), ts: new Date().toISOString() });
      if (navigator.sendBeacon) { navigator.sendBeacon("/.netlify/functions/track", b); }
      else { fetch("/.netlify/functions/track", { method: "POST", body: b, keepalive: true }); }
    } catch (e) {}
  }

  /* ---------- 3) Los mismos clics a Google Analytics (anónimos, sin cookies) ---------- */
  var GA = { llamar: "lead_llamada", whatsapp: "lead_whatsapp", email: "lead_email", mapa: "lead_como_llegar" };
  function ga(cta, el) {
    if (typeof gtag !== "function" || !GA[cta]) return;
    var texto = (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
    gtag("event", GA[cta], { boton: texto, pagina: location.pathname, origen: origen() });
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href],[data-cta]"); if (!a) return;
    var c = ctaOf(a); if (!c) return;
    send(c, sectionOf(a)); ga(c, a);
  }, true);
  document.addEventListener("submit", function (e) {
    var f = e.target; if (!f || f.tagName !== "FORM") return;
    send("formulario", sectionOf(f));
    if (typeof gtag === "function") gtag("event", "lead_formulario", { pagina: location.pathname, origen: origen() });
  }, true);
})();
