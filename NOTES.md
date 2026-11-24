# Concept jury — 24 November 2026 news image

## Concept #1 — DISCARDED (the cliché AI idea)
A glossy holographic globe with glowing neon network arcs and floating
headline shards. Discarded on sight: it is the default "AI news" look, names
no day, shows no identifiable event, hides every fact behind glow and
gradients, and turns to mush at 300 px. It fails the "Aturan 5 Detik" and
criterion 5 (craft) outright.

## Concept #2 — considered
A 24-hour clock dial with stories pinned around the rim. It would name the
day cleanly, but it gives the biggest story no dominance, forces tiny text
onto an arc, and the circular reading order is slow — a weak 5-second read.

## Concept #3 — CHOSEN: the editorial front page
A single confident newspaper front page: an oversized ink-and-red nameplate
reading TUESDAY / 24 NOVEMBER 2026, one dominant hand-drawn flat-vector lead
(Huang, GPU chip, rising arrow), a four-cell high-contrast index panel, and a
3×3 grid of short labelled tiles with original symbolic icons.

Why it wins against the Aturan 5 Detik: in five seconds the eye lands on the
date, then the one big illustration, then the index numbers, then the tile
grid. Nothing competes for attention, and the hierarchy is decided by size
and colour blocks rather than by reading body copy.

Why it wins against the judge's criteria:
1. Names the day — TUESDAY 24 NOVEMBER 2026 is the largest type on the page,
   and every tile is reporting from that day, none from before 13 November.
2. Breadth — markets/US, Middle East, Myanmar, Bangladesh, Vatican, Ukraine,
   Zanzibar, Indonesia, EU and US courts: nine regions/beats, not one country.
3. Reads — each story has a symbolic icon and a two-word-ish label; the lead
   and the four index numbers carry the day even if the small type is skipped.
4. Faithful — "Iran says", "Ukraine says", "EU proposes", "court clears" stay
   literal; "about 30%" and "about $1T" are marked approximate; no invented
   casualties, quotes or outcomes.
5. Craft — one grid, paper/ink/red only, no gradients, photos or garbled text;
   major type is sized to survive a ~300 px downscale.

## Revision #2

Revision #2 corrected the poster copy: the meta-note became "COMPILED FROM
THE DAY'S REPORTING · 24 NOVEMBER 2026" (no judge-facing instruction text),
the lead tag became "WALL STREET · TECH", the index labels became "NVIDIA
SHARES (ABOUT)" and "DEMOCRAT HOUSE SEATS", and five tiles were rewritten to
read naturally ("ICJ FINDS MYANMAR GENOCIDE", "HASINA ASKS TO RETURN DEC 16",
"NUNGWI HOTELS BURN · TOURISTS EVACUATE", "EU PROPOSES NEW RUSSIA SANCTIONS",
"COURT CLEARS IOWA EXPLOSIVES PLAN"). The entrypoint was hardened in two
separate edits: a full PNG chunk walk with CRC-32 through IEND, then stricter
IHDR checks and clearer failures. The three concepts are unchanged; concept
#1 is still the discarded cliché.
