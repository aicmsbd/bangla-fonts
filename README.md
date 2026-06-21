# বাঙলা (Bangla) — Universal Web Font System

**146 Scripts · 374 WOFF2 · Every Human Writing System Online**

The only web font covering virtually every script in one `font-family`.  
Browser fetches **only the script your page actually uses** via CSS `unicode-range`.

---

## Usage — 3 options (fastest → easiest)

### Option 1 — Load only what you need (fastest)

Pick the scripts your site uses. Each is a tiny separate file:

```html
<!-- Bengali website -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bengali.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">

<!-- Arabic + English -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-arabic.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">

<!-- Hindi website -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-devanagari.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">
```

### Option 2 — Load all 146 scripts (easiest, browser still lazy-loads)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/bangla-universal.css">
```

### Option 3 — CSS `@import` (development)

```css
@import url("https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bengali.css");
@import url("https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-arabic.css");
```

Then in your CSS:

```css
body {
  font-family: "Bangla", system-ui, sans-serif;
}
```

---

## Why separate CSS files?

| Approach | CSS loaded | Font files downloaded |
|----------|-----------|----------------------|
| `bangla-universal.css` | 126 KB | Only scripts present on page |
| `css/bangla-bengali.css` only | **2 KB** | Only Bengali weights used |
| `css/bangla-arabic.css` only | **2 KB** | Only Arabic weights used |

The `unicode-range` in every `@font-face` means the browser **never downloads a font file** unless a character from that range appears on the page. But loading fewer CSS files = less CSS parsing, faster first paint.

---

## All Per-Script CDN Links

Base URL: `https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/`

### South Asia

| Script | Language | CSS Link | Weights |
|--------|----------|----------|---------|
| Bengali | বাংলা | [bangla-bengali.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bengali.css) | 100–900 |
| Dogra | 𑠙𑠵𑠘𑠤 Jammu | [bangla-dogra.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-dogra.css) | 400 |
| Dives Akuru | Maldives historical | [bangla-dives-akuru.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-dives-akuru.css) | 400 |
| Toto | West Bengal/Bhutan | [bangla-toto.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-toto.css) | 400 |
| Devanagari | हिन्दी · मराठी · नेपाली | [bangla-devanagari.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-devanagari.css) | 100–900 |
| Tamil | தமிழ் | [bangla-tamil.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tamil.css) | 100–900 |
| Telugu | తెలుగు | [bangla-telugu.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-telugu.css) | 100–900 |
| Kannada | ಕನ್ನಡ | [bangla-kannada.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-kannada.css) | 100–900 |
| Malayalam | മലയാളം | [bangla-malayalam.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-malayalam.css) | 100–900 |
| Gujarati | ગુજરાતી | [bangla-gujarati.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-gujarati.css) | 100–900 |
| Gurmukhi | ਪੰਜਾਬੀ | [bangla-gurmukhi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-gurmukhi.css) | 100–900 |
| Odia | ଓଡ଼ିଆ | [bangla-odia.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-odia.css) | 400 700 |
| Sinhala | සිංහල | [bangla-sinhala.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-sinhala.css) | 100–900 |
| Meetei Mayek | Manipuri | [bangla-meetei-mayek.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-meetei-mayek.css) | 100–900 |
| Ol Chiki | Santali | [bangla-ol-chiki.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-ol-chiki.css) | 400 500 600 700 |
| Chakma | 𑄌𑄋𑄴𑄟 | [bangla-chakma.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-chakma.css) | 400 |
| Syloti Nagri | Sylheti | [bangla-syloti-nagri.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-syloti-nagri.css) | 400 |
| Limbu | Nepal/Sikkim | [bangla-limbu.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-limbu.css) | 400 |
| Lepcha | Sikkim | [bangla-lepcha.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-lepcha.css) | 400 |
| Newa | Nepal Lipi | [bangla-newa.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-newa.css) | 400 |
| Saurashtra | India | [bangla-saurashtra.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-saurashtra.css) | 400 |
| Kaithi | India | [bangla-kaithi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-kaithi.css) | 400 |
| Tirhuta | Maithili | [bangla-tirhuta.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tirhuta.css) | 400 |
| Sharada | Kashmir | [bangla-sharada.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-sharada.css) | 400 |
| Khojki | Sindh | [bangla-khojki.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-khojki.css) | 400 |
| Khudawadi | Sindhi | [bangla-khudawadi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-khudawadi.css) | 400 |
| Takri | North India | [bangla-takri.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-takri.css) | 400 |
| Multani | Pakistan | [bangla-multani.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-multani.css) | 400 |
| Modi | Marathi hist. | [bangla-modi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-modi.css) | 400 |
| Masaram Gondi | India | [bangla-masaram-gondi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-masaram-gondi.css) | 400 |
| Gunjala Gondi | India | [bangla-gunjala-gondi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-gunjala-gondi.css) | 400 700 |
| Mahajani | India | [bangla-mahajani.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-mahajani.css) | 400 |
| Sora Sompeng | India | [bangla-sora-sompeng.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-sora-sompeng.css) | 400 700 |
| Warang Citi | Ho/India | [bangla-warang-citi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-warang-citi.css) | 400 |
| Mro | Bangladesh | [bangla-mro.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-mro.css) | 400 |
| Wancho | Arunachal | [bangla-wancho.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-wancho.css) | 400 |

### Southeast Asia

| Script | Language | CSS Link | Weights |
|--------|----------|----------|---------|
| Thai | ภาษาไทย | [bangla-thai.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-thai.css) | 100–900 |
| Lao | ພາສາລາວ | [bangla-lao.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-lao.css) | 100–900 |
| Myanmar | မြန်မာ | [bangla-myanmar.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-myanmar.css) | 300 400 700 900 |
| Khmer | ភាសាខ្មែរ | [bangla-khmer.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-khmer.css) | 100–900 |
| Tai Tham | Lanna | [bangla-tai-tham.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tai-tham.css) | 400 700 |
| Tai Le | SE Asia | [bangla-tai-le.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tai-le.css) | 400 |
| New Tai Lue | SE Asia | [bangla-new-tai-lue.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-new-tai-lue.css) | 400 |
| Tai Viet | Vietnam | [bangla-tai-viet.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tai-viet.css) | 400 |
| Cham | Vietnam/Cambodia | [bangla-cham.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-cham.css) | 400 700 |
| Kayah Li | Myanmar/Thailand | [bangla-kayah-li.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-kayah-li.css) | 400 700 |
| Sundanese | Indonesia | [bangla-sundanese.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-sundanese.css) | 400 500 600 700 |
| Batak | Indonesia | [bangla-batak.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-batak.css) | 400 |
| Javanese | Indonesia | [bangla-javanese.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-javanese.css) | 400 |
| Buginese | Indonesia | [bangla-buginese.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-buginese.css) | 400 |
| Rejang | Indonesia | [bangla-rejang.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-rejang.css) | 400 |
| Balinese | ᬩᬲᬩᬮᬶ Bali | [bangla-balinese.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-balinese.css) | 300 400 700 |
| Makasar | South Sulawesi | [bangla-makasar.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-makasar.css) | 400 |
| Nyiakeng Puachue Hmong | SE Asia | [bangla-nyiakeng-hmong.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-nyiakeng-hmong.css) | 400 |
| Pahawh Hmong | SE Asia | [bangla-pahawh-hmong.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-pahawh-hmong.css) | 400 |
| Pau Cin Hau | Myanmar | [bangla-pau-cin-hau.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-pau-cin-hau.css) | 400 |

### Philippines

| Script | | CSS Link |
|--------|--|----------|
| Tagalog/Baybayin | | [bangla-tagalog.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tagalog.css) |
| Hanunoo | | [bangla-hanunoo.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-hanunoo.css) |
| Buhid | | [bangla-buhid.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-buhid.css) |
| Tagbanwa | | [bangla-tagbanwa.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tagbanwa.css) |

### East Asia

| Script | Language | CSS Link | Weights |
|--------|----------|----------|---------|
| CJK | Chinese · Japanese | [bangla-cjk.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-cjk.css) | 100 300 400 500 700 900 |
| Tibetan | བོད་སྐད། | [bangla-tibetan.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tibetan.css) | 400 700 |
| Mongolian | Монгол | [bangla-mongolian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-mongolian.css) | 400 |
| Yi | ꆈꌠ China | [bangla-yi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-yi.css) | 400 |
| Lisu | China/Myanmar | [bangla-lisu.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-lisu.css) | 400 700 |
| Miao/Pollard | China | [bangla-miao.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-miao.css) | 400 |
| Nushu | China (women's) | [bangla-nushu.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-nushu.css) | 400 |
| Zanabazar | Mongolia | [bangla-zanabazar.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-zanabazar.css) | 400 |
| Soyombo | Mongolia | [bangla-soyombo.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-soyombo.css) | 400 |
| Phags-Pa | Mongol Empire | [bangla-phags-pa.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-phags-pa.css) | 400 |
| Bhaiksuki | Buddhist | [bangla-bhaiksuki.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bhaiksuki.css) | 400 |
| Marchen | Tibet | [bangla-marchen.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-marchen.css) | 400 |
| Siddham | Buddhist mantra | [bangla-siddham.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-siddham.css) | 400 |

### Middle East / Africa

| Script | Language | CSS Link | Weights |
|--------|----------|----------|---------|
| Arabic | العربية | [bangla-arabic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-arabic.css) | 100–900 |
| Hebrew | עברית | [bangla-hebrew.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-hebrew.css) | 100 300 400 700 900 |
| Ethiopic | አማርኛ · Tigrinya | [bangla-ethiopic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-ethiopic.css) | 100–900 |
| Thaana | ދިވެހި Maldivian | [bangla-thaana.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-thaana.css) | 100–900 |
| Syriac | ܣܘܪܝܝܐ | [bangla-syriac.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-syriac.css) | 400 900 |
| N'Ko | ߒߞߏ West Africa | [bangla-nko.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-nko.css) | 400 |
| Adlam | Fulani West Africa | [bangla-adlam.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-adlam.css) | 400 700 |
| Bamum | Cameroon | [bangla-bamum.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bamum.css) | 400 |
| Tifinagh | Amazigh/Berber | [bangla-tifinagh.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tifinagh.css) | 400 |
| Vai | Liberia | [bangla-vai.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-vai.css) | 400 |
| Mende Kikakui | Sierra Leone | [bangla-mende-kikakui.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-mende-kikakui.css) | 400 |
| Osmanya | Somali | [bangla-osmanya.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-osmanya.css) | 400 |
| Hanifi Rohingya | Rohingya | [bangla-hanifi-rohingya.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-hanifi-rohingya.css) | 400 700 |
| Samaritan | Palestine | [bangla-samaritan.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-samaritan.css) | 400 |
| Mandaic | Iraq/Iran | [bangla-mandaic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-mandaic.css) | 400 |
| Yezidi | Yazidi (Iraq/Syria/Turkey) | [bangla-yezidi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-yezidi.css) | 400 |

### Europe

| Script | Language | CSS Link | Weights |
|--------|----------|----------|---------|
| Latin | English · All European | [bangla-latin.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css) | 100–900 |
| Latin Extended | Diacritics | [bangla-latin-ext.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin-ext.css) | 100–900 |
| Greek | Ελληνικά | [bangla-greek.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-greek.css) | 100–900 |
| Cyrillic | Русский · etc | [bangla-cyrillic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-cyrillic.css) | 100–900 |
| Armenian | Հայերեն | [bangla-armenian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-armenian.css) | 100–900 |
| Georgian | ქართული | [bangla-georgian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-georgian.css) | 100–900 |
| Glagolitic | Old Slavic | [bangla-glagolitic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-glagolitic.css) | 400 |
| Coptic | Egypt liturgy | [bangla-coptic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-coptic.css) | 400 |
| Gothic | Germanic hist. | [bangla-gothic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-gothic.css) | 400 |
| Elbasan | Albania hist. | [bangla-elbasan.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-elbasan.css) | 400 |
| Shavian | Shaw Alphabet | [bangla-shavian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-shavian.css) | 400 |
| Ogham | Ancient Irish | [bangla-ogham.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-ogham.css) | 400 |
| Runic | Germanic | [bangla-runic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-runic.css) | 400 |

### Americas

| Script | | CSS Link | Weights |
|--------|--|----------|---------|
| Canadian Aboriginal Syllabics | | [bangla-canadian-aboriginal.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-canadian-aboriginal.css) | 100–900 |
| Cherokee | ᎠᏍᎦᏯ | [bangla-cherokee.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-cherokee.css) | 100–900 |
| Deseret | Utah/USA hist. | [bangla-deseret.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-deseret.css) | 400 |
| Osage | USA | [bangla-osage.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-osage.css) | 400 |

### Historical & Ancient

| Script | | CSS Link |
|--------|--|----------|
| Imperial Aramaic | [bangla-imperial-aramaic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-imperial-aramaic.css) | |
| Nabataean | [bangla-nabataean.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-nabataean.css) | |
| Phoenician | [bangla-phoenician.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-phoenician.css) | |
| Old South Arabian | [bangla-old-south-arabian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-south-arabian.css) | |
| Old North Arabian | [bangla-old-north-arabian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-north-arabian.css) | |
| Old Hungarian (Rovas) | [bangla-old-hungarian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-hungarian.css) | |
| Old Italic | [bangla-old-italic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-italic.css) | |
| Old Turkic (Orkhon) | [bangla-old-turkic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-turkic.css) | |
| Sogdian | [bangla-sogdian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-sogdian.css) | |
| Old Sogdian | [bangla-old-sogdian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-sogdian.css) | |
| Inscriptional Pahlavi | [bangla-inscriptional-pahlavi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-inscriptional-pahlavi.css) | |
| Inscriptional Parthian | [bangla-inscriptional-parthian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-inscriptional-parthian.css) | |
| Psalter Pahlavi | [bangla-psalter-pahlavi.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-psalter-pahlavi.css) | |
| Manichaean | [bangla-manichaean.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-manichaean.css) | |
| Hatran | [bangla-hatran.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-hatran.css) | |
| Palmyrene | [bangla-palmyrene.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-palmyrene.css) | |
| Ugaritic | [bangla-ugaritic.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-ugaritic.css) | |
| Linear B Syllabary | [bangla-linear-b-syllabary.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-linear-b-syllabary.css) | |
| Lycian | [bangla-lycian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-lycian.css) | |
| Lydian | [bangla-lydian.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-lydian.css) | |
| Cypriot Syllabary | ancient Cyprus | [bangla-cypriote.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-cypriote.css) | 400 |
| Old Uyghur | Central Asia historical | [bangla-old-uyghur.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-old-uyghur.css) | 400 |
| Duployan (shorthand) | [bangla-duployan.css](https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-duployan.css) | |

---

## Common Combinations

```html
<!-- Bangladesh / Bengali websites -->
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bengali.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-arabic.css">

<!-- India (Hindi) -->
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-devanagari.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">

<!-- Pan-India (all 8 official scripts) -->
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-devanagari.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-bengali.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-tamil.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-telugu.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-kannada.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-malayalam.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-gujarati.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-gurmukhi.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">

<!-- Southeast Asia -->
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-thai.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-khmer.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-myanmar.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">

<!-- Middle East -->
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-arabic.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-hebrew.css">
<link href="https://cdn.jsdelivr.net/gh/aicmsbd/bangla-fonts@main/css/bangla-latin.css">
```

---

## Repository

**[https://github.com/aicmsbd/bangla-fonts](https://github.com/aicmsbd/bangla-fonts)**

```
fonts/weights/     374 WOFF2 files (one per script × weight)
css/               146 CSS files  (one per script)
bangla-universal.css  all scripts in one file
bangla-index.css      @import bundle for dev
```

Copyright © 2026 বাঙলা (bangla.it.com). All Rights Reserved.
