// Upload + review feature.
// - Researchers tap the "Add Finding" floating button → modal with photo + description
// - Photo goes to Firebase Storage, metadata to Firestore family_uploads with status='pending'
// - Admin sees "Pending review" nav link, can approve / reject from a queue
//
// All Firebase calls go through firebase-init.js. The user's identity comes from
// the magic-link JWT (window.__rftAuth) — Firebase Anonymous Auth just gives
// the browser an ephemeral UID for rule-gating writes.

import {
  auth, db, storage, ensureFirebaseAuth,
  collection, addDoc, query, where, orderBy, getDocs, doc, updateDoc, deleteDoc, serverTimestamp,
  storageRef, uploadBytes, getDownloadURL, deleteObject,
} from "./firebase-init.js";

const ME = () => window.__rftAuth || null;
const isAdmin = () => ME() && ME().role === "admin";

// ── load related-entity pickers ────────────────────────────────────
let _peopleCache = null, _placesCache = null, _hypCache = null;
async function loadEntities() {
  if (_peopleCache) return;
  const [p, pl, h] = await Promise.all([
    fetch("data/people.json").then(r => r.json()),
    fetch("data/places.json").then(r => r.json()),
    fetch("data/hypotheses.json").then(r => r.json()),
  ]);
  _peopleCache = p.people || [];
  _placesCache = pl.places || [];
  _hypCache = h.hypotheses || [];
}

function nameOf(person) {
  return person?.primary_name?.en || person?.primary_name?.he || person?.id || "—";
}
function placeName(place) {
  return place?.primary_name?.en || place?.primary_name?.he || place?.id || "—";
}

// ── floating "Add Finding" button ──────────────────────────────────
function injectFab() {
  if (!ME() || document.getElementById("rft-fab")) return;
  const fab = document.createElement("button");
  fab.id = "rft-fab";
  fab.innerHTML = "📷 Add finding";
  fab.title = "Upload a photo / document with notes";
  Object.assign(fab.style, {
    position: "fixed", bottom: "1.5rem", right: "1.5rem", zIndex: 50,
    padding: "0.85rem 1.2rem", borderRadius: "999px", border: "none",
    background: "#6b1f1f", color: "#f8f3e8", fontWeight: "600",
    fontSize: "0.95rem", boxShadow: "0 4px 14px rgba(0,0,0,0.25)",
    cursor: "pointer", fontFamily: "Inter, sans-serif",
  });
  fab.onclick = openUploadModal;
  document.body.appendChild(fab);
}

// ── upload modal ───────────────────────────────────────────────────
async function openUploadModal() {
  await loadEntities();
  await ensureFirebaseAuth();
  const me = ME();

  const ov = document.createElement("div");
  ov.id = "rft-upload-overlay";
  Object.assign(ov.style, {
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.6)", zIndex: 100,
    display: "flex", alignItems: "center", justifyContent: "center", padding: "1rem",
  });
  ov.innerHTML = `
<div style="background:#f8f3e8;max-width:520px;width:100%;max-height:90vh;overflow-y:auto;padding:1.5rem;border-radius:8px;font-family:Inter,sans-serif;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
    <h2 style="margin:0;font-family:Georgia,serif;color:#6b1f1f;">Add a finding</h2>
    <button data-close style="background:none;border:none;font-size:1.5rem;cursor:pointer;color:#6b5440;">×</button>
  </div>
  <p style="font-size:0.85rem;color:#6b5440;margin:0 0 1rem;">
    Uploading as <strong>${me.name}</strong>. Your photo / chat export / document goes to Doron's review queue.
    Nothing appears in the public archive until Doron approves it.
  </p>
  <form id="rft-upload-form">
    <label style="display:block;margin-bottom:0.8rem;">
      <span style="display:block;font-weight:600;margin-bottom:0.3rem;">File (max 10 MB)</span>
      <input type="file" name="file" required
             accept="image/*,application/pdf,text/plain,.txt,application/zip,.zip"
             capture="environment"
             style="width:100%;padding:0.5rem;border:1px solid #cdb892;border-radius:4px;background:#fff;" />
      <span style="display:block;margin-top:0.35rem;font-size:0.78rem;color:#6b5440;">
        📷 photo · 📄 PDF · 💬 <strong>WhatsApp chat export</strong> (.txt or .zip — share chat → "Export chat" → "Without media" or "Include media" → save the file → upload here)
      </span>
    </label>
    <label style="display:block;margin-bottom:0.8rem;">
      <span style="display:block;font-weight:600;margin-bottom:0.3rem;">What is this?</span>
      <input type="text" name="title" required placeholder="e.g. Rebeka's 1888 birth certificate"
             style="width:100%;padding:0.55rem;border:1px solid #cdb892;border-radius:4px;background:#fff;" />
    </label>
    <label style="display:block;margin-bottom:0.8rem;">
      <span style="display:block;font-weight:600;margin-bottom:0.3rem;">Notes (where it came from, what it tells us)</span>
      <textarea name="notes" rows="3" placeholder="Source, date, archive reference, your interpretation…"
                style="width:100%;padding:0.55rem;border:1px solid #cdb892;border-radius:4px;background:#fff;font-family:inherit;"></textarea>
    </label>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:0.8rem;">
      <label style="display:block;">
        <span style="display:block;font-weight:600;margin-bottom:0.3rem;">Related person</span>
        <select name="person_id" style="width:100%;padding:0.55rem;border:1px solid #cdb892;border-radius:4px;background:#fff;">
          <option value="">(none)</option>
          ${_peopleCache.map(p => `<option value="${p.id}">${nameOf(p)}</option>`).join("")}
        </select>
      </label>
      <label style="display:block;">
        <span style="display:block;font-weight:600;margin-bottom:0.3rem;">Related place</span>
        <select name="place_id" style="width:100%;padding:0.55rem;border:1px solid #cdb892;border-radius:4px;background:#fff;">
          <option value="">(none)</option>
          ${_placesCache.map(p => `<option value="${p.id}">${placeName(p)}</option>`).join("")}
        </select>
      </label>
    </div>
    <label style="display:block;margin-bottom:1rem;">
      <span style="display:block;font-weight:600;margin-bottom:0.3rem;">Related open question</span>
      <select name="hypothesis_id" style="width:100%;padding:0.55rem;border:1px solid #cdb892;border-radius:4px;background:#fff;">
        <option value="">(none)</option>
        ${_hypCache.map(h => `<option value="${h.id}">${h.question?.en || h.id}</option>`).join("")}
      </select>
    </label>
    <button type="submit" id="rft-upload-submit"
            style="width:100%;padding:0.85rem;background:#6b1f1f;color:#f8f3e8;border:none;border-radius:4px;font-weight:600;font-size:1rem;cursor:pointer;">
      Send to Doron
    </button>
    <div id="rft-upload-status" style="margin-top:0.8rem;text-align:center;color:#6b5440;font-size:0.9rem;"></div>
  </form>
</div>`;
  document.body.appendChild(ov);
  ov.querySelector("[data-close]").onclick = () => ov.remove();
  ov.onclick = (e) => { if (e.target === ov) ov.remove(); };

  ov.querySelector("#rft-upload-form").onsubmit = async (e) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const file = fd.get("file");
    const status = ov.querySelector("#rft-upload-status");
    const btn = ov.querySelector("#rft-upload-submit");
    if (!file || file.size === 0) return;
    if (file.size > 10 * 1024 * 1024) { status.textContent = "File too large (max 10 MB)"; return; }
    btn.disabled = true; btn.textContent = "Uploading…"; status.textContent = "";

    try {
      const safeName = file.name.replace(/[^\w.-]/g, "_");
      const path = `uploads/pending/${me.sub}/${Date.now()}_${safeName}`;
      const sref = storageRef(storage, path);
      await uploadBytes(sref, file, { contentType: file.type });
      const url = await getDownloadURL(sref);

      // Categorize: photo / pdf / chat-export / other.
      // Chat exports get a special flag so CC's session-start protocol
      // (see docs/CC_SESSION_PROTOCOL.md) processes them differently.
      const lname = file.name.toLowerCase();
      let kind = "other";
      if ((file.type || "").startsWith("image/")) kind = "photo";
      else if (file.type === "application/pdf" || lname.endsWith(".pdf")) kind = "pdf";
      else if (lname.endsWith(".txt") || /whatsapp.*chat/i.test(file.name)) kind = "whatsapp_chat";
      else if (lname.endsWith(".zip") || file.type === "application/zip") kind = "whatsapp_chat_archive";

      await addDoc(collection(db, "family_uploads"), {
        status: "pending",
        kind: kind,
        title: (fd.get("title") || "").toString().trim(),
        notes: (fd.get("notes") || "").toString().trim(),
        person_id: fd.get("person_id") || null,
        place_id: fd.get("place_id") || null,
        hypothesis_id: fd.get("hypothesis_id") || null,
        uploader_sub: me.sub,
        uploader_name: me.name,
        uploader_role: me.role,
        file_path: path,
        file_url: url,
        file_name: file.name,
        file_size: file.size,
        file_type: file.type,
        created_at: serverTimestamp(),
      });

      status.textContent = "✓ Sent! Doron will review it.";
      btn.style.background = "#3a6b3a";
      setTimeout(() => ov.remove(), 1800);
    } catch (err) {
      console.error(err);
      status.textContent = "Upload failed: " + (err.message || err);
      btn.disabled = false; btn.textContent = "Send to Doron";
    }
  };
}

// ── admin review queue (rendered as full page when route = #/review) ─
export async function renderReview(root) {
  if (!isAdmin()) {
    root.innerHTML = `<div class="page-pad"><h1>Not authorized</h1>
      <p>The review queue is admin-only.</p></div>`;
    return;
  }
  await loadEntities();
  await ensureFirebaseAuth();

  root.innerHTML = `<div class="page-pad">
    <h1 style="font-family:Georgia,serif;color:#6b1f1f;">Pending review</h1>
    <p class="muted">Findings uploaded by the research circle. Approve to add to the archive, reject to delete.</p>
    <div id="rft-review-list">Loading…</div>
  </div>`;

  const listEl = root.querySelector("#rft-review-list");
  try {
    const q = query(collection(db, "family_uploads"), where("status", "==", "pending"), orderBy("created_at", "desc"));
    const snap = await getDocs(q);
    if (snap.empty) { listEl.innerHTML = "<p>Nothing pending. The queue is empty.</p>"; return; }

    listEl.innerHTML = "";
    snap.forEach((docSnap) => {
      const d = docSnap.data();
      const card = document.createElement("div");
      card.style.cssText = "background:#fff;border:1px solid #cdb892;border-radius:6px;padding:1rem;margin-bottom:1rem;display:grid;grid-template-columns:140px 1fr;gap:1rem;";
      const person = _peopleCache.find(p => p.id === d.person_id);
      const place = _placesCache.find(p => p.id === d.place_id);
      const hyp = _hypCache.find(h => h.id === d.hypothesis_id);

      const isImage = (d.file_type || "").startsWith("image/");
      card.innerHTML = `
        <div>
          ${isImage
            ? `<a href="${d.file_url}" target="_blank"><img src="${d.file_url}" style="width:140px;height:140px;object-fit:cover;border-radius:4px;border:1px solid #cdb892;" /></a>`
            : `<a href="${d.file_url}" target="_blank" style="display:block;width:140px;height:140px;background:#f0e4cf;display:flex;align-items:center;justify-content:center;border-radius:4px;border:1px solid #cdb892;text-align:center;padding:0.5rem;">📄<br>${escapeHtml(d.file_name || 'file')}</a>`}
        </div>
        <div>
          <div style="font-weight:600;color:#2b1d10;margin-bottom:0.3rem;">${escapeHtml(d.title || '(untitled)')}</div>
          <div style="font-size:0.85rem;color:#6b5440;margin-bottom:0.3rem;">From <strong>${escapeHtml(d.uploader_name)}</strong></div>
          ${d.notes ? `<div style="margin:0.5rem 0;color:#2b1d10;">${escapeHtml(d.notes)}</div>` : ''}
          <div style="font-size:0.8rem;color:#6b5440;margin-bottom:0.6rem;">
            ${person ? `Person: <strong>${nameOf(person)}</strong> · ` : ''}
            ${place ? `Place: <strong>${placeName(place)}</strong> · ` : ''}
            ${hyp ? `Q: <em>${escapeHtml(hyp.question?.en || hyp.id)}</em>` : ''}
          </div>
          <div style="display:flex;gap:0.6rem;">
            <button data-approve="${docSnap.id}" style="background:#3a6b3a;color:#fff;border:none;padding:0.5rem 1rem;border-radius:4px;cursor:pointer;font-weight:600;">✓ Approve</button>
            <button data-reject="${docSnap.id}" data-path="${d.file_path}" style="background:#a04040;color:#fff;border:none;padding:0.5rem 1rem;border-radius:4px;cursor:pointer;">✗ Reject &amp; delete</button>
          </div>
        </div>`;
      listEl.appendChild(card);
    });

    listEl.onclick = async (e) => {
      const aId = e.target.dataset.approve;
      const rId = e.target.dataset.reject;
      if (aId) {
        e.target.disabled = true; e.target.textContent = "Approving…";
        await updateDoc(doc(db, "family_uploads", aId), {
          status: "approved",
          approved_by: ME().name, approved_at: serverTimestamp(),
        });
        e.target.closest("[style*='grid']").remove();
      } else if (rId) {
        if (!confirm("Delete this upload permanently?")) return;
        e.target.disabled = true; e.target.textContent = "Deleting…";
        try { await deleteObject(storageRef(storage, e.target.dataset.path)); } catch {}
        await deleteDoc(doc(db, "family_uploads", rId));
        e.target.closest("[style*='grid']").remove();
      }
    };
  } catch (err) {
    listEl.innerHTML = `<p style="color:#a04040;">Couldn't load queue: ${escapeHtml(err.message || err)}</p>`;
  }
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}

// ── "Install as app" — auto-prompt after 30 seconds ──────────────
// Shows a center-screen modal asking to install. If the browser supports the
// native beforeinstallprompt event (Android Chrome), tapping "Install" fires
// the system install dialog. Otherwise (iOS Safari, or Chrome that suppressed
// the event), we show explicit step-by-step instructions for that device.
let _installPromptEvent = null;

function setupInstallButton() {
  // Always capture native install event so the header Install button can use it
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    _installPromptEvent = e;
  });

  // If already installed (running standalone), don't auto-prompt
  if (window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone) return;
  // Don't auto-prompt again in the same browser within 24h (header button still works)
  const dismissed = parseInt(localStorage.getItem("rft.install.dismissed_at") || "0", 10);
  if (dismissed && Date.now() - dismissed < 24 * 60 * 60 * 1000) return;

  // After 30 seconds on the page, auto-prompt
  setTimeout(showInstallModal, 30000);
}

// When user clicks "Install" in header, force-show even if dismissed before
function showInstallModal(opts = {}) {
  if (document.getElementById("rft-install-modal")) return;
  if (window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone) {
    alert("The app is already installed on this device. Look for the Rapaport icon on your home screen.");
    return;
  }

  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isSafari = /^((?!chrome|android|crios|fxios).)*safari/i.test(navigator.userAgent);
  const isAndroid = /Android/i.test(navigator.userAgent);

  const ov = document.createElement("div");
  ov.id = "rft-install-modal";
  Object.assign(ov.style, {
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", zIndex: 200,
    display: "flex", alignItems: "center", justifyContent: "center", padding: "1.5rem",
  });
  ov.innerHTML = `
<div style="background:#f8f3e8;max-width:420px;width:100%;padding:1.8rem 1.5rem;border-radius:10px;font-family:Inter,sans-serif;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,0.4);">
  <img src="assets/img/rapaport-coat-of-arms.jpg" alt="" style="width:80px;height:80px;object-fit:contain;border-radius:6px;margin-bottom:1rem;" />
  <h2 style="margin:0 0 0.6rem;color:#6b1f1f;font-family:Georgia,serif;font-size:1.3rem;">Install on your home screen?</h2>
  <p style="margin:0 0 1.2rem;color:#2b1d10;line-height:1.5;font-size:0.95rem;">
    The Rapaport family archive can live on your home screen like a real app — one tap to open, no browser bars, stays signed in.
  </p>
  <div id="rft-install-body"></div>
  <button id="rft-install-not-now" style="margin-top:1rem;background:transparent;border:none;color:#6b5440;font-size:0.85rem;cursor:pointer;text-decoration:underline;">Not now</button>
</div>`;
  document.body.appendChild(ov);

  const body = ov.querySelector("#rft-install-body");
  const close = () => { localStorage.setItem("rft.install.dismissed_at", String(Date.now())); ov.remove(); };
  ov.querySelector("#rft-install-not-now").onclick = close;
  ov.onclick = (e) => { if (e.target === ov) close(); };

  if (_installPromptEvent) {
    // Native install (Android Chrome / Edge / desktop Chrome) — one tap
    const btn = document.createElement("button");
    btn.textContent = "📲  Install app";
    btn.style.cssText = "width:100%;background:#6b1f1f;color:#f8f3e8;border:none;padding:0.9rem 1rem;border-radius:6px;font-weight:700;font-size:1rem;cursor:pointer;";
    btn.onclick = async () => {
      _installPromptEvent.prompt();
      const { outcome } = await _installPromptEvent.userChoice;
      _installPromptEvent = null;
      close();
      if (outcome === "accepted") setTimeout(() => alert("Installed! Check your home screen for the Rapaport icon."), 300);
    };
    body.appendChild(btn);
  } else if (isAndroid) {
    // Android Chrome but no event — show explicit menu steps
    body.innerHTML = `
<div style="background:#fff;border:1px solid #cdb892;border-radius:6px;padding:1rem;text-align:left;font-size:0.95rem;line-height:1.6;color:#2b1d10;">
  <strong>Two taps from your Chrome menu:</strong>
  <ol style="padding-left:1.4rem;margin:0.6rem 0 0;">
    <li>Tap the <strong>⋮</strong> menu (top-right of Chrome)</li>
    <li>Tap <strong>"Install app"</strong> or <strong>"Add to Home screen"</strong></li>
  </ol>
</div>`;
  } else if (isIOS && isSafari) {
    // iOS Safari — explicit Share-button steps
    body.innerHTML = `
<div style="background:#fff;border:1px solid #cdb892;border-radius:6px;padding:1rem;text-align:left;font-size:0.95rem;line-height:1.6;color:#2b1d10;">
  <strong>Three taps from Safari:</strong>
  <ol style="padding-left:1.4rem;margin:0.6rem 0 0;">
    <li>Tap the <strong>Share</strong> button ⬆️ at the bottom of Safari</li>
    <li>Scroll down and tap <strong>"Add to Home Screen"</strong></li>
    <li>Tap <strong>Add</strong> top-right</li>
  </ol>
</div>`;
  } else {
    // Desktop fallback
    body.innerHTML = `
<div style="background:#fff;border:1px solid #cdb892;border-radius:6px;padding:1rem;text-align:left;font-size:0.95rem;line-height:1.6;color:#2b1d10;">
  Look for the <strong>install icon</strong> in your browser's address bar (⬇️ in a screen icon), or open the browser menu and tap <strong>"Install Rapaport…"</strong>.
</div>`;
  }
}

// ── Header toolbar: Share + Install (persistent, mobile-friendly) ──
function injectHeaderToolbar() {
  if (document.getElementById("rft-header-toolbar")) return;
  const header = document.querySelector(".site-header .header-controls") || document.querySelector(".site-header .header-inner");
  if (!header) return;

  const bar = document.createElement("div");
  bar.id = "rft-header-toolbar";
  bar.style.cssText = "display:flex;gap:0.4rem;align-items:center;margin-inline-start:0.6rem;";

  // Share button — always visible if Web Share API supported, else copy-to-clipboard
  const share = document.createElement("button");
  share.id = "rft-share-btn";
  share.innerHTML = "↗ Share";
  share.title = "Share this page";
  share.style.cssText = "background:#6b1f1f;color:#f8f3e8;border:none;padding:0.4rem 0.75rem;border-radius:20px;font-size:0.82rem;font-weight:600;cursor:pointer;font-family:Inter,sans-serif;white-space:nowrap;";
  share.onclick = shareCurrentPage;
  bar.appendChild(share);

  // Install button — only if not already installed; hidden if PWA standalone
  const isStandalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone;
  if (!isStandalone) {
    const install = document.createElement("button");
    install.id = "rft-install-header-btn";
    install.innerHTML = "📲 Install";
    install.title = "Install as app on home screen";
    install.style.cssText = "background:transparent;color:#6b1f1f;border:1.5px solid #6b1f1f;padding:0.35rem 0.7rem;border-radius:20px;font-size:0.82rem;font-weight:600;cursor:pointer;font-family:Inter,sans-serif;white-space:nowrap;";
    install.onclick = showInstallModal;
    bar.appendChild(install);
  }

  header.appendChild(bar);
}

function shareCurrentPage() {
  // Build a safe share URL — strip ?t=... so we never leak someone's magic link
  const origin = location.origin + location.pathname;
  const hash = location.hash || "";
  const url = origin + hash;

  // Build a context-aware title from the current view
  let title = "The Rapaport Family Tree";
  let text = "Our family research archive — from Galicia to Brussels to Israel, 1888-2026. Ask Doron for a personal access link.";
  const view = (hash.replace(/^#\//, "") || "home").split("/")[0];
  const viewLabel = {
    home: "Home", tree: "Family Tree", timeline: "Timeline",
    people: "People", places: "Places", documents: "Documents",
    hypotheses: "Open Questions", chat: "Research Chat", about: "About", review: "Pending Review",
  }[view];
  if (viewLabel && view !== "home") title = `${viewLabel} — Rapaport Family Tree`;

  if (navigator.share) {
    navigator.share({ title, text, url }).catch(() => {});
  } else {
    // Desktop fallback: copy to clipboard
    navigator.clipboard.writeText(url).then(() => {
      const old = document.getElementById("rft-share-btn");
      if (old) {
        const orig = old.innerHTML;
        old.innerHTML = "✓ Copied";
        setTimeout(() => { old.innerHTML = orig; }, 1500);
      }
    }).catch(() => { prompt("Copy this link:", url); });
  }
}

// ── boot ───────────────────────────────────────────────────────────
// Inject FAB once the SPA's nav has rendered (auth-gate has set window.__rftAuth)
function boot() {
  if (!ME()) return; // auth-gate hasn't run yet or no token
  injectFab();
  injectHeaderToolbar();
  setupInstallButton();
  // Add an admin-only "Review" nav link
  if (isAdmin()) {
    const primaryNav = document.querySelector(".primary-nav .nav-inner");
    if (primaryNav && !primaryNav.querySelector('[data-nav="review"]')) {
      const a = document.createElement("a");
      a.href = "#/review";
      a.dataset.link = "";
      a.dataset.nav = "review";
      a.textContent = "Review queue";
      primaryNav.appendChild(a);
    }
  }
  // Intercept #/review hash so we render this view instead of the SPA default
  function maybeRender() {
    const hash = (location.hash || "").replace(/^#\//, "").split("/")[0];
    if (hash === "review") {
      const root = document.getElementById("view");
      if (root) renderReview(root);
    }
  }
  window.addEventListener("hashchange", maybeRender);
  setTimeout(maybeRender, 100);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", boot);
} else {
  // The auth gate injects this script dynamically, so DOM is already ready.
  boot();
}
