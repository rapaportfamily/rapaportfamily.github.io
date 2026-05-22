"""LinkedIn public-profile discovery via Bing search (DDG blocks scrapers).

LinkedIn blocks unauthenticated access. Bing indexes public LinkedIn cards
so we can get titles + headlines + companies without logging in.
"""
from playwright.sync_api import sync_playwright
import json, time, re
from pathlib import Path
import urllib.parse

OUT = Path(__file__).resolve().parent.parent / "research_cache" / "linkedin_search_results.json"
OUT.parent.mkdir(exist_ok=True)

QUERIES = [
    ("doron_rapaport",  '"Doron Rapaport" linkedin'),
    ("daniel_rapaport", '"Daniel Rapaport" linkedin'),
    ("lior_hinkus",     '"Lior Hinkus" linkedin'),
    ("heli_rapaport",   '"Heli Rapaport" linkedin'),
    ("heli_avitan",     '"Heli Avitan" linkedin'),
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="en-US",
    )
    page = ctx.new_page()
    for key, q in QUERIES:
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(q)
        print(f"\n[{key}] {q}", flush=True)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(4)  # let SERP finish rendering
            html = page.content()
            linkedin_urls = list(dict.fromkeys(
                re.findall(r'(?:https?://)?[a-z]{2,3}\.linkedin\.com/in/[a-zA-Z0-9\-_%]+', html)
            ))
            # Extract h2 titles + companion paragraph (Bing structure)
            blocks = page.eval_on_selector_all(
                "li.b_algo",
                """nodes => nodes.slice(0,12).map(n => ({
                    title: (n.querySelector('h2') || {}).innerText || '',
                    href:  (n.querySelector('h2 a') || {}).href || '',
                    text:  (n.querySelector('.b_caption p') || n.querySelector('p') || {}).innerText || ''
                }))"""
            )
            li_blocks = [b for b in blocks if 'linkedin.com' in (b.get('href','')+b.get('text','')).lower()]
            print(f"   {len(blocks)} results, {len(li_blocks)} look like LinkedIn, {len(linkedin_urls)} URL refs")
            results[key] = {
                "query": q,
                "all_results": blocks,
                "linkedin_results": li_blocks,
                "linkedin_url_refs": linkedin_urls,
            }
        except Exception as e:
            print(f"   ERROR: {e}")
            results[key] = {"query": q, "error": str(e)}
        time.sleep(3)
    browser.close()

OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nDONE: {OUT}\n")
for k, v in results.items():
    li_results = v.get("linkedin_results", [])
    print(f"=== {k} — {len(li_results)} LinkedIn hits ===")
    for h in li_results[:6]:
        print(f"  TITLE: {h.get('title','')[:120]}")
        print(f"  TEXT : {h.get('text','')[:200]}")
        print(f"  HREF : {h.get('href','')[:150]}")
        print()
