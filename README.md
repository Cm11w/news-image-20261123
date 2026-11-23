# news-image-20261123 — World News, Monday, November 23, 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Cm11w/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Cm11w/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One 1024x1024 PNG summarising the world news of Monday, 23 November
2026 as a newspaper front page: a dark masthead with the date, one lead
story (Ukraine's overnight deep strikes and the NATO emergency session),
and 39 further stories in a dense 3x13 grid across 9 regions, with 3
drawn panels (a Bitcoin sparkline, a tanker in the Strait of Hormuz, a
ballot box) and a one-line source footer. Built Monday 23 November 2026
~12:20 WIB (05:20 UTC) as a morning snapshot — see `research-23nov.md`.
The entry will be refreshed once more on Tuesday 25 November 2026
07:00 WIB before submission, as with the 20261121/22 entries.

Formula (from our top-20 study of past winners): 35-48 dated stories
from 7-9 regions, drawn illustration panels, newspaper layout, submitted
as early as possible. Our old 5-story formula scored only 57-63% with
the judge; this entry follows the winning formula: 40 stories, 9
regions, 3 drawn panels.

## The lead + the 39 grid stories (all traceable to `research-23nov.md`)

**Lead — WAR: Ukraine strikes deep into Russia as NATO meets.**
Overnight drones hit the Kaleykino oil station in Tatarstan, ~1,500 km
from the front, and the Novoshakhtinsk refinery; a Russian corvette sank
off Libya. Three Russian missiles were confirmed in Poland on Nov 20;
NATO holds an emergency session in Brussels today. In Dymer, nine were
killed when a drone collapsed a block; Odesa is in blackout. Sources: ukraine monitor
briefing 23 Nov 04:02 UTC; h.ua; globalsconflicts.com live timeline;
thefirebrandproject.substack.com.

**Europe (6):** COP31 collapses with no deal — longest summit ever;
France rejects the EU budget over farm income guarantees; thousands
march on living costs in Lisbon, Paris, Madrid; EU and Indonesia sign a
free-trade deal after a decade; Germany gives spies wider powers against
hybrid threats; UK extends the NHS Palantir data deal to 2029.

**Middle East (6):** two tankers hit mines in the Strait of Hormuz
(drawn panel); Houthis claim strikes on a Saudi oil refinery; Bahrain:
two hurt as an Iran strike hits a civilian site; IDF warns Netanyahu an
Iran strike risks wider war; Likud and Eisenkot end coalition talks with
no deal; Gaza: nine killed, 1,600+ dead since the ceasefire.

**East Asia (6):** Kospi falls 3.7% as the AI selloff spreads, Seoul
readies a fund; South Korea's education minister quits over an AI
exam-cheating scandal; Japan quake M5.7 injures 22, trains halted; Kim
Jong Un visits China via the new Yalu River bridge; Taiwan shares down
17% in a week, short sales curbed; China cuts margin needs to 80% from
November 30.

**South Asia (3):** India now Asia's third most powerful nation; Nepal
PM Balen Shah begins his first India visit; India and China hold 10-day
talks to ease border tensions.

**Southeast Asia (2):** Indonesia factory fire: 3 dead, dozens missing;
Selangor floods: 1,800+ evacuated in Malaysia. (Research item #24, the
first frost on Thailand's Doi Inthanon, was cut when drawing: the 3x13
grid holds only 39 cards, and the frost was the lightest story — the
image holds lead + 39 = 40 stories, as the masthead says.)

**Oceania (3):** New Zealand election too close to call; Australian
music promoter Molly Meldrum dies at 83; M6.5 quake hits the Vanuatu
region, deep, no tsunami alert.

**North America (5):** Democrats win the biggest House majority since
1992 (drawn ballot-box panel, 258+ seats); Nasdaq falls 5.3% in its
worst week since 2020; Trump reposts a "TrumpCare" pitch and hits out at
Schumer; Chapo Isidro captured in Sinaloa, 11 killed in a gunfight;
1,389 Indian children held in US custody since 2023.

**South America (3):** Peru: 5,459 coastal animals dead, El Nino until
Feb 2027; Ecuador readies a flood plan for the November 29 vote;
Colombia: man hit by a firebomb during protests.

**Africa (4):** Sudan: drones hit Khartoum, damage a UN building; WHO
warns as fighting disrupts Ebola work in Congo; Nigeria boat capsizes,
29 mourners drowned; Ethiopia launches a polio drive for 11m children.

**Markets (1):** Bitcoin holds above $61,000 (drawn sparkline: Fri
58,952 - Sat 60,216 - Sun 60,784 - Mon 61,100).

Honesty notes (from the research): most events took place on Saturday
or Sunday, Nov 21-22, and were reported on Monday, Nov 23 — the image
says "as reported on Monday" in the masthead. The Dymer block was hit
on Sunday Nov 22 and reported Monday Nov 23, so it sits in the lead.
The COP31 "no deal since 2009" note (CNN/Reuters) is in the research
but the image keeps only "longest summit ever" — the safer claim. The
18 Nov Iran strike on US bases in Bahrain/Kuwait is NOT a separate card:
it was already reported on 18 Nov; the 23 Nov development — the civilian
site hit, 2 hurt — IS in the image as the Bahrain card. The tanker mine
strikes are real (two tankers, two mines, reported by Reuters/BBC) but
the culprit is unknown — the image does not blame anyone. Crypto
"winter" talk is not used — Bitcoin is a 4-day rebound from a low, not
a full recovery.

## How to run

```sh
python3 draw_entry.py   # regenerates entry.png (deterministic)
node main.ts             # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

`draw_entry.py` draws everything with PIL (Noto Sans) and aborts with
an error if any text would overflow its card. Two runs produce a
byte-identical PNG.

## Files

- `draw_entry.py` — fresh PIL drawing script for this entry
- `entry.png` — the image (1024x1024, < 1 MiB)
- `main.ts` — copies `entry.png` to the output directory
- `research-23nov.md` — the research behind every sentence
- `LICENSE` — license
