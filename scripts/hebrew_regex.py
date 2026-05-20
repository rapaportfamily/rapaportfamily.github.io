"""Hebrew regex toolkit for entity extraction from genealogical text.

Designed for the Rapaport Family Tree memoir + WhatsApp chat archive.
Pure stdlib (re, datetime). No external dependencies.

USAGE:
    from hebrew_regex import HebrewExtractor
    ext = HebrewExtractor()
    facts = ext.extract(hebrew_text)
    # → {dates: [...], years: [...], places: [...], people: [...], hs_codes: [...]}
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional


# ── Hebrew unicode ranges ──────────────────────────────────────────
HEB_LETTERS = r"א-ת"
HEB_FINAL_LETTERS = r"ךםןףץ"  # ך ם ן ף ץ
HEB_PUNCT = r"־׳״"  # maqaf ׳ ״
HEB_WORD = rf"[{HEB_LETTERS}{HEB_PUNCT}'\"`]+"

# ── Hebrew months (Gregorian transliterations + Jewish months) ─────
HEB_MONTHS_GREGORIAN = {
    "ינואר": 1, "פברואר": 2, "מרץ": 3, "מארס": 3, "אפריל": 4, "מאי": 5, "יוני": 6,
    "יולי": 7, "אוגוסט": 8, "ספטמבר": 9, "אוקטובר": 10, "נובמבר": 11, "דצמבר": 12,
}
HEB_MONTHS_JEWISH = {
    "תשרי": 1, "חשוון": 2, "חשון": 2, "מרחשוון": 2, "מרחשון": 2,
    "כסלו": 3, "טבת": 4, "שבט": 5, "אדר": 6, "אדר א": 6, "אדר ב": 7,
    "ניסן": 8, "אייר": 9, "סיון": 10, "סיוון": 10, "תמוז": 11, "אב": 12, "אלול": 13,
}

# ── Common Hebrew place-name particles to strip ────────────────────
# When matching against our places.json, also try variants with/without these prefixes:
HEB_PLACE_PREFIXES = ["ב", "מ", "ל", "ה", "וב", "ומ", "ול", "וה"]  # in, from, to, the…

# ── Known places we are tracking — load from JSON or hard-code seed list ──
KNOWN_PLACES_HE = {
    # Galician
    "נדבורנה": "pl_nadworna",       "נדבורנא": "pl_nadworna",
    "בולחוב": "pl_bolechow",         "בולחוף": "pl_bolechow",
    "דולינה": "pl_dolina",
    "סטרי": "pl_stryj",               "סטריי": "pl_stryj",
    "לבוב": "pl_lwow",                "לבב": "pl_lwow",                   "לביב": "pl_lwow",
    "פשמישל": "pl_przemysl",        "פרזמישל": "pl_przemysl",
    "סטניסלבוב": "pl_stanislawow",
    "מוסינה": "pl_mosina_disputed",  "מוסינא": "pl_mosina_disputed",
    "מורשין": "pl_morszyn",          "מורשן": "pl_morszyn",
    "מושינה": "pl_muszyna",          "מושינא": "pl_muszyna",
    "משאנה": "pl_mszana_dolna",
    "קרינצה": "pl_krynica",          "קרניצה": "pl_krynica",
    # Wartime locations
    "סיביר": None,                    "סיביריה": None,
    "וורקוטה": None,
    "אוזבקיסטן": None,
    "טהרן": None,                     "איראן": None,                       "פרס": None,
    # Post-war
    "בריסל": "pl_brussels",          "בריסעל": "pl_brussels",
    "קפריסין": "pl_cyprus",
    "עתלית": "pl_atlit",
    "ישראל": "pl_israel",             "ארץ ישראל": "pl_israel",
    "חיפה": "pl_haifa",
    "תל אביב": "pl_telaviv",
    # Italian / pre-15th-c family origin
    "מנטובה": None,                   "פורטו": None,
}

KNOWN_PEOPLE_HE = {
    "דוד": "p_david",                  "דוד מנדל": "p_david",                  "דוד רפפורט": "p_david",
    "לאה": "p_leah",                   "לוסיה": "p_leah",                       "לוסיא": "p_leah",
    "שמעון": "p_shimon",
    "דב": "p_dov_bernard",              "ברנרד": "p_dov_bernard",                "דב ברנרד": "p_dov_bernard",
    "דליה": "p_dalia",
    "דורון": "p_doron",
    "דנה": "p_dana",                    "דניאל": "p_daniel",
    "אליהו": "p_elias_weitzner",        "אליאס": "p_elias_weitzner",
    "מתל": "p_matel_weinreb",          "מתלה": "p_matel_weinreb",
    "ברנרד רפפורט": "p_berisz",        "בריש": "p_berisz",
    "רבקה": "p_rebeka",                 "רגינה": "p_rebeka",
    "ליזר": "p_leizor_griffel",        "לייזר": "p_leizor_griffel",
    "שרה חיות": "p_sara_chajes",
    "פייגה": "p_feige",                 "ציפורה": "p_feige",
    "משה": "p_moses_weitzner",         "מויזש": "p_moses_weitzner",
    "פנינה": "p_pnina_weitzner",
    "לוטה": "p_lota",                   "לוטא": "p_lota",
    # War-era false identities
    "מריה ציזליק": "p_leah",            "ציזליק": "p_leah",
    # Researchers (just in case they appear)
    "מגדה": None,                       "באסיה": None,                          "קאשיה": None,
}


@dataclass
class HebrewFact:
    text: str            # the original Hebrew snippet
    type: str            # date, year, place, person, age, address
    value: str | dict    # normalized form
    id_ref: Optional[str] = None  # matching id in people/places.json
    start: int = 0
    end: int = 0
    context_before: str = ""
    context_after: str = ""


class HebrewExtractor:
    """Extract structured facts from Hebrew text.

    Optimized for memoir-style narrative + WhatsApp chat exports.
    """

    # ── Date / year patterns ───────────────────────────────────────
    YEAR_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")  # 1800-2099 — wide enough
    # "ה-3 ביולי 1942" or "3 ביולי 1942" or "ביולי 1942"
    DATE_DAY_MONTH_YEAR = re.compile(
        rf"(?:ה[-־]?)?(\d{{1,2}})\s*ב[-־]?({'|'.join(HEB_MONTHS_GREGORIAN.keys())})\s*(1[89]\d{{2}}|20\d{{2}})"
    )
    DATE_MONTH_YEAR = re.compile(
        rf"ב[-־]?({'|'.join(HEB_MONTHS_GREGORIAN.keys())})\s*(1[89]\d{{2}}|20\d{{2}})"
    )
    # Age: "בת 18", "בן 80"
    AGE_RE = re.compile(r"(בת|בן)\s+(\d{1,3})")

    # Street + house number: "רחוב לגיונוב 24" or "ברחוב … 24"
    STREET_RE = re.compile(rf"(?:רחוב|רח'?)\s+({HEB_WORD})(?:\s+(\d+))?")

    def __init__(self, extra_places: dict | None = None, extra_people: dict | None = None):
        self.places = dict(KNOWN_PLACES_HE)
        if extra_places: self.places.update(extra_places)
        self.people = dict(KNOWN_PEOPLE_HE)
        if extra_people: self.people.update(extra_people)
        # Pre-compile alternation for places + people (sorted longest first to avoid overlapping short matches)
        self._place_re = re.compile(
            r"\b(" + "|".join(re.escape(k) for k in sorted(self.places, key=len, reverse=True)) + r")\b"
        )
        self._people_re = re.compile(
            r"\b(" + "|".join(re.escape(k) for k in sorted(self.people, key=len, reverse=True)) + r")\b"
        )

    def _context(self, text: str, start: int, end: int, n: int = 40) -> tuple[str, str]:
        return text[max(0, start - n):start].strip(), text[end:end + n].strip()

    def extract(self, text: str) -> dict:
        facts: dict[str, list[HebrewFact]] = {
            "dates": [], "years": [], "ages": [], "places": [], "people": [], "addresses": [],
        }

        for m in self.DATE_DAY_MONTH_YEAR.finditer(text):
            d, mo, y = m.group(1), m.group(2), m.group(3)
            month_idx = HEB_MONTHS_GREGORIAN.get(mo, 0)
            b, a = self._context(text, m.start(), m.end())
            facts["dates"].append(HebrewFact(
                text=m.group(0), type="date",
                value={"year": int(y), "month": month_idx, "day": int(d), "iso": f"{y}-{month_idx:02d}-{int(d):02d}" if month_idx else None},
                start=m.start(), end=m.end(), context_before=b, context_after=a,
            ))
        seen_year_spans = {(f.start, f.end) for f in facts["dates"]}
        for m in self.DATE_MONTH_YEAR.finditer(text):
            if (m.start(), m.end()) in seen_year_spans: continue
            mo, y = m.group(1), m.group(2)
            month_idx = HEB_MONTHS_GREGORIAN.get(mo, 0)
            b, a = self._context(text, m.start(), m.end())
            facts["dates"].append(HebrewFact(
                text=m.group(0), type="month_year",
                value={"year": int(y), "month": month_idx},
                start=m.start(), end=m.end(), context_before=b, context_after=a,
            ))
        # Standalone years that weren't already part of a date
        date_year_spans = []
        for f in facts["dates"]:
            v = f.value
            if isinstance(v, dict) and "year" in v:
                # find year span inside the matched text
                ym = re.search(r"(1[89]\d{2}|20\d{2})", f.text)
                if ym: date_year_spans.append((f.start + ym.start(), f.start + ym.end()))
        for m in self.YEAR_RE.finditer(text):
            if any(s <= m.start() < e for s, e in date_year_spans): continue
            b, a = self._context(text, m.start(), m.end())
            facts["years"].append(HebrewFact(
                text=m.group(0), type="year", value=int(m.group(1)),
                start=m.start(), end=m.end(), context_before=b, context_after=a,
            ))

        for m in self.AGE_RE.finditer(text):
            b, a = self._context(text, m.start(), m.end())
            facts["ages"].append(HebrewFact(
                text=m.group(0), type="age",
                value={"gender": "F" if m.group(1) == "בת" else "M", "age": int(m.group(2))},
                start=m.start(), end=m.end(), context_before=b, context_after=a,
            ))

        for m in self._place_re.finditer(text):
            place_he = m.group(1)
            b, a = self._context(text, m.start(), m.end())
            facts["places"].append(HebrewFact(
                text=place_he, type="place", value=place_he,
                id_ref=self.places.get(place_he), start=m.start(), end=m.end(),
                context_before=b, context_after=a,
            ))

        for m in self._people_re.finditer(text):
            name_he = m.group(1)
            b, a = self._context(text, m.start(), m.end())
            facts["people"].append(HebrewFact(
                text=name_he, type="person", value=name_he,
                id_ref=self.people.get(name_he), start=m.start(), end=m.end(),
                context_before=b, context_after=a,
            ))

        for m in self.STREET_RE.finditer(text):
            street, num = m.group(1), m.group(2)
            b, a = self._context(text, m.start(), m.end())
            facts["addresses"].append(HebrewFact(
                text=m.group(0), type="address",
                value={"street": street, "number": num},
                start=m.start(), end=m.end(), context_before=b, context_after=a,
            ))

        return facts


def facts_to_dict(facts: dict) -> dict:
    return {
        category: [
            {"text": f.text, "type": f.type, "value": f.value, "id_ref": f.id_ref,
             "start": f.start, "end": f.end,
             "context_before": f.context_before, "context_after": f.context_after}
            for f in items
        ]
        for category, items in facts.items()
    }


if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2:
        print("Usage: python hebrew_regex.py <input.txt> [<output.json>]")
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8").read()
    ext = HebrewExtractor()
    facts = ext.extract(text)
    out = facts_to_dict(facts)
    if len(sys.argv) >= 3:
        open(sys.argv[2], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
        print(f"Wrote {sys.argv[2]}")
    else:
        print(json.dumps({k: len(v) for k, v in out.items()}, indent=2))
        print(json.dumps(out, ensure_ascii=False, indent=2)[:3000])
