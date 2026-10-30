# Machaque

Personal offline Spanish drill app (Spain Spanish, B1+ to C1). Live at https://jeffpatten-source.github.io/machaque/

- The site files at the root (`index.html`, `sw.js`, `manifest.webmanifest`, icons) are generated. Don't edit them by hand.
- `source/` holds everything needed to rebuild:
  - `units/uNN.py`: one file per course unit (50 items each). `items.py` holds the two pilot units (33, 35) and the item helpers.
  - `WRITING.md` / `REVIEW.md`: the rules for writing and reviewing a new unit.
  - `build.py`: expands accepted answers, builds the typo lexicon, and writes the site to the repository root.
  - `app/`: the page template, app code and service worker.
- Rebuild: `cd source && python3 build.py` (needs `pip install verbecc` only when the verb list changes). Then commit and push; GitHub Pages serves the new version, and the phone picks it up the next time it opens online.
- Item ids are a hash of the unit and prompt, so progress survives adding units. Editing a prompt's English makes it a new item.
- Progress lives only in the phone's browser storage (`machaque.app.v1`), with a manual backup file from the home screen.
