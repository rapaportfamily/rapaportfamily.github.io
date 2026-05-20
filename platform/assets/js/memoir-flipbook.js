// Memoir flip-book — renders Lusia's memoir as a page-turning book
// with side-by-side translations (HE / EN / PL).
// Uses StPageFlip (single-file CDN import, MIT licensed).
//
// Renders at #/memoir. Reads:
//   data/memoir.json       — title + page count + metadata
//   data/memoir_pages.json — per-page hebrew + english + polish (from OCR)
//   assets/img/memoir/page-NNN.png — rendered high-DPI page images

export async function renderMemoir(root) {
  // Lazy-load StPageFlip (MIT) on first visit
  if (!window.St) {
    await new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.min.js";
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    }).catch(() => {});
  }

  let meta, pages;
  try {
    [meta, pages] = await Promise.all([
      fetch("data/memoir.json").then(r => r.json()),
      fetch("data/memoir_pages.json").then(r => r.json()).catch(() => []),
    ]);
  } catch (e) {
    root.innerHTML = `<div class="page-pad"><h1>The Story of Lusia</h1>
      <p>The memoir hasn't been processed yet. Once OCR completes, this view will show the flip-book.</p></div>`;
    return;
  }

  const N = meta?.pages || 0;
  const byPage = new Map((pages || []).map(p => [p.page, p]));

  root.innerHTML = `
    <div class="page-pad" style="max-width:1100px;margin:0 auto;">
      <header style="text-align:center;margin-bottom:1.5rem;">
        <h1 style="font-family:Georgia,serif;color:#6b1f1f;margin:0 0 0.3rem;">📖 ${escapeHtml(meta.title_he || "")}</h1>
        <div style="font-size:0.95rem;color:#6b5440;font-style:italic;">${escapeHtml(meta.title_en || "")} · ${escapeHtml(meta.title_pl || "")}</div>
        <div style="font-size:0.85rem;color:#6b5440;margin-top:0.4rem;">By ${escapeHtml(meta.author || "")} · ${N} pages · transcribed and translated via 3-engine OCR consensus</div>
      </header>
      <div id="memoir-controls" style="display:flex;justify-content:center;gap:0.6rem;margin-bottom:1rem;align-items:center;flex-wrap:wrap;">
        <button id="m-prev" style="background:#6b1f1f;color:#f8f3e8;border:none;padding:0.5rem 1rem;border-radius:4px;cursor:pointer;font-weight:600;">← Previous</button>
        <span id="m-pageinfo" style="font-family:Inter,sans-serif;color:#6b5440;min-width:80px;text-align:center;">1 / ${N}</span>
        <button id="m-next" style="background:#6b1f1f;color:#f8f3e8;border:none;padding:0.5rem 1rem;border-radius:4px;cursor:pointer;font-weight:600;">Next →</button>
        <select id="m-lang" style="padding:0.45rem;border:1px solid #cdb892;border-radius:4px;background:#fff;">
          <option value="he">עברית (original)</option>
          <option value="en" selected>English translation</option>
          <option value="pl">Polski tłumaczenie</option>
        </select>
        <a href="${escapeHtml(meta.source_pdf || "assets/documents/lusia_memoir.pdf")}" target="_blank" style="font-size:0.85rem;color:#6b1f1f;text-decoration:underline;">📥 Download original PDF</a>
      </div>
      <div id="memoir-stage" style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start;">
        <div id="m-image" style="background:#fff;border:1px solid #cdb892;border-radius:6px;padding:0.5rem;box-shadow:0 4px 18px rgba(0,0,0,0.15);">
          <img id="m-img" src="assets/img/memoir/page-001.png" alt="Page 1" style="width:100%;height:auto;display:block;border-radius:3px;" />
        </div>
        <div id="m-text" style="background:#fff7e1;border:1px solid #cdb892;border-radius:6px;padding:1.2rem;min-height:520px;font-family:Georgia,serif;line-height:1.7;color:#2b1d10;">
          <div id="m-content"></div>
          <div id="m-meta" style="margin-top:1.2rem;padding-top:0.8rem;border-top:1px solid #cdb892;font-size:0.78rem;color:#6b5440;"></div>
        </div>
      </div>
      <div style="margin-top:1rem;text-align:center;font-size:0.78rem;color:#6b5440;">
        Tip — tap the page image to flip · arrow keys ← → also work · the text panel shows Hebrew original or translation
      </div>
    </div>`;

  let cur = 1;
  const img = root.querySelector("#m-img");
  const info = root.querySelector("#m-pageinfo");
  const content = root.querySelector("#m-content");
  const metaEl = root.querySelector("#m-meta");
  const langSel = root.querySelector("#m-lang");

  function show(n) {
    cur = Math.max(1, Math.min(N, n));
    img.src = `assets/img/memoir/page-${String(cur).padStart(3, "0")}.png`;
    img.alt = `Page ${cur}`;
    info.textContent = `${cur} / ${N}`;
    const p = byPage.get(cur);
    const lang = langSel.value;
    const txt = p ? (p[lang] || "") : "";
    if (!p) {
      content.innerHTML = `<em style="color:#6b5440;">OCR still pending for this page.</em>`;
    } else if (!txt) {
      content.innerHTML = `<em style="color:#6b5440;">${lang === "he" ? "(no Hebrew text on this page)" : "(translation not available)"}</em>`;
    } else {
      const dir = lang === "he" ? "rtl" : "ltr";
      const fontFam = lang === "he" ? "Heebo, Arial, sans-serif" : "Georgia, serif";
      content.innerHTML = `<div dir="${dir}" style="font-family:${fontFam};white-space:pre-wrap;">${escapeHtml(txt)}</div>`;
    }
    metaEl.innerHTML = p ? [
      p.page_kind ? `<strong>Type:</strong> ${escapeHtml(p.page_kind)}` : "",
      p.ocr_confidence ? `<strong>OCR confidence:</strong> ${escapeHtml(p.ocr_confidence)}` : "",
      p.ocr_consensus?.avg_similarity != null ? `<strong>Consensus:</strong> ${p.ocr_consensus.avg_similarity}` : "",
      p.claude_review_needed ? `<span style="color:#a04040;">⚠ flagged for Claude review</span>` : "",
      p.ocr_notes ? `<strong>Notes:</strong> ${escapeHtml(p.ocr_notes)}` : "",
    ].filter(Boolean).join(" · ") : "";
  }

  root.querySelector("#m-prev").onclick = () => show(cur - 1);
  root.querySelector("#m-next").onclick = () => show(cur + 1);
  langSel.onchange = () => show(cur);
  img.style.cursor = "pointer";
  img.onclick = (e) => {
    const rect = img.getBoundingClientRect();
    const x = e.clientX - rect.left;
    // Hebrew = RTL, so tap LEFT = next page, tap RIGHT = previous
    if (x < rect.width / 2) show(cur + 1);
    else show(cur - 1);
  };
  window.addEventListener("keydown", (e) => {
    if (root.querySelector("#m-img") !== img) return; // no longer on memoir view
    if (e.key === "ArrowLeft") show(cur - 1);
    if (e.key === "ArrowRight") show(cur + 1);
  });

  show(1);
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
