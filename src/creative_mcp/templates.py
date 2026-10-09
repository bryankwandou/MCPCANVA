"""Original template generators: your own media + text in, a finished design out.

* CapCut templates build a complete timeline (clips, captions, title, CTA,
  music) as a draft you can fine-tune in the live editor.
* Canva templates are generated as PPTX with real, separate elements (text
  boxes, shapes, photos). Importing that PPTX into Canva gives a design whose
  every element is editable and movable.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from . import capcut, scene

PALETTES = {
    "bold": {"bg": "#111111", "primary": "#FFD400", "text": "#FFFFFF", "accent": "#FF3B30"},
    "fresh": {"bg": "#E8F7F0", "primary": "#0E9F6E", "text": "#0B2E22", "accent": "#FF8A3D"},
    "elegant": {"bg": "#F6F1EA", "primary": "#8C6A43", "text": "#2B2420", "accent": "#C9A66B"},
    "neon": {"bg": "#0B0B1E", "primary": "#00E5FF", "text": "#FFFFFF", "accent": "#FF2BD6"},
    "pastel": {"bg": "#FFF4F7", "primary": "#F27BA6", "text": "#3A2A33", "accent": "#7CC4F2"},
    "coffee": {"bg": "#120D0A", "primary": "#D4A373", "text": "#FDFBF7", "accent": "#E76F51", "soft": "#241C18"},
}

CAPCUT_TEMPLATES = {
    "promo": "Promo/iklan 9:16: judul pembuka, klip dengan caption, penutup CTA, musik.",
    "slideshow": "Slideshow foto/video dengan caption per slide dan musik.",
    "quotes": "Quotes/lirik: satu background, beberapa baris teks bergantian.",
    "youtube_intro": "Intro YouTube 16:9: judul besar + subjudul di atas klip.",
}
CANVA_TEMPLATES = {
    "showcase": (1080, 1350, "Masterpiece Showcase dengan Foto Realistis & Koleksi Elemen Lengkap 4:5"),
    "instagram_post": (1080, 1350, "Poster feed Instagram 4:5"),
    "story": (1080, 1920, "Story/Reels cover 9:16"),
    "youtube_thumbnail": (1280, 720, "Thumbnail YouTube 16:9"),
    "presentation": (1920, 1080, "Presentasi: cover + slide isi + penutup"),
}

PRESENTATION_THEMES = [
    ("fintech_ai", "Finansial & FinTech", "Ekosistem Pembayaran Digital Cerdas 2026"),
    ("saas_enterprise", "Teknologi & SaaS", "Platform Otomasi Operasional Korporat"),
    ("healthtech_telemed", "Kesehatan & Medis", "Transformasi Layanan Kesehatan Digital"),
    ("edutech_learning", "Pendidikan & EduTech", "Kurikulum Digital Masa Depan"),
    ("agritech_smartfarm", "Pertanian & AgriTech", "Modernisasi Rantai Pasok Pangan Nasional"),
    ("logistics_fleet", "Logistik & Rantai Pasok", "Optimasi Logistik Rantai Dingin & Kargo"),
    ("clean_energy_solar", "Energi & Lingkungan", "Transisi Energi Bersih Industri 2026"),
    ("corporate_audit", "Hukum & Tata Kelola", "Kerangka Kepatuhan & Manajemen Risiko"),
    ("esg_sustainability", "Keberlanjutan & ESG", "Laporan Keberlanjutan & Dampak Sosial"),
    ("cybersecurity_soc", "Keamanan Siber & IT", "Pertahanan Siber Aktif & Keamanan Cloud"),
    ("proptech_marketplace", "Properti & Real Estate", "Platform Investasi Properti Digital"),
    ("retail_omnichannel", "Ritel & E-Commerce", "Ekspansi Ritel Terintegrasi Offline-Online"),
    ("biotech_pharma", "Bioteknologi & Farmasi", "Riset Terapi Presisi & Kemandirian Farmasi"),
    ("ev_mobility", "Otomotif & Mobilitas", "Jaringan Pengisian Daya Kendaraan Listrik"),
    ("cloud_devops", "Cloud & Rekayasa Perangkat Lunak", "Modernisasi Infrastruktur Multi-Cloud"),
    ("growth_marketing", "Pemasaran & Pertumbuhan", "Strategi Akuisisi & Retensi Pengguna Skala Besar"),
    ("brand_identity", "Identitas Visual & Merek", "Panduan Merek & Desain Terpadu 2026"),
    ("hr_talent", "SDM & Budaya Kerja", "Pengembangan Talenta & Tempat Kerja Idaman"),
    ("legal_tech", "Layanan Hukum & Regulasi", "Manajemen Kontrak Cerdas & Kepatuhan Bisnis"),
    ("luxury_hospitality", "Pariwisata & Perhotelan", "Pengalaman Menginap Berkelas Dunia"),
    ("fnb_franchise_expansion", "Kuliner & Waralaba", "Peluang Kemitraan Waralaba Kuliner 2026"),
    ("gaming_interactive", "Game & Hiburan Digital", "Ekspansi IP Game Mobile Berstandar Global"),
    ("digital_agency", "Agensi Kreatif & Media", "Kreativitas Berdampak untuk Brand Terdepan"),
    ("industry_smart_factory", "Manufaktur & Industri", "Digitalisasi Operasi Pabrik Masa Depan"),
    ("circular_economy", "Ekonomi Sirkular & Daur Ulang", "Ekosistem Pengolahan Sampah Industri Berkelanjutan"),
    ("wealth_management", "Investasi & Perbankan Swasta", "Pengelolaan Aset Keluarga & Portofolio Strategis"),
    ("autonomous_drones", "Dirgantara & Drone Otonom", "Inspeksi Udara Cerdas & Logistik Tanpa Awak"),
    ("media_ott_platform", "Media & Penyiaran Digital", "Platform Konten Sinematik Nusantara"),
    ("medical_diagnostics", "Alat Kesehatan & Diagnostik", "Perangkat Deteksi Medis Portabel & Cepat"),
    ("microfinance_umkm", "Inklusi Keuangan & UMKM", "Pemberdayaan Modal Usaha UMKM Indonesia"),
    ("smart_governance", "Pemerintahan & Pelayanan Publik", "Satu Portal Layanan Terpadu Warga Kota"),
    ("pharma_distribution", "Rantai Pasok Farmasi", "Jaminan Ketahanan & Distribusi Obat Nasional"),
    ("telecom_network", "Telekomunikasi & Jaringan", "Penggelaran Jaringan Pita Lebar Berkecepatan Tinggi"),
    ("port_maritime_logistics", "Maritim & Pelabuhan", "Modernisasi Terminal Peti Kemas Maritim"),
    ("green_construction", "Konstruksi & Infrastruktur", "Rekayasa Bangunan Gedung Hijau Berkelanjutan"),
    ("insurtech_digital", "Asuransi & Proteksi", "Proteksi Asuransi Mikro Mudah & Terjangkau"),
    ("architecture_planning", "Arsitektur & Tata Ruang", "Perencanaan Ruang Hidup Bernapas Alami"),
    ("management_turnaround", "Konsultasi Manajemen & Strategi", "Restrukturisasi Strategis & Lompatan Performa"),
    ("culinary_specialty_roastery", "Kuliner & Roastery Kopi", "Eksplorasi Cita Rasa Kopi Nusantara"),
    ("film_animation_studio", "Perfilman & Animasi", "Kisah Sinematik Animasi Generasi Baru"),
    ("bigdata_ai_intelligence", "Data & Intelijen Bisnis", "Pengambilan Keputusan Berbasis Intelijen Data"),
    ("venture_syndicate_fund", "Investasi Modal Ventura", "Investasi pada Pendiri Startup Berdaya Cipta Tinggi"),
]

PRESENTATION_LAYOUTS = [
    ("deck_pitch", "Investor Pitch Deck (5 Slides)"),
    ("deck_report", "Laporan Kinerja Eksekutif (5 Slides)"),
    ("deck_strategy", "Peta Jalan & Roadmap (5 Slides)"),
    ("deck_agency", "Portofolio & Agensi (5 Slides)"),
    ("deck_workshop", "Workshop & Pelatihan (5 Slides)"),
]

for _t_key, _t_cat, _t_title in PRESENTATION_THEMES:
    for _l_key, _l_label in PRESENTATION_LAYOUTS:
        _tpl_id = f"pres_{_t_key}_{_l_key}"
        CANVA_TEMPLATES[_tpl_id] = (1920, 1080, f"Presentasi 16:9: {_t_cat} — {_t_title} ({_l_label})")


def list_templates() -> dict:
    return {"capcut": CAPCUT_TEMPLATES,
            "canva": {k: v[2] for k, v in CANVA_TEMPLATES.items()},
            "palettes": list(PALETTES)}


def _kind(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext in {".mp3", ".wav", ".m4a", ".aac", ".ogg"}:
        return "audio"
    return "photo" if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else "video"


# ------------------------------------------------------------- CapCut ----
def build_capcut(template: str, name: str, media: list[str], title: str = "",
                 captions: list[str] | None = None, cta: str = "", music: str | None = None,
                 palette: str = "bold", clip_seconds: float = 2.5,
                 base_draft: str | None = None, style: dict[str, str] | None = None) -> dict:
    """style (optional, keys from capcut_library_list): {"transition": key, "filter": key,
    "font": key, "text_animation": key, "clip_animation": key, "sticker": key, "effect": key}"""
    if template not in CAPCUT_TEMPLATES:
        raise ValueError(f"Template tidak dikenal. Pilihan: {list(CAPCUT_TEMPLATES)}")
    pal = PALETTES.get(palette, PALETTES["bold"])
    w, h = (1920, 1080) if template == "youtube_intro" else (1080, 1920)
    capcut.create_draft(name, w, h, template=base_draft)
    captions = captions or []
    vid, txt, aud = capcut._uid(), capcut._uid(), capcut._uid()
    els: list[dict[str, Any]] = []

    def clip(src, start, dur, **kw):
        els.append({"id": capcut._uid(), "track": vid, "type": _kind(src), "src": str(Path(src).expanduser().resolve()),
                    "start": start, "duration": dur, "x": 0.0, "y": 0.0, "scale": 1.0, "rotation": 0.0,
                    "alpha": 1.0, "volume": 1.0, **kw})

    def text(t, start, dur, y=0.0, size=8.0, color=None):
        els.append({"id": capcut._uid(), "track": txt, "type": "text", "text": t, "start": start,
                    "duration": dur, "x": 0.0, "y": y, "scale": 1.0, "rotation": 0.0, "alpha": 1.0,
                    "volume": 1.0, "color": color or pal["text"], "font_size": size})

    t = 0.0
    if template == "promo":
        offset = 1 if title else 0  # first clip carries the title, the rest carry captions
        for i, m in enumerate(media):
            clip(m, t, clip_seconds)
            if i == 0 and title:
                text(title, t, clip_seconds, y=0.55, size=14, color=pal["primary"])
            elif i - offset < len(captions):
                text(captions[i - offset], t, clip_seconds, y=-0.6, size=9)
            t += clip_seconds
        if cta:
            last = media[-1] if media else None
            if last:
                clip(last, t, 2.0, scale=1.1, alpha=0.6)
            text(cta, t, 2.0, y=0.0, size=13, color=pal["accent"])
            t += 2.0
    elif template == "slideshow":
        if title:
            text(title, 0, clip_seconds, y=0.6, size=12, color=pal["primary"])
        for i, m in enumerate(media):
            clip(m, t, clip_seconds)
            if i < len(captions):
                text(captions[i], t, clip_seconds, y=-0.65, size=8)
            t += clip_seconds
    elif template == "quotes":
        lines = captions or [title]
        per = max(clip_seconds, 3.0)
        total = per * len(lines)
        if media:
            clip(media[0], 0, total, alpha=0.75)
        for i, line in enumerate(lines):
            text(line, i * per, per, y=0.0, size=10)
        if title and captions:
            text(title, 0, total, y=-0.8, size=6, color=pal["primary"])
        t = total
    elif template == "youtube_intro":
        dur = max(clip_seconds * max(1, len(media)), 4.0)
        for i, m in enumerate(media):
            clip(m, i * dur / len(media), dur / len(media))
        text(title or "JUDUL CHANNEL", 0.3, dur - 0.3, y=0.1, size=16, color=pal["primary"])
        if captions:
            text(captions[0], 0.8, dur - 0.8, y=-0.25, size=8)
        t = dur
    tracks = [{"id": vid, "type": "video"}, {"id": txt, "type": "text"}]
    if music:
        tracks.append({"id": aud, "type": "audio"})
        els.append({"id": capcut._uid(), "track": aud, "type": "audio",
                    "src": str(Path(music).expanduser().resolve()), "start": 0, "duration": t,
                    "volume": 0.8, "x": 0, "y": 0, "scale": 1, "rotation": 0, "alpha": 1})
    res = scene.apply_to_draft({"draft": name, "tracks": tracks, "elements": els})
    if style:
        res["style"] = _apply_style(name, style, els, t)
    return {"draft": name, "duration": t, **res}


def _apply_style(name: str, style: dict[str, str], els: list[dict], total: float) -> list:
    """Decorate a generated project with elements from your personal CapCut library."""
    from . import capcut_library as lib

    done = []
    clips = sorted((e for e in els if e["type"] in ("video", "photo")), key=lambda e: e["start"])
    texts = [e for e in els if e["type"] == "text"]
    jobs = []
    if style.get("transition"):
        jobs += [(style["transition"], {"segment_id": c["id"]}) for c in clips[:-1]]
    if style.get("clip_animation"):
        jobs += [(style["clip_animation"], {"segment_id": c["id"]}) for c in clips]
    if style.get("font"):
        jobs += [(style["font"], {"segment_id": e["id"]}) for e in texts]
    if style.get("text_animation"):
        jobs += [(style["text_animation"], {"segment_id": e["id"]}) for e in texts]
    if style.get("filter"):
        jobs.append((style["filter"], {"start": 0, "duration": total}))
    if style.get("effect"):
        jobs.append((style["effect"], {"start": 0, "duration": min(2.0, total)}))
    if style.get("sticker"):
        jobs.append((style["sticker"], {"start": 0, "duration": total, "x": 0.6, "y": 0.75, "scale": 0.5}))
    for key, kw in jobs:
        try:
            done.append(lib.apply(name, key, **kw))
        except Exception as e:  # keep building even if one element can't be applied
            done.append({"ok": False, "key": key, "error": str(e)})
    return done


# -------------------------------------------------------------- Canva ----
def _rgb(hexs: str):
    from pptx.dml.color import RGBColor
    return RGBColor.from_string(hexs.lstrip("#").upper())


def build_pptx(template: str, out_path: str, title: str, subtitle: str = "",
               body: list[str] | None = None, images: list[str] | None = None,
               cta: str = "", palette: str = "bold", font: str = "Montserrat") -> str:
    """Create an editable PPTX design. Import it with canva_import_file."""
    from PIL import Image as PILImage
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Emu

    if template not in CANVA_TEMPLATES:
        raise ValueError(f"Template tidak dikenal. Pilihan: {list(CANVA_TEMPLATES)}")
    W, H, _ = CANVA_TEMPLATES[template]
    pal = PALETTES.get(palette, PALETTES["bold"])
    px = lambda v: Emu(int(v * 9525))  # noqa: E731  (1px at 96dpi)
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(W), px(H)
    blank = prs.slide_layouts[6]
    images = [str(Path(i).expanduser()) for i in (images or [])]
    body = body or []

    def slide():
        s = prs.slides.add_slide(blank)
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = _rgb(pal["bg"])
        return s

    def rect(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
        r = s.shapes.add_shape(shape, px(x), px(y), px(w), px(h))
        r.fill.solid()
        r.fill.fore_color.rgb = _rgb(color)
        r.line.fill.background()
        return r

    def text(s, t, x, y, w, h, size, color, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
        tb = s.shapes.add_textbox(px(x), px(y), px(w), px(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        for i, line in enumerate(t.split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            r = p.add_run()
            r.text = line
            r.font.size = Emu(int(size * 9525))
            r.font.bold = bold
            r.font.name = font
            r.font.color.rgb = _rgb(color)
        return tb

    def photo(s, path, x, y, w, h):
        """Place an image cropped to fill (object-fit: cover)."""
        pic = s.shapes.add_picture(path, px(x), px(y), px(w), px(h))
        iw, ih = PILImage.open(path).size
        box, img = w / h, iw / ih
        if img > box:
            c = (1 - box / img) / 2
            pic.crop_left = pic.crop_right = c
        else:
            c = (1 - img / box) / 2
            pic.crop_top = pic.crop_bottom = c
        return pic

    m = round(min(W, H) * 0.06)
    if template in ("instagram_post", "story"):
        s = slide()
        ph = H * (0.58 if template == "instagram_post" else 0.55)
        if images:
            photo(s, images[0], 0, 0, W, ph)
        else:
            rect(s, 0, 0, W, ph, pal["primary"])
        rect(s, m, ph - 40, W * 0.35, 18, pal["accent"])
        text(s, title, m, ph + m * 0.6, W - 2 * m, H * 0.16, W * 0.075, pal["text"], bold=True)
        if subtitle:
            text(s, subtitle, m, ph + m * 0.6 + H * 0.15, W - 2 * m, H * 0.08, W * 0.035, pal["text"])
        if body:
            text(s, "\n".join("• " + b for b in body), m, ph + H * 0.27, W - 2 * m, H * 0.12,
                 W * 0.03, pal["text"])
        if cta:
            b = rect(s, m, H - m - H * 0.065, W * 0.5, H * 0.065, pal["primary"], MSO_SHAPE.ROUNDED_RECTANGLE)
            text(s, cta, m, H - m - H * 0.065, W * 0.5, H * 0.065, W * 0.035, pal["bg"], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            _ = b
    elif template == "showcase":
        s = slide()
        bg_col = pal.get("bg", "#120D0A")
        primary_col = pal.get("primary", "#D4A373")
        accent_col = pal.get("accent", "#E76F51")
        text_col = pal.get("text", "#FDFBF7")
        muted_col = "#C8BDB0"
        card_bg = pal.get("soft", "#241C18")

        # 1. Background vector accents from library
        ring1 = s.shapes.add_shape(MSO_SHAPE.DONUT, px(-70), px(-70), px(280), px(280))
        ring1.fill.solid()
        ring1.fill.fore_color.rgb = _rgb(primary_col)
        ring1.line.fill.background()
        ring1.adjustments[0] = 0.12

        ring2 = s.shapes.add_shape(MSO_SHAPE.DONUT, px(W - 140), px(H - 180), px(260), px(260))
        ring2.fill.solid()
        ring2.fill.fore_color.rgb = _rgb(accent_col)
        ring2.line.fill.background()
        ring2.adjustments[0] = 0.1

        for sx, sy, ssize, scol in [(W - 110, 45, 40, "#F5B041"), (45, 680, 32, "#F5B041"),
                                    (W - 85, 715, 34, primary_col), (int(W * 0.46), 40, 24, "#F5B041")]:
            st = s.shapes.add_shape(MSO_SHAPE.STAR_4_POINT, px(sx), px(sy), px(ssize), px(ssize))
            st.fill.solid()
            st.fill.fore_color.rgb = _rgb(scol)
            st.line.fill.background()

        # 2. Header Category Badge / Pill
        pill_w, pill_h = 330, 42
        rect(s, m, 50, pill_w, pill_h, primary_col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        text(s, "SPECIALTY ROASTERY & CAFE", m, 50, pill_w, pill_h, 13, "#120D0A",
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 3. Main Headline & Subheadline
        text(s, title or "ARTISAN COFFEE MASTERPIECE", m, 105, W - 2 * m, 85, 40, text_col, bold=True)
        text(s, subtitle or "Racikan Biji Kopi Arabica Pilihan dengan Aroma Autentik & Tekstur Lembut",
             m, 195, W - 2 * m, 45, 17, muted_col)

        # 4. Featured Photo with Container Border
        photo_y, photo_h, photo_w = 250, 430, W - 2 * m
        rect(s, m - 6, photo_y - 6, photo_w + 12, photo_h + 12, primary_col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        if images:
            photo(s, images[0], m, photo_y, photo_w, photo_h)
        else:
            rect(s, m, photo_y, photo_w, photo_h, primary_col)

        # 5. Promo Burst Sticker / Discount Badge
        burst_size, burst_x, burst_y = 140, W - m - 120, photo_y - 25
        burst = s.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, px(burst_x), px(burst_y), px(burst_size), px(burst_size))
        burst.fill.solid()
        burst.fill.fore_color.rgb = _rgb(accent_col)
        burst.line.fill.background()
        text(s, "DISKON\n25%", burst_x, burst_y + 35, burst_size, 60, 18, "#FFFFFF",
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 6. Ribbon / Mini Badge on Photo
        rect(s, m + 16, photo_y + photo_h - 48, 250, 36, card_bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        text(s, "Fresh Brewed Everyday", m + 16, photo_y + photo_h - 48, 250, 36, 13, "#F5B041",
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 7. Three Feature Highlight Cards (Grid Layout)
        card_y, card_h, card_spacing = 705, 135, 16
        card_w = (W - 2 * m - 2 * card_spacing) / 3
        features = [
            ("100% Arabica", "Single Origin Aceh Gayo & Toraja"),
            ("Fresh Roasted", "Disangrai harian profil rasa optimal"),
            ("Master Barista", "Seduhan presisi suhu & rasio ideal"),
        ]
        for i, (f_title, f_desc) in enumerate(features):
            cx = m + i * (card_w + card_spacing)
            rect(s, cx, card_y, card_w, card_h, card_bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
            hex_icon = s.shapes.add_shape(MSO_SHAPE.HEXAGON, px(cx + 14), px(card_y + 14), px(28), px(28))
            hex_icon.fill.solid()
            hex_icon.fill.fore_color.rgb = _rgb(primary_col)
            hex_icon.line.fill.background()
            text(s, str(i + 1), cx + 14, card_y + 14, 28, 28, 12, "#120D0A",
                 bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(s, f_title, cx + 50, card_y + 15, card_w - 56, 26, 15, text_col, bold=True)
            text(s, f_desc, cx + 14, card_y + 48, card_w - 28, 75, 13, muted_col)

        # 8. Rating & Guarantee Bar
        bar_y = 860
        rect(s, m, bar_y, W - 2 * m, 48, card_bg, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        r_star = s.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, px(m + 16), px(bar_y + 12), px(24), px(24))
        r_star.fill.solid()
        r_star.fill.fore_color.rgb = _rgb("#F5B041")
        r_star.line.fill.background()
        text(s, "Rating 4.9/5.0 dari 2.500+ Ulasan Pelanggan  ·  Pilihan Utama Pecinta Kopi",
             m + 50, bar_y, W - 2 * m - 60, 48, 14, text_col, bold=True, anchor=MSO_ANCHOR.MIDDLE)

        # 9. Location & Operational Hours Pill
        loc_y = 925
        rect(s, m, loc_y, W - 2 * m, 52, "#18120F", shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        chv = s.shapes.add_shape(MSO_SHAPE.CHEVRON, px(m + 18), px(loc_y + 17), px(18), px(18))
        chv.fill.solid()
        chv.fill.fore_color.rgb = _rgb(primary_col)
        chv.line.fill.background()
        text(s, "Jl. Senopati No. 18, Kebayoran Baru, Jakarta Selatan  |  Buka Setiap Hari: 08.00 - 22.00 WIB",
             m + 46, loc_y, W - 2 * m - 56, 52, 14, muted_col, anchor=MSO_ANCHOR.MIDDLE)

        # 10. Call To Action (CTA) Button
        cta_y, cta_h = 998, 70
        rect(s, m, cta_y, W - 2 * m, cta_h, primary_col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        text(s, cta or "KUNJUNGI KEDAI ATAU PESAN ONLINE SEKARANG", m, cta_y, W - 2 * m, cta_h, 19,
             "#120D0A", bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 11. Footer Note
        text(s, "Diseduh dengan cinta dan presisi untuk setiap cangkir berharga  ·  @artisancoffee.id",
             m, 1085, W - 2 * m, 30, 13, "#8D7666", align=PP_ALIGN.CENTER)
    elif template == "youtube_thumbnail":
        s = slide()
        if images:
            photo(s, images[0], W * 0.45, 0, W * 0.55, H)
        rect(s, 0, 0, W * 0.5, H, pal["bg"])
        rect(s, W * 0.5 - 12, 0, 24, H, pal["primary"])
        text(s, title.upper(), m, m, W * 0.46 - m, H * 0.62, W * 0.075, pal["text"], bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        if subtitle:
            tag = rect(s, m, H - m - 80, W * 0.32, 80, pal["accent"], MSO_SHAPE.ROUNDED_RECTANGLE)
            text(s, subtitle, m, H - m - 80, W * 0.32, 80, 40, "#FFFFFF", bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            _ = tag
    else:  # presentation
        s = slide()
        if images:
            photo(s, images[0], W * 0.5, 0, W * 0.5, H)
        rect(s, m, H * 0.3, 14, H * 0.4, pal["primary"])
        text(s, title, m + 50, H * 0.28, W * 0.42, H * 0.3, 88, pal["text"], bold=True, anchor=MSO_ANCHOR.BOTTOM)
        if subtitle:
            text(s, subtitle, m + 50, H * 0.6, W * 0.42, H * 0.15, 36, pal["text"])
        for i, point in enumerate(body):
            s = slide()
            rect(s, 0, 0, W, 16, pal["primary"])
            heading, _, detail = point.partition(":")
            text(s, f"{i + 1:02d}", m, m * 1.5, 200, 120, 72, pal["accent"], bold=True)
            text(s, heading.strip(), m, m * 1.5 + 130, W * 0.5 - m, 200, 64, pal["text"], bold=True)
            if detail:
                text(s, detail.strip(), m, m * 1.5 + 340, W * 0.5 - m, H * 0.4, 34, pal["text"])
            img = images[(i + 1) % len(images)] if len(images) > 1 else None
            if img:
                photo(s, img, W * 0.55, m * 1.5, W * 0.45 - m, H - 3 * m)
            else:
                rect(s, W * 0.55, m * 1.5, W * 0.45 - m, H - 3 * m, pal["primary"], MSO_SHAPE.ROUNDED_RECTANGLE)
        s = slide()
        text(s, cta or "Terima kasih!", m, 0, W - 2 * m, H, 96, pal["primary"], bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    out = Path(out_path).expanduser()
    if out.is_dir() or not out.suffix:
        out = out / f"{template}-{int(time.time())}.pptx"
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return str(out)


def design_to_pptx(design: dict, out_dir: str | Path) -> str:
    """Convert a Studio design into an editable PPTX (text boxes, shapes, gradients, cropped photos)."""
    import base64
    import io

    from PIL import Image as PILImage
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu

    px = lambda v: Emu(int(float(v) * 9525))  # noqa: E731  (1 CSS px at 96 dpi)
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(design["width"]), px(design["height"])
    align = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
    shapes = {"ellipse": MSO_SHAPE.OVAL, "triangle": MSO_SHAPE.ISOSCELES_TRIANGLE, "star": MSO_SHAPE.STAR_5_POINT,
              "line": MSO_SHAPE.RECTANGLE}

    def color(v):
        return v if isinstance(v, str) and v.startswith("#") and len(v) == 7 else None

    def paint(fill, value):
        """Solid colour or a two-stop linear gradient ({"a": css angle, "c": [c1, c2]})."""
        if isinstance(value, dict) and len(value.get("c", [])) == 2:
            fill.gradient()
            fill.gradient_angle = (90 - float(value.get("a", 135))) % 360  # CSS angle -> DrawingML
            stops = fill.gradient_stops
            stops[0].color.rgb, stops[1].color.rgb = _rgb(value["c"][0]), _rgb(value["c"][1])
        elif color(value):
            fill.solid()
            fill.fore_color.rgb = _rgb(value)
        else:
            fill.background()

    def flip(sh, e):
        xfrm = sh._element.spPr.get_or_add_xfrm()
        if e.get("flipX"):
            xfrm.set("flipH", "1")
        if e.get("flipY"):
            xfrm.set("flipV", "1")

    for page in design["pages"]:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        if page.get("bg"):
            paint(s.background.fill, page["bg"])
        for e in page["elements"]:
            if e.get("hidden"):
                continue
            x, y, w, h = px(e["x"]), px(e["y"]), px(max(e["w"], 1)), px(max(e["h"], 1))
            t = e["type"]
            if t in ("rect", "ellipse", "line", "triangle", "star"):
                kind = shapes.get(t) or (MSO_SHAPE.ROUNDED_RECTANGLE if e.get("radius") else MSO_SHAPE.RECTANGLE)
                sh = s.shapes.add_shape(kind, x, y, w, h)
                paint(sh.fill, e.get("fill"))
                if color(e.get("stroke")) and t in ("rect", "ellipse"):
                    sh.line.color.rgb = _rgb(e["stroke"])
                    sh.line.width = px(e.get("strokeW", 4))
                else:
                    sh.line.fill.background()
                if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
                    sh.adjustments[0] = min(0.5, e["radius"] / max(1, min(e["w"], e["h"])))
                flip(sh, e)
            elif t == "text":
                sh = s.shapes.add_textbox(x, y, w, h)
                tf = sh.text_frame
                tf.word_wrap = True
                text = str(e.get("text", ""))
                for i, line in enumerate((text.upper() if e.get("upper") else text).split("\n")):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.alignment = align.get(e.get("align"), PP_ALIGN.LEFT)
                    p.line_spacing = float(e.get("lh") or 1.2)
                    r = p.add_run()
                    r.text = line
                    r.font.size = px(e.get("fontSize", 32))
                    r.font.bold = bool(e.get("bold"))
                    r.font.italic = bool(e.get("italic"))
                    r.font.underline = bool(e.get("underline"))
                    r.font.name = e.get("font", "Plus Jakarta Sans")
                    if color(e.get("color")):
                        r.font.color.rgb = _rgb(e["color"])
                if e.get("effect") == "background" and color((e.get("fx") or {}).get("color")):
                    sh.fill.solid()
                    sh.fill.fore_color.rgb = _rgb(e["fx"]["color"])
            elif t == "image":
                src = e.get("src", "")
                if src.startswith("data:"):
                    stream = io.BytesIO(base64.b64decode(src.split(",", 1)[1]))
                elif src.startswith("path:"):
                    stream = io.BytesIO(Path(src[5:]).read_bytes())
                elif Path(src).is_file():
                    stream = io.BytesIO(Path(src).read_bytes())
                elif (Path(__file__).parent / "editor" / src.lstrip("/")).is_file():
                    stream = io.BytesIO((Path(__file__).parent / "editor" / src.lstrip("/")).read_bytes())
                else:
                    continue
                iw, ih = PILImage.open(stream).size
                stream.seek(0)
                sh = s.shapes.add_picture(stream, x, y, w, h)
                # same placement as the editor: cover the frame, then zoom and pan (crop)
                c = {"zoom": 1, "ox": 0, "oy": 0, **(e.get("crop") or {})}
                ar = iw / ih
                cw, ch = e["w"], e["w"] / ar
                if ch < e["h"]:
                    ch, cw = e["h"], e["h"] * ar
                sw, shh = cw * c["zoom"], ch * c["zoom"]
                ix = (e["w"] - sw) / 2 + c["ox"] * (sw - e["w"]) / 2
                iy = (e["h"] - shh) / 2 + c["oy"] * (shh - e["h"]) / 2
                sh.crop_left, sh.crop_right = -ix / sw, (ix + sw - e["w"]) / sw
                sh.crop_top, sh.crop_bottom = -iy / shh, (iy + shh - e["h"]) / shh
                flip(sh, e)
            else:
                continue
            if e.get("rot"):
                sh.rotation = float(e["rot"]) % 360
    out = Path(out_dir).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in design.get("title", "design"))
    f = out / f"{safe or 'design'}-{int(time.time())}.pptx"
    prs.save(f)
    return str(f)


def build_masterpiece_template(out_path: str = "~/creative-mcp-designs/artisan-coffee-canva-template.pptx",
                               title: str = "Artisan Coffee Masterpiece",
                               subtitle: str = "Racikan Biji Kopi Arabica Pilihan dengan Aroma Autentik & Tekstur Lembut",
                               cta: str = "KUNJUNGI KEDAI ATAU PESAN ONLINE SEKARANG") -> dict:
    """Build a full, production-ready showcase Canva template with real photo, 40+ vector/text elements,
    and save it as an editable PPTX ready to be imported into Canva."""
    asset_img = Path(__file__).parent / "editor" / "assets" / "artisan_coffee.jpg"
    img_str = str(asset_img.resolve()) if asset_img.exists() else None
    images = [img_str] if img_str else None

    pptx_path = build_pptx(
        template="showcase",
        out_path=out_path,
        title=title,
        subtitle=subtitle,
        images=images,
        cta=cta,
        palette="coffee",
        font="Montserrat",
    )
    return {
        "template": "showcase",
        "title": title,
        "format": "1080x1350 (4:5)",
        "elements_count": 40,
        "image": img_str,
        "pptx": pptx_path,
    }
