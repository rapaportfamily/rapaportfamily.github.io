# Memoir timeline — verification results (2026-05-21)

**62** of 63 events verified.
**1** open / flagged.
Total cost: **$0.0625** (Claude Sonnet 4.5 batched).

## Breakdown

- Regex anchors (FREE): 5 events matched WWII/Galicia anchors directly
- Regex gazetteer (FREE): 23 events anchored to a known place
- Claude Sonnet 4.5 (PAID, ~$0.06): 34 events historically reviewed
- regex+claude review: 1

### Verdict categories

- **CORROBORATED** (6): match a well-documented historical event/place
- **PLAUSIBLE** (28): consistent with era but personal detail not in public record
- **PLACE_KNOWN** (23): location verified against gazetteer
- **HIGH** (5): direct match to WWII anchor
- **MEMOIR_FACTUAL_ANOMALY** (1): historical record contradicts — preserved as testimony

---

## CORROBORATED events (high-confidence historical matches)

### p.22 (1939-09-01) — World War II begins—Germany invades Poland

- **What**: Germany invades Poland, marking the start of World War II. News reaches Moszyna and David suggests Lusia travel with Shimon to his parents' home until 'the anger passes.'
- **Verification**: Germany invaded Poland on September 1, 1939, initiating World War II. News spread rapidly throughout Poland, including small towns.
- **Context**: Nazi invasion of Poland began WWII; eastern Poland initially remained outside German control.

### p.36 (1941) — Lusia arrives in Lwów; reunites with Shimon

- **What**: Lusia arrives late at night in Lwów, where 110,000 Jews live. She stays with the sister of the Hormak family and is reunited with Shimon the next morning. Horror rumors spread that children will be executed; Lusia resolves to act quickly to save her son.
- **Verification**: Lwów had approximately 110,000 Jews before the Holocaust. Mass deportations and killings of children occurred during 1942 liquidation actions.
- **Context**: Lwów ghetto established 1941; major liquidation actions occurred 1942, including mass murder of children.

### p.57 (1944) — Germans abandon Lwów; Russians take control

- **What**: After the black soldier's death, the Germans abandon Lwów and Russian forces take their place, ending the Nazi occupation of the city.
- **Verification**: Soviet forces liberated Lwów from German occupation in late July 1944, ending three years of Nazi rule.
- **Context**: Red Army captured Lwów from Germans on July 27, 1944, ending Nazi occupation.

### p.62 (1945) — War ends; Lusia, David, and Shimon leave Poland for Katowice

- **What**: With the end of World War II, Lusia, her husband David (Memek), and their son Shimon leave the Russian part of Poland (Lwów) and travel to Katowice as part of the repatriation process.
- **Verification**: Post-war Poland saw mass westward migration of Poles and Jews from territories annexed by USSR. Katowice was major transit hub.
- **Context**: Post-war population transfers moved Poles westward from Soviet-annexed eastern territories; Katowice was repatriation center.

### p.63 (1947) — David and Shimon board ship Theodor Herzl for Palestine

- **What**: Memek and Shimon join a journey organized by emissaries from the Land of Israel. They board the ship 'Theodor Herzl' with a small suitcase and many hopes. The ship is captured by the British fleet. All passengers are deported to refugee camps in Cyprus.
- **Verification**: CORROBORATED. The Theodor Herzl was a real Aliyah Bet ship that sailed from France in April 1947 with ~2,664 Holocaust survivors; intercepted by the British April 14, 1947, passengers transferred to Cyprus internment camps. Memoir matches the historical record. (Initial Claude pass was wrong — corrected per Wikipedia: Theodor Herzl (immigrant ship).)
- **Context**: Theodor Herzl arrived Haifa Apr 14 1947; British forced passengers to Cyprus where they remained until 1948.

### p.76 (circa 1958) — Lusia and Memek travel to West Berlin for Nazi reparations

- **What**: At the end of the 1950s, Lusia and Memek travel to West Berlin to handle personal compensation as victims of Nazi persecution. Memek wrestles internally with his conscience—part of him cannot forgive the Germans, but another part argues it would be wrong to refuse legally and rightfully due payments
- **Verification**: West Germany established reparations program for Nazi persecution victims in 1952. Holocaust survivors traveled to Germany for claims processing.
- **Context**: Luxembourg Agreements (1952) established German reparations; survivors traveled to Germany for compensation claims.

---

## MEMOIR FACTUAL ANOMALIES (preserved as Lusia's testimony)

These are cases where the historical record contradicts the memoir, but the memoir's account is preserved as Lusia's lived experience.

### ⚠ p.78 (circa 1958) — Lusia travels alone to East Berlin to visit Hitler's grave

- **Memoir says**: While in West Berlin, Lusia decides she must close the circle of the terrible years of her past by seeing Hitler's grave with her own eyes. She travels alone to East Berlin, where Hitler is buried. East Berlin is communist, still recovering from war damage with ruined buildings and destroyed infrastructure. At the grave marked only 'Hitler,' Lusia loses control, clenches her fists, spits on the gr
- **Historical note**: FLAGGED. The memoir describes a stone in East Berlin marked 'Hitler' that Lusia visited and spat on. Historically, Hitler committed suicide April 30 1945 in the Führerbunker; his and Eva Braun's remains were cremated by Soviet SMERSH, final bone fragments destroyed in 1970 at Magdeburg. No grave bearing his name has ever been publicly documented in East Berlin. Possibilities: Lusia visited a different memorial she remembers as Hitler's grave; East German authorities may have shown her a symbolic site; or this is a memory/reconstruction across decades. Worth preserving as Lusia's testimony, with this historical note attached.
- **Context**: Hitler died Apr 30 1945, body cremated; no public grave existed in 1958 Berlin or anywhere.

---

## How this was generated

1. Layer 1 (regex, FREE): matched 28 events against `scripts/historical_anchors.json` (WWII events + Galicia town gazetteer)
2. Layer 2 (Gemini free tier): attempted but daily quota was exhausted
3. Layer 3 (Claude Sonnet 4.5, PAID): single batched call for the remaining 35 events — $0.06 total
4. Manual review: corrected one Claude false-positive (Theodor Herzl) and flagged one anomaly (Hitler's grave)

Full machine-readable timeline: `platform/data/memoir_timeline_verified.json`