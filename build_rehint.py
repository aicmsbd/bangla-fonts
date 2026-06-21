#!/usr/bin/env python3
"""
Rebuild all WOFF2 files WITHOUT --no-hinting.
Source fonts are cached in .font_cache/ — no re-downloading.
Removing --no-hinting keeps TrueType hinting data for sharper ClearType rendering.
"""

import sys, subprocess, re
from pathlib import Path

for p in ["fonttools[woff]", "brotli"]:
    try: __import__(p.split("[")[0])
    except ImportError: subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", p])

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fontTools.ttLib import TTFont

ROOT   = Path(__file__).resolve().parent
CACHE  = ROOT / ".font_cache"
OUT    = ROOT / "fonts" / "weights"
CSS    = ROOT / "css"
FAMILY = "Bangla"

WEIGHT_NAMES = {
    100:"Thin", 200:"ExtraLight", 300:"Light", 400:"Regular",
    500:"Medium", 600:"SemiBold", 700:"Bold", 800:"ExtraBold", 900:"Black"
}

# Scripts that use NotoSans (no script suffix) for base Latin/Cyrillic/Greek
LATIN_BASE = {"latin", "latin-ext", "cyrillic", "greek", "math", "symbols", "ipa", "phonetic"}

# NotoSans{Pascal} prefix mapping for scripts with non-obvious pascal names
PASCAL_OVERRIDE = {
    "cjk":           None,          # handled separately
    "bopomofo":      None,          # handled separately
    "tibetan":       "SerifTibetan", # NotoSerifTibetan-{w}.ttf
    "balinese":      None,          # variable font
    "cypriote":      "SansCypriot", # NotoSansCypriot.ttf (no weight suffix)
    # 9 remaining scripts from Serif ZIP extracts
    "nyiakeng-hmong":  "SerifNPHmong",
    "old-uyghur":      "SerifOldUyghur",
    "dogra":           "SerifDogra",
    "dives-akuru":     "SerifDivesAkuru",
    "yezidi":          "SerifYezidi",
    "toto":            "SerifToto",
    "makasar":         "SerifMakasar",
    "batak":           None,  # noto-batak-Regular.ttf
    "thaana":          None,  # noto-thaana-{w}.ttf  (NOT NotoSansThaana)
}

CJK_WEIGHTS = {100:"Thin", 300:"Light", 400:"Regular", 500:"Medium", 700:"Bold", 900:"Black"}

# ── Read unicode-range from per-script CSS ──────────────────────────────────────
def get_ranges():
    ranges = {}
    for f in CSS.glob("bangla-*.css"):
        stem = f.stem
        if stem.split("-")[-1].isdigit():
            continue  # skip per-weight files
        script = stem[len("bangla-"):]
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'unicode-range:\s*([^\n;]+)', text)
        if m:
            ranges[script] = m.group(1).strip().rstrip(";").strip()
    return ranges

# ── Find cached source font ─────────────────────────────────────────────────────
def find_source(script, css_w):
    """Return (kind, Path) or None. kind = 'static' | 'var' | 'bin'"""
    wname = WEIGHT_NAMES.get(css_w, "Regular")

    # Balinese: variable font
    if script == "balinese":
        p = CACHE / "NotoSansBalinese_var.ttf"
        return ("var", p) if p.exists() else None

    # CJK
    if script == "cjk":
        wn = CJK_WEIGHTS.get(css_w)
        if wn:
            p = CACHE / f"NotoSansCJKsc-{wn}.otf"
            if p.exists():
                return ("static", p)
        return None

    # Bopomofo (Traditional Chinese)
    if script == "bopomofo":
        p = CACHE / f"NotoSansTC-{wname}.otf"
        return ("static", p) if p.exists() else None

    # Latin-base scripts (NotoSans-{Weight}.ttf with no script suffix)
    if script in LATIN_BASE:
        for ext in [".ttf", ".otf"]:
            p = CACHE / f"NotoSans-{wname}{ext}"
            if p.exists():
                return ("static", p)
        return None

    # Scripts with NotoSerif or special override
    if script in PASCAL_OVERRIDE:
        override = PASCAL_OVERRIDE[script]
        if override is None:
            pass  # fall through to noto- pattern below
        elif script == "cypriote":
            p = CACHE / "NotoSansCypriot.ttf"
            if p.exists() and css_w == 400:
                return ("static", p)
            return None
        else:
            # Try both plain and extracted_ prefix versions
            prefix = f"Noto{override}"
            for pre in ["", "extracted_"]:
                for ext in [".ttf", ".otf"]:
                    p = CACHE / f"{pre}{prefix}-{wname}{ext}"
                    if p.exists():
                        return ("static", p)
            # Serif scripts may only have Regular
            if css_w == 400:
                for pre in ["", "extracted_"]:
                    for ext in [".ttf", ".otf"]:
                        p = CACHE / f"{pre}{prefix}-Regular{ext}"
                        if p.exists():
                            return ("static", p)
            return None

    # Odia uses Oriya filename (legacy Noto naming)
    if script == "odia":
        for ext in [".ttf", ".otf"]:
            p = CACHE / f"NotoSansOriya-{wname}{ext}"
            if p.exists():
                return ("static", p)
        return None

    # Try NotoSans{Pascal}-{Weight}.ttf  (standard Noto pattern)
    pascal = "".join(w.title() for w in script.replace("-","_").split("_"))
    for ext in [".ttf", ".otf"]:
        p = CACHE / f"NotoSans{pascal}-{wname}{ext}"
        if p.exists():
            return ("static", p)

    # Try noto-{script}-{Weight}.ttf  (bulk-downloaded pattern)
    for sep in [script, script.replace("-", "_")]:
        p = CACHE / f"noto-{sep}-{wname}.ttf"
        if p.exists():
            return ("static", p)
        # single-weight scripts only have Regular in cache
        if css_w == 400:
            p = CACHE / f"noto-{sep}-Regular.ttf"
            if p.exists():
                return ("static", p)

    # noto-final-{script}-{weight}.bin (cached raw font data from prior build)
    for sep in [script, script.replace("-","_")]:
        p = CACHE / f"noto-final-{sep}-{wname}.bin"
        if p.exists():
            return ("bin", p)
        if css_w == 400:
            p = CACHE / f"noto-final-{sep}-Regular.bin"
            if p.exists():
                return ("bin", p)

    return None

# ── Subset WOFF2 without --no-hinting ──────────────────────────────────────────
def subset_woff2(src, dst, unicodes):
    if dst.exists():
        dst.unlink()
    cmd = [
        sys.executable, "-m", "fontTools.subset", str(src),
        f"--unicodes={unicodes}",
        "--layout-features=*",
        "--flavor=woff2",
        # NOTE: --no-hinting intentionally REMOVED
        "--desubroutinize",
        "--notdef-outline",
        f"--output-file={dst}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    ok = r.returncode == 0 and dst.exists() and dst.stat().st_size > 50
    if not ok:
        if dst.exists():
            dst.unlink()
        if r.stderr:
            print(f"\n    err: {r.stderr[:300]}", end="")
    return ok

# ── Patch name table ────────────────────────────────────────────────────────────
def patch_name(path, script, css_w):
    wname = WEIGHT_NAMES.get(css_w, "Regular")
    try:
        font = TTFont(str(path))
        tbl  = font["name"]
        for nid, val in {
            1: FAMILY, 2: wname,
            4: f"{FAMILY} {wname}",
            6: f"{FAMILY}-{script}-{css_w}",
            16: FAMILY, 17: wname,
        }.items():
            tbl.setName(val, nid, 3, 1, 0x0409)
        if "OS/2" in font:
            font["OS/2"].usWeightClass = css_w
        font.save(str(path))
        font.close()
    except Exception as e:
        print(f" [name-patch failed: {e}]", end="")

# ── Instantiate weight from variable font then subset ───────────────────────────
def instantiate_and_subset(var_path, css_w, unicodes, dst):
    from fontTools.varLib.instancer import instantiateVariableFont
    try:
        font = TTFont(str(var_path))
        if "fvar" not in font:
            font.close()
            return subset_woff2(var_path, dst, unicodes)
        static = instantiateVariableFont(font, {"wght": float(css_w)})
        tmp = CACHE / f"_tmp_static_{css_w}.ttf"
        static.save(str(tmp))
        font.close()
        ok = subset_woff2(tmp, dst, unicodes)
        tmp.unlink(missing_ok=True)
        return ok
    except Exception as e:
        print(f" [instantiate failed: {e}]", end="")
        return False

# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Rebuild WOFF2 — removing --no-hinting")
    print("  (sharper ClearType rendering on Windows)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    ranges  = get_ranges()
    pat     = re.compile(r'^Bangla-(.+)-(\d+)\.woff2$')
    woff2s  = sorted(OUT.glob("Bangla-*.woff2"))

    rebuilt = failed = no_src = no_range = 0
    no_src_list = []

    for wf in woff2s:
        m = pat.match(wf.name)
        if not m:
            continue
        script = m.group(1)
        css_w  = int(m.group(2))
        urange = ranges.get(script, "")

        if not urange:
            no_range += 1
            continue

        info = find_source(script, css_w)
        if not info:
            no_src += 1
            no_src_list.append(wf.name)
            continue

        kind, src = info
        if not src.exists():
            no_src += 1
            no_src_list.append(wf.name)
            continue

        print(f"  ↻  {wf.name:<40} ← {src.name}", end=" ", flush=True)

        if kind == "var":
            ok = instantiate_and_subset(src, css_w, urange, wf)
        elif kind == "bin":
            # .bin may be raw font data — write to tmp and subset
            tmp = CACHE / f"_tmp_bin_{script}_{css_w}.ttf"
            tmp.write_bytes(src.read_bytes())
            ok = subset_woff2(tmp, wf, urange)
            tmp.unlink(missing_ok=True)
        else:
            ok = subset_woff2(src, wf, urange)

        if ok:
            patch_name(wf, script, css_w)
            print(f"{wf.stat().st_size//1024} KB  ✓")
            rebuilt += 1
        else:
            print("FAIL")
            failed += 1

    print(f"\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Rebuilt:       {rebuilt}")
    print(f"  Failed:        {failed}")
    print(f"  No source:     {no_src} (existing kept as-is)")
    print(f"  No CSS range:  {no_range}")

    if no_src_list:
        print(f"\n  Skipped (no cached source):")
        for n in no_src_list[:20]:
            print(f"    {n}")
        if len(no_src_list) > 20:
            print(f"    ... and {len(no_src_list)-20} more")

    print(f"\n  Regenerating per-weight CSS...")
    subprocess.run([sys.executable, str(ROOT / "generate_per_weight_css.py")])
    print("\n  Done.")

if __name__ == "__main__":
    main()
