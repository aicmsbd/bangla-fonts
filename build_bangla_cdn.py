#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
বাঙলা (B angla) CDN Multi-Format Font Builder
===============================================
Converts the unicode-range WOFF2 slices into a full CDN-ready
distribution: TTF + WOFF + WOFF2 for each script slice.

LEGAL NOTE
----------
Source fonts (Noto Sans, Noto Sans Bengali, Noto Sans Arabic, Noto Sans CJK)
are licensed under OFL 1.1 and/or Apache 2.0. Both licenses require that
original copyright notices are RETAINED in all copies and derivative works.
This script adds "B angla" branding WITHOUT removing the original credits —
doing so would violate the license terms and constitute copyright misrepresentation.

What this script DOES change:
  - NameID 1/4  (Family / Full name)  →  "B angla"
  - NameID 6    (PostScript name)     →  "Bangla-<script>"
  - NameID 8/9  (Manufacturer / Designer)  →  "B angla"
  - NameID 11   (Vendor URL)          →  "https://bangla.it.com/"
  - Appends a B-angla modification notice to NameID 0 (copyright)
  - Adds NameID 13 CC-BY-4.0 notice ONLY for the modifications

Usage:
    python build_bangla_cdn.py
    (Run build_bangla_fonts.py first to produce the font cache)
"""

from __future__ import annotations

import io
import sys
import subprocess
from pathlib import Path
from typing import Dict, Optional

# ── bootstrap deps ────────────────────────────────────────────────────────────
def _ensure_deps() -> None:
    missing = []
    try:
        import fontTools  # noqa: F401
    except ImportError:
        missing.append("fonttools[woff]")
    try:
        import brotli  # noqa: F401
    except ImportError:
        missing.append("brotli")
    if missing:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing
        )

_ensure_deps()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fontTools.ttLib import TTFont  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).resolve().parent
CACHE_DIR   = ROOT / ".font_cache"    # source TTF/OTF (from build_bangla_fonts.py)
CDN_DIR     = ROOT / "cdn-fonts"      # output: all formats
CSS_OUT     = ROOT / "bangla-cdn.css"
HTML_OUT    = ROOT / "index.html"     # overwrite demo with CDN version

# ── branding constants ────────────────────────────────────────────────────────
FAMILY     = "Bangla"
PS_BASE    = "Bangla"
VENDOR_URL = "https://bangla.it.com/"
MOD_COPYRIGHT = (
    "Sliced and branded as 'B angla' — modifications Copyright © 2026 B angla. "
    "Licensed under CC BY 4.0 (modifications only). "
    "Original font software subject to original license terms (see below)."
)
CC_LICENSE = (
    "B angla modifications: Creative Commons Attribution 4.0 International "
    "(https://creativecommons.org/licenses/by/4.0/). "
    "ORIGINAL font software is governed by its original license (OFL 1.1 / Apache 2.0). "
    "Original copyright notices are retained as required by those licenses."
)
CC_URL     = "https://creativecommons.org/licenses/by/4.0/"

# ── unicode slices (must match build_bangla_fonts.py) ────────────────────────
SLICES: Dict[str, Dict] = {
    "latin": {
        "source_ttf": "NotoSans-Regular.ttf",
        "unicodes":   (
            "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,"
            "U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,"
            "U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
        ),
        "css_range": (
            "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, "
            "U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, "
            "U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
        ),
        "note": "Latin, extended-A, punctuation, currency",
    },
    "bengali": {
        "source_ttf": "NotoSansBengali-Regular.ttf",
        "unicodes":   "U+0980-09FF,U+200C,U+200D,U+25CC",
        "css_range":  "U+0980-09FF, U+200C, U+200D, U+25CC",
        "note": "Bengali block + ZWJ/ZWNJ for যুক্তাক্ষর conjuncts",
    },
    "arabic": {
        "source_ttf": "NotoSansArabic-Regular.ttf",
        "unicodes":   (
            "U+0600-06FF,U+0750-077F,U+08A0-08FF,"
            "U+FB50-FDFF,U+FE70-FEFF,U+200C,U+200D,U+200F"
        ),
        "css_range": (
            "U+0600-06FF, U+0750-077F, U+08A0-08FF, "
            "U+FB50-FDFF, U+FE70-FEFF, U+200C, U+200D, U+200F"
        ),
        "note": "Arabic + Supplement + Extended-A + Presentation Forms A/B",
    },
    "cyrillic": {
        "source_ttf": "NotoSans-Regular.ttf",
        "unicodes":   "U+0400-04FF,U+0500-052F,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F",
        "css_range":  "U+0400-04FF, U+0500-052F, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F",
        "note": "Cyrillic + Supplement + Extended-A/B",
    },
    "cjk": {
        "source_ttf": "NotoSansCJKsc-Regular.otf",
        "unicodes":   (
            "U+3000-303F,U+3040-309F,U+30A0-30FF,"
            "U+4E00-9FFF,U+3400-4DBF,U+F900-FAFF,U+FF00-FFEF"
        ),
        "css_range": (
            "U+3000-303F, U+3040-309F, U+30A0-30FF, "
            "U+4E00-9FFF, U+3400-4DBF, U+F900-FAFF, U+FF00-FFEF"
        ),
        "note": "CJK Unified Ideographs, Hiragana, Katakana, Compat.",
    },
}

FORMATS = [
    ("ttf",   None),    # TrueType / CFF — no flavor = binary sfnt
    ("woff",  "woff"),  # WOFF1 (zlib)
    ("woff2", "woff2"), # WOFF2 (brotli)
]


# ── subsetter ─────────────────────────────────────────────────────────────────
def subset_font(src: Path, dst: Path, unicodes: str, flavor: Optional[str]) -> bool:
    """Subset src → dst, optionally with WOFF/WOFF2 flavor."""
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        str(src),
        f"--unicodes={unicodes}",
        "--layout-features=*",
        "--no-hinting",
        "--desubroutinize",
        "--notdef-outline",
        f"--output-file={dst}",
    ]
    if flavor:
        cmd.append(f"--flavor={flavor}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"      stderr: {(res.stderr or res.stdout)[:300]}")
    return res.returncode == 0 and dst.exists() and dst.stat().st_size > 50


# ── metadata patcher ──────────────────────────────────────────────────────────
def patch_name_table(path: Path, script: str) -> None:
    """
    Inject B angla branding while RETAINING original copyright notices.
    This complies with OFL 1.1 §2 and Apache 2.0 §4(c).
    """
    font = TTFont(str(path))
    tbl  = font["name"]

    # Collect original copyright string(s) before modifying anything
    orig_copyrights = []
    for rec in tbl.names:
        if rec.nameID == 0:
            try:
                orig_copyrights.append(rec.toUnicode())
            except Exception:
                pass
    orig_copyright_str = " | ".join(dict.fromkeys(orig_copyrights))  # dedup, order-preserve

    # Build the combined copyright notice (modification credit + original retained)
    combined_copyright = f"{MOD_COPYRIGHT} | Original: {orig_copyright_str}"

    # Records to inject / overwrite (IDs that don't affect legal attribution)
    inject = {
        0:  combined_copyright,          # Copyright — modified+original
        1:  FAMILY,                      # Family name
        4:  FAMILY,                      # Full name
        6:  f"{PS_BASE}-{script.capitalize()}",  # PostScript name
        8:  FAMILY,                      # Manufacturer
        9:  FAMILY,                      # Designer
        11: VENDOR_URL,                  # Vendor URL
        13: CC_LICENSE,                  # License description (CC BY 4.0 for modifications)
        14: CC_URL,                      # License URL
    }

    for nid, val in inject.items():
        tbl.setName(val, nid, 3, 1, 0x0409)  # Windows/Unicode/English
        tbl.setName(val, nid, 1, 0, 0)       # Mac/Roman/English

    font.save(str(path))
    font.close()


# ── CSS generator ─────────────────────────────────────────────────────────────
def build_cdn_css(built: Dict[str, Dict[str, Path]]) -> str:
    lines = [
        "/*",
        " * বাঙলা (B angla) — CDN-Ready Universal Font System",
        " * Sliced and branded by B angla. Modifications © 2026 B angla.",
        " * Licensed under CC BY 4.0 (modifications): https://creativecommons.org/licenses/by/4.0/",
        " * Original Noto fonts © Google, licensed OFL-1.1 / Apache 2.0.",
        " * Original copyright notices are retained in all font files as required.",
        " * Generated by build_bangla_cdn.py",
        " */",
        "",
    ]
    for script, fmt_paths in built.items():
        woff2_path = fmt_paths.get("woff2")
        woff_path  = fmt_paths.get("woff")
        if not woff2_path:
            continue
        info      = SLICES[script]
        css_range = info["css_range"]
        note      = info["note"]
        woff2_rel = f"./cdn-fonts/{woff2_path.name}"
        woff_rel  = f"./cdn-fonts/{woff_path.name}" if woff_path else None

        src_parts = []
        if woff_rel:
            src_parts.append(f'url("{woff_rel}") format("woff")')
        src_parts.append(f'url("{woff2_rel}") format("woff2")')

        lines += [
            f"/* {script.upper()} — {note} */",
            "@font-face {",
            f'  font-family: "{FAMILY}";',
            "  font-style: normal;",
            "  font-weight: 400;",
            "  font-display: swap;",
            f"  src: {', '.join(src_parts)};",
            f"  unicode-range: {css_range};",
            "}",
            "",
        ]
    return "\n".join(lines)


# ── HTML demo ─────────────────────────────────────────────────────────────────
def build_html(built: Dict[str, Dict[str, Path]]) -> str:
    rows = ""
    for script, fmt_paths in built.items():
        row_cells = f"<td><span class='b {script}'>{script.upper()}</span></td>"
        for ext in ("ttf", "woff", "woff2"):
            p = fmt_paths.get(ext)
            if p:
                kb = p.stat().st_size // 1024
                row_cells += f"<td class='num'><code>{p.name}</code><br>{kb} KB</td>"
            else:
                row_cells += "<td>—</td>"
        rows += f"\n            <tr>{row_cells}</tr>"

    total_bytes = sum(
        p.stat().st_size
        for fmt_paths in built.values()
        for p in fmt_paths.values()
    )

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>বাঙলা (B angla) — CDN Font System</title>
<link rel="stylesheet" href="bangla-cdn.css">
<style>
:root{{
  --bg:#0d0f1a;--s:#151827;--bdr:#242742;--t:#e4e6f0;--m:#7b88a0;
  --acc:#6c63ff;--red:#ff6b6b;--grn:#4caf89;--yel:#ffa726;--cya:#26c6da;--pur:#ab47bc;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"{FAMILY}",system-ui,sans-serif;background:var(--bg);color:var(--t);line-height:1.8;padding:2rem 1rem}}
.wrap{{max-width:980px;margin:0 auto}}
header{{text-align:center;padding:3rem 1rem 2rem;border-bottom:1px solid var(--bdr);margin-bottom:2.5rem}}
h1{{font-size:clamp(2rem,5vw,3.5rem);background:linear-gradient(135deg,var(--acc),var(--red));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.4rem}}
.sub{{color:var(--m);font-size:.95rem}}
.tag{{display:inline-block;background:var(--s);border:1px solid var(--bdr);border-radius:20px;
      padding:.18rem .7rem;font-size:.78rem;margin:.3rem .1rem;color:var(--m)}}
h2{{font-size:1.3rem;margin:0 0 1rem;color:var(--t)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:1.3rem;margin-bottom:2.5rem}}
.card{{background:var(--s);border:1px solid var(--bdr);border-radius:12px;padding:1.5rem;transition:border-color .2s}}
.card:hover{{border-color:var(--acc)}}
.ch{{display:flex;align-items:center;gap:.6rem;margin-bottom:.9rem}}
[dir=rtl] .ch{{flex-direction:row-reverse}}
.b{{padding:.15rem .5rem;border-radius:5px;font-size:.68rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#fff}}
.b.latin{{background:var(--acc)}}.b.bengali{{background:var(--red)}}
.b.arabic{{background:var(--yel);color:#111}}.b.cyrillic{{background:var(--cya);color:#111}}
.b.cjk{{background:var(--pur)}}
.lbl{{font-size:.78rem;color:var(--m)}}
.s{{font-size:1.4rem;line-height:2;margin:.15rem 0}}
.xl{{font-size:2rem;font-weight:600}}
.pills{{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.7rem}}
.pill{{background:#1e2135;border:1px solid var(--bdr);border-radius:7px;padding:.18rem .55rem;font-size:1.15rem}}
table{{width:100%;border-collapse:collapse;margin-bottom:2.5rem;font-size:.83rem}}
th{{text-align:left;padding:.65rem 1rem;background:var(--s);border-bottom:2px solid var(--bdr);
    color:var(--m);text-transform:uppercase;letter-spacing:.06em;font-size:.68rem;font-weight:700}}
td{{padding:.55rem 1rem;border-bottom:1px solid var(--bdr);color:var(--t);vertical-align:top}}
tr:hover td{{background:#131524}}
.num{{text-align:center;font-family:"Courier New",monospace;font-size:.82rem}}
tfoot td{{border-top:2px solid var(--bdr);border-bottom:none;font-weight:700;color:var(--grn)}}
code{{font-family:"Courier New",monospace;font-size:.8em;color:var(--acc)}}
.legal{{background:#0d1520;border:1px solid var(--bdr);border-radius:8px;
         padding:1rem 1.2rem;margin-bottom:2.5rem;font-size:.8rem;color:var(--m);line-height:1.6}}
.legal strong{{color:var(--t)}}
footer{{text-align:center;padding:2rem;color:var(--m);font-size:.8rem;border-top:1px solid var(--bdr)}}
footer p+p{{margin-top:.35rem}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>বাঙলা &mdash; B angla</h1>
  <p class="sub">CDN-Ready Universal Font System &bull; TTF + WOFF + WOFF2 &bull; 5 Scripts</p>
  <div style="margin-top:.7rem">
    <span class="tag">Zero-Tofu</span>
    <span class="tag">unicode-range</span>
    <span class="tag">Bengali GSUB</span>
    <span class="tag">CDN / pak-ready</span>
    <span class="tag">Chromium-optimised</span>
  </div>
</header>

<h2>Script Samples</h2>
<div class="grid">

  <div class="card">
    <div class="ch"><span class="b bengali">Bengali</span><span class="lbl">বাংলা &bull; U+0980–09FF</span></div>
    <p class="s xl">যুক্তাক্ষর পরীক্ষা</p>
    <p class="s">কক্সবাজার &bull; স্বাস্থ্য</p>
    <p class="s">বাংলাদেশ — প্রকৃতির রূপ অপরূপ।</p>
    <div class="pills">
      <span class="pill">ক্ষ</span><span class="pill">ত্র</span><span class="pill">জ্ঞ</span>
      <span class="pill">স্ব</span><span class="pill">ন্ত</span><span class="pill">ষ্ঠ</span>
      <span class="pill">হ্ম</span><span class="pill">শ্চ</span>
    </div>
  </div>

  <div class="card">
    <div class="ch"><span class="b latin">Latin</span><span class="lbl">English &bull; U+0000–00FF</span></div>
    <p class="s xl">The Quick Brown Fox</p>
    <p class="s">jumps over the lazy dog.</p>
    <p class="s">Sphinx of black quartz — judge my vow!</p>
  </div>

  <div class="card">
    <div class="ch"><span class="b cjk">CJK</span><span class="lbl">中文 / 日本語 &bull; U+4E00–9FFF</span></div>
    <p class="s xl">你好，世界！</p>
    <p class="s">中国有着悠久的历史与文化。</p>
    <p class="s">日本語：桜の花が咲いています。</p>
  </div>

  <div class="card" dir="rtl">
    <div class="ch"><span class="b arabic">Arabic</span><span class="lbl">العربية &bull; U+0600–06FF</span></div>
    <p class="s xl">مرحباً بالعالم</p>
    <p class="s">اللغة العربية لغة جميلة ذات تاريخ عريق.</p>
    <p class="s">بسم الله الرحمن الرحيم</p>
  </div>

  <div class="card">
    <div class="ch"><span class="b cyrillic">Cyrillic</span><span class="lbl">Русский &bull; U+0400–04FF</span></div>
    <p class="s xl">Привет, мир!</p>
    <p class="s">Россия — великая страна с богатой историей.</p>
    <p class="s">Все люди рождаются свободными и равными.</p>
  </div>

</div>

<div class="legal">
  <strong>Licensing:</strong> B angla modifications &copy; 2026 B angla, CC BY 4.0.
  Original Noto fonts &copy; Google Inc., licensed under OFL-1.1 and Apache 2.0.
  Original copyright notices are retained inside each font file as required by those licenses.
  CDN deployment of these files constitutes redistribution under OFL-1.1 / Apache 2.0 terms —
  you must preserve the embedded attribution in the name table of each font file.
</div>

<h2>Generated Font Files — cdn-fonts/</h2>
<table>
  <thead>
    <tr>
      <th>Script</th>
      <th style="text-align:center">TTF</th>
      <th style="text-align:center">WOFF</th>
      <th style="text-align:center">WOFF2</th>
    </tr>
  </thead>
  <tbody>{rows}
  </tbody>
  <tfoot>
    <tr>
      <td>Total ({len(built)} scripts × 3 formats)</td>
      <td colspan="3" style="text-align:center;font-family:'Courier New',monospace">{total_bytes // 1024} KB</td>
    </tr>
  </tfoot>
</table>

<footer>
  <p>বাঙলা (B angla) — built locally, CDN-ready, Chromium pak-ready.</p>
  <p>Noto &copy; Google (OFL-1.1 / Apache 2.0) &bull; B angla modifications &copy; 2026 CC BY 4.0</p>
</footer>

</div>
</body>
</html>
"""


# ── main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    bar = "━" * 62
    print(f"\n{bar}")
    print("  বাঙলা (B angla) — CDN Multi-Format Builder")
    print(f"{bar}\n")

    CDN_DIR.mkdir(exist_ok=True)

    # Verify cache
    missing_sources = [
        s for info in SLICES.values()
        if not (CACHE_DIR / info["source_ttf"]).exists()
        for s in [info["source_ttf"]]
    ]
    if missing_sources:
        print(f"✗  Missing cached fonts: {missing_sources}")
        print(f"   Run build_bangla_fonts.py first.\n")
        sys.exit(1)

    built: Dict[str, Dict[str, Path]] = {}

    for script, info in SLICES.items():
        src = CACHE_DIR / info["source_ttf"]
        print(f"▶ {script.upper():<12}  source: {src.name}")
        built[script] = {}

        for ext, flavor in FORMATS:
            dst = CDN_DIR / f"B-angla-{script}.{ext}"
            if dst.exists() and dst.stat().st_size > 50:
                print(f"  ✓ cached  {dst.name}  ({dst.stat().st_size//1024} KB)")
                built[script][ext] = dst
                continue

            print(f"  ⟳ {ext:<6}  {dst.name}", end="", flush=True)
            ok = subset_font(src, dst, info["unicodes"], flavor)
            if ok:
                kb = dst.stat().st_size // 1024
                print(f"  →  {kb} KB")
                patch_name_table(dst, script)
                built[script][ext] = dst
            else:
                print("  ✗ failed")
        print()

    # CSS
    print(f"▶ CSS  →  {CSS_OUT}")
    CSS_OUT.write_text(build_cdn_css(built), encoding="utf-8")
    print(f"  ✓ {CSS_OUT.name}\n")

    # HTML
    print(f"▶ HTML →  {HTML_OUT}")
    HTML_OUT.write_text(build_html(built), encoding="utf-8")
    print(f"  ✓ {HTML_OUT.name}\n")

    # Summary
    total_bytes = sum(
        p.stat().st_size
        for fmt_paths in built.values()
        for p in fmt_paths.values()
    )
    print(f"{bar}")
    print("  CDN build complete!\n")
    print(f"  {'FILE':<45}  {'SIZE':>7}")
    print(f"  {'─'*45}  {'─'*7}")
    for script, fmt_paths in built.items():
        for ext, path in fmt_paths.items():
            kb = path.stat().st_size // 1024
            print(f"  cdn-fonts/{path.name:<36}  {kb:>5} KB")
    print(f"  {'─'*45}  {'─'*7}")
    print(f"  {'TOTAL':<45}  {total_bytes//1024:>5} KB")
    print()
    print(f"  bangla-cdn.css   — CDN @font-face rules (WOFF + WOFF2 sources)")
    print(f"  index.html       — demo, open in Chromium")
    print(f"{bar}\n")


if __name__ == "__main__":
    main()
