/* Centro Canino de Lorca
   - Seguimiento de leads en GA4 (clics de llamada, WhatsApp y formularios)
   - Banner de consentimiento de cookies con Google Consent Mode v2
   Eventos que se envían a GA4:
     lead_llamada     -> clic en un botón/enlace de teléfono (tel:)
     lead_whatsapp    -> clic en un botón/enlace de WhatsApp (wa.me)
     lead_formulario  -> envío de un formulario de la web
*/
(function () {
  "use strict";

  /* ---------- 1) Seguimiento de leads ----------
     Los eventos se envían siempre. Con Consent Mode, si el usuario no ha
     aceptado cookies, GA los recibe de forma anónima (sin cookies). */
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a") : null;
    if (!a || typeof gtag !== "function") return;
    var href = a.getAttribute("href") || "";
    var texto = (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
    if (href.indexOf("tel:") === 0) {
      gtag("event", "lead_llamada", { boton: texto, pagina: location.pathname });
    } else if (href.indexOf("wa.me") > -1 || href.indexOf("api.whatsapp") > -1) {
      gtag("event", "lead_whatsapp", { boton: texto, pagina: location.pathname });
    }
  }, true);

  Array.prototype.forEach.call(document.querySelectorAll("form"), function (f) {
    f.addEventListener("submit", function () {
      if (typeof gtag === "function") {
        gtag("event", "lead_formulario", { pagina: location.pathname });
      }
    });
  });

  /* ---------- 2) Consentimiento de cookies (Consent Mode) ---------- */
  var KEY = "cc_consent_v1", saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}

  if (saved === "granted") {
    if (typeof gtag === "function") gtag("consent", "update", { analytics_storage: "granted" });
    return; // ya aceptó: sin banner
  }
  if (saved === "denied") return; // ya rechazó: no insistimos

  function build() {
    var bar = document.createElement("div");
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
    document.getElementById("cc-ok").addEventListener("click", function () {
      try { localStorage.setItem(KEY, "granted"); } catch (e) {}
      if (typeof gtag === "function") gtag("consent", "update", { analytics_storage: "granted" });
      close();
    });
    document.getElementById("cc-no").addEventListener("click", function () {
      try { localStorage.setItem(KEY, "denied"); } catch (e) {}
      close();
    });
  }

  if (document.body) build();
  else document.addEventListener("DOMContentLoaded", build);
})();
