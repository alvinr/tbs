# Bundled fonts — IBM Plex (SIL Open Font License 1.1)

The brochure PDF (`generate_brochure.py`) renders in **IBM Plex Sans** / **IBM Plex Mono**
to match the mkdocs Material site (`theme.font: text: IBM Plex Sans / code: IBM Plex Mono`).
Bundled here so the build is self-contained and reproducible.

- `IBMPlexSans-{Regular,Bold,Italic,BoldItalic}.ttf` — static instances extracted from Google
  Fonts' variable `IBMPlexSans[wdth,wght].ttf` (upright/italic) via `fontTools.varLib.instancer`
  at `wght=400/700, wdth=100`.
- `IBMPlexMono-Regular.ttf` — static, from Google Fonts `ofl/ibmplexmono`.
- Arial Unicode stays registered as a per-glyph fallback for symbols IBM Plex lacks (e.g. ⌀).

License: SIL OFL 1.1 — see `OFL.txt`. Copyright 2017 IBM Corp.
