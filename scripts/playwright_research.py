"""Playwright-driven research across archive sites where JS-form searches
defeated earlier Claude-Code agents.

Sites covered:
  ushmm        — USHMM HSV person-search for Rapaport on Theodor Herzl
  yadvashem    — Yad Vashem Names DB POTs for Berisz/Rebeka/Lota Rapaport
  arolsen      — Arolsen Archives for David Rapaport b.1911 Nadworna
  righteous    — Polscy Sprawiedliwi for Hormak family of Nadwórna
  jri          — JRI-Poland Skole surname index for Goldfischer

Usage:
    python scripts/playwright_research.py            # run all
    python scripts/playwright_research.py ushmm      # run one site
    python scripts/playwright_research.py ushmm yadvashem  # multiple

Output:
    research_cache/playwright_results/{site}_{YYYYMMDD_HHMMSS}.json
    research_cache/playwright_results/{site}_{YYYYMMDD_HHMMSS}.png  (screenshot)

The script runs Chromium HEADED (headless=False) so you can watch / step
in if a CAPTCHA appears. If a search times out or hits a CAPTCHA, it logs
the obstacle and moves on — does NOT crash.
"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research_cache" / "playwright_results"
OUT.mkdir(parents=True, exist_ok=True)

# User-Agent to be a polite citizen of these archives
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 "
      "(RapaportFamilyArchive; contact doronrpa@gmail.com)")


def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_print(*args):
    # Avoid Windows cp1252 console crashes on Unicode arrows etc.
    try:
        print(*args)
    except UnicodeEncodeError:
        print(*(str(a).encode("ascii", "replace").decode("ascii") for a in args))


async def _save(site, query, result, page=None):
    stamp = _ts()
    fp = OUT / f"{site}_{stamp}.json"
    fp.write_text(json.dumps({
        "site": site,
        "timestamp": stamp,
        "query": query,
        "result": result,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    _safe_print(f"  -> {fp.relative_to(REPO)}")
    if page is not None:
        try:
            shot = OUT / f"{site}_{stamp}.png"
            await page.screenshot(path=str(shot), full_page=True)
            _safe_print(f"  -> {shot.relative_to(REPO)}")
        except Exception as e:
            _safe_print(f"  (screenshot failed: {e})")


# ── SITE 1: USHMM HSV person-search ───────────────────────────────────
async def ushmm(browser):
    site = "ushmm"
    _safe_print(f"\n[{site}] Opening USHMM HSV person-search…")
    ctx = await browser.new_context(user_agent=UA)
    page = await ctx.new_page()
    # Run multiple focused queries so we can pin our family members specifically.
    # 49944 = USHMM Source ID for the Theodor Herzl passenger documents (per agent finding).
    THEODOR_HERZL_SRC = "49944"
    queries = [
        # Theodor Herzl-source-filtered Rapaport (highest yield if our family is in it)
        {"lname": "Rapaport", "fname": "", "place_birth": "", "src": THEODOR_HERZL_SRC, "acc": "broad"},
        # Theodor Herzl-source-filtered Weitzner (Lusia née Weitzner — though manifests
        # may list her as Rapaport, the ship loaded under whatever name they registered)
        {"lname": "Weitzner", "fname": "", "place_birth": "", "src": THEODOR_HERZL_SRC, "acc": "broad"},
        # Same for Goldfischer (S. Goldfischer came independently 1930s — unlikely in Herzl,
        # but Isak Goldfischer hit shows there are records)
        {"lname": "Goldfischer","fname":"","place_birth": "", "src": THEODOR_HERZL_SRC, "acc": "broad"},
        # David relax accuracy + alt birthplace spellings
        {"lname": "Rapaport", "fname": "David",  "place_birth": "Nadworna", "src": "", "acc": "broad"},
        {"lname": "Rapaport", "fname": "David",  "place_birth": "",          "src": "", "acc": "broad"},
        {"lname": "Rapaport", "fname": "Berisz", "place_birth": "",          "src": "", "acc": "broad"},
        {"lname": "Rapaport", "fname": "Lota",   "place_birth": "",          "src": "", "acc": "broad"},
        {"lname": "Rapaport", "fname": "Shimon", "place_birth": "",          "src": "", "acc": "broad"},
        {"lname": "Weitzner", "fname": "Lusia",  "place_birth": "",          "src": "", "acc": "broad"},
        {"lname": "Weitzner", "fname": "Eli",    "place_birth": "",          "src": "", "acc": "broad"},
        # Goldfischer Skole — found Isak in prior pass; widen now
        {"lname": "Goldfischer","fname":"",      "place_birth": "Skole",     "src": "", "acc": "broad"},
    ]
    all_results = []
    try:
        for q in queries:
            params = {
                "NameSearch__lname": q["lname"],
                "NameSearch__fname": q["fname"],
                "NameSearch__place_birth": q["place_birth"],
                "NameSearch__lname_accuracy": q.get("acc", "broad"),
                "NameSearch__fname_accuracy": q.get("acc", "broad"),
                "NameSearch__place_birth_accuracy": "broad",
                "NameSearch__SourceId": q.get("src", ""),
                "NameSearch__sort": "score",
                "NameSearch__MaxPageDocs": "50",
            }
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"https://www.ushmm.org/online/hsv/person_advance_search.php?{qs}"
            _safe_print(f"  searching: {q['fname']} {q['lname']} / {q['place_birth']}")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                await page.wait_for_timeout(2500)
                text = await page.locator("body").inner_text()
                # Extract the "Displaying N matches" header
                import re
                m = re.search(r"Displaying[^\n]+", text)
                match_header = m.group(0) if m else None
                # Extract numbered result blocks
                blocks = []
                # Results show as "N. Lastname, Firstname" then several lines
                for block in re.split(r"\n(?=\d+\.\s+[A-Z])", text):
                    if any(name in block for name in [q["lname"], "Rapaport", "Weitzner", "Goldfischer"]):
                        blocks.append(block.strip()[:600])
                all_results.append({
                    "query": q,
                    "url": page.url,
                    "match_header": match_header,
                    "result_blocks": blocks[:25],
                })
            except Exception as e:
                all_results.append({"query": q, "error": str(e)})
        await _save(site, {"queries": queries}, all_results, page=page)
    finally:
        await ctx.close()


# ── SITE 2: Yad Vashem Names DB ────────────────────────────────────────
async def yadvashem(browser):
    site = "yadvashem"
    print(f"\n[{site}] Opening Yad Vashem Names DB…")
    queries = [
        # Each: (first_name, last_name, place)
        ("Berisz",   "Rapaport", "Nadworna"),
        ("Rebeka",   "Griffel",  "Nadworna"),
        ("Rebeka",   "Rapaport", "Nadworna"),
        ("Lota",     "Rapaport", "Lwow"),
        ("Lotka",    "Rapaport", "Lwow"),
        ("Eli",      "Weitzner", "Bolechow"),
        ("Mathilde", "Weinreb",  "Bolechow"),
    ]
    ctx = await browser.new_context(user_agent=UA)
    page = await ctx.new_page()
    all_results = []
    try:
        for first, last, place in queries:
            print(f"  searching: {first} {last} / {place}")
            try:
                await page.goto("https://collections.yadvashem.org/en/names",
                                wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2500)
                # Yad Vashem uses a complex SPA — try multiple selectors
                # Heuristic: find input fields by placeholder or aria-label
                async def fill_field(labels, value):
                    for label in labels:
                        try:
                            await page.get_by_label(label, exact=False).first.fill(value, timeout=3000)
                            return True
                        except Exception:
                            pass
                    return False
                await fill_field(["First Name", "Given name", "First"], first)
                await fill_field(["Last Name", "Surname", "Family"], last)
                await fill_field(["Place", "Birthplace", "Residence"], place)
                # Submit
                try:
                    await page.get_by_role("button", name="Search").first.click(timeout=4000)
                except Exception:
                    await page.keyboard.press("Enter")
                await page.wait_for_load_state("domcontentloaded", timeout=30000)
                await page.wait_for_timeout(4500)
                text = await page.locator("body").inner_text()
                # Look for "results" / "No results"
                hits = text.lower().count(last.lower())
                no_results = "no result" in text.lower() or "no matching" in text.lower()
                snippet = text[:1500]
                all_results.append({
                    "query": {"first": first, "last": last, "place": place},
                    "url": page.url,
                    "no_results": no_results,
                    "surname_mentions": hits,
                    "page_snippet": snippet,
                })
            except Exception as e:
                all_results.append({
                    "query": {"first": first, "last": last, "place": place},
                    "error": str(e),
                })
        await _save(site, {"queries": queries}, all_results, page=page)
    finally:
        await ctx.close()


# ── SITE 3: Arolsen Archives ──────────────────────────────────────────
async def arolsen(browser):
    site = "arolsen"
    print(f"\n[{site}] Opening Arolsen Archives search…")
    ctx = await browser.new_context(user_agent=UA)
    page = await ctx.new_page()
    try:
        # Their search lives at /en/archive/online-search/ via a JS app
        await page.goto("https://collections.arolsen-archives.org/en/search/person/?s=Rapaport+David+Nadworna",
                        wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(5000)
        text = await page.locator("body").inner_text()
        # Look for result count
        result_count_match = None
        for line in text.splitlines():
            if any(k in line.lower() for k in ["result", "hits", "treffer", "found"]):
                result_count_match = line.strip()
                break
        await _save(site, {"query": "Rapaport David Nadworna"}, {
            "url": page.url,
            "result_count_line": result_count_match,
            "page_snippet": text[:3000],
        }, page=page)
    except Exception as e:
        await _save(site, {"query": "Rapaport"}, {"error": str(e)}, page=page)
    finally:
        await ctx.close()


# ── SITE 4: Polscy Sprawiedliwi ────────────────────────────────────────
async def righteous(browser):
    site = "righteous"
    print(f"\n[{site}] Opening Polscy Sprawiedliwi…")
    ctx = await browser.new_context(user_agent=UA)
    page = await ctx.new_page()
    try:
        for q in ["Hormak", "Hurmak", "Chormak", "Nadworna rescuers"]:
            print(f"  searching: {q}")
            try:
                await page.goto(f"https://sprawiedliwi.org.pl/en/search/{q}",
                                wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2500)
                text = await page.locator("body").inner_text()
                await _save(site, {"query": q}, {
                    "url": page.url,
                    "page_snippet": text[:2500],
                }, page=page)
            except Exception as e:
                await _save(site, {"query": q}, {"error": str(e)}, page=page)
    finally:
        await ctx.close()


# ── SITE 5: JRI-Poland Skole ──────────────────────────────────────────
async def jri(browser):
    site = "jri"
    print(f"\n[{site}] Opening JRI-Poland Skole…")
    ctx = await browser.new_context(user_agent=UA)
    page = await ctx.new_page()
    try:
        await page.goto("https://jri-poland.org/jriplweb.htm",
                        wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        # Try to fill surname=Goldfischer, town=Skole
        try:
            await page.fill('input[name*="lname"], input[name*="surname"]', "Goldfischer")
        except Exception:
            pass
        try:
            await page.fill('input[name*="town"]', "Skole")
        except Exception:
            pass
        # Submit
        try:
            await page.click('input[type="submit"], button[type="submit"]', timeout=4000)
        except Exception:
            await page.keyboard.press("Enter")
        await page.wait_for_load_state("domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        text = await page.locator("body").inner_text()
        await _save(site, {"surname": "Goldfischer", "town": "Skole"}, {
            "url": page.url,
            "page_snippet": text[:3000],
        }, page=page)
    except Exception as e:
        await _save(site, {"surname": "Goldfischer"}, {"error": str(e)}, page=page)
    finally:
        await ctx.close()


SITES = {
    "ushmm":     ushmm,
    "yadvashem": yadvashem,
    "arolsen":   arolsen,
    "righteous": righteous,
    "jri":       jri,
}


async def main(sites):
    sites = sites or list(SITES.keys())
    unknown = [s for s in sites if s not in SITES]
    if unknown:
        print(f"Unknown sites: {unknown}. Known: {list(SITES.keys())}")
        sys.exit(1)
    async with async_playwright() as p:
        # Headed Chromium so user can watch / take over if a CAPTCHA appears.
        browser = await p.chromium.launch(headless=False, slow_mo=120)
        for s in sites:
            try:
                await SITES[s](browser)
            except Exception as e:
                print(f"  [{s}] uncaught error: {e}")
        await browser.close()
    print(f"\nAll runs complete. Results in: {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    asyncio.run(main(args))
