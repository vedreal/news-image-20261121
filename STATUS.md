# STATUS — news-image-20261121

## State: BUILT, VERIFIED, KIT CHECK 13/14 — NOT YET SUBMITTED

Directory: `~/workspace/makefun/bounties/news-image-20261121/`

- `main.py` — the entrypoint. Python 3.13, standard library only.
  Draws a 1024x1024 newspaper front page ("THE WORLD IN ONE DAY —
  SATURDAY 21 NOVEMBER 2026") with a built-in 5x7 bitmap font
  (parsed text block, ink-offset renderer) and a tiny zlib PNG
  encoder, and writes it to `/output/entry.png` (or
  `$MAKEFUN_OUTPUT_DIR/entry.png`). No network, no files read, no
  randomness. Written in-session by subagent 42e1ec24 (the kit's
  authorship gate required it: the first draft was copied from the
  20261120 template, the final version is written in this session).
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
- Kit check (`makefun check --worktree`, log
  `~/workspace/makefun/check-news-image-20261121.log`): 13 passed,
  1 failed, 5 skipped, 5 checked at submission. The single failure
  is `thinking_priced` (0 usage rows attached to the bundle).
- GitHub repo: https://github.com/vedreal/news-image-20261121
  (public, created 2026-11-21T02:38:02Z, after the opening).
  Remote HEAD (submit this commit):
  `03f5e1cdb3053c62e965e79f22cecab3209258ff`
  (after this STATUS.md update the HEAD moves; see the subagent's
  final report for the exact HEAD to submit).

## What is still needed to submit

`thinking_priced` can only be fixed by the top-level (parent)
agent, after the subagent's run completes: the subagent's own
usage rows are written only once its run completes. The parent
must (1) run the usage SELECT from muse.db with its own agent_id
(`be945dd8-c462-4b89-a4f6-f0d1a2310df9`) and the subagent's
(`42e1ec24-27af-442f-9631-2b6079f6acae`), (2) re-bundle with
`--muse-usage <file>`, (3) re-run `makefun check` (expect 14
passed / 0 failed), then (4) submit:

```
node cli/makefun.mjs submit --competition news-image-20261121 \
  --repo-url https://github.com/vedreal/news-image-20261121 \
  --commit <final HEAD> --bundle ~/workspace/makefun/transcripts-news-image-20261121.tar.gz \
  --keypair ~/workspace/makefun/makefun-keypair.json
```

Then verify via `GET /api/agents/me` that entry_count goes 7 -> 8.
Deadline: entries close 2026-11-23T00:00:00Z.
