#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
বাঙলা (B angla) Universal Font System Builder
==============================================
Replicates Google Fonts' unicode-range architecture for local storage.
Produces WOFF2 slices from Noto + SolaimanLipi sources.

  pip install fonttools[woff] brotli requests
  python build_bangla_fonts.py
"""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Optional

# ── auto-install deps ─────────────────────────────────────────────────────────
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
        print(f"[setup] Installing: {' '.join(missing)} …")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing
        )

_ensure_deps()

# Ensure UTF-8 output on Windows consoles that default to cp1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fontTools.ttLib import TTFont  # noqa: E402
import requests                     # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).resolve().parent
FONTS_DIR = ROOT / "fonts"
CACHE_DIR = ROOT / ".font_cache"
CSS_OUT   = ROOT / "bangla-local.css"
HTML_OUT  = ROOT / "index.html"

# ── branding ──────────────────────────────────────────────────────────────────
FAMILY   = "Bangla"    # CSS font-family
PS_BASE  = "Bangla"    # PostScript name base (no spaces)
VERSION  = "1.0"

# ── unicode slices ────────────────────────────────────────────────────────────
# Mirrors Google Fonts segmentation strategy exactly.
SLICES: Dict[str, Dict] = {
    "latin": {
        "unicodes": (
            "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,"
            "U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,"
            "U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
        ),
        "css_range": (
            "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, "
            "U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, "
            "U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
        ),
        "source": "noto-sans",
        "note": "Latin, extended-A, punctuation, currency",
    },
    "bengali": {
        # U+200C ZWNJ + U+200D ZWJ are mandatory for conjunct (যুক্তাক্ষর) shaping.
        # U+25CC is the placeholder circle shown with floating vowel signs.
        "unicodes": "U+0980-09FF,U+200C,U+200D,U+25CC",
        "css_range": "U+0980-09FF, U+200C, U+200D, U+25CC",
        "source": "bengali",
        "note": "Bengali block + ZWJ/ZWNJ for যুক্তাক্ষর conjuncts",
    },
    "arabic": {
        "unicodes": (
            "U+0600-06FF,U+0750-077F,U+08A0-08FF,"
            "U+FB50-FDFF,U+FE70-FEFF,U+200C,U+200D,U+200F"
        ),
        "css_range": (
            "U+0600-06FF, U+0750-077F, U+08A0-08FF, "
            "U+FB50-FDFF, U+FE70-FEFF, U+200C, U+200D, U+200F"
        ),
        "source": "noto-sans-arabic",
        "note": "Arabic + Supplement + Extended-A + Presentation Forms A/B",
    },
    "cyrillic": {
        "unicodes": (
            "U+0400-04FF,U+0500-052F,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F"
        ),
        "css_range": (
            "U+0400-04FF, U+0500-052F, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F"
        ),
        "source": "noto-sans",
        "note": "Cyrillic + Supplement + Extended-A/B",
    },
    "cjk": {
        "unicodes": (
            "U+3000-303F,U+3040-309F,U+30A0-30FF,"
            "U+4E00-9FFF,U+3400-4DBF,U+F900-FAFF,U+FF00-FFEF"
        ),
        "css_range": (
            "U+3000-303F, U+3040-309F, U+30A0-30FF, "
            "U+4E00-9FFF, U+3400-4DBF, U+F900-FAFF, U+FF00-FFEF"
        ),
        "source": "noto-sans-cjk",
        "note": "CJK Unified Ideographs, Hiragana, Katakana, Compat.",
    },
}

# ── download sources ──────────────────────────────────────────────────────────
SOURCES: Dict[str, Dict] = {
    "noto-sans": {
        "filename": "NotoSans-Regular.ttf",
        "size":     "~460 KB",
        "urls": [
            "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
            "https://cdn.jsdelivr.net/gh/googlefonts/noto-fonts@main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
        ],
    },
    "noto-sans-arabic": {
        "filename": "NotoSansArabic-Regular.ttf",
        "size":     "~400 KB",
        "urls": [
            "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf",
            "https://cdn.jsdelivr.net/gh/googlefonts/noto-fonts@main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf",
        ],
    },
    "noto-sans-cjk": {
        "filename": "NotoSansCJKsc-Regular.otf",
        "size":     "~15 MB — large download, be patient",
        "urls": [
            "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
            "https://cdn.jsdelivr.net/gh/googlefonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
        ],
    },
    "bengali": {
        # Noto Sans Bengali — OFL-1.1, complete GSUB/GPOS for all Bengali conjuncts
        "filename": "NotoSansBengali-Regular.ttf",
        "size":     "~195 KB",
        "urls": [
            "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansBengali/NotoSansBengali-Regular.ttf",
            "https://cdn.jsdelivr.net/gh/googlefonts/noto-fonts@main/hinted/ttf/NotoSansBengali/NotoSansBengali-Regular.ttf",
        ],
        "fallback_filename": "Nikosh.ttf",
        "fallback_urls": [
            "https://github.com/opengits/nikosh-font/raw/master/Nikosh.ttf",
        ],
    },
}

HEADERS = {"User-Agent": "Mozilla/5.0 BanglaFontBuilder/1.0"}


# ── download helper ───────────────────────────────────────────────────────────
def download_source(key: str, cache: Path) -> Optional[Path]:
    src  = SOURCES[key]
    dest = cache / src["filename"]

    if dest.exists() and dest.stat().st_size > 10_000:
        print(f"  ✓ cached   {src['filename']}")
        return dest

    for url in src["urls"]:
        print(f"  ↓ {src['filename']}  ({src['size']})")
        print(f"    {url}")
        try:
            resp = requests.get(url, stream=True, timeout=300, headers=HEADERS)
            resp.raise_for_status()
            total  = int(resp.headers.get("content-length", 0))
            got    = 0
            with open(dest, "wb") as fh:
                for chunk in resp.iter_content(65536):
                    if chunk:
                        fh.write(chunk)
                        got += len(chunk)
                        if total:
                            filled = int(32 * got / total)
                            bar    = "█" * filled + "░" * (32 - filled)
                            print(f"\r    [{bar}] {got//1024:>6}KB/{total//1024}KB",
                                  end="", flush=True)
            print(f"\r  ✓ {src['filename']}  {got//1024} KB saved{' '*20}")
            return dest
        except Exception as exc:
            print(f"\n  ✗ {url}\n    {exc}")
            dest.unlink(missing_ok=True)

    # Bengali-only: try Nikosh fallback
    if "fallback_urls" in src:
        fb_dest = cache / src["fallback_filename"]
        for url in src["fallback_urls"]:
            print(f"  ↓ fallback {src['fallback_filename']}")
            try:
                resp = requests.get(url, timeout=60, headers=HEADERS)
                resp.raise_for_status()
                fb_dest.write_bytes(resp.content)
                print(f"  ✓ {src['fallback_filename']}  {len(resp.content)//1024} KB")
                return fb_dest
            except Exception as exc:
                print(f"  ✗ fallback: {exc}")

    print(f"  ✗ could not download {src['filename']} — this slice will be skipped")
    return None


# ── subsetter ─────────────────────────────────────────────────────────────────
def subset_to_woff2(src: Path, dst: Path, unicodes: str) -> bool:
    """
    Slice src → dst (WOFF2) keeping only the given unicode range.
    --layout-features=* preserves ALL GSUB/GPOS tables, which is essential
    for Bengali conjuncts (akhn, rphf, blwf, half, pstf, cjct …).
    """
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        str(src),
        f"--unicodes={unicodes}",
        "--layout-features=*",    # keep every GSUB/GPOS feature
        "--flavor=woff2",
        "--no-hinting",
        "--desubroutinize",       # required for CFF/OTF (CJK) sources
        "--notdef-outline",
        f"--output-file={dst}",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        snippet = (res.stderr or res.stdout)[:500]
        print(f"    stderr: {snippet}")
    return res.returncode == 0 and dst.exists() and dst.stat().st_size > 50


# ── metadata patcher ──────────────────────────────────────────────────────────
def patch_name_table(path: Path, script: str) -> None:
    """Rewrite embedded font name table to B angla branding."""
    try:
        font = TTFont(str(path))
        tbl  = font["name"]
        patches = {
            1:  FAMILY,                                 # Family name
            3:  f"{PS_BASE}:{script}:{VERSION}",        # Unique font ID
            4:  FAMILY,                                 # Full name
            6:  f"{PS_BASE}-{script.capitalize()}",     # PostScript name
            16: FAMILY,                                 # Preferred family
            17: "Regular",                              # Preferred subfamily
        }
        for nid, val in patches.items():
            tbl.setName(val, nid, 3, 1, 0x0409)  # Windows / Unicode / English
            tbl.setName(val, nid, 1, 0, 0)       # Mac / Roman / English
        font.save(str(path))
        font.close()
        print(f"    name table → \"{FAMILY}\" ({PS_BASE}-{script.capitalize()})")
    except Exception as exc:
        print(f"    [warn] name-table patch skipped: {exc}")


# ── CSS generator ─────────────────────────────────────────────────────────────
def build_css(slices: Dict[str, Path]) -> str:
    out = [
        "/*",
        " * বাঙলা (B angla) — Universal Local Font System",
        " * Architecture: Google Fonts unicode-range slicing, served locally.",
        " * All src: paths are relative — no external network requests.",
        " * Generated by build_bangla_fonts.py",
        " */",
        "",
    ]
    for script, path in slices.items():
        info = SLICES[script]
        out += [
            f"/* {script.upper()} — {info['note']} */",
            "@font-face {",
            f'  font-family: "{FAMILY}";',
            "  font-style: normal;",
            "  font-weight: 400;",
            "  font-display: swap;",
            f'  src: url("./fonts/{path.name}") format("woff2");',
            f"  unicode-range: {info['css_range']};",
            "}",
            "",
        ]
    return "\n".join(out)


# ── HTML generator ────────────────────────────────────────────────────────────
def build_html(slices: Dict[str, Path]) -> str:
    rows = ""
    for script, path in slices.items():
        kb   = path.stat().st_size // 1024
        note = SLICES[script]["note"]
        rows += (
            f"\n            <tr>"
            f"<td><span class='b {script}'>{script.upper()}</span></td>"
            f"<td><code>fonts/{path.name}</code></td>"
            f"<td class='num'>{kb} KB</td>"
            f"<td>{note}</td>"
            f"</tr>"
        )

    total_kb = sum(p.stat().st_size for p in slices.values()) // 1024

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>বাঙলা (B angla) — Universal Font System</title>
<link rel="stylesheet" href="bangla-local.css">
<style>
:root{{
  --bg:#0d0f1a;--s:#151827;--bdr:#242742;--t:#e4e6f0;--m:#7b88a0;
  --acc:#6c63ff;--red:#ff6b6b;--grn:#4caf89;--yel:#ffa726;--cya:#26c6da;--pur:#ab47bc;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"{FAMILY}",system-ui,sans-serif;background:var(--bg);color:var(--t);line-height:1.8;padding:2rem 1rem}}
.wrap{{max-width:960px;margin:0 auto}}

header{{text-align:center;padding:3.5rem 1rem 2.5rem;border-bottom:1px solid var(--bdr);margin-bottom:2.5rem}}
h1{{font-size:clamp(2.2rem,5vw,3.8rem);background:linear-gradient(135deg,var(--acc) 30%,var(--red));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.5rem;letter-spacing:-.01em}}
.tagline{{color:var(--m);font-size:1rem}}
.tag{{display:inline-block;background:var(--s);border:1px solid var(--bdr);border-radius:20px;
      padding:.2rem .75rem;font-size:.8rem;margin:.3rem .15rem;color:var(--m)}}

h2{{font-size:1.3rem;color:var(--t);margin:0 0 1.1rem;font-weight:600}}

.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:1.4rem;margin-bottom:3rem}}
.card{{background:var(--s);border:1px solid var(--bdr);border-radius:14px;padding:1.6rem;transition:border-color .25s,box-shadow .25s}}
.card:hover{{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)20}}

.ch{{display:flex;align-items:center;gap:.7rem;margin-bottom:1rem}}
[dir=rtl] .ch{{flex-direction:row-reverse}}
.b{{padding:.18rem .52rem;border-radius:6px;font-size:.7rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#fff}}
.b.latin{{background:var(--acc)}}.b.bengali{{background:var(--red)}}
.b.arabic{{background:var(--yel);color:#111}}.b.cyrillic{{background:var(--cya);color:#111}}
.b.cjk{{background:var(--pur)}}
.lbl{{font-size:.8rem;color:var(--m)}}

.s{{font-size:1.45rem;line-height:2;margin:.2rem 0}}
.xl{{font-size:2.1rem;font-weight:600}}
.pills{{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.8rem}}
.pill{{background:#1e2135;border:1px solid var(--bdr);border-radius:8px;padding:.2rem .6rem;font-size:1.2rem}}

table{{width:100%;border-collapse:collapse;margin-bottom:3rem;font-size:.88rem}}
th{{text-align:left;padding:.7rem 1.1rem;background:var(--s);border-bottom:2px solid var(--bdr);
    color:var(--m);text-transform:uppercase;letter-spacing:.06em;font-size:.7rem;font-weight:700}}
td{{padding:.6rem 1.1rem;border-bottom:1px solid var(--bdr);color:var(--t)}}
tr:hover td{{background:#131524}}
.num{{font-variant-numeric:tabular-nums;text-align:right;font-family:"Courier New",monospace}}
tfoot td{{border-top:2px solid var(--bdr);border-bottom:none;font-weight:700;color:var(--grn)}}
code{{font-family:"Courier New",monospace;font-size:.85em;color:var(--acc)}}

footer{{text-align:center;padding:2rem;color:var(--m);font-size:.82rem;border-top:1px solid var(--bdr)}}
footer p+p{{margin-top:.4rem}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>বাঙলা &mdash; B angla</h1>
  <p class="tagline">Universal Local Font System</p>
  <div style="margin-top:.8rem">
    <span class="tag">Zero-CDN</span>
    <span class="tag">Zero-Network</span>
    <span class="tag">Zero-Tofu</span>
    <span class="tag">unicode-range optimised</span>
    <span class="tag">WOFF2 + Brotli</span>
    <span class="tag">Bengali GSUB preserved</span>
  </div>
</header>

<h2>Script Samples</h2>
<div class="grid">

  <!-- Bengali -->
  <div class="card">
    <div class="ch">
      <span class="b bengali">Bengali</span>
      <span class="lbl">বাংলা &bull; U+0980–09FF</span>
    </div>
    <p class="s xl">যুক্তাক্ষর পরীক্ষা</p>
    <p class="s">কক্সবাজার &bull; স্বাস্থ্য</p>
    <p class="s">বাংলাদেশ — প্রকৃতির রূপ অপরূপ সুন্দর।</p>
    <div class="pills">
      <span class="pill" title="ksha">ক্ষ</span>
      <span class="pill" title="tra">ত্র</span>
      <span class="pill" title="gya">জ্ঞ</span>
      <span class="pill" title="swa">স্ব</span>
      <span class="pill" title="nta">ন্ত</span>
      <span class="pill" title="shtha">ষ্ঠ</span>
      <span class="pill" title="hma">হ্ম</span>
      <span class="pill" title="shcha">শ্চ</span>
    </div>
  </div>

  <!-- Latin / English -->
  <div class="card">
    <div class="ch">
      <span class="b latin">Latin</span>
      <span class="lbl">English &bull; U+0000–00FF</span>
    </div>
    <p class="s xl">The Quick Brown Fox</p>
    <p class="s">jumps over the lazy dog.</p>
    <p class="s">Sphinx of black quartz — judge my vow!</p>
  </div>

  <!-- CJK -->
  <div class="card">
    <div class="ch">
      <span class="b cjk">CJK</span>
      <span class="lbl">中文 / 日本語 &bull; U+4E00–9FFF</span>
    </div>
    <p class="s xl">你好，世界！</p>
    <p class="s">中国有着悠久的历史与文化。</p>
    <p class="s">日本語：桜の花が咲いています。</p>
  </div>

  <!-- Arabic -->
  <div class="card" dir="rtl">
    <div class="ch">
      <span class="b arabic">Arabic</span>
      <span class="lbl">العربية &bull; U+0600–06FF</span>
    </div>
    <p class="s xl">مرحباً بالعالم</p>
    <p class="s">اللغة العربية لغة جميلة ذات تاريخ عريق.</p>
    <p class="s">بسم الله الرحمن الرحيم</p>
  </div>

  <!-- Cyrillic / Russian -->
  <div class="card">
    <div class="ch">
      <span class="b cyrillic">Cyrillic</span>
      <span class="lbl">Русский &bull; U+0400–04FF</span>
    </div>
    <p class="s xl">Привет, мир!</p>
    <p class="s">Россия — великая страна с богатой историей.</p>
    <p class="s">Все люди рождаются свободными и равными.</p>
  </div>

</div>

<h2>Generated WOFF2 Slices</h2>
<table>
  <thead>
    <tr>
      <th>Script</th>
      <th>File</th>
      <th style="text-align:right">Size</th>
      <th>Coverage</th>
    </tr>
  </thead>
  <tbody>{rows}
  </tbody>
  <tfoot>
    <tr>
      <td colspan="2">Total payload</td>
      <td class="num">{total_kb} KB</td>
      <td>5 scripts, fully local</td>
    </tr>
  </tfoot>
</table>

<footer>
  <p>বাঙলা (B angla) — built locally, served locally, embedded locally.</p>
  <p>Noto fonts &copy; Google (OFL-1.1 / Apache 2.0) &bull; SolaimanLipi &copy; Kazi Fahim Shahriyar (OFL-1.1)</p>
</footer>

</div>
</body>
</html>
"""


# ── main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    bar = "━" * 60
    print(f"\n{bar}")
    print("  বাঙলা (B angla) — Universal Font System Builder")
    print(f"{bar}\n")

    FONTS_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

    # ── Phase 1: Download ───────────────────────────────────────────────────
    print(f"▶ Phase 1 — Download source fonts  →  {CACHE_DIR}\n")
    needed: set = {info["source"] for info in SLICES.values()}
    cached: Dict[str, Optional[Path]] = {k: download_source(k, CACHE_DIR) for k in needed}
    print()

    # ── Phase 2: Slice + compress ────────────────────────────────────────────
    print(f"▶ Phase 2 — Slice & WOFF2 compress  →  {FONTS_DIR}\n")
    built: Dict[str, Path] = {}

    for script, info in SLICES.items():
        src_path = cached.get(info["source"])
        if not src_path:
            print(f"  ✗  {script:<12} — source unavailable, skipping\n")
            continue

        out_path = FONTS_DIR / f"B-angla-{script}.woff2"
        print(f"  ⟳  {script.upper():<12} {src_path.name}  →  {out_path.name}")

        ok = subset_to_woff2(src_path, out_path, info["unicodes"])
        if ok:
            kb = out_path.stat().st_size // 1024
            print(f"  ✓  {script.upper():<12} {kb:>5} KB  (WOFF2)")
            patch_name_table(out_path, script)
            built[script] = out_path
        else:
            print(f"  ✗  {script} — subset failed")
        print()

    if not built:
        print("✗  No slices produced — check internet connection and dependencies.")
        sys.exit(1)

    # ── Phase 3: CSS ─────────────────────────────────────────────────────────
    print(f"▶ Phase 3 — Generate CSS  →  {CSS_OUT}\n")
    CSS_OUT.write_text(build_css(built), encoding="utf-8")
    print(f"  ✓  {CSS_OUT.name}\n")

    # ── Phase 4: HTML ────────────────────────────────────────────────────────
    print(f"▶ Phase 4 — Generate HTML demo  →  {HTML_OUT}\n")
    HTML_OUT.write_text(build_html(built), encoding="utf-8")
    print(f"  ✓  {HTML_OUT.name}\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_kb = sum(p.stat().st_size for p in built.values()) // 1024
    print(f"{bar}")
    print("  Build complete!\n")
    for script, path in built.items():
        kb = path.stat().st_size // 1024
        print(f"  fonts/{path.name:<38}  {kb:>5} KB")
    print(f"  {'TOTAL':<44}  {total_kb:>5} KB")
    print()
    print(f"  bangla-local.css          — @font-face rules, local paths only")
    print(f"  index.html                — open in Chromium to verify")
    print(f"{bar}\n")


if __name__ == "__main__":
    main()
