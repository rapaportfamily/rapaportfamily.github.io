# Closing the data gate

**Status as of 3 August 2026:** the *site* is closed. The *data files* are not.

---

## What was actually wrong

The archive was described as private, and the gate code looked the part —
`showNoToken()` renders a "Private family archive" screen in English and Hebrew.
But nothing ever called it. The main path read:

```js
if (!candidate) {
  loadSPA();      // no token → load everything anyway
  return;
}
```

An invalid or forged token did the same thing: it logged a warning and fell
through to "guest mode", which was the entire archive, read-only. The magic link
never gated the archive — it only decided whether the *upload* UI appeared.

So anyone with the address had the whole thing: 122 people, the memoir, the
documents, the living family.

## What is fixed now

`REQUIRE_TOKEN = true` in `auth-gate.js`. Three paths, all tested in the browser
on 3 August 2026:

| Visitor | Result | Verified |
|---|---|---|
| No token | "Private family archive" screen; `app.js` never injected | 0 script tags, no nav |
| Forged / expired token | "Invalid or revoked link"; nothing stored | no localStorage entry |
| Valid token | SPA loads, identity attached, `?t=` stripped from the URL | 14 nav links, `sub: gate-test` |

The valid-token path was tested by generating a throwaway P-256 keypair,
swapping the *public* key in locally, and minting a test token — then restoring
the real key with `git checkout`. Doron's private key was not needed and not
touched. `scripts/` has no minting tool; it lives on his PC.

**The one-line undo:** set `REQUIRE_TOKEN = false` and redeploy. Do this if
someone in the family is locked out at a bad moment — it is a deliberate escape
hatch, not a mistake.

## What is still open, and why it is harder

`data/people.json` and every other file under `data/` are static files served by
GitHub Pages. GitHub Pages has no server-side logic, so **there is no way to
make it check a token before serving a file.** The gate stops people browsing
the archive; it does not stop this:

```bash
curl https://rapaportfamily.github.io/data/people.json     # HTTP 200, 176 KB
```

`robots.txt` and `noindex` (added the same day) keep it out of search results.
Both are requests that well-behaved crawlers honour. Neither is a lock.

## The two real options

### A. Encrypt the data, carry the key in the link

Encrypt each JSON file with AES-GCM under one data key. Put that key as a claim
in the signed JWT. The gate already verifies the JWT; after verifying, it reads
the key and decrypts. Ciphertext on disk is useless without a link.

- **Cost:** every existing family link stops working. Doron must re-mint all of
  them from the private key on his PC and re-send them.
- **Honest limit:** anyone holding a valid link can extract the key from browser
  memory. That is fine — they are entitled to the data. It defends against
  strangers and crawlers, which is the actual threat.
- **Work:** a build step that encrypts `data/*.json`, plus decrypt-on-load in
  `auth-gate.js`, plus adding the claim to the minting script.

### B. Serve the data from a backend that checks the token

The project already runs on Firebase/GCP. Move the JSON behind a Cloud Function
or Firestore rules that verify the same token.

- **Cost:** real backend work, a deploy target, and the site stops being a
  static archive that will still open in twenty years' time.
- **Benefit:** the key never reaches the browser, and access can be revoked per
  person after the fact.

**Recommendation:** A, and only when there is time to re-send every link
calmly — not in the days before 28 August. Until then the site is closed, the
files are unlisted, and living people's dates stay out of the data.

## If you do nothing else

Check that Dalia, Dana and Daniel each have a working personal link **before**
the birthday. As of now, a bare URL shows them the locked screen.
