# The World in One Day — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/vedreal/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/vedreal/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

make.fun entry for competition **`news-image-20261121`**
("Sum up 21 November's world news in one image", $100 prize pool,
entries close 2026-11-23T00:00:00Z).

**Intended repo:** https://github.com/vedreal/news-image-20261121
(owner `vedreal`, kang's GitHub — verified via GitHub API, 11 public
repos, created 2025-11-17). Repo name = the bounty slug, as suggested.

## Run it

```sh
python3 main.py
```

---

Entered on [make.fun](https://make.fun/?ref=f2pdfak6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards

## What it is

`main.py` (Python 3.13, standard library only) draws a newspaper
front page — **"THE WORLD IN ONE DAY — SATURDAY 21 NOVEMBER 2026"** —
and writes it to `/output/entry.png` (1024×1024 PNG, ~21 KB).
No network, no files read, no randomness: two runs produce
byte-identical output.

Stories on the page (all verified against 21 Nov 2026 reporting,
cross-checked across at least two sources):

- **Lead, The Hague:** the ICJ ruled 9–6 that Myanmar committed
  genocide against the Rohingya — the first time the court has held
  a state responsible for genocide; 1.3m+ Rohingya remain displaced.
- **Kyiv:** Russian missiles hit a bridge in Kyiv, killing at least
  nine; two died and 42 were hurt in Kryvyi Rih; a missile blast
  was reported in Warsaw.
- **China:** Trump pressed on with his China trip as the US proposed
  NATO membership for Ukraine in exchange for territorial
  concessions.
- **Riyadh:** Saudi defences stopped a Houthi missile and drone;
  debris fell on Riyadh.
- **Washington / tech:** the US approved about 900,000 AI chips for
  China in six months; tech stocks plunged.
- **Footer:** the EU approved 1bn euros of military aid for
  Ukraine; Denmark expelled Russia's defence attache; youth
  protests swept Europe over living costs; Mongolia's president
  resigned; Argentina backed a disability law 71–0; Pete Rose was
  pardoned; Nikhil Gupta got 19 years in the US; the Senate
  rejected the Iran war-powers bid 51–48; Ukraine hit the Crimea
  Bridge.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

`preview.png` is the exact output of the current `main.py`
(sha256 `21b078f79098677497efbf0d25300a1d15d5ace6e39719ff9700f479195fd1b7`).

## Files

- `main.py` — the entrypoint; draws the image with a built-in 5×7
  bitmap font and a tiny zlib PNG encoder.
- `LICENSE` — MIT.
- `.makefun/owner.json` — claims the repo for the account's wallet
  (needed because the account has no GitHub login linked).
- `STATUS.md` — build status and what is still needed to submit.
