# Giving the archive a short address

Written 5 August 2026, because `rapaportfamily.github.io` is 24 characters and hard to say aloud.

**Doron has to buy the domain — I cannot.** Everything after that is one commit.

---

## What is free and what is not

GitHub Pages serves a custom domain **free**, with a **free** HTTPS certificate. The only cost is
the domain name itself, roughly **$10–15 a year** from any registrar (Namecheap, Porkbun,
Cloudflare, GoDaddy, or an Israeli registrar for a `.il` name).

---

## Available on 5 August 2026 — checked by RDAP

Shortest first. `rapaportfamily.github.io` is **24** characters.

| Domain | Length | Cost/yr | Note |
|---|---|---|---|
| **`rapaport.me`** | 11 | ~$10–20 | **recommended** — short, personal, permanent, cheap |
| **`rapaport.io`** | 11 | ~$35–60 | same length, looks sharper, three times the price — and see the note below |
| `rapaport.co` | 11 | ~$25–35 | Colombia's TLD, used generically worldwide |
| `rapaport.us` | 11 | ~$10 | shortest tier, but reads American |
| `rapaport.link` | 13 | |
| `rapaport.life` | 13 | |
| `rapaport.house` | 14 | |
| `rapaport.story` | 14 | |
| `rapaport.org.il` | 15 | no DNS, so probably free — **ISOC-IL is the authority, check there** |
| `beitrapaport.com` | 16 | "בית רפפורט" |
| `rapaportarchive.com` | 19 | |

**Already taken, do not bother:** `rapaport.com` and `.net` and `.org` (the diamond-industry
Rapaport group), `rapaport.family`, `rapaportfamily.com`, `rapaports.com`, `rapaport.info`,
`rapaport.name`, and `rapaport.co.il` — which resolves, so someone holds it.

**Avoid anything dated.** `dov80.com` is available and it is a bad idea: this archive should
outlive the birthday by fifty years.

**Avoid `rpaport.io`** — it is available, and one character shorter, because it is the family name
misspelled. Not on a memorial.

### One caveat about `.io`, since it is worth knowing before paying

`.io` belongs to the British Indian Ocean Territory. In 2024 the UK agreed to hand the Chagos
Archipelago to Mauritius, and when a territory stops existing its country code has historically
been retired — `.su`, `.yu`, `.cs`. ICANN has signalled that `.io` will continue, registrars are
still selling it, and nothing is expected to change for years. But for an archive meant to last
fifty years it is a real if small risk, and `.me` (Montenegro) carries no such question and costs a
third as much. If the look of `.io` matters more than that, buy it — just buy it knowing.

### Shortening the GitHub address instead — checked, and not worth it

Only the account name can change; `.github.io` is a fixed 10 characters. Checked 5 August 2026:
`rapaport` (2012), `rpprt`, `dovr`, `rapa` and `rprt` are all **taken**. What is free is longer —
`rapaports.github.io` (19), `rapaportfam.github.io` (21), `beitrapaport.github.io` (22).

So the best case is 19 characters against 11 for a domain, **and renaming loses the redirect**:
GitHub forwards renamed *repository* URLs, but `oldname.github.io` does not forward, and the old
name is released for anyone to claim. Every link already sent to the family would die. A custom
domain redirects permanently and breaks nothing. Buy the domain.

---

## The switch, once the domain is bought

Assume the name is `rapaport.me`. Substitute your own throughout.

### 1. DNS at the registrar

For the bare domain (`rapaport.me`), four A records and four AAAA records, all with host `@`:

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
AAAA  @   2606:50c0:8000::153
AAAA  @   2606:50c0:8001::153
AAAA  @   2606:50c0:8002::153
AAAA  @   2606:50c0:8003::153
```

And so `www` works too:

```
CNAME  www   rapaportfamily.github.io.
```

### 2. One file in this repo

`.github/workflows/pages.yml` publishes the `platform/` folder as the site root, so the file goes
**inside `platform/`**, not at the top:

```bash
echo "rapaport.me" > platform/CNAME && git add platform/CNAME && git commit -m "custom domain" && git push
```

### 3. Turn on HTTPS

Repo → **Settings → Pages** → confirm the custom domain is shown, then tick **Enforce HTTPS**.
The certificate can take a few minutes and occasionally up to 24 hours. Until it appears the site
may warn about the connection; that is normal and it clears itself.

---

## Order matters

**Set the DNS first, push the CNAME file second.** If the file lands before DNS resolves, GitHub
stops serving `rapaportfamily.github.io` and the new name does not work yet, so the archive is
down in the gap. With DNS already in place the switch is seamless.

---

## What does not break

- **Every link already shared keeps working.** GitHub permanently redirects
  `rapaportfamily.github.io` to the new domain. Nothing sent to family goes dead.
- **Nothing in the code hard-codes the address.** `manifest.webmanifest` uses relative paths
  (`start_url: "./"`), and the only mentions of the old URL anywhere are two lines of prose inside
  `research_center.json`.
- **No magic links need reissuing** — none have been minted yet. If you mint them after the
  switch, mint them on the new domain.

## What to redo

- **The phone app.** An installed home-screen icon points at the old origin. It will keep working
  through the redirect, but remove it and add it again from the new address for a clean install.
- **`robots.txt` and the `noindex` tag stay as they are.** A short domain does not make the archive
  easier to find, and it should not.
