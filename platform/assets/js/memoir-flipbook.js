// Memoir flip-book v2 — renders the ACTUAL PDF (lusia_memoir.pdf) using PDF.js,
// with side-by-side OCR'd Hebrew + English + Polish translations.
//
// No PNG copies — the PDF is the source of truth, the same scanned book the family has.
// PDF.js (Mozilla, Apache 2.0) loaded lazily from CDN on first visit.

export async function renderMemoir(root) {
  root.innerHTML = `<div class="page-pad"><h1 style="font-family:Georgia,serif;color:#6b1f1f;">📖 Loading memoir…</h1></div>`;

  // Load PDF.js v3 (UMD build — works as a regular <script> tag, no module gymnastics)
  if (!window.pdfjsLib) {
    try {
      await new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js";
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
      });
    } catch (e) {
      root.innerHTML = `<div class="page-pad"><h1>Memoir</h1><p>PDF.js failed to load: ${escapeHtml(e.message || e)}</p></div>`;
      return;
    }
  }
  const pdfjsLib = window.pdfjsLib;
  if (!pdfjsLib) {
    root.innerHTML = `<div class="page-pad"><h1>Memoir</h1><p>PDF.js library not available after load.</p></div>`;
    return;
  }
  pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js";

  let meta = {}, pages = [];
  // Hard cache-bust at the call site so even an old service worker can't serve stale
  const bust = "?v=" + Date.now();
  try {
    const [metaResp, pagesResp] = await Promise.all([
      fetch("data/memoir.json" + bust, { cache: "no-store" }),
      fetch("data/memoir_pages.json" + bust, { cache: "no-store" }),
    ]);
    if (metaResp.ok) meta = await metaResp.json();
    if (pagesResp.ok) {
      pages = await pagesResp.json();
      console.log(`[memoir] loaded ${pages.length} pages, ${pages.filter(p => p.english).length} with English translation`);
    } else {
      console.error(`[memoir] memoir_pages.json HTTP ${pagesResp.status}`);
    }
  } catch (e) {
    console.error("[memoir] data load failed:", e);
  }

  const byPage = new Map((pages || []).map(p => [p.page, p]));
  // Strip any leading "platform/" prefix (legacy data files may include it; the SPA's base path already covers it)
  const pdfUrl = (meta.source_pdf || "assets/documents/lusia_memoir.pdf").replace(/^platform\//, "");

  root.innerHTML = `
    <div class="page-pad" style="max-width:1200px;margin:0 auto;">
      <header style="text-align:center;margin-bottom:1.2rem;">
        <h1 style="font-family:Georgia,serif;color:#6b1f1f;margin:0 0 0.3rem;">📖 ${escapeHtml(meta.title_he || "סיפורה של לוסיה")}</h1>
        <div style="font-size:0.95rem;color:#6b5440;font-style:italic;">${escapeHtml(meta.title_en || "The Story of Lusia")} · ${escapeHtml(meta.title_pl || "Historia Lusi")}</div>
        <div style="font-size:0.85rem;color:#6b5440;margin-top:0.4rem;">By ${escapeHtml(meta.author || "Leah (Lusia) Rapaport née Weitzner")} · loaded from the original scanned PDF</div>
      </header>
      <div id="m-controls" style="display:flex;justify-content:center;gap:0.6rem;margin-bottom:1rem;align-items:center;flex-wrap:wrap;">
        <button id="m-first" style="background:transparent;border:1.5px solid #6b1f1f;color:#6b1f1f;padding:0.35rem 0.55rem;border-radius:4px;cursor:pointer;font-size:0.85rem;">⏮</button>
        <button id="m-prev" style="background:#6b1f1f;color:#f8f3e8;border:none;padding:0.5rem 0.9rem;border-radius:4px;cursor:pointer;font-weight:600;">←</button>
        <span id="m-pageinfo" style="font-family:Inter,sans-serif;color:#6b5440;min-width:60px;text-align:center;font-size:0.95rem;">…</span>
        <button id="m-next" style="background:#6b1f1f;color:#f8f3e8;border:none;padding:0.5rem 0.9rem;border-radius:4px;cursor:pointer;font-weight:600;">→</button>
        <button id="m-last" style="background:transparent;border:1.5px solid #6b1f1f;color:#6b1f1f;padding:0.35rem 0.55rem;border-radius:4px;cursor:pointer;font-size:0.85rem;">⏭</button>
        <select id="m-lang" style="padding:0.45rem;border:1px solid #cdb892;border-radius:4px;background:#fff;max-width:180px;">
          <option value="hebrew">עברית</option>
          <option value="english" selected>English</option>
          <option value="polish">Polski</option>
        </select>
        <a href="${escapeHtml(pdfUrl)}" target="_blank" style="font-size:0.82rem;color:#6b1f1f;text-decoration:underline;white-space:nowrap;">📥 PDF</a>
      </div>
      <div id="m-stage" class="m-stage">
        <div id="m-canvas-wrap" class="m-canvas-wrap">
          <canvas id="m-canvas" class="m-canvas"></canvas>
        </div>
        <div id="m-text-wrap" class="m-text-wrap">
          <div id="m-content" class="m-content"></div>
          <div id="m-meta" class="m-meta"></div>
        </div>
      </div>
      <style>
        /* Desktop layout (default): side-by-side */
        .m-stage {
          display: grid;
          grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
          gap: 1.5rem;
          align-items: stretch;
        }
        .m-canvas-wrap {
          background: #fff;
          border: 1px solid #cdb892;
          border-radius: 6px;
          padding: 0.6rem;
          box-shadow: 0 6px 22px rgba(0,0,0,0.18);
          display: flex;
          justify-content: center;
          align-items: flex-start;
          perspective: 1500px;
          height: 78vh;
          overflow: hidden;
        }
        .m-canvas {
          max-width: 100%;
          max-height: 100%;
          height: auto;
          display: block;
          transition: transform 0.4s ease, opacity 0.2s;
        }
        .m-text-wrap {
          background: #fff7e1;
          border: 1px solid #cdb892;
          border-radius: 6px;
          height: 78vh;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }
        .m-content {
          flex: 1 1 auto;
          overflow-y: auto;
          padding: 1.5rem 1.5rem 1rem;
          font-family: Georgia, serif;
          line-height: 1.8;
          color: #2b1d10;
          font-size: 1.02rem;
          scrollbar-width: thin;
          scrollbar-color: #cdb892 transparent;
        }
        .m-meta {
          flex: 0 0 auto;
          padding: 0.6rem 1rem;
          background: #f6ecd2;
          border-top: 1px solid #cdb892;
          font-size: 0.78rem;
          color: #6b5440;
          font-family: Inter, sans-serif;
        }
        .m-content::-webkit-scrollbar { width: 8px; }
        .m-content::-webkit-scrollbar-thumb { background: #cdb892; border-radius: 4px; }
        .m-content::-webkit-scrollbar-track { background: transparent; }
        .m-chapter {
          font-weight: 700; color: #6b1f1f; font-size: 1.15rem;
          margin-top: 1.4rem; margin-bottom: 0.3rem; display: block;
        }
        .m-pagenum { color: #6b5440; font-size: 0.85rem; }

        /* PHONE / NARROW SCREEN: TEXT FIRST (selected language is what the reader sees) */
        @media (max-width: 780px) {
          .m-stage {
            grid-template-columns: 1fr;
            gap: 0.8rem;
          }
          /* Reorder: text on top, PDF below — easier to read in chosen language first */
          .m-text-wrap { order: 1; height: auto; min-height: 50vh; max-height: 70vh; }
          .m-canvas-wrap { order: 2; height: 50vh; padding: 0.3rem; }
          .m-content {
            font-size: 1.08rem;
            padding: 1rem 1rem 0.8rem;
            line-height: 1.75;
          }
          .m-chapter { font-size: 1.12rem; margin-top: 1.2rem; }

          /* Sticky controls — always visible while scrolling */
          #memoir-controls {
            position: sticky !important;
            top: 0;
            background: #f8f3e8;
            padding: 0.6rem 0.4rem !important;
            margin: 0 -0.5rem 0.8rem !important;
            border-bottom: 1px solid #cdb892;
            z-index: 20;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
          }
          /* Bigger tap targets on phone */
          #m-prev, #m-next {
            padding: 0.65rem 1.1rem !important;
            font-size: 1.05rem !important;
          }
          #m-first, #m-last {
            padding: 0.5rem 0.7rem !important;
            font-size: 0.95rem !important;
          }
        }

        /* MOBILE LANDSCAPE: keep side-by-side but shorter */
        @media (max-height: 600px) and (min-width: 781px) {
          .m-canvas-wrap, .m-text-wrap { height: 70vh; }
        }
      </style>
      <div style="margin-top:1rem;text-align:center;font-size:0.78rem;color:#6b5440;">
        Tap the page to flip · ← → keys also work · text panel shows Hebrew OCR or AI translation
      </div>
    </div>`;

  const canvas = root.querySelector("#m-canvas");
  const ctx2d = canvas.getContext("2d");
  const info = root.querySelector("#m-pageinfo");
  const content = root.querySelector("#m-content");
  const metaEl = root.querySelector("#m-meta");
  const langSel = root.querySelector("#m-lang");

  // Better page-flip animation: fade + slight scale
  function animateFlip(dir) {
    canvas.style.opacity = "0.4";
    canvas.style.transform = dir === "next" ? "translateX(-12px) scale(0.99)" : "translateX(12px) scale(0.99)";
    setTimeout(() => {
      canvas.style.opacity = "1";
      canvas.style.transform = "";
    }, 220);
  }

  // Load the PDF
  let pdf;
  try {
    const loadingTask = pdfjsLib.getDocument(pdfUrl);
    pdf = await loadingTask.promise;
  } catch (e) {
    info.textContent = "PDF failed to load";
    root.querySelector("#m-content").innerHTML = `<p style="color:#a04040;">${escapeHtml(e.message || e)}</p>`;
    return;
  }
  const N = pdf.numPages;
  let cur = 1;

  async function show(n, dir = "next") {
    cur = Math.max(1, Math.min(N, n));
    info.textContent = `${cur} / ${N}`;
    animateFlip(dir);
    try {
      const page = await pdf.getPage(cur);
      const viewport = page.getViewport({ scale: 1.5 });
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      await page.render({ canvasContext: ctx2d, viewport }).promise;
    } catch (e) {
      console.warn("Page render failed:", e);
    }
    // Text panel
    const p = byPage.get(cur);
    const lang = langSel.value;
    const txt = p ? (p[lang] || "") : "";
    if (!p) {
      content.innerHTML = `<em style="color:#6b5440;">OCR still pending for this page.</em>`;
    } else if (!txt) {
      const isHe = lang === "hebrew";
      content.innerHTML = `<em style="color:#6b5440;">${isHe ? "(no Hebrew text on this page)" : "(translation not available — Hebrew OCR was empty)"}</em>`;
    } else {
      const isHe = lang === "hebrew";
      const dir2 = isHe ? "rtl" : "ltr";
      const fontFam = isHe ? "Heebo, Arial, sans-serif" : "Georgia, serif";
      // Style chapter headings (Chapter X: / פרק / Rozdział) and standalone page numbers
      const styled = escapeHtml(txt)
        .replace(/^(Chapter [A-Z]+:[^\n]*)/gm, '<span class="m-chapter">$1</span>')
        .replace(/^(פרק [א-ת]'?:[^\n]*)/gm, '<span class="m-chapter">$1</span>')
        .replace(/^(Rozdział [^\n]*)/gm, '<span class="m-chapter">$1</span>')
        .replace(/^(\d{1,3})$/gm, '<span class="m-pagenum">$1</span>');
      content.innerHTML = `<div dir="${dir2}" style="font-family:${fontFam};white-space:pre-wrap;">${styled}</div>`;
      content.scrollTop = 0; // reset scroll on page change
    }
    metaEl.innerHTML = p ? [
      p.page_kind ? `<strong>Kind:</strong> ${escapeHtml(p.page_kind)}` : "",
      p.ocr_confidence ? `<strong>OCR confidence:</strong> ${escapeHtml(p.ocr_confidence)}` : "",
      p.ocr_notes ? `<strong>Notes:</strong> ${escapeHtml(p.ocr_notes)}` : "",
    ].filter(Boolean).join(" · ") : "";
  }

  root.querySelector("#m-first").onclick = () => show(1, "prev");
  root.querySelector("#m-prev").onclick = () => show(cur - 1, "prev");
  root.querySelector("#m-next").onclick = () => show(cur + 1, "next");
  root.querySelector("#m-last").onclick = () => show(N, "next");
  langSel.onchange = () => show(cur);
  canvas.style.cursor = "pointer";
  canvas.onclick = (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    // Hebrew is RTL — tap left side = next, right side = previous (matches book reading direction)
    if (x < rect.width / 2) show(cur + 1, "next");
    else show(cur - 1, "prev");
  };
  const keyHandler = (e) => {
    if (!canvas.isConnected) { window.removeEventListener("keydown", keyHandler); return; }
    if (e.key === "ArrowLeft") show(cur - 1, "prev");
    if (e.key === "ArrowRight") show(cur + 1, "next");
  };
  window.addEventListener("keydown", keyHandler);

  show(1);
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
