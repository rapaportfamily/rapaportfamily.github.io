// Service worker — required for PWA install prompt on Android Chrome.
//
// Strategy: network-first for the shell (HTML / app JS / data JSON) so the
// installed PWA on the user's phone always picks up the latest deploy on
// next launch. We don't pre-cache; the live site loads fast enough.
//
// SW_VERSION must be bumped on every deploy that ships JS/HTML changes —
// browsers re-fetch a new SW when its byte-content changes.

const SW_VERSION = "2026-08-11-t132";

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    await self.clients.claim();
    // Notify any open clients that a new SW took over → they should reload.
    const clients = await self.clients.matchAll({ includeUncontrolled: true });
    for (const c of clients) {
      c.postMessage({ type: "sw-updated", version: SW_VERSION });
    }
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Network-first for HTML and JS — guarantees latest code reaches the PWA.
  const isShell =
    url.pathname.endsWith(".html") ||
    url.pathname.endsWith("/") ||
    url.pathname.endsWith(".js") ||
    url.pathname.endsWith(".webmanifest");
  if (!isShell) return;

  event.respondWith((async () => {
    try {
      return await fetch(req, { cache: "no-store" });
    } catch (e) {
      // Offline fallback: defer to whatever the browser has.
      return fetch(req);
    }
  })());
});
