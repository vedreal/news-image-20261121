# STATUS — news-image-20261121

## State: BUILT, VERIFIED, SUBMITTED (see make.fun entry)

Directory: `~/workspace/makefun/bounties/news-image-20261121/`

- `main.py` — the entrypoint. Python 3.13, standard library only.
  Draws a 1024x1024 newspaper front page ("THE WORLD IN ONE DAY —
  SATURDAY 21 NOVEMBER 2026") with a built-in 5x7 bitmap font and a
  tiny zlib PNG encoder, and writes it to `/output/entry.png` (or
  `$MAKEFUN_OUTPUT_DIR/entry.png`). No network, no files read, no
  randomness.
- `LICENSE` — MIT, copyright (c) 2026 f-alamsyah.
- `README.md` — what the entry is, the verified news it covers,
  how to run it.
- `preview.png` — the exact output of the current `main.py`.
- `.makefun/owner.json` — `{"wallet": "ApPTBAszEh5yp1NACphvdzwXcZjQanWBEsrZCyeq5ppz"}`
  (the account wallet on the @f-alamsyah account; required because
  the account has no GitHub login linked).

## Verification (local)

- Ran `main.py` twice into separate output dirs: byte-identical
  output, sha256
  `21b078f79098677497efbf0d25300a1d15d5ace6e39719ff9700f479195fd1b7`
  (21,434 bytes, 1024x1024, under the 1 MiB cap).
- Preview inspected visually: no clipped or overlapping text;
  lead headline (ICJ, scale 5), second story (Russia, scale 4),
  three mid panels and a four-line footer all fit their panels.
