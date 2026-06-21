import os
import sys
import glob
from fontTools.ttLib import TTFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ডিরেক্টরি পাথ সেট করুন (আপনার ফোল্ডার অনুযায়ী)
input_dir = r"C:\Users\Z\Desktop\fonts\fonts\weights"
output_dir = r"C:\Users\Z\Desktop\fonts\fonts\all_formats"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# আপনার নিজস্ব কপিরাইট এবং ব্র্যান্ড মেটাডেটা
COPYRIGHT_TEXT = "Copyright (c) 2026 বাঙলা (bangla.it.com). All Rights Reserved."
MANUFACTURER = "বাঙলা"
DESIGNER = "বাঙলা"
VENDOR_URL = "https://bangla.it.com/"
LICENSE_INFO = "Proprietary License - All rights reserved by bangla.it.com"

def _encode(text: str, unicode_record: bool) -> bytes:
    """Unicode record → utf-16-be; mac record → ascii-safe fallback (mac-roman)."""
    if unicode_record:
        return text.encode('utf-16-be')
    # mac-roman cannot represent Bengali — use ASCII-only fallback for mac records
    ascii_text = text.encode('ascii', errors='replace').decode('ascii')
    return ascii_text.encode('mac-roman', errors='replace')

def update_metadata(font):
    """ফন্টের নাম এবং কপিরাইট মেটাডেটা আপডেট করার ফাংশন"""
    name_table = font['name']

    updates = {
        0:  COPYRIGHT_TEXT,
        8:  MANUFACTURER,
        9:  DESIGNER,
        11: VENDOR_URL,
        13: LICENSE_INFO,
    }

    # nameID: 0=Copyright, 8=Manufacturer, 9=Designer, 11=Vendor URL, 13=License Description
    for record in name_table.names:
        if record.nameID in updates:
            record.string = _encode(updates[record.nameID], record.isUnicode())

def process_fonts():
    woff2_files = glob.glob(os.path.join(input_dir, "*.woff2"))

    print(f"Total WOFF2 files found: {len(woff2_files)}\n")

    for woff2_path in sorted(woff2_files):
        filename = os.path.basename(woff2_path)
        base_name = os.path.splitext(filename)[0]

        try:
            print(f"Processing: {base_name}...")

            # Load WOFF2 font
            font = TTFont(woff2_path)

            # Update Copyright and Metadata
            update_metadata(font)

            # Save as TTF
            ttf_path = os.path.join(output_dir, f"{base_name}.ttf")
            font.flavor = None # flavor None means TTF/OTF
            font.save(ttf_path)
            print(f"  ✓ Saved TTF")

            # Save as WOFF
            woff_path = os.path.join(output_dir, f"{base_name}.woff")
            font.flavor = 'woff'
            font.save(woff_path)
            print(f"  ✓ Saved WOFF")

            # Save back to WOFF2 (with updated copyright)
            new_woff2_path = os.path.join(output_dir, f"{base_name}.woff2")
            font.flavor = 'woff2'
            font.save(new_woff2_path)
            print(f"  ✓ Saved WOFF2 (Updated Copyright)")

            # Verification Step
            verify_file(ttf_path)
            verify_file(woff_path)
            verify_file(new_woff2_path)

        except Exception as e:
            print(f"  ✗ Error processing {filename}: {str(e)}")

def verify_file(filepath):
    """চেক করবে ফাইলটি সফলভাবে তৈরি হয়েছে কিনা এবং সাইজ > 0 কিনা"""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        pass # All good
    else:
        print(f"  [WARNING] Verification failed for: {filepath}")

if __name__ == "__main__":
    print("Starting conversion and copyright update for 'বাঙলা'...\n")
    process_fonts()
    print("\nProcess Completed. Check 'all_formats' directory.")
