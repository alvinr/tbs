#!/usr/bin/env python3
"""
generate_brochure.py -- Build tbs-brochure.pdf from all TBS project pages.

Reads mkdocs.yml for page order, converts each .md source to HTML via the
`markdown` library, then renders a combined PDF via fpdf2.

Output: tbs-brochure.pdf (project root)
Usage:  python3 generate_brochure.py
"""

import logging
import os
import re
import sys
import datetime

# Suppress fpdf2 font-subsetting warnings (Apple-specific tables: Zapf, bdat, etc.)
logging.getLogger("fpdf.drawing").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.ERROR)

# -- Imports -------------------------------------------------------------------
try:
    import yaml
except ImportError:
    sys.exit("ERROR: PyYAML not installed. Run: python3 -m pip install --user pyyaml")

try:
    import markdown
except ImportError:
    sys.exit("ERROR: markdown not installed. Run: python3 -m pip install --user markdown")

try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    sys.exit("ERROR: fpdf2 not installed. Run: python3 -m pip install --user fpdf2")

# -- Constants -----------------------------------------------------------------
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MKDOCS_YML   = os.path.join(PROJECT_ROOT, "mkdocs.yml")
OUTPUT_PDF   = os.path.join(PROJECT_ROOT, "tbs-brochure.pdf")
DIAGRAMS_DIR = os.path.join(PROJECT_ROOT, "diagrams")
ASSETS_DIR   = os.path.join(PROJECT_ROOT, "assets")

# index.md in mkdocs nav is sourced from project-summary.md
NAV_SOURCE_OVERRIDE = {"index.md": "project-summary.md"}

# Pages that appear in the site nav but are intentionally omitted from the
# brochure PDF (developer reference, not part of the printed engineering set).
BROCHURE_EXCLUDE = {
    # dev/reference + galleries — web-only, not in the printed set
    "component-dependency-map.md", "all-diagrams.md", "engineering-diagrams.md",
    # Phase-1 brochure condensation (2026-07-07): exploratory / superseded / decision-record content
    # stays on the site but is dropped from the prospectus PDF (the live docs are the deep-dive appendix).
    "film-plane-mechanism-analysis.md",                                       # superseded by film-plane-mechanism-report
    "lens-options.md", "lens-vs-pinhole-exposure.md", "pinhole-option-b-optics.md",  # optics options not chosen
    "container-transport-options.md", "process-comparison.md",                # alternatives not chosen
    "tilt-swing-board-analysis.md",                                           # tilt-swing distortion renders
    "right-walkway-cantilever-study.md",                                      # decision record
    "component-dimension-audit.md",                                           # internal QA audit
    "cost-analysis-report.md",                                                # overlaps project-cost-breakdown
    "operating-manual.md",                                                    # operator procedure — not needed for funding/validation
}

# Unicode font path (macOS system font with broad Unicode coverage)
# fpdf2 needs a TTF font for characters outside Latin-1
_UNICODE_FONT_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
]
_UNICODE_FONT_BOLD_PATHS = [
    "/Library/Fonts/Arial Bold.ttf",
    "/Library/Fonts/Arial.ttf",       # fallback bold using regular
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]
_UNICODE_FONT_ITALIC_PATHS = [
    "/Library/Fonts/Arial Italic.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Oblique.ttf",
]
_UNICODE_MONO_PATHS = [
    "/System/Library/Fonts/Menlo.ttc",   # monospace WITH Greek/arrow coverage (code formulas)
    "/Library/Fonts/Andale Mono.ttf",
    "/System/Library/Fonts/Monaco.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
]

def _find_font(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

UNICODE_FONT_PATH      = _find_font(_UNICODE_FONT_PATHS)
UNICODE_FONT_BOLD_PATH = _find_font(_UNICODE_FONT_BOLD_PATHS)
UNICODE_FONT_ITALIC_PATH = _find_font(_UNICODE_FONT_ITALIC_PATHS)
UNICODE_MONO_PATH      = _find_font(_UNICODE_MONO_PATHS)
USE_UNICODE_FONT       = UNICODE_FONT_PATH is not None

if USE_UNICODE_FONT:
    FONT_BODY = "Body"
    FONT_MONO = "Mono" if UNICODE_MONO_PATH else "Courier"
    print(f"Unicode font: {UNICODE_FONT_PATH}")
else:
    FONT_BODY = "Helvetica"
    FONT_MONO = "Courier"
    print("No Unicode TTF found -- using Helvetica (ASCII-safe mode)")

# Color palette (R, G, B)
C_DARK      = (15,  30,  50)     # near-black navy (cover / section bg)
C_ACCENT    = (220, 80,  30)     # deep orange (headings, rules)
C_WHITE     = (255, 255, 255)
C_LIGHT_BG  = (245, 245, 245)    # code blocks
C_TABLE_HDR = (30,  40,  55)     # table header row bg
C_TABLE_ALT = (235, 240, 248)    # alternating table row bg
C_BODY      = (30,  30,  30)     # body text
C_MUTED     = (100, 100, 110)    # footers / captions
C_RULE      = (160, 160, 170)    # header/footer rules (neutral grey)

PAGE_W   = 210   # A4 mm
PAGE_H   = 297

# ── Page zone model ──────────────────────────────────────────────────────────
# Every page is divided into three fixed zones:
#
#   HEADER ZONE   y = 0  →  HEADER_H      (header text + rule)
#   CONTENT ZONE  y = HEADER_H → PAGE_H - FOOTER_H   (all body content)
#   FOOTER ZONE   y = PAGE_H - FOOTER_H → PAGE_H     (rule + footer text)
#
# fpdf2 enforces this via:
#   M_T = HEADER_H         → cursor starts at top of content zone
#   M_B = FOOTER_H         → auto page break at bottom of content zone
#   header() draws only within [0, HEADER_H)
#   footer() draws only within [PAGE_H - FOOTER_H, PAGE_H]
# ─────────────────────────────────────────────────────────────────────────────
HEADER_H = 16    # reserved header zone (mm)
FOOTER_H = 16    # reserved footer zone (mm)
M_L      = 20    # left margin
M_R      = 20    # right margin
M_T      = HEADER_H   # content starts here
M_B      = FOOTER_H   # auto break triggers here (from bottom)
BODY_W   = PAGE_W - M_L - M_R   # 170mm usable width
CONTENT_H = PAGE_H - HEADER_H - FOOTER_H  # 265mm usable height


# -- Unicode sanitiser (used when no Unicode TTF is available) ----------------

# Comprehensive map of common non-Latin-1 chars to ASCII equivalents
_UNICODE_SUBS = {
    "\u2014": "--",    # em dash
    "\u2013": "-",     # en dash
    "\u2019": "'",     # right single quote
    "\u2018": "'",     # left single quote
    "\u201c": '"',     # left double quote
    "\u201d": '"',     # right double quote
    "\u2026": "...",   # ellipsis
    "\u00b7": "*",     # middle dot
    "\u00d7": "x",     # multiplication sign
    "\u00f7": "/",     # division sign
    "\u00b1": "+/-",   # plus-minus
    "\u00b0": " deg",  # degree
    "\u00b2": "^2",    # superscript 2
    "\u00b3": "^3",    # superscript 3
    "\u00bc": "1/4",   # vulgar fraction 1/4
    "\u00bd": "1/2",   # vulgar fraction 1/2
    "\u00be": "3/4",   # vulgar fraction 3/4
    "\u2248": "~=",    # almost equal
    "\u2260": "!=",    # not equal
    "\u2264": "<=",    # less than or equal
    "\u2265": ">=",    # greater than or equal
    "\u03bc": "u",     # Greek mu (micro)
    "\u03a9": "ohm",   # Greek Omega
    "\u03c0": "pi",    # pi
    "\u00e9": "e",     # e with acute
    "\u00e8": "e",     # e with grave
    "\u00ea": "e",     # e with circumflex
    "\u00e0": "a",     # a with grave
    "\u00e2": "a",     # a with circumflex
    "\u00fc": "u",     # u with umlaut
    "\u00f6": "o",     # o with umlaut
    "\u00e4": "a",     # a with umlaut
    "\u00f1": "n",     # n with tilde
    "\u00ae": "(R)",   # registered
    "\u2122": "(TM)",  # trademark
    "\u00a9": "(C)",   # copyright
    "\u00a3": "GBP",   # pound
    "\u20ac": "EUR",   # euro
    "\u2192": "->",    # right arrow
    "\u2190": "<-",    # left arrow
    "\u2022": "*",     # bullet
    "\u25cf": "*",     # filled circle (bullet)
    "\u2610": "[ ]",   # ballot box
    "\u2611": "[x]",   # ballot box checked
    "\u00a0": " ",     # non-breaking space
    "\u200b": "",      # zero-width space
    "\u26a0": "[!]",   # warning sign
    "\u2705": "[ok]",  # check mark
    "\u2714": "[ok]",  # heavy check mark
    "\u274c": "[x]",   # cross mark
    "\u2603": "*",     # snowman
    "\u2b50": "*",     # star
}

# Glyphs missing from Arial Unicode that must always be substituted
_MISSING_GLYPHS = {
    "\u26a0": "[!]",   # warning sign
    "\u2705": "[ok]",  # check mark button (emoji)
    "\u2714": "[ok]",  # heavy check mark
    "\u274c": "[x]",   # cross mark
}

def _safe(text):
    """Convert text to font-safe string, substituting missing glyphs."""
    # Always substitute glyphs missing from Arial Unicode
    for ch, sub in _MISSING_GLYPHS.items():
        text = text.replace(ch, sub)
    if USE_UNICODE_FONT:
        return text
    for ch, sub in _UNICODE_SUBS.items():
        text = text.replace(ch, sub)
    # Strip any remaining non-Latin-1 characters
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _safe_html(html):
    """Make HTML content safe by replacing unsupported glyphs/entities."""
    # Always substitute glyphs missing from Arial Unicode
    for ch, sub in _MISSING_GLYPHS.items():
        html = html.replace(ch, sub)
    if USE_UNICODE_FONT:
        return html
    # Named HTML entities that expand to non-Latin-1
    html = html.replace("&mdash;", "--")
    html = html.replace("&ndash;", "-")
    html = html.replace("&hellip;", "...")
    html = html.replace("&middot;", "*")
    html = html.replace("&times;", "x")
    html = html.replace("&plusmn;", "+/-")
    html = html.replace("&deg;", " deg")
    html = html.replace("&lsquo;", "'")
    html = html.replace("&rsquo;", "'")
    html = html.replace("&ldquo;", '"')
    html = html.replace("&rdquo;", '"')
    html = html.replace("&nbsp;", " ")
    html = html.replace("&rarr;", "->")
    html = html.replace("&larr;", "<-")
    html = html.replace("&bull;", "*")
    # Numeric entities -- convert common ones
    html = re.sub(r"&#8212;", "--", html)   # em dash
    html = re.sub(r"&#8211;", "-", html)    # en dash
    html = re.sub(r"&#8217;", "'", html)    # right single quote
    html = re.sub(r"&#8216;", "'", html)    # left single quote
    html = re.sub(r"&#8220;", '"', html)    # left double quote
    html = re.sub(r"&#8221;", '"', html)    # right double quote
    html = re.sub(r"&#183;",  "*", html)    # middle dot
    html = re.sub(r"&#215;",  "x", html)    # times
    html = re.sub(r"&#176;",  " deg", html) # degree
    html = re.sub(r"&#960;",  "pi", html)   # pi
    # Apply character-level substitutions inside text nodes
    for ch, sub in _UNICODE_SUBS.items():
        html = html.replace(ch, sub)
    # Strip remaining non-Latin-1
    return html.encode("latin-1", errors="replace").decode("latin-1")


# -- Nav parsing ---------------------------------------------------------------

def parse_nav(mkdocs_yml_path):
    """
    Flatten mkdocs.yml nav into:
      [{"title": str, "src": str, "section": str|None}, ...]
    Deduplicates by source path (first occurrence wins).
    """
    with open(mkdocs_yml_path) as f:
        cfg = yaml.safe_load(f)

    nav   = cfg.get("nav", [])
    pages = []
    seen  = set()

    def _walk(items, current_section):
        for item in items:
            if isinstance(item, dict):
                for key, val in item.items():
                    if isinstance(val, str):
                        if val in BROCHURE_EXCLUDE:
                            continue
                        src_md   = NAV_SOURCE_OVERRIDE.get(val, val)
                        src_path = os.path.join(PROJECT_ROOT, src_md)
                        if src_md not in seen:
                            seen.add(src_md)
                            pages.append({
                                "title":   key,
                                "src":     src_path,
                                "section": current_section,
                            })
                    elif isinstance(val, list):
                        _walk(val, key)

    _walk(nav, None)
    return pages


# -- Markdown to HTML ----------------------------------------------------------

_MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists"],
)

def md_to_html(md_path):
    """Read a .md file, return converted HTML body string."""
    if not os.path.exists(md_path):
        return f"<p><em>Source file not found: {md_path}</em></p>"
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    # Brochure-only condensation: drop regions wrapped in
    #   <!-- brochure:skip -->  …detail the prospectus omits…  <!-- brochure:endskip -->
    # from the PDF only. The markers are HTML comments, so mkdocs renders the FULL content on the
    # website — the live site stays the complete deep-dive appendix; the PDF carries the condensed set.
    text = re.sub(r"<!--\s*brochure:skip\s*-->.*?<!--\s*brochure:endskip\s*-->", "",
                  text, flags=re.DOTALL)
    # The per-doc copyright/licence line renders in the PAGE FOOTER of the PDF, not inline at the end
    # of each section — strip it here (the website keeps it via the unchanged .md).
    text = re.sub(r"(?m)^.*©[^\n]*Alvin Richards[^\n]*Released under[^\n]*$", "", text)
    _MD.reset()
    return _MD.convert(text)


# -- Image path rewriting ------------------------------------------------------

def resolve_image(name):
    """Return absolute path for an image basename, or None."""
    for d in [DIAGRAMS_DIR, ASSETS_DIR, PROJECT_ROOT]:
        candidate = os.path.join(d, name)
        if os.path.exists(candidate):
            return candidate
    return None


def strip_embeds(html):
    """Remove interactive 3D-model (Sketchfab) embeds — they can't render in a
    static PDF, and their iframe `src=".../embed"` otherwise trips the image
    resolver ('[warn] image not found: embed'). Drops the whole embed wrapper,
    any stray iframes, and the 'Interactive 3D model — …' lead-in line."""
    html = re.sub(r'<div class="sketchfab-embed-wrapper">.*?Sketchfab</a></p>\s*</div>',
                  "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<iframe\b.*?</iframe>', "", html,
                  flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<p>\s*<strong>Interactive 3D model</strong>.*?</p>', "",
                  html, flags=re.DOTALL | re.IGNORECASE)
    return html


def rewrite_image_srcs(html):
    """
    Rewrite src="assets/<name>" to absolute file paths.
    Removes width/height attrs (fpdf2 scales images itself).
    Strips MathJax/script blocks, LaTeX delimiters, admonition divs, and
    interactive 3D-model embeds.
    """
    html = strip_embeds(html)

    def _replace(m):
        src  = m.group(1)
        name = re.sub(r"[?#].*$", "", src)   # strip query/fragment
        name = re.sub(r"^(\.\./)*assets/", "", name)  # strip assets/ or ../assets/ prefix
        name = os.path.basename(name)  # use basename for subdirectory images
        abs_path = resolve_image(name)
        if abs_path:
            return f'src="{abs_path}"'
        print(f"  [warn] image not found: {name}", file=sys.stderr)
        return f'src="{src}"'

    html = re.sub(r'src="([^"]+)"', _replace, html)
    html = re.sub(r'\s+(?:width|height)="[^"]*"', "", html)

    # Remove script blocks (MathJax etc.)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html,
                  flags=re.DOTALL | re.IGNORECASE)
    # Replace LaTeX/MathJax math blocks with code-styled placeholder
    html = re.sub(r"\\\[.*?\\\]", "<code>[formula -- see online docs]</code>",
                  html, flags=re.DOTALL)
    html = re.sub(r"\\\(.*?\\\)", "<code>[formula]</code>", html, flags=re.DOTALL)
    html = re.sub(r"\[\[.*?\]\]", "<code>[formula -- see online docs]</code>",
                  html, flags=re.DOTALL)
    # Unwrap admonition wrappers
    html = re.sub(r'<div class="admonition[^"]*"[^>]*>', "",
                  html, flags=re.IGNORECASE)
    html = re.sub(r'<p class="admonition-title"[^>]*>.*?</p>', "",
                  html, flags=re.DOTALL | re.IGNORECASE)
    return html


# -- HTML cleanup for fpdf2 ----------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")


_IMG_SRC_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.IGNORECASE)


def _decode_html(text):
    """Decode common HTML entities in plain text."""
    text = text.replace("&amp;", "&").replace("&lt;", "<")
    text = text.replace("&gt;", ">").replace("&quot;", '"')
    text = text.replace("&#39;", "'").replace("&nbsp;", " ")
    return " ".join(text.split())


def _parse_table_html(table_html):
    """
    Parse an HTML table into structured data.
    Returns: {"header": [str, ...], "rows": [[str, ...], ...],
              "row_images": [[str|None, ...], ...]}
    row_images[i][j] is the image path found in that cell, or None.
    header may be empty if the table has no <th> cells.
    """
    header = []
    rows = []
    row_images = []   # parallel to rows

    def _extract_cell(cell_html):
        """Return (plain_text, img_path_or_None) for a cell."""
        img_m = _IMG_SRC_RE.search(cell_html)
        img_path = img_m.group(1) if img_m else None
        text = _TAG_RE.sub("", cell_html)
        return _decode_html(text), img_path

    # Check for <thead> — its <tr> cells become the header
    thead_m = re.search(r"<thead[^>]*>(.*?)</thead>", table_html,
                        flags=re.DOTALL | re.IGNORECASE)
    if thead_m:
        for cell_m in re.finditer(r"<t[dh][^>]*>(.*?)</t[dh]>",
                                  thead_m.group(1),
                                  flags=re.DOTALL | re.IGNORECASE):
            text, _ = _extract_cell(cell_m.group(1))
            header.append(text)

    # Body rows come from <tbody> if present, else the whole table
    tbody_m = re.search(r"<tbody[^>]*>(.*?)</tbody>", table_html,
                        flags=re.DOTALL | re.IGNORECASE)
    body_html = tbody_m.group(1) if tbody_m else table_html

    for tr_m in re.finditer(r"<tr[^>]*>(.*?)</tr>", body_html,
                            flags=re.DOTALL | re.IGNORECASE):
        if thead_m and tr_m.start() < thead_m.end() and tr_m.end() <= thead_m.end():
            continue
        cells = []
        imgs = []
        has_th = bool(re.search(r"<th[\s>]", tr_m.group(1), re.IGNORECASE))
        for cell_m in re.finditer(r"<t[dh][^>]*>(.*?)</t[dh]>",
                                  tr_m.group(1),
                                  flags=re.DOTALL | re.IGNORECASE):
            text, img = _extract_cell(cell_m.group(1))
            cells.append(text)
            imgs.append(img)
        if not cells:
            continue
        if has_th and not header:
            header = cells
        else:
            rows.append(cells)
            row_images.append(imgs)

    return {"header": header, "rows": rows, "row_images": row_images}


def _extract_tables(html):
    """
    Pull all <table>...</table> blocks out of the HTML.
    Replace each with a marker <!--TABLE:n-->.
    Returns (modified_html, [table_data, ...]).
    """
    tables = []
    def _replace(m):
        tdata = _parse_table_html(m.group(0))
        if not tdata["header"] and not tdata["rows"]:
            return ""
        idx = len(tables)
        tables.append(tdata)
        return f"<!--TABLE:{idx}-->"

    html = re.sub(r"<table[^>]*>.*?</table>", _replace, html,
                  flags=re.DOTALL | re.IGNORECASE)
    return html, tables


def _flatten_lists(html):
    """
    Convert <ol>/<ul> lists to <br>-separated lines with manual
    numbering/bullets.  Uses <br> instead of <p> to avoid paragraph
    margin spacing that can push content past the auto page break
    threshold without triggering a break check.
    """
    def _replace_ol(m):
        inner = m.group(1)
        items = re.findall(r"<li[^>]*>(.*?)</li>", inner,
                           flags=re.DOTALL | re.IGNORECASE)
        lines = []
        for i, item in enumerate(items, 1):
            text = item.strip()
            lines.append(f"{i}. {text}")
        return "<br>\n".join(lines) + "<br>\n"

    def _replace_ul(m):
        inner = m.group(1)
        items = re.findall(r"<li[^>]*>(.*?)</li>", inner,
                           flags=re.DOTALL | re.IGNORECASE)
        lines = []
        for item in items:
            text = item.strip()
            # Task-list items (`- [ ]` / `- [x]`) already carry their own checkbox marker — render it
            # as-is instead of prefixing the "-- " bullet (which produced "-- [ ]"). Tolerate a leading
            # <p> wrapper the markdown may add.
            if re.match(r"(?:<p[^>]*>)?\s*\[[ xX]\]", text):
                lines.append(text)
            else:
                lines.append(f"•  {text}")
        return "<br>\n".join(lines) + "<br>\n"

    # Process nested lists inside-out (deepest first)
    for _ in range(5):   # max nesting depth
        prev = html
        html = re.sub(r"<ol[^>]*>(.*?)</ol>", _replace_ol, html,
                       flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<ul[^>]*>(.*?)</ul>", _replace_ul, html,
                       flags=re.DOTALL | re.IGNORECASE)
        if html == prev:
            break
    return html


def _clean_html_for_fpdf(html):
    """
    Simplify HTML so fpdf2's write_html handles it gracefully:
    - Extract HTML tables (replaced with markers, rendered separately)
    - Unwrap unsupported block containers
    - Strip class/id/style attributes
    - Remove HTML comments
    """

    for tag in ("details", "summary", "figure", "figcaption", "nav",
                "aside", "section", "article", "main", "header",
                "footer", "div", "blockquote"):
        html = re.sub(rf"<{tag}(?:\s[^>]*)?>", "", html, flags=re.IGNORECASE)
        html = re.sub(rf"</{tag}>", "", html, flags=re.IGNORECASE)

    # Strip <hr> — markdown --- separators are unnecessary in a brochure
    html = re.sub(r"<hr\s*/?>", "", html, flags=re.IGNORECASE)

    # Convert <ol>/<ul> lists to br-separated lines — fpdf2's list rendering
    # inherits heading style for number/bullet prefixes, producing wrong
    # color and font size.  Manual numbering avoids this entirely.
    html = _flatten_lists(html)


    def _strip_attrs(m):
        tag_full = m.group(0)
        tag_full = re.sub(r'\s+(?:class|id|style)="[^"]*"', "", tag_full)
        tag_full = re.sub(r"\s+(?:class|id|style)='[^']*'", "", tag_full)
        return tag_full

    html = re.sub(r"<[a-zA-Z][^>]*>", _strip_attrs, html)
    # Substitute glyphs missing from Arial Unicode (emoji etc.)
    for ch, sub in _MISSING_GLYPHS.items():
        html = html.replace(ch, sub)
    # Remove HTML comments but preserve <!--TABLE:n--> markers
    html = re.sub(r"<!--(?!TABLE:\d+).*?-->", "", html, flags=re.DOTALL)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


# -- PDF builder ---------------------------------------------------------------

class BrochurePDF(FPDF):

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(M_L, M_T, M_R)
        self.set_auto_page_break(auto=True, margin=M_B)
        self._current_chapter = ""
        self._suppress_chrome = False   # when True, suppress header/footer

        # Register Unicode fonts if available
        # All four variants must be registered so write_html never hits
        # an undefined "bodyBI" / "bodyB" / "bodyI" font error.
        if USE_UNICODE_FONT:
            self.add_font("Body", "",   UNICODE_FONT_PATH)
            bold_path   = UNICODE_FONT_BOLD_PATH   or UNICODE_FONT_PATH
            italic_path = UNICODE_FONT_ITALIC_PATH or UNICODE_FONT_PATH
            self.add_font("Body", "B",  bold_path)
            self.add_font("Body", "I",  italic_path)
            self.add_font("Body", "BI", bold_path)   # BI uses bold face
            if UNICODE_MONO_PATH:
                self.add_font("Mono", "",   UNICODE_MONO_PATH)
                self.add_font("Mono", "B",  UNICODE_MONO_PATH)
                self.add_font("Mono", "I",  UNICODE_MONO_PATH)
                self.add_font("Mono", "BI", UNICODE_MONO_PATH)

    # -- Auto page break override ---------------------------------------------

    def accept_page_break(self):
        """Force portrait on auto page breaks (landscape is image-only)."""
        from fpdf.enums import PageOrientation
        if self.cur_orientation == PageOrientation.LANDSCAPE:
            self.add_page(orientation="P")
            return False   # we already added the page
        return True        # let fpdf2 handle normally

    # -- Header / Footer -------------------------------------------------------

    def header(self):
        """Draw within HEADER ZONE [y=0 .. HEADER_H]. Content starts below."""
        if self._suppress_chrome:
            return
        # Text at y=4, rule at y=HEADER_H-3 (leaves 3mm gap before content)
        self.set_font(FONT_BODY, "I", 7)
        self.set_text_color(*C_MUTED)
        self.set_xy(M_L, 4)
        self.cell(0, 5, _safe("The Big Shoebox Project  --  TBS-001"),
                  align="L")
        rule_y = HEADER_H - 3
        self.set_draw_color(*C_RULE)
        self.set_line_width(0.4)
        self.line(M_L, rule_y, PAGE_W - M_R, rule_y)

    def footer(self):
        """Draw within FOOTER ZONE [PAGE_H - FOOTER_H .. PAGE_H]."""
        if self._suppress_chrome:
            return
        cur_page_w = self.w
        cur_page_h = self.h
        cur_body_w = cur_page_w - M_L - M_R
        # Rule 3mm into footer zone, text below it
        rule_y = cur_page_h - FOOTER_H + 3
        self.set_draw_color(*C_RULE)
        self.set_line_width(0.3)
        self.line(M_L, rule_y, cur_page_w - M_R, rule_y)
        self.set_xy(M_L, rule_y + 2)
        self.set_font(FONT_BODY, "I", 7)
        self.set_text_color(*C_MUTED)
        self.cell(cur_body_w / 2, 5,
                  _safe("© 2026 Alvin Richards — Released under GNU AGPLv3"),
                  align="L", new_x=XPos.RIGHT)
        self.cell(cur_body_w / 2, 5,
                  _safe(f"{self._current_chapter}   Page {self.page_no()}"), align="R")

    # -- Cover page ------------------------------------------------------------

    def cover_page(self, pages):
        self._suppress_chrome = True
        self.set_auto_page_break(auto=False)
        self.add_page()
        self.set_fill_color(*C_DARK)
        self.rect(0, 0, PAGE_W, PAGE_H, "F")

        logo_path = resolve_image("logo-final.png")
        if logo_path:
            logo_w = 60
            self.image(logo_path, x=(PAGE_W - logo_w) / 2, y=50,
                       w=logo_w, keep_aspect_ratio=True)

        y_title = 135 if logo_path else 90
        self.set_font(FONT_BODY, "B", 28)
        self.set_text_color(*C_WHITE)
        self.set_xy(0, y_title)
        self.cell(PAGE_W, 14, _safe("The Big Shoebox Project"), align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font(FONT_BODY, "", 14)
        self.set_text_color(*C_ACCENT)
        self.cell(PAGE_W, 8,
                  _safe("TBS-001  --  Research & Build Documentation"),
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(4)
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.8)
        cx = PAGE_W / 2
        self.line(cx - 40, self.get_y(), cx + 40, self.get_y())
        self.ln(6)

        self.set_font(FONT_BODY, "", 10)
        self.set_text_color(*C_WHITE)
        self.cell(PAGE_W, 6,
                  _safe("20 ft ISO Container  *  O2.17mm Pinhole"
                        "  *  f/1088  *  2362mm Focal Length"),
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(4)
        self.set_font(FONT_BODY, "I", 9)
        self.set_text_color(*C_MUTED)
        self.cell(PAGE_W, 6,
                  _safe(f"Generated {datetime.date.today().strftime('%B %d, %Y')}"),
                  align="C")

        self.set_xy(0, PAGE_H - 30)
        self.set_font(FONT_BODY, "", 8)
        self.set_text_color(100, 120, 140)
        self.cell(PAGE_W, 6,
                  _safe(f"{len(pages)} chapters  *  alvinr.github.io/tbs"),
                  align="C")

        self.set_auto_page_break(auto=True, margin=M_B)
        self._suppress_chrome = False

    # -- TOC page --------------------------------------------------------------

    def toc_page(self, pages):
        self._suppress_chrome = True
        self.add_page()
        self.set_fill_color(*C_DARK)
        self.rect(0, 0, PAGE_W, 28, "F")
        self.set_font(FONT_BODY, "B", 18)
        self.set_text_color(*C_WHITE)
        self.set_xy(M_L, 8)
        self.cell(BODY_W, 12, "Table of Contents", align="L")

        self.set_y(34)
        current_section = None
        ch_num = 0

        for p in pages:
            if p["section"] != current_section:
                current_section = p["section"]
                if current_section:
                    self.ln(3)
                    self.set_font(FONT_BODY, "B", 9)
                    self.set_text_color(*C_ACCENT)
                    self.set_x(M_L)
                    self.cell(BODY_W, 5,
                              _safe(current_section.upper()), align="L",
                              new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    self.set_draw_color(*C_ACCENT)
                    self.set_line_width(0.2)
                    self.line(M_L, self.get_y(), PAGE_W - M_R, self.get_y())
                    self.ln(1)

            ch_num += 1
            self.set_font(FONT_BODY, "", 9)
            self.set_text_color(*C_BODY)
            indent = M_L + (4 if p["section"] else 0)
            self.set_x(indent)
            self.cell(8, 5, f"{ch_num}.", align="L")
            self.cell(BODY_W - 8, 5, _safe(p["title"]), align="L",
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self._suppress_chrome = False

    # -- Section break page ----------------------------------------------------

    def section_break(self, section_name):
        self._suppress_chrome = True
        self.add_page()
        self.set_fill_color(*C_DARK)
        self.rect(0, 0, PAGE_W, PAGE_H, "F")

        mid_y = (PAGE_H - 30) / 2
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(1.0)
        self.line(M_L, mid_y - 8, PAGE_W - M_R, mid_y - 8)

        self.set_xy(M_L, mid_y)
        self.set_font(FONT_BODY, "B", 24)
        self.set_text_color(*C_WHITE)
        self.cell(BODY_W, 14, _safe(section_name), align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        rule_y = self.get_y() + 4
        self.line(M_L, rule_y, PAGE_W - M_R, rule_y)
        self._suppress_chrome = False

    # -- Chapter header --------------------------------------------------------

    def chapter_header(self, num, title, section):
        self._current_chapter = title
        self._suppress_chrome = True    # no header on chapter title pages
        self.add_page()
        self._suppress_chrome = False
        self.set_y(M_T + 2)

        if section:
            self.set_font(FONT_BODY, "I", 8)
            self.set_text_color(*C_MUTED)
            self.set_x(M_L)
            self.cell(BODY_W, 5, _safe(section), align="L",
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font(FONT_BODY, "B", 11)
        self.set_text_color(*C_ACCENT)
        self.set_x(M_L)
        self.cell(BODY_W, 6, f"Chapter {num}", align="L",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font(FONT_BODY, "B", 18)
        self.set_text_color(*C_DARK)
        self.set_x(M_L)
        self.multi_cell(BODY_W, 9, _safe(title), align="L")

        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.6)
        self.line(M_L, self.get_y() + 1, PAGE_W - M_R, self.get_y() + 1)
        self.ln(6)

    # -- Chapter body ----------------------------------------------------------

    def chapter_body(self, html):
        """
        Render chapter HTML body.

        Tables are extracted and rendered via _render_table (fpdf2 primitives).
        Standalone images (<p><img></p>) are rendered as full-page figures.
        Everything else goes through write_html.
        """
        # Extract tables first (before general cleanup removes their markers)
        html, tables = _extract_tables(html)
        html = _clean_html_for_fpdf(html)
        if not USE_UNICODE_FONT:
            html = _safe_html(html)

        # Split at standalone images, preserving order
        segments = _split_at_images(html)

        for seg_html, img_path in segments:
            # ── text segment (may contain <!--TABLE:n--> markers) ────────────
            if seg_html.strip():
                # Ensure text is rendered on a portrait page
                from fpdf.enums import PageOrientation
                if self.cur_orientation == PageOrientation.LANDSCAPE:
                    self.add_page(orientation="P")
                # Split on table markers to interleave text and tables
                parts = re.split(r"<!--TABLE:(\d+)-->", seg_html)
                # parts alternates: text, table_idx, text, table_idx, text ...
                for pi, part in enumerate(parts):
                    if pi % 2 == 0:
                        # Text fragment — render via write_html
                        if part.strip():
                            self._render_html_with_heading_breaks(
                                part, tables)
                    else:
                        # Table marker — render the extracted table
                        tidx = int(part)
                        if tidx < len(tables):
                            self._render_table(tables[tidx])

            # ── full-page image ───────────────────────────────────────────────
            if img_path:
                self._render_image_page(img_path)

    # -- Heading-aware HTML renderer -------------------------------------------

    # Minimum space (mm) required below a heading on the same page.
    # If less than this remains, break to the next page first.
    _HEADING_KEEP_MM = 35   # heading + ~4 lines of body text

    _HEADING_SPLIT_RE = re.compile(
        r'(<h[1-6][\s>])', re.IGNORECASE,
    )

    def _render_html_with_heading_breaks(self, html, tables):
        """
        Render an HTML fragment via write_html, but split at headings
        and insert page breaks to prevent orphaned headings at page bottom.

        For each heading fragment, measure its full height via dry_run.
        If the block fits on a fresh page but not in the remaining space,
        break first so the heading + its content stay together.
        """
        # Split HTML at heading tags, keeping the delimiter with the
        # fragment that follows it (the heading's own block).
        pieces = self._HEADING_SPLIT_RE.split(html)
        # pieces: [before_first_heading, '<h2 ', rest, '<h3 ', rest, ...]
        # Re-join: first piece is standalone, then pairs of (tag_start, rest)
        fragments = [pieces[0]] if pieces else []
        for i in range(1, len(pieces), 2):
            # Re-attach the heading tag start to its content
            if i + 1 < len(pieces):
                fragments.append(pieces[i] + pieces[i + 1])
            else:
                fragments.append(pieces[i])

        tag_styles = _build_tag_styles()
        page_bottom = PAGE_H - FOOTER_H

        for frag in fragments:
            if not frag.strip():
                continue

            # If this fragment starts with a heading, measure its height
            # and break to a new page if it won't fit but would fit on
            # a fresh page.
            if self._HEADING_SPLIT_RE.match(frag):
                remaining = page_bottom - self.get_y()
                # Measure fragment height via dry_run write_html
                frag_h = self._measure_html_height(frag, tag_styles)
                # If it won't fit here but WOULD fit on a full page, break
                if frag_h > remaining and frag_h <= CONTENT_H:
                    self.add_page()
                # Fallback: if it won't even fit a full page, at least
                # ensure minimum keep space for the heading itself
                elif remaining < self._HEADING_KEEP_MM:
                    self.add_page()

            self._render_paras(frag, tag_styles)

    def _render_paras(self, html, tag_styles):
        """
        Split HTML at </p> boundaries and render each paragraph via
        write_html with an explicit page-break check between them.
        fpdf2's <p> margin spacing can push the cursor past the auto
        page break threshold, so we verify position after every chunk.
        """
        page_bottom = PAGE_H - FOOTER_H
        # Split at </p> but keep the closing tag with its paragraph
        chunks = re.split(r'(</p>)', html, flags=re.IGNORECASE)
        # Re-join: pairs of (content, </p>) plus possible trailing text
        paragraphs = []
        buf = ""
        for chunk in chunks:
            buf += chunk
            if re.match(r'</p>', chunk, re.IGNORECASE):
                paragraphs.append(buf)
                buf = ""
        if buf.strip():
            paragraphs.append(buf)

        for para in paragraphs:
            if not para.strip():
                continue
            # Measure paragraph height and break preemptively if it
            # won't fit in remaining space.  This prevents write_html
            # from drawing text into the footer zone.
            para_h = self._measure_html_height(para, tag_styles)
            remaining = page_bottom - self.get_y()
            if para_h > remaining or remaining < 8:
                # Break unless para won't fit even on a fresh page
                if para_h <= CONTENT_H:
                    self.add_page()
            self.set_font(FONT_BODY, "", 9)
            self.set_text_color(*C_BODY)
            self.set_x(M_L)
            try:
                self.write_html(para, tag_styles=tag_styles)
            except Exception as e:
                print(f"  [warn] HTML render error: {e}",
                      file=sys.stderr)
                plain = re.sub(r"<[^>]+>", " ", para)
                plain = re.sub(r"\s+", " ", plain).strip()
                if self.page == 0:
                    self.add_page()
                self.set_font(FONT_BODY, "", 9)
                self.set_text_color(*C_BODY)
                self.set_x(M_L)
                self.multi_cell(BODY_W, 5, plain[:8000])
            # Safety net: if margin spacing still pushed cursor past
            # the content zone, force a break.
            if self.get_y() > page_bottom:
                self.add_page()

    def _measure_html_height(self, html_frag, tag_styles):
        """Estimate height of an HTML fragment without rendering.

        Counts lines by stripping tags and measuring text width against
        BODY_W, plus extra height for headings and paragraph spacing.
        """
        # Strip tags to get plain text
        plain = re.sub(r"<[^>]+>", " ", html_frag)
        plain = re.sub(r"\s+", " ", plain).strip()
        if not plain:
            return 0
        # Measure total text width
        self.set_font(FONT_BODY, "", 9)
        tw = self.get_string_width(plain)
        n_lines = max(1, int(tw / BODY_W + 0.99))
        line_h = 5.0  # approximate line height for 9pt
        # Add height for headings (larger font + spacing)
        n_headings = len(re.findall(r"<h[1-6][\s>]", html_frag, re.IGNORECASE))
        heading_extra = n_headings * 8  # extra space per heading
        # Add height for paragraph breaks
        n_paras = len(re.findall(r"<p[\s>]", html_frag, re.IGNORECASE))
        para_extra = n_paras * 3  # spacing between paragraphs
        return n_lines * line_h + heading_extra + para_extra

    # -- Table renderer (drawn with fpdf2 primitives) --------------------------

    def _render_table(self, tdata):
        """
        Draw a table using fpdf2 rect/cell primitives.
        - Dark header row with white bold text
        - Alternating light/white body rows
        - Thin border lines
        - Auto column widths proportional to content
        - Wraps cell text with multi_cell for long content
        - Page breaks between rows when needed
        """
        header = tdata["header"]
        rows = tdata["rows"]
        if not header and not rows:
            return

        n_cols = max(
            len(header) if header else 0,
            max((len(r) for r in rows), default=0),
        )
        if n_cols == 0:
            return

        all_rows = ([header] if header else []) + rows
        FONT_SZ = 7
        PAD_X = 1.0      # horizontal cell padding (mm)
        PAD_Y = 0.5      # vertical cell padding (mm)
        LINE_H = 3.2     # line height within cells (mm)

        # -- Measure column widths using actual font metrics -------------------
        self.set_font(FONT_BODY, "B", FONT_SZ)
        col_w = [0.0] * n_cols
        for row in all_rows:
            for i, cell in enumerate(row):
                if i < n_cols:
                    tw = self.get_string_width(_safe(cell)) + 2 * PAD_X
                    col_w[i] = max(col_w[i], tw)

        # Ensure every column has at least enough room for ~3 chars
        min_w = max(10, BODY_W / n_cols * 0.35)
        col_w = [max(min_w, min(w, BODY_W * 0.6)) for w in col_w]

        # Scale to fit exactly in BODY_W
        total = sum(col_w)
        if total > 0:
            scale = BODY_W / total
            col_w = [w * scale for w in col_w]
            # After scaling, enforce absolute minimum of 10mm
            for i in range(n_cols):
                if col_w[i] < 10:
                    col_w[i] = 10
            # Re-scale if minimums pushed us over
            total2 = sum(col_w)
            if total2 > BODY_W:
                scale2 = BODY_W / total2
                col_w = [w * scale2 for w in col_w]

        # -- Helper: compute exact row height via dry_run multi_cell ----------
        def _row_height(row, bold=False):
            self.set_font(FONT_BODY, "B" if bold else "", FONT_SZ)
            max_cell_h = LINE_H   # minimum one line
            for i in range(n_cols):
                text = _safe(row[i] if i < len(row) else "")
                cell_w = col_w[i] - 2 * PAD_X
                if cell_w <= 0:
                    continue
                result = self.multi_cell(
                    cell_w, LINE_H, text, align="L", dry_run=True,
                    output="HEIGHT",
                )
                max_cell_h = max(max_cell_h, result)
            return max_cell_h + 2 * PAD_Y

        # -- Helper: draw one row ----------------------------------------------
        def _draw_row(row, is_header=False, is_alt=False):
            rh = _row_height(row, bold=is_header)

            # Page break if row won't fit
            if self.get_y() + rh > PAGE_H - M_B:
                self.add_page()
                self.set_y(M_T + 4)   # gap below header zone
                if header and not is_header:
                    _draw_row(header, is_header=True)

            y0 = self.get_y()

            # Row background
            if is_header:
                self.set_fill_color(*C_TABLE_HDR)
            elif is_alt:
                self.set_fill_color(*C_TABLE_ALT)
            else:
                self.set_fill_color(255, 255, 255)
            self.rect(M_L, y0, BODY_W, rh, "F")

            # Disable auto page break while drawing cells — we handle
            # page breaks ourselves above.  multi_cell auto-break would
            # split a row across pages, leaving blank space and orphaned
            # background rects.
            self.set_auto_page_break(auto=False)

            # Cell text
            x = M_L
            for i in range(n_cols):
                text = _safe(row[i] if i < len(row) else "")
                w = col_w[i]

                if is_header:
                    self.set_font(FONT_BODY, "B", FONT_SZ)
                    self.set_text_color(*C_WHITE)
                else:
                    self.set_font(FONT_BODY, "", FONT_SZ)
                    self.set_text_color(*C_BODY)

                self.set_xy(x + PAD_X, y0 + PAD_Y)
                self.multi_cell(w - 2 * PAD_X, LINE_H, text, align="L")
                x += w

            self.set_auto_page_break(auto=True, margin=M_B)

            # Horizontal rule under row
            self.set_draw_color(180, 180, 190)
            self.set_line_width(0.15)
            self.line(M_L, y0 + rh, M_L + BODY_W, y0 + rh)

            # Vertical column separators
            vx = M_L
            for i in range(n_cols + 1):
                self.line(vx, y0, vx, y0 + rh)
                if i < n_cols:
                    vx += col_w[i]

            self.set_y(y0 + rh)

        # -- Draw the table ----------------------------------------------------
        self.ln(2)
        # Ensure table doesn't start in the header zone
        if self.get_y() < M_T + 4:
            self.set_y(M_T + 4)

        if header:
            _draw_row(header, is_header=True)

        row_images = tdata.get("row_images", [])
        for ri, row in enumerate(rows):
            # If this row contains images, skip the table row and render
            # each image on its own page with the row text as caption.
            has_img = (ri < len(row_images)
                       and any(img for img in row_images[ri] if img))
            if has_img:
                # Build caption from non-image cells in this row
                caption_parts = [c for c in row if c.strip()]
                caption = " — ".join(caption_parts) if caption_parts else None
                for img_src in row_images[ri]:
                    if img_src:
                        self._render_image_page(img_src, caption=caption)
            else:
                _draw_row(row, is_alt=(ri % 2 == 1))

        self.ln(2)

    def _render_image_page(self, img_path, caption=None):
        """Render an image INLINE in the text flow, capped to BODY_W x MAX_IMG_H so it does not
        dominate a page (was one dedicated full page per image, which ballooned the PDF). A page
        break happens only when the image + caption will not fit in the remaining content zone."""
        MAX_IMG_H = 118   # mm — cap so ~2 diagrams share a page; still readable
        import tempfile
        _tmp_file = None
        try:
            from PIL import Image as PILImage
            img = PILImage.open(img_path)
            img_w_px, img_h_px = img.size
            aspect = img_w_px / img_h_px
            if img.mode != "RGB":
                if img.mode == "P":
                    img = img.convert("RGBA")
                if img.mode in ("RGBA", "LA"):
                    bg = PILImage.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[-1])
                    img = bg
                else:
                    img = img.convert("RGB")
            fd, tmp_path = tempfile.mkstemp(suffix=".png", prefix="tbs_img_")
            os.close(fd)
            img.save(tmp_path, format="PNG")
            embed_src = tmp_path
            _tmp_file = tmp_path
        except Exception as e:
            print(f"  [warn] PIL error for {img_path}: {e}", file=sys.stderr)
            embed_src = img_path
            aspect = 1.5

        # Scale to fit BODY_W x MAX_IMG_H, preserving aspect.
        fit_w = BODY_W
        fit_h = fit_w / aspect
        if fit_h > MAX_IMG_H:
            fit_h = MAX_IMG_H
            fit_w = fit_h * aspect
        caption_h = 6

        # Break to a new page if the figure + caption won't fit. Disable auto-break during placement
        # so fpdf never reflows the explicitly-positioned image, and clamp the top into the content
        # zone so it can't overlap the header rule.
        self.set_auto_page_break(auto=False)
        if self.get_y() + fit_h + caption_h > PAGE_H - M_B:
            self.add_page()
        x = M_L + (BODY_W - fit_w) / 2
        y = self.get_y() + 2
        if y < M_T + 2:
            y = M_T + 2
        self.image(embed_src, x=x, y=y, w=fit_w, h=fit_h)
        if _tmp_file and os.path.exists(_tmp_file):
            os.unlink(_tmp_file)
        self.set_y(y + fit_h + 1)
        self.set_auto_page_break(auto=True, margin=M_B)

        if not caption:
            caption = os.path.splitext(os.path.basename(img_path))[0]
        self.set_x(M_L)
        self.set_font(FONT_BODY, "I", 7)
        self.set_text_color(*C_MUTED)
        self.cell(BODY_W, 4, _safe(caption), align="C")
        self.ln(6)
        self.set_text_color(*C_BODY)


def _split_at_images(html):
    """
    Find standalone images — <p><img src="path"></p> — and split the HTML
    into a list of (text_segment, img_path_or_None) pairs, in document order.

    Each pair means: render text_segment first, then render img_path as a
    full-page figure.  The final pair always has img_path=None (trailing text).

    Any remaining <img> tags NOT wrapped in a solitary <p> are stripped
    (they would be inside tables, which already had their images stripped by
    _flatten_table_cells, but this catches any stragglers).
    """
    # Match <p [attrs]><img [any attrs including alt before src]></p>
    # markdown generates: <p><img alt="..." src="path" /></p>
    _STANDALONE = re.compile(
        r'<p[^>]*>\s*<img\b[^>]*\bsrc="([^"]+)"[^>]*/?\s*>\s*</p>',
        re.IGNORECASE | re.DOTALL,
    )

    result   = []
    last_end = 0

    for m in _STANDALONE.finditer(html):
        text_before = html[last_end : m.start()]
        result.append((text_before, None))
        result.append(("", m.group(1)))
        last_end = m.end()

    # Trailing text after last image
    remaining = html[last_end:]
    # Strip any stray <img> tags that weren't in standalone <p> wrappers
    remaining = re.sub(r'<img[^>]*/?>',  "", remaining, flags=re.IGNORECASE)
    result.append((remaining, None))

    # Also strip stray <img> from earlier text segments
    cleaned = []
    for text, img in result:
        if img is None:
            text = re.sub(r'<img[^>]*/?>',  "", text, flags=re.IGNORECASE)
        cleaned.append((text, img))

    return cleaned


def _build_tag_styles():
    """Return tag_styles dict for write_html (uses fpdf2 FontFace API)."""
    from fpdf.fonts import FontFace
    def ts(emphasis, size, color, font=None):
        return FontFace(
            family=font or FONT_BODY,
            emphasis=emphasis or None,
            size_pt=size,
            color=color,
        )
    # code/pre: monospace so code/config reads as FIXED-WIDTH (the styling the reports need).
    code_font = FONT_MONO   # "Mono" (Andale Mono / Monaco / DejaVu Mono) or Courier (ASCII fallback)
    return {
        "h1": ts("B",  15, C_ACCENT),
        "h2": ts("B",  13, C_DARK),
        "h3": ts("B",  11, C_DARK),
        "h4": ts("BI", 10, C_DARK),
        "h5": ts("BI",  9, C_DARK),
        "h6": ts("I",   9, C_MUTED),
        "code": FontFace(
            family=code_font, size_pt=8, color=C_BODY,
            fill_color=(230, 230, 235),
        ),
        "pre": FontFace(
            family=code_font, size_pt=7, color=C_BODY,
            fill_color=(235, 235, 240),
        ),
        "ol":         ts("",   9, C_BODY),
        "ul":         ts("",   9, C_BODY),
        "li":         ts("",   9, C_BODY),
        "p":          ts("",   9, C_BODY),
        "blockquote": ts("",   9, C_BODY),
        "a":          ts("",   9, C_BODY),
        "em":         ts("I",  9, C_BODY),
        "strong":     ts("B",  9, C_BODY),
    }


# -- Main ----------------------------------------------------------------------

def main():
    print(f"Parsing navigation from {MKDOCS_YML}...")
    pages = parse_nav(MKDOCS_YML)
    print(f"  {len(pages)} unique pages found")

    pdf = BrochurePDF()

    print("Building cover page...")
    pdf.cover_page(pages)

    print("Building table of contents...")
    pdf.toc_page(pages)

    prev_section = None
    for i, page in enumerate(pages, start=1):
        src     = page["src"]
        title   = page["title"]
        section = page["section"]
        basename = os.path.basename(src)

        page_before = pdf.page_no()

        if section and section != prev_section:
            pdf.section_break(section)
        prev_section = section

        html_body = md_to_html(src)
        html_body = rewrite_image_srcs(html_body)
        # Strip first h1 — already rendered by chapter_header
        html_body = re.sub(r'<h1[^>]*>.*?</h1>\s*', '', html_body,
                           count=1, flags=re.DOTALL)

        pdf.chapter_header(i, title, section)
        pdf.chapter_body(html_body)

        print(f"  [{i:2d}/{len(pages)}] {title}  ({basename})  "
              f"pp {page_before+1}-{pdf.page_no()}")

    print(f"\nWriting {OUTPUT_PDF}...")
    pdf.output(OUTPUT_PDF)

    size_mb = os.path.getsize(OUTPUT_PDF) / 1_048_576
    print(f"Done. {pdf.page_no()} pages, {size_mb:.1f} MB -> {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
