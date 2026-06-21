#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
বাঙলা (Bangla) — All Weights Builder
======================================
Downloads every weight variant (Thin → Black) for all 5 scripts,
slices to unicode-range WOFF2 chunks, patches name tables,
and generates a comprehensive bangla-weights.css + demo HTML.

Outputs:
  fonts/weights/Bangla-<script>-<weight>.woff2   (45 files)
  bangla-weights.css
  index.html  (updated demo with weight switcher)

Usage:
  python build_bangla_weights.py
"""

from __future__ import annotations

import sys, subprocess, os, io
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── dep bootstrap ──────────────────────────────────────────────────────────────
def _ensure():
    missing = []
    try: import fontTools          # noqa
    except ImportError: missing.append("fonttools[woff]")
    try: import brotli             # noqa
    except ImportError: missing.append("brotli")
    if missing:
        print(f"[setup] pip install {' '.join(missing)} …")
        subprocess.check_call([sys.executable,"-m","pip","install","--quiet"]+missing)

_ensure()

if hasattr(sys.stdout,"reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fontTools.ttLib import TTFont   # noqa: E402
import requests                      # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).resolve().parent
CACHE     = ROOT / ".font_cache"
OUT       = ROOT / "fonts" / "weights"
CSS_OUT   = ROOT / "bangla-weights.css"
HTML_OUT  = ROOT / "index.html"

FAMILY    = "Bangla"
PS_BASE   = "Bangla"
HDRS      = {"User-Agent": "Mozilla/5.0 BanglaWeightBuilder/1.0"}

# ── weight definitions ─────────────────────────────────────────────────────────
#  (css_weight, weight_name_in_filename, display_name)
STANDARD_WEIGHTS: List[Tuple[int,str,str]] = [
    (100, "Thin",       "Thin"),
    (200, "ExtraLight", "ExtraLight"),
    (300, "Light",      "Light"),
    (400, "Regular",    "Regular"),
    (500, "Medium",     "Medium"),
    (600, "SemiBold",   "SemiBold"),
    (700, "Bold",       "Bold"),
    (800, "ExtraBold",  "ExtraBold"),
    (900, "Black",      "Black"),
]

# CJK uses different weight names and only 6 standard CSS weights
CJK_WEIGHTS: List[Tuple[int,str,str]] = [
    (100, "Thin",    "Thin"),
    (300, "Light",   "Light"),
    (400, "Regular", "Regular"),
    (500, "Medium",  "Medium"),
    (700, "Bold",    "Bold"),
    (900, "Black",   "Black"),
]

# ── source font URLs per weight ───────────────────────────────────────────────
def noto_url(family_dir: str, family_file: str, wname: str) -> List[str]:
    base = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf"
    cdn  = "https://cdn.jsdelivr.net/gh/googlefonts/noto-fonts@main/hinted/ttf"
    return [
        f"{base}/{family_dir}/{family_file}-{wname}.ttf",
        f"{cdn}/{family_dir}/{family_file}-{wname}.ttf",
    ]

def cjk_url(wname: str) -> List[str]:
    base = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese"
    cdn  = "https://cdn.jsdelivr.net/gh/googlefonts/noto-cjk@main/Sans/OTF/SimplifiedChinese"
    return [
        f"{base}/NotoSansCJKsc-{wname}.otf",
        f"{cdn}/NotoSansCJKsc-{wname}.otf",
    ]

SOURCES: Dict[str, Dict] = {
    "noto-sans": {
        "weights": STANDARD_WEIGHTS,
        "file": lambda wname: f"NotoSans-{wname}.ttf",
        "urls": lambda wname: noto_url("NotoSans", "NotoSans", wname),
        "slices": ["latin","cyrillic"],
    },
    "noto-sans-bengali": {
        "weights": STANDARD_WEIGHTS,
        "file": lambda wname: f"NotoSansBengali-{wname}.ttf",
        "urls": lambda wname: noto_url("NotoSansBengali","NotoSansBengali", wname),
        "slices": ["bengali"],
    },
    "noto-sans-arabic": {
        "weights": STANDARD_WEIGHTS,
        "file": lambda wname: f"NotoSansArabic-{wname}.ttf",
        "urls": lambda wname: noto_url("NotoSansArabic","NotoSansArabic", wname),
        "slices": ["arabic"],
    },
    "noto-sans-cjk": {
        "weights": CJK_WEIGHTS,
        "file": lambda wname: f"NotoSansCJKsc-{wname}.otf",
        "urls": lambda wname: cjk_url(wname),
        "slices": ["cjk"],
    },
}

# ── unicode slices ─────────────────────────────────────────────────────────────
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
        "note": "Latin + extended",
    },
    "bengali": {
        "unicodes":  "U+0980-09FF,U+200C,U+200D,U+25CC",
        "css_range": "U+0980-09FF, U+200C, U+200D, U+25CC",
        "note": "Bengali + conjunct control",
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
        "note": "Arabic + Presentation Forms",
    },
    "cyrillic": {
        "unicodes":  "U+0400-04FF,U+0500-052F,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F",
        "css_range": "U+0400-04FF, U+0500-052F, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F",
        "note": "Cyrillic + Extended",
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
        "note": "CJK Ideographs + Kana",
    },
}

WEIGHT_NAMES = {
    100: "Thin", 200: "ExtraLight", 300: "Light",
    400: "Regular", 500: "Medium", 600: "SemiBold",
    700: "Bold", 800: "ExtraBold", 900: "Black",
}

# ── download ───────────────────────────────────────────────────────────────────
def _download_one(urls: List[str], dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 10_000:
        return dest
    for url in urls:
        try:
            r = requests.get(url, stream=True, timeout=300, headers=HDRS)
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            got   = 0
            with open(dest, "wb") as fh:
                for chunk in r.iter_content(65536):
                    if chunk:
                        fh.write(chunk)
                        got += len(chunk)
            print(f"    ✓ {dest.name}  {got//1024} KB")
            return dest
        except Exception as exc:
            print(f"    ✗ {url[:60]}…  {exc}")
            dest.unlink(missing_ok=True)
    raise RuntimeError(f"All URLs failed for {dest.name}")

def download_all_weights(cache: Path) -> Dict[Tuple[str,int], Optional[Path]]:
    """Download every source font weight, return mapping (source_key, css_weight) → Path."""
    cache.mkdir(exist_ok=True)
    tasks = []
    for src_key, src in SOURCES.items():
        for css_w, wname, _ in src["weights"]:
            filename = src["file"](wname)
            dest     = cache / filename
            urls     = src["urls"](wname)
            tasks.append((src_key, css_w, urls, dest))

    results: Dict[Tuple[str,int], Optional[Path]] = {}
    print(f"  Parallel download of {len(tasks)} weight files …\n")
    with ThreadPoolExecutor(max_workers=4) as ex:
        fmap = {ex.submit(_download_one, urls, dest): (src_key, css_w)
                for src_key, css_w, urls, dest in tasks}
        for fut in as_completed(fmap):
            key = fmap[fut]
            try:
                results[key] = fut.result()
            except Exception as e:
                print(f"    ✗ {key}: {e}")
                results[key] = None
    return results

# ── subset ─────────────────────────────────────────────────────────────────────
def subset_woff2(src: Path, dst: Path, unicodes: str) -> bool:
    if dst.exists() and dst.stat().st_size > 50:
        return True
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        str(src),
        f"--unicodes={unicodes}",
        "--layout-features=*",
        "--flavor=woff2",
        "--no-hinting",
        "--desubroutinize",
        "--notdef-outline",
        f"--output-file={dst}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"      subset err: {(r.stderr or r.stdout)[:200]}")
    return r.returncode == 0 and dst.exists() and dst.stat().st_size > 50

def patch_name(path: Path, script: str, css_weight: int) -> None:
    wname    = WEIGHT_NAMES.get(css_weight, "Regular")
    is_bold  = css_weight >= 700
    try:
        font = TTFont(str(path))
        tbl  = font["name"]
        patches = {
            1:  FAMILY,
            2:  wname,
            3:  f"{PS_BASE}:{script}:{css_weight}",
            4:  f"{FAMILY} {wname}",
            6:  f"{PS_BASE}-{script.capitalize()}-{wname}",
            16: FAMILY,
            17: wname,
        }
        # Update OS/2 weight class
        if "OS/2" in font:
            font["OS/2"].usWeightClass = css_weight
        # Update head macStyle bold flag
        if "head" in font:
            if is_bold:
                font["head"].macStyle |= 1
            else:
                font["head"].macStyle &= ~1
        for nid, val in patches.items():
            tbl.setName(val, nid, 3, 1, 0x0409)
            tbl.setName(val, nid, 1, 0, 0)
        font.save(str(path))
        font.close()
    except Exception as e:
        print(f"      [warn] name patch: {e}")

# ── CSS generator ──────────────────────────────────────────────────────────────
def build_css(built: Dict[Tuple[str,int], Path]) -> str:
    """
    built: {(script, css_weight): woff2_path}
    """
    lines = [
        "/*",
        " * বাঙলা (Bangla) — All Weights Font System",
        " * font-family: \"Bangla\" — 9 weights × 5 scripts",
        " * Branding © 2026 Bangla. No external network requests.",
        " */",
        "",
    ]

    # Group by script then weight
    by_script: Dict[str, Dict[int, Path]] = {}
    for (script, w), path in built.items():
        by_script.setdefault(script, {})[w] = path

    for script in ["latin","bengali","arabic","cyrillic","cjk"]:
        if script not in by_script:
            continue
        info = SLICES[script]
        lines.append(f"/* {'━'*55} */")
        lines.append(f"/* {script.upper()} — {info['note']} */")
        lines.append(f"/* {'━'*55} */")
        lines.append("")

        for css_w in sorted(by_script[script]):
            path  = by_script[script][css_w]
            wname = WEIGHT_NAMES.get(css_w,"Regular")
            rel   = f"./fonts/weights/{path.name}"
            lines += [
                f"/* {wname} ({css_w}) */",
                "@font-face {",
                f'  font-family: "{FAMILY}";',
                "  font-style: normal;",
                f"  font-weight: {css_w};",
                "  font-display: swap;",
                f'  src: url("{rel}") format("woff2");',
                f"  unicode-range: {info['css_range']};",
                "}",
                "",
            ]
    return "\n".join(lines)

# ── HTML demo ──────────────────────────────────────────────────────────────────
def build_html(built: Dict[Tuple[str,int], Path]) -> str:
    # Collect available weights
    all_weights = sorted({w for _, w in built})
    weight_opts = "".join(
        f'<option value="{w}"{"selected" if w==400 else ""}>{WEIGHT_NAMES.get(w,w)} ({w})</option>'
        for w in all_weights
    )

    # Stats table rows
    by_script: Dict[str, Dict[int, Path]] = {}
    for (script, w), path in built.items():
        by_script.setdefault(script, {})[w] = path

    rows = ""
    for script in ["latin","bengali","arabic","cyrillic","cjk"]:
        if script not in by_script:
            continue
        total_kb = sum(p.stat().st_size for p in by_script[script].values()) // 1024
        n = len(by_script[script])
        rows += (
            f"<tr>"
            f"<td><span class='b {script}'>{script.upper()}</span></td>"
            f"<td>{n} weights</td>"
            f"<td class='num'>{total_kb} KB</td>"
            f"<td>{SLICES[script]['note']}</td>"
            f"</tr>\n"
        )

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>বাঙলা (Bangla) — All Weights</title>
<link rel="stylesheet" href="bangla-weights.css">
<style>
:root{{
  --bg:#0d0f1a;--s:#151827;--bdr:#242742;--t:#e4e6f0;--m:#7b88a0;
  --acc:#6c63ff;--red:#ff6b6b;--grn:#4caf89;--yel:#ffa726;--cya:#26c6da;--pur:#ab47bc;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"{FAMILY}",system-ui,sans-serif;background:var(--bg);color:var(--t);line-height:1.8;padding:2rem 1rem}}
.wrap{{max-width:960px;margin:0 auto}}

header{{text-align:center;padding:3rem 1rem 2rem;border-bottom:1px solid var(--bdr);margin-bottom:2.5rem}}
h1{{font-size:clamp(2rem,5vw,3.5rem);background:linear-gradient(135deg,var(--acc),var(--red));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.4rem}}
.sub{{color:var(--m);font-size:.95rem}}

/* Weight selector */
.ctrl{{display:flex;flex-wrap:wrap;align-items:center;gap:1rem;
       background:var(--s);border:1px solid var(--bdr);border-radius:10px;
       padding:1rem 1.4rem;margin-bottom:2.5rem}}
.ctrl label{{color:var(--m);font-size:.85rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em}}
.ctrl select{{background:#0d0f1a;border:1px solid var(--bdr);border-radius:6px;color:var(--t);
              padding:.35rem .7rem;font-family:"{FAMILY}",sans-serif;font-size:.9rem;cursor:pointer}}
.ctrl select:focus{{outline:2px solid var(--acc);border-color:transparent}}
.wt-label{{font-size:2rem;font-weight:700;color:var(--acc)}}

/* Weight scale strip */
.scale{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:2.5rem}}
.scale-chip{{background:var(--s);border:1px solid var(--bdr);border-radius:8px;
             padding:.6rem 1rem;flex:1;min-width:80px;text-align:center;cursor:pointer;
             transition:border-color .2s,background .2s}}
.scale-chip:hover,.scale-chip.active{{background:#1e2135;border-color:var(--acc)}}
.scale-chip .wnum{{font-size:.7rem;color:var(--m);letter-spacing:.05em}}
.scale-chip .wsample{{font-size:1.1rem;line-height:1.4}}

h2{{font-size:1.2rem;margin:0 0 1rem;color:var(--t)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:1.3rem;margin-bottom:2.5rem}}
.card{{background:var(--s);border:1px solid var(--bdr);border-radius:12px;padding:1.5rem;
       transition:border-color .2s}}
.card:hover{{border-color:var(--acc)}}
.ch{{display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem}}
[dir=rtl] .ch{{flex-direction:row-reverse}}
.b{{padding:.15rem .5rem;border-radius:5px;font-size:.68rem;font-weight:700;letter-spacing:.07em;
    text-transform:uppercase;color:#fff}}
.b.latin{{background:var(--acc)}}.b.bengali{{background:var(--red)}}
.b.arabic{{background:var(--yel);color:#111}}.b.cyrillic{{background:var(--cya);color:#111}}
.b.cjk{{background:var(--pur)}}
.lbl{{font-size:.78rem;color:var(--m)}}
.s{{font-size:1.4rem;line-height:2;margin:.1rem 0}}
.xl{{font-size:1.9rem}}
.pills{{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.6rem}}
.pill{{background:#1e2135;border:1px solid var(--bdr);border-radius:7px;padding:.18rem .55rem;font-size:1.1rem}}

table{{width:100%;border-collapse:collapse;margin-bottom:2.5rem;font-size:.85rem}}
th{{text-align:left;padding:.65rem 1rem;background:var(--s);border-bottom:2px solid var(--bdr);
    color:var(--m);text-transform:uppercase;letter-spacing:.06em;font-size:.68rem;font-weight:700}}
td{{padding:.55rem 1rem;border-bottom:1px solid var(--bdr);color:var(--t)}}
tr:hover td{{background:#131524}}
.num{{text-align:right;font-family:"Courier New",monospace}}
tfoot td{{border-top:2px solid var(--bdr);border-bottom:none;font-weight:700;color:var(--grn)}}
code{{font-family:"Courier New",monospace;font-size:.82em;color:var(--acc)}}
footer{{text-align:center;padding:2rem;color:var(--m);font-size:.8rem;border-top:1px solid var(--bdr)}}
footer p+p{{margin-top:.35rem}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>বাঙলা &mdash; Bangla</h1>
  <p class="sub">All Weights &bull; Thin–Black &bull; 5 Scripts &bull; Zero-CDN</p>
</header>

<!-- Weight selector -->
<div class="ctrl">
  <label>Font Weight</label>
  <select id="wsel" onchange="setWeight(this.value)">
    {weight_opts}
  </select>
  <span class="wt-label" id="wlabel">Regular 400</span>
</div>

<!-- Weight scale -->
<h2>Weight Scale</h2>
<div class="scale" id="wscale">
  {"".join(
    f'<div class="scale-chip{"active" if w==400 else ""}" onclick="setWeight({w})" data-w="{w}">'
    f'<div class="wnum">{WEIGHT_NAMES.get(w,w)}<br>{w}</div>'
    f'<div class="wsample" style="font-weight:{w}">Aa বাংলা</div>'
    f'</div>'
    for w in all_weights
  )}
</div>

<!-- Script samples -->
<h2>Script Samples</h2>
<div class="grid" id="samples">

  <div class="card">
    <div class="ch"><span class="b bengali">Bengali</span><span class="lbl">বাংলা · U+0980–09FF</span></div>
    <p class="s xl sample">যুক্তাক্ষর পরীক্ষা</p>
    <p class="s sample">কক্সবাজার · স্বাস্থ্য</p>
    <p class="s sample">বাংলাদেশ — প্রকৃতির রূপ অপরূপ।</p>
    <div class="pills">
      <span class="pill">ক্ষ</span><span class="pill">ত্র</span><span class="pill">জ্ঞ</span>
      <span class="pill">স্ব</span><span class="pill">ন্ত</span><span class="pill">ষ্ঠ</span>
    </div>
  </div>

  <div class="card">
    <div class="ch"><span class="b latin">Latin</span><span class="lbl">English · U+0000–00FF</span></div>
    <p class="s xl sample">The Quick Brown Fox</p>
    <p class="s sample">jumps over the lazy dog.</p>
    <p class="s sample">Sphinx of black quartz — judge my vow!</p>
  </div>

  <div class="card">
    <div class="ch"><span class="b cjk">CJK</span><span class="lbl">中文 / 日本語 · U+4E00–9FFF</span></div>
    <p class="s xl sample">你好，世界！</p>
    <p class="s sample">中国有着悠久的历史与文化。</p>
    <p class="s sample">日本語：桜の花が咲いています。</p>
  </div>

  <div class="card" dir="rtl">
    <div class="ch"><span class="b arabic">Arabic</span><span class="lbl">العربية · U+0600–06FF</span></div>
    <p class="s xl sample">مرحباً بالعالم</p>
    <p class="s sample">اللغة العربية لغة جميلة ذات تاريخ عريق.</p>
  </div>

  <div class="card">
    <div class="ch"><span class="b cyrillic">Cyrillic</span><span class="lbl">Русский · U+0400–04FF</span></div>
    <p class="s xl sample">Привет, мир!</p>
    <p class="s sample">Россия — великая страна с богатой историей.</p>
  </div>

</div>

<!-- Stats -->
<h2>Generated WOFF2 Files</h2>
<table>
  <thead><tr><th>Script</th><th>Weights</th><th style="text-align:right">Total Size</th><th>Coverage</th></tr></thead>
  <tbody>{rows}</tbody>
  <tfoot>
    <tr>
      <td colspan="2">Grand total</td>
      <td class="num">{sum(p.stat().st_size for p in built.values())//1024} KB</td>
      <td>5 scripts × all weights</td>
    </tr>
  </tfoot>
</table>

<footer>
  <p>বাঙলা (Bangla) — All Weights Edition &bull; Zero-CDN &bull; Chromium pak-ready</p>
  <p>Noto fonts © Google (OFL-1.1 / Apache 2.0) &bull; Bangla branding © 2026</p>
</footer>

</div>

<script>
const WN = {{100:"Thin",200:"ExtraLight",300:"Light",400:"Regular",500:"Medium",600:"SemiBold",700:"Bold",800:"ExtraBold",900:"Black"}};

function setWeight(w) {{
  w = parseInt(w);
  document.documentElement.style.setProperty('--cur-weight', w);
  document.querySelectorAll('.sample').forEach(el => el.style.fontWeight = w);
  document.querySelector('#wsel').value = w;
  document.querySelector('#wlabel').textContent = (WN[w]||'') + ' ' + w;
  document.querySelectorAll('.scale-chip').forEach(c => {{
    c.classList.toggle('active', parseInt(c.dataset.w) === w);
  }});
}}

// Apply initial weight
setWeight(400);
</script>
</body>
</html>
"""

# ── main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    bar = "━" * 64
    print(f"\n{bar}")
    print("  বাঙলা (Bangla) — All Weights Builder")
    print(f"{bar}\n")

    CACHE.mkdir(exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    # ── Phase 1: Download all weight source fonts ────────────────────────────
    print(f"▶ Phase 1 — Download source fonts  →  {CACHE}\n")
    downloaded = download_all_weights(CACHE)
    n_ok  = sum(1 for v in downloaded.values() if v)
    n_tot = len(downloaded)
    print(f"\n  Downloaded: {n_ok}/{n_tot} files\n")

    # ── Phase 2: Slice each (source, weight) → (script, weight) ─────────────
    print(f"▶ Phase 2 — Slice & WOFF2 compress  →  {OUT}\n")
    built: Dict[Tuple[str,int], Path] = {}

    # Build list of (script, css_weight, src_path) jobs
    jobs = []
    for src_key, src in SOURCES.items():
        for css_w, wname, _ in src["weights"]:
            src_path = downloaded.get((src_key, css_w))
            if not src_path:
                continue
            for script in src["slices"]:
                jobs.append((script, css_w, src_path))

    # Subset all jobs (parallel)
    def _slice_job(args):
        script, css_w, src_path = args
        out_name = f"Bangla-{script}-{css_w}.woff2"
        dst      = OUT / out_name
        ok       = subset_woff2(src_path, dst, SLICES[script]["unicodes"])
        if ok:
            patch_name(dst, script, css_w)
        return script, css_w, dst, ok

    print(f"  Slicing {len(jobs)} combinations in parallel …\n")
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        futs = {ex.submit(_slice_job, j): j for j in jobs}
        for fut in as_completed(futs):
            try:
                script, css_w, dst, ok = fut.result()
                if ok:
                    kb = dst.stat().st_size // 1024
                    wname = WEIGHT_NAMES.get(css_w,"?")
                    print(f"  ✓  {script:<12} {wname:<12} ({css_w})  →  {kb:>6} KB")
                    built[(script, css_w)] = dst
                else:
                    print(f"  ✗  {script} {css_w}")
            except Exception as e:
                print(f"  ✗  {e}")

    if not built:
        print("\n✗  No files built. Check downloads.")
        sys.exit(1)

    # ── Phase 3: CSS ─────────────────────────────────────────────────────────
    print(f"\n▶ Phase 3 — Generate CSS  →  {CSS_OUT}\n")
    CSS_OUT.write_text(build_css(built), encoding="utf-8")
    print(f"  ✓  {CSS_OUT.name}")

    # ── Phase 4: HTML ────────────────────────────────────────────────────────
    print(f"\n▶ Phase 4 — Generate demo  →  {HTML_OUT}\n")
    HTML_OUT.write_text(build_html(built), encoding="utf-8")
    print(f"  ✓  {HTML_OUT.name}")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_kb  = sum(p.stat().st_size for p in built.values()) // 1024
    scripts   = sorted({s for s,_ in built})
    weights   = sorted({w for _,w in built})
    n_files   = len(built)

    print(f"\n{bar}")
    print(f"  Build complete!\n")
    print(f"  Scripts  : {', '.join(scripts)}")
    print(f"  Weights  : {', '.join(str(w) for w in weights)}")
    print(f"  Files    : {n_files} WOFF2 slices")
    print(f"  Total    : {total_kb} KB  ({total_kb//1024} MB)")
    print(f"\n  fonts/weights/  — all WOFF2 slices")
    print(f"  bangla-weights.css  — 9 weights × 5 scripts @font-face")
    print(f"  index.html          — interactive weight demo")
    print(f"{bar}\n")


if __name__ == "__main__":
    main()
