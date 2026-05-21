// Rapaport Family Tree — access gate
// Validates a per-person ES256 JWT magic-link token before loading the SPA.
// Public key lives at assets/auth/pubkey.json. Private key NEVER leaves Doron's home PC.

// Capture the PWA install prompt event AS EARLY AS POSSIBLE so it isn't missed.
// Chrome only fires beforeinstallprompt once per session — if our listener is added
// after the gate validates the token, we miss it. So grab it synchronously here at top.
window.__rftInstallEvent = null;
window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  window.__rftInstallEvent = e;
  // Notify upload-feature.js if it's already loaded
  if (window.__rftOnInstallReady) try { window.__rftOnInstallReady(e); } catch {}
});
window.addEventListener("appinstalled", () => {
  window.__rftInstallEvent = null;
  document.getElementById("rft-install-bar")?.remove();
  document.getElementById("rft-install-modal")?.remove();
});

(async function () {
  "use strict";

  // Cache-bust static data fetches so GitHub Pages CDN doesn't serve stale JSON.
  // Only touches relative `data/...` and `assets/auth/pubkey.json` URLs — leaves
  // Firebase SDK + everything else alone.
  const _origFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    try {
      const url = typeof input === "string" ? input : (input?.url || "");
      // Cache-bust all relative same-origin assets (JSON + JS modules)
      if (/^(data\/|assets\/)[^?#]*\.(json|js|mjs|webmanifest)/.test(url)) {
        const sep = url.includes("?") ? "&" : "?";
        const busted = url + sep + "v=" + Date.now();
        return _origFetch(busted, init);
      }
    } catch {}
    return _origFetch(input, init);
  };

  const STORAGE_KEY = "rft.auth.v1";
  // BUILD bumps on every deploy so browsers fetch the latest JS modules,
  // not a stale cached copy. If you don't see Research Center updates, this
  // is the line that fixes it.
  const BUILD = "2026-05-21-t8";
  const APP_SCRIPT_SRC = `assets/js/app.js?v=${BUILD}`;
  const UPLOAD_SCRIPT_SRC = `assets/js/upload-feature.js?v=${BUILD}`;

  // ── helpers ───────────────────────────────────────────────────────
  const b64urlToBytes = (s) => {
    s = s.replace(/-/g, "+").replace(/_/g, "/");
    while (s.length % 4) s += "=";
    const bin = atob(s);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  };
  const bytesToUtf8 = (b) => new TextDecoder().decode(b);
  const nowSec = () => Math.floor(Date.now() / 1000);

  async function verifyJWT(token, jwk) {
    const parts = token.split(".");
    if (parts.length !== 3) throw new Error("malformed");
    const [headerB64, payloadB64, sigB64] = parts;

    const header = JSON.parse(bytesToUtf8(b64urlToBytes(headerB64)));
    if (header.alg !== "ES256") throw new Error("alg mismatch");

    const key = await crypto.subtle.importKey(
      "jwk", jwk,
      { name: "ECDSA", namedCurve: "P-256" },
      false, ["verify"]
    );

    const signed = new TextEncoder().encode(`${headerB64}.${payloadB64}`);
    const sig = b64urlToBytes(sigB64);
    const ok = await crypto.subtle.verify(
      { name: "ECDSA", hash: "SHA-256" }, key, sig, signed
    );
    if (!ok) throw new Error("signature");

    const payload = JSON.parse(bytesToUtf8(b64urlToBytes(payloadB64)));
    const now = nowSec();
    if (payload.exp && now > payload.exp) throw new Error("expired");
    if (payload.nbf && now < payload.nbf) {
      const e = new Error("notyet");
      e.nbf = payload.nbf;
      throw e;
    }
    return payload;
  }

  function renderBlock(htmlByLang) {
    document.body.innerHTML = `
<style>
  .gate-card { max-width: 520px; margin: 10vh auto; padding: 2.5rem; background: #f8f3e8;
    border: 1px solid #cdb892; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    font-family: Georgia, 'Crimson Pro', serif; color: #2b1d10; line-height: 1.55; }
  .gate-card img { display: block; margin: 0 auto 1.2rem; width: 120px; border-radius: 4px; }
  .gate-card h1 { font-size: 1.3rem; margin: 0 0 1rem; text-align: center; color: #6b1f1f; }
  .gate-card p { margin: 0.4rem 0; }
  .gate-card .he { direction: rtl; text-align: right; font-family: Heebo, sans-serif; }
  .gate-card .muted { color: #6b5440; font-size: 0.85rem; margin-top: 1.5rem; border-top: 1px solid #cdb892; padding-top: 1rem; }
</style>
<div class="gate-card">
  <img src="assets/img/rapaport-coat-of-arms.jpg" alt="Rapaport coat of arms" />
  ${htmlByLang}
</div>`;
  }

  function showNoToken() {
    renderBlock(`
      <h1>Private family archive</h1>
      <p>This is the Rapaport family research archive. Access is by personal invitation only.</p>
      <p class="he"><strong>ארכיון משפחתי פרטי.</strong> הגישה רק באמצעות הזמנה אישית מדורון.</p>
      <p>If Doron sent you a link, please open <em>his</em> link directly (don't paste the URL — use the link as he sent it).</p>
      <p class="muted">For Dov Bernard Rapaport's 80th birthday · August 2026</p>`);
  }
  function showInvalid() {
    renderBlock(`
      <h1>Invalid or revoked link</h1>
      <p>This link can't be verified. It may have been mistyped, revoked, or generated under an older key.</p>
      <p class="he">קישור לא תקין או שבוטל. אנא פנה לדורון לקבלת קישור חדש.</p>
      <p class="muted">Contact Doron for a fresh personal link.</p>`);
  }
  function showNotYet(nbf) {
    const d = new Date(nbf * 1000).toLocaleDateString("en-GB", {day:"numeric", month:"long", year:"numeric"});
    renderBlock(`
      <h1>This link comes alive on ${d}</h1>
      <p>This personal archive link is held until ${d}, as a surprise.</p>
      <p class="he">קישור זה ייפתח ב-${d}, מתנת יום הולדת.</p>
      <p class="muted">— Doron</p>`);
  }

  // ── main ─────────────────────────────────────────────────────────
  let jwk;
  try {
    jwk = await fetch("assets/auth/pubkey.json").then(r => r.json());
  } catch (e) {
    console.error("auth-gate: cannot load public key", e);
    showInvalid();
    return;
  }

  // Read token from URL (?t=...) or from localStorage
  const urlToken = new URLSearchParams(location.search).get("t");
  let stored = null;
  try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null"); } catch {}

  const candidate = urlToken || (stored && stored.token);
  if (!candidate) { showNoToken(); return; }

  let payload;
  try {
    payload = await verifyJWT(candidate, jwk);
  } catch (e) {
    if (e.message === "notyet") { showNotYet(e.nbf); return; }
    console.warn("auth-gate: invalid token", e.message);
    // If stored token failed, wipe it
    if (stored && stored.token === candidate) localStorage.removeItem(STORAGE_KEY);
    showInvalid();
    return;
  }

  // Valid! Persist token + identity, clear URL, load the SPA.
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: candidate, identity: payload, ts: Date.now() }));
  window.__rftAuth = payload;

  if (urlToken && history.replaceState) {
    const cleanUrl = location.pathname + location.hash;
    history.replaceState(null, "", cleanUrl);
  }

  // Register the service worker — required for the Android Chrome install prompt
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js", { scope: "./" }).catch(() => {});
  }

  // Inject the actual app + the upload feature module
  const s = document.createElement("script");
  s.type = "module";
  s.src = APP_SCRIPT_SRC;
  document.body.appendChild(s);

  const u = document.createElement("script");
  u.type = "module";
  u.src = UPLOAD_SCRIPT_SRC;
  document.body.appendChild(u);
})();
