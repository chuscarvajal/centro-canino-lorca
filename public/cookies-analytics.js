/* Centro Canino de Lorca
   - Seguimiento de leads en GA4 (clics de llamada, WhatsApp y formularios)
   - Banner de consentimiento de cookies con Google Consent Mode v2
   - Enlace "Configurar cookies" en el pie para cambiar el consentimiento
   Eventos que se envían a GA4:
     lead_llamada     -> clic en un botón/enlace de teléfono (tel:)
     lead_whatsapp    -> clic en un botón/enlace de WhatsApp (wa.me)
     lead_email       -> clic en un enlace de correo (mailto:)
     lead_como_llegar -> clic en un enlace de mapa / cómo llegar
     lead_formulario  -> envío de un formulario de la web
   Cada evento incluye el parámetro "origen" (utm_source/campaña o el sitio
   de procedencia) para poder atribuir de DÓNDE viene cada lead. */
(function () {
  "use strict";
  var KEY = "cc_consent_v1";

  /* ---------- 0) Origen de la visita (atribución) ----------
     Se calcula una vez por sesión (primer toque) y se adjunta a cada lead.
     Prioridad: utm_source[/utm_campaign] del enlace de entrada; si no,
     el dominio de procedencia (referrer); si no, "directo". */
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

  /* ---------- 1) Seguimiento de leads ----------
     Los eventos se envían siempre. Con Consent Mode, si el usuario no ha
     aceptado cookies, GA los recibe de forma anónima (sin cookies). */
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a") : null;
    if (!a || typeof gtag !== "function") return;
    var href = a.getAttribute("href") || "";
    var texto = (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
    var base = { boton: texto, pagina: location.pathname, origen: origen() };
    if (href.indexOf("tel:") === 0) {
      gtag("event", "lead_llamada", base);
    } else if (href.indexOf("wa.me") > -1 || href.indexOf("api.whatsapp") > -1) {
      gtag("event", "lead_whatsapp", base);
    } else if (href.indexOf("mailto:") === 0) {
      gtag("event", "lead_email", base);
    } else if (/(maps\.google|google\.[a-z.]+\/maps|goo\.gl\/maps|maps\.app\.goo\.gl)/i.test(href)) {
      gtag("event", "lead_como_llegar", base);
    }
  }, true);

  Array.prototype.forEach.call(document.querySelectorAll("form"), function (f) {
    f.addEventListener("submit", function () {
      if (typeof gtag === "function") {
        gtag("event", "lead_formulario", { pagina: location.pathname, origen: origen() });
      }
    });
  });

  /* ---------- 2) Consentimiento (Consent Mode) ---------- */
  function setConsent(value) {
    try { localStorage.setItem(KEY, value); } catch (e) {}
    if (typeof gtag === "function") {
      gtag("consent", "update", { analytics_storage: value === "granted" ? "granted" : "denied" });
    }
  }

  function showBanner() {
    if (document.getElementById("cc-bar")) return; // ya está abierto
    var bar = document.createElement("div");
    bar.id = "cc-bar";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", "Aviso de cookies");
    bar.style.cssText = "position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin:0 auto;background:#1c1c1c;color:#fff;border-radius:16px;padding:18px 20px;box-shadow:0 8px 30px rgba(0,0,0,.35);font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.5;";
    bar.innerHTML =
      '<p style="margin:0 0 12px;">Usamos cookies de análisis (Google Analytics) para entender cómo se usa la web y mejorar. ¿Nos das permiso? <a href="politica-cookies.html" style="color:#a7f3d0;text-decoration:underline;">Más información</a>.</p>' +
      '<div style="display:flex;gap:10px;flex-wrap:wrap;">' +
      '<button type="button" id="cc-ok" style="cursor:pointer;border:0;background:#059669;color:#fff;font-weight:700;padding:10px 18px;border-radius:10px;font-size:14px;">Aceptar</button>' +
      '<button type="button" id="cc-no" style="cursor:pointer;border:1px solid rgba(255,255,255,.4);background:transparent;color:#fff;font-weight:600;padding:10px 18px;border-radius:10px;font-size:14px;">Rechazar</button>' +
      "</div>";
    document.body.appendChild(bar);
    function close() { if (bar.parentNode) bar.parentNode.removeChild(bar); }
    document.getElementById("cc-ok").addEventListener("click", function () { setConsent("granted"); close(); });
    document.getElementById("cc-no").addEventListener("click", function () { setConsent("denied"); close(); });
  }

  /* Enlace "Configurar cookies" en el pie (junto a Política de cookies) */
  function injectSettingsLink() {
    if (document.getElementById("cc-settings-link")) return;
    var ref = document.querySelector('footer a[href$="politica-cookies.html"]');
    if (!ref) return;
    var link = document.createElement("a");
    link.id = "cc-settings-link";
    link.href = "#";
    link.textContent = "Configurar cookies";
    link.className = ref.className; // misma estética que el resto de enlaces del pie
    link.addEventListener("click", function (e) { e.preventDefault(); showBanner(); });
    ref.parentNode.insertBefore(link, ref.nextSibling);
  }

  function init() {
    origen(); // fija el origen de la sesión en la primera carga (con el UTM aún en la URL)
    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) {}
    if (saved === "granted" && typeof gtag === "function") {
      gtag("consent", "update", { analytics_storage: "granted" });
    } else if (saved !== "granted" && saved !== "denied") {
      showBanner(); // primera visita: pedir consentimiento
    }
    injectSettingsLink(); // siempre, para poder cambiar la elección
  }

  if (document.body) init();
  else document.addEventListener("DOMContentLoaded", init);
})();

/* ---------- 3) Analítica propia de clics en CTAs (sin cookies, sin terceros) ----------
   Envía {cta, section, page, ts} a la función de Netlify /track; el panel está en
   /.netlify/functions/stats?key=... Las secciones solo llevan clases de Tailwind, así que
   se etiquetan por su titular: "hero" si contiene el H1 y, si no, el H2/H3 en slug. */
(function(){
  function slug(t){return (t||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,32)||'seccion';}
  function ctaOf(a){
    var h=(a.getAttribute('href')||'');
    if(h.indexOf('tel:')===0)return'llamar';
    if(/wa\.me|whatsapp|api\.whatsapp/i.test(h))return'whatsapp';
    if(h.indexOf('mailto:')===0)return'email';
    if(/google\.[a-z.]+\/maps|maps\.app\.goo|maps\.google\./i.test(h))return'mapa';
    return a.getAttribute('data-cta')||null;
  }
  function sectionOf(el){
    var d=el.closest('[data-section]'); if(d)return d.getAttribute('data-section');
    if(el.closest('footer'))return'footer';
    if(el.closest('nav'))return'menu';
    if(el.closest('header'))return'cabecera';
    if(el.closest('.fixed'))return'flotante';
    var s=el.closest('section,aside'); if(!s)return'otro';
    if(s.id)return s.id;
    var h=s.querySelector('h1,h2,h3'); if(!h)return'seccion';
    return h.tagName==='H1'?'hero':slug(h.textContent);
  }
  function send(cta,section){
    try{
      var b=JSON.stringify({cta:cta,section:section,page:location.pathname,ts:new Date().toISOString()});
      if(navigator.sendBeacon){navigator.sendBeacon('/.netlify/functions/track',b);}
      else{fetch('/.netlify/functions/track',{method:'POST',body:b,keepalive:true});}
    }catch(e){}
  }
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href],[data-cta]'); if(!a)return;
    var c=ctaOf(a); if(!c)return; send(c,sectionOf(a));
  },true);
  document.addEventListener('submit',function(e){
    var f=e.target; if(f&&f.tagName==='FORM') send('formulario',sectionOf(f));
  },true);
})();
