// Minimal service worker — required for PWA install prompt on Android Chrome.
// We intentionally don't cache anything; the SPA loads fast over HTTPS already
// and aggressive caching would make data updates invisible to users.

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  // Pure passthrough — let the browser handle every request normally.
  return;
});
