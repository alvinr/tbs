#!/usr/bin/env python3
"""
generate_brochure.py -- Build tbs-brochure.pdf from all TBS project pages.

Reads mkdocs.yml for page order, converts each .md source to HTML via the
`markdown` library, then renders a combined PDF via fpdf2.

Output: tbs-brochure.pdf (project root)
Usage:  python3 generate_brochure.py
"""

import os
import re
import sys
import datetime

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
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MKDOCS_YML   = os.path.join(PROJECT_ROOT, "mkdocs.yml")
OUTPUT_PDF   = os.path.join(PROJECT_ROOT, "tbs-brochure.pdf")
DIAGRAMS_DIR = os.path.join(PROJECT_ROOT, "diagrams")
ASSETS_DIR   = os.path.join(PROJECT_ROOT, "assets")

# index.md in mkdocs nav is sourced from project-summary.md
NAV_SOURCE_OVERRIDE = {"index.md": "project-summary.md"}

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
C_RULE      = (200, 70,  20)     # chapter header underline

PAGE_W   = 210   # A4 mm
PAGE_H   = 297
M_L      = 20    # left margin
M_R      = 20    # right margin
M_T      = 20    # top margin
M_B      = 25    # bottom margin
BODY_W   = PAGE_W - M_L - M_R   # 170mm usable width


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
}

def _safe(text):
    """Convert text to Latin-1-safe string for core PDF fonts."""
    if USE_UNICODE_FONT:
        return text
    for ch, sub in _UNICODE_SUBS.items():
        text = text.replace(ch, sub)
    # Strip any remaining non-Latin-1 characters
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _safe_html(html):
    """Make HTML content Latin-1-safe by replacing common Unicode entities."""
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


def rewrite_image_srcs(html):
    """
    Rewrite src="assets/<name>" to absolute file paths.
    Removes width/height attrs (fpdf2 scales images itself).
    Strips MathJax/script blocks, LaTeX delimiters, admonition divs.
    """
    def _replace(m):
        src  = m.group(1)
        name = re.sub(r"[?#].*$", "", src)   # strip query/fragment
        name = re.sub(r"^assets/", "", name)  # strip assets/ prefix
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
    # Replace LaTeX/MathJax math blocks with placeholder
    html = re.sub(r"\\\[.*?\\\]", "<em>[formula -- see online docs]</em>",
                  html, flags=re.DOTALL)
    html = re.sub(r"\\\(.*?\\\)", "<em>[formula]</em>", html, flags=re.DOTALL)
    html = re.sub(r"\[\[.*?\]\]", "<em>[formula -- see online docs]</em>",
                  html, flags=re.DOTALL)
    # Unwrap admonition wrappers
    html = re.sub(r'<div class="admonition[^"]*"[^>]*>', "<blockquote>",
                  html, flags=re.IGNORECASE)
    html = re.sub(r'<p class="admonition-title"[^>]*>.*?</p>', "",
                  html, flags=re.DOTALL | re.IGNORECASE)
    return html


# -- HTML cleanup for fpdf2 ----------------------------------------------------

def _flatten_table_cells(html):
    """
    fpdf2 write_html raises NotImplementedError when it encounters any inline
    tag (<strong>, <em>, <a>, <code>, ...) nested inside a <td> or <th>.
    This function strips all inline tags from cell content while preserving
    the text. Block-level tags (br) and img are kept.
    """
    _INLINE = re.compile(
        r"</?(?:a|b|i|u|s|strong|em|span|code|small|sup|sub|abbr|cite"
        r"|mark|kbd|var|samp|ins|del|font)[^>]*>",
        re.IGNORECASE,
    )

    def _flatten_cell(m):
        open_tag = m.group(1)   # <td ...> or <th ...>
        content  = m.group(2)   # inner HTML
        content  = _INLINE.sub("", content)
        close    = m.group(3)   # </td> or </th>
        return f"{open_tag}{content}{close}"

    html = re.sub(
        r"(<t[dh][^>]*>)(.*?)(</t[dh]>)",
        _flatten_cell,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return html


def _clean_html_for_fpdf(html):
    """
    Simplify HTML so fpdf2's write_html handles it gracefully:
    - Unwrap unsupported block containers
    - Strip inline tags from table cells (fpdf2 limitation)
    - Strip class/id/style attributes (keep src, href, alt, colspan, rowspan, border)
    - Remove HTML comments
    """
    for tag in ("details", "summary", "figure", "figcaption", "nav",
                "aside", "section", "article", "main", "header",
                "footer", "div"):
        html = re.sub(rf"<{tag}(?:\s[^>]*)?>", "", html, flags=re.IGNORECASE)
        html = re.sub(rf"</{tag}>", "", html, flags=re.IGNORECASE)

    # Flatten inline formatting inside table cells
    html = _flatten_table_cells(html)

    def _strip_attrs(m):
        tag_full = m.group(0)
        tag_full = re.sub(r'\s+(?:class|id|style)="[^"]*"', "", tag_full)
        tag_full = re.sub(r"\s+(?:class|id|style)='[^']*'", "", tag_full)
        return tag_full

    html = re.sub(r"<[a-zA-Z][^>]*>", _strip_attrs, html)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
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

    # -- Header / Footer -------------------------------------------------------

    def header(self):
        if self._suppress_chrome:
            return
        self.set_draw_color(*C_RULE)
        self.set_line_width(0.4)
        self.line(M_L, 10, PAGE_W - M_R, 10)
        self.set_font(FONT_BODY, "I", 7)
        self.set_text_color(*C_MUTED)
        self.set_xy(M_L, 5)
        self.cell(0, 5, _safe("The Big Shoebox Project  --  TBS-001"), align="L")

    def footer(self):
        if self._suppress_chrome:
            return
        self.set_y(-M_B + 5)
        self.set_draw_color(*C_RULE)
        self.set_line_width(0.3)
        self.line(M_L, self.get_y(), PAGE_W - M_R, self.get_y())
        self.set_y(self.get_y() + 1)
        self.set_font(FONT_BODY, "I", 7)
        self.set_text_color(*C_MUTED)
        self.cell(BODY_W // 2, 5, _safe(self._current_chapter), align="C",
                  new_x=XPos.RIGHT)
        self.cell(BODY_W // 2, 5, f"Page {self.page_no()}", align="R")

    # -- Cover page ------------------------------------------------------------

    def cover_page(self, pages):
        self._suppress_chrome = True
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
                  _safe("20 ft ISO Container  *  O2.17 mm Pinhole"
                        "  *  f/1088  *  2362 mm Focal Length"),
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
        self.add_page()
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

        self.set_draw_color(*C_RULE)
        self.set_line_width(0.6)
        self.line(M_L, self.get_y() + 1, PAGE_W - M_R, self.get_y() + 1)
        self.ln(6)

    # -- Chapter body ----------------------------------------------------------

    def chapter_body(self, html):
        """Render cleaned HTML body."""
        self.set_font(FONT_BODY, "", 9)
        self.set_text_color(*C_BODY)
        self.set_x(M_L)

        html = _clean_html_for_fpdf(html)

        # Apply Unicode sanitisation to HTML text nodes
        if not USE_UNICODE_FONT:
            html = _safe_html(html)

        try:
            self.write_html(
                html,
                table_line_separators=True,
                tag_styles=_build_tag_styles(),
            )
        except Exception as e:
            print(f"  [warn] HTML render error: {e}", file=sys.stderr)
            # Fallback: strip tags, write as plain text
            plain = re.sub(r"<[^>]+>", " ", html)
            plain = re.sub(r"\s+", " ", plain).strip()
            # Ensure a page is open after a failed write_html
            if self.page == 0:
                self.add_page()
            self.set_font(FONT_BODY, "", 9)
            self.set_text_color(*C_BODY)
            self.set_x(M_L)
            self.multi_cell(BODY_W, 5,
                            plain[:8000] + ("..." if len(plain) > 8000 else ""))


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
    # code/pre: use Body (Unicode-capable) so Greek/Unicode chars in code
    # blocks render correctly.  All Body variants are registered so bodyBI etc.
    # won't trigger an undefined-font crash.
    code_font = FONT_BODY   # Body (Unicode) or Helvetica (ASCII-safe mode)
    return {
        "h1": ts("B",  15, C_ACCENT),
        "h2": ts("B",  13, C_DARK),
        "h3": ts("B",  11, C_DARK),
        "h4": ts("BI", 10, C_DARK),
        "h5": ts("BI",  9, C_DARK),
        "h6": ts("I",   9, C_MUTED),
        "code": ts("",  8, C_BODY, font=code_font),
        "pre":  ts("",  7, C_BODY, font=code_font),
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

        print(f"  [{i:2d}/{len(pages)}] {title}  ({basename})")

        if section and section != prev_section:
            pdf.section_break(section)
        prev_section = section

        html_body = md_to_html(src)
        html_body = rewrite_image_srcs(html_body)

        pdf.chapter_header(i, title, section)
        pdf.chapter_body(html_body)

    print(f"\nWriting {OUTPUT_PDF}...")
    pdf.output(OUTPUT_PDF)

    size_mb = os.path.getsize(OUTPUT_PDF) / 1_048_576
    print(f"Done. {pdf.page_no()} pages, {size_mb:.1f} MB -> {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
