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
    ("corporate_audit", "Tata Kelola & Kepatuhan Korporat", "Kerangka Kepatuhan & Manajemen Risiko"),
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
    ("legal_tech", "Administrasi Kontrak & Kepatuhan Bisnis", "Manajemen Kontrak Cerdas & Efisiensi Operasional"),
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
    pal = palette if isinstance(palette, dict) else PALETTES.get(palette, PALETTES["bold"])
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
        card_bg = pal.get("soft", "#1E1814")
        border_col = "#3A2E26"

        # 1. Hairline header divider and architectural kicker
        line_top = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(45), px(W - 2 * m), px(1))
        line_top.fill.solid()
        line_top.fill.fore_color.rgb = _rgb(border_col)
        line_top.line.fill.background()

        text(s, "SPECIALTY ROASTERY & ESPRESSO BAR", m, 55, (W - 2 * m) * 0.6, 28, 12, primary_col, bold=True)
        text(s, "EST. 2026 // EDITION 01", W - m - 200, 55, 200, 28, 11, "#9E8E80", align=PP_ALIGN.RIGHT)

        # 2. Main Headline & Subheadline
        text(s, title or "ARTISAN COFFEE MASTERPIECE", m, 98, W - 2 * m, 95, 42, text_col, bold=True)
        text(s, subtitle or "Racikan Biji Kopi Arabica Pilihan dengan Aroma Autentik & Tekstur Lembut",
             m, 198, W - 2 * m, 45, 16, muted_col)

        # 3. Featured Photo with Clean Hairline Border
        photo_y, photo_h, photo_w = 250, 440, W - 2 * m
        if images:
            photo(s, images[0], m, photo_y, photo_w, photo_h)
        else:
            rect(s, m, photo_y, photo_w, photo_h, primary_col)
        photo_frame = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(photo_y), px(photo_w), px(photo_h))
        photo_frame.fill.background()
        photo_frame.line.color.rgb = _rgb(border_col)
        photo_frame.line.width = px(1)

        # 4. Three Feature Highlight Cards (Grid Layout with Hairline Rules)
        card_y, card_h, card_spacing = 715, 130, 16
        card_w = (W - 2 * m - 2 * card_spacing) / 3
        features = [
            ("01", "100% Arabica", "Single Origin Aceh Gayo & Toraja Kalosi terkurasi."),
            ("02", "Fresh Roasted", "Disangrai harian berkalibrasi kurva suhu presisi."),
            ("03", "Master Barista", "Ekstraksi rasio ideal 1:2 bertekanan stabil 9 bar."),
        ]
        for i, (num, f_title, f_desc) in enumerate(features):
            cx = m + i * (card_w + card_spacing)
            card_box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(cx), px(card_y), px(card_w), px(card_h))
            card_box.fill.solid()
            card_box.fill.fore_color.rgb = _rgb(card_bg)
            card_box.line.color.rgb = _rgb(border_col)
            card_box.line.width = px(1)

            text(s, num, cx + 16, card_y + 14, 32, 28, 14, primary_col, bold=True)
            text(s, f_title, cx + 52, card_y + 14, card_w - 68, 28, 15, text_col, bold=True)
            div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(cx + 16), px(card_y + 46), px(card_w - 32), px(1))
            div.fill.solid()
            div.fill.fore_color.rgb = _rgb(border_col)
            div.line.fill.background()
            text(s, f_desc, cx + 16, card_y + 54, card_w - 32, 65, 12, muted_col)

        # 5. Quality Benchmark Bar
        bar_y = 865
        bar_box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(bar_y), px(W - 2 * m), px(44))
        bar_box.fill.solid()
        bar_box.fill.fore_color.rgb = _rgb(card_bg)
        bar_box.line.color.rgb = _rgb(border_col)
        bar_box.line.width = px(1)
        text(s, "SKOR MUTU 94.6 SCA  ·  2.500+ ULASAN KEPUASAN PELANGGAN  ·  SERAHAN TANGAN TERTINGGI",
             m, bar_y + 12, W - 2 * m, 24, 12, primary_col, bold=True, align=PP_ALIGN.CENTER)

        # 6. Location & Operational Hours
        loc_y = 925
        loc_box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(loc_y), px(W - 2 * m), px(48))
        loc_box.fill.solid()
        loc_box.fill.fore_color.rgb = _rgb("#16110D")
        loc_box.line.color.rgb = _rgb(border_col)
        loc_box.line.width = px(1)
        text(s, "JL. SENOPATI NO. 18, JAKARTA SELATAN  |  BUKA SETIAP HARI: 08.00 - 22.00 WIB",
             m, loc_y + 14, W - 2 * m, 24, 12, muted_col, align=PP_ALIGN.CENTER)

        # 7. Call To Action (CTA) Button
        cta_y, cta_h = 992, 68
        rect(s, m, cta_y, W - 2 * m, cta_h, primary_col)
        text(s, cta or "KUNJUNGI KEDAI ATAU PESAN ONLINE SEKARANG", m, cta_y, W - 2 * m, cta_h, 17,
             "#120D0A", bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 8. Footer Note
        text(s, "Diseduh dengan dedikasi dan presisi untuk setiap cangkir bernilai  ·  @artisancoffee.id",
             m, 1075, W - 2 * m, 28, 12, "#8D7666", align=PP_ALIGN.CENTER)
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
    else:  # presentation (1920x1080 16:9, 5-Slide Swiss Editorial Executive Deck)
        dark = str(pal.get("bg", "#0F172A")).startswith("#0") or str(pal.get("bg", "#0F172A")).startswith("#1")
        ink = "#F8FAFC" if dark else "#0F172A"
        sub_ink = "#94A3B8" if dark else "#475569"
        border_col = "#334155" if dark else "#CBD5E1"
        primary_col = pal.get("primary", "#38BDF8")
        accent_col = pal.get("accent", "#818CF8")

        # Slide 1: High-End Asymmetric Editorial Split with Photo
        s1 = slide()
        line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(m * 0.7), px(W - 2 * m), px(2))
        line1.fill.solid()
        line1.fill.fore_color.rgb = _rgb(border_col)
        line1.line.fill.background()

        text(s1, "VENTURE PITCH DECK // 2026", m, m * 0.7 + 16, 400, 30, 15, primary_col, bold=True)
        text(s1, "CONFIDENTIAL & PROPRIETARY", W - m - 350, m * 0.7 + 16, 350, 30, 14, sub_ink, align=PP_ALIGN.RIGHT)

        split_w = (W - 2 * m) * 0.52
        photo_x = m + split_w + 30
        photo_w = W - photo_x - m
        photo_y = H * 0.22
        photo_h = H * 0.66

        # Place the executive hero photo on the right half
        hero_img = None
        if images and len(images) > 0 and Path(images[0]).exists():
            hero_img = str(images[0])
        else:
            cand_list = [
                Path(__file__).parent / "editor" / "assets" / "executive_hero.jpg",
                Path(__file__).parent / "editor" / "assets" / "fintech_hero.jpg",
                Path(__file__).parent / "editor" / "assets" / "tech_hero.jpg",
                Path(__file__).parent / "editor" / "assets" / "skyscraper_hero.jpg",
                Path(__file__).parent / "editor" / "assets" / "artisan_coffee.jpg",
            ]
            for img_cand in cand_list:
                if img_cand.exists():
                    hero_img = str(img_cand)
                    break
        if hero_img:
            photo(s1, hero_img, photo_x, photo_y, photo_w, photo_h)
            p_frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(photo_x), px(photo_y), px(photo_w), px(photo_h))
            p_frame.fill.background()
            p_frame.line.color.rgb = _rgb(border_col)
            p_frame.line.width = px(1)

            badge_h = 44
            badge_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(photo_x + 20), px(photo_y + photo_h - badge_h - 20), px(260), px(badge_h))
            badge_box.fill.solid()
            badge_box.fill.fore_color.rgb = _rgb("#0A0E17")
            badge_box.line.color.rgb = _rgb(primary_col)
            badge_box.line.width = px(1)
            text(s1, "SERI A // Rp 50 MILIAR", photo_x + 20, photo_y + photo_h - badge_h - 12, 260, 30, 13, primary_col, bold=True, align=PP_ALIGN.CENTER)

        # Left Column Copy
        text(s1, title or "EKOSISTEM DIGITAL NUSANTARA 2026", m, H * 0.25, split_w - 20, 200, 48, ink, bold=True)

        vline = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(H * 0.55), px(4), px(110))
        vline.fill.solid()
        vline.fill.fore_color.rgb = _rgb(primary_col)
        vline.line.fill.background()

        text(s1, subtitle or "Arsitektur Platform Skalabel dengan Keamanan Mutakhir dan Efisiensi Operasional Teruji",
             m + 24, H * 0.55, split_w - 44, 110, 20, sub_ink)

        line1_b = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(H - m - 60), px(split_w), px(1))
        line1_b.fill.solid()
        line1_b.fill.fore_color.rgb = _rgb(border_col)
        line1_b.line.fill.background()

        text(s1, "Direktorat Strategi & Kemitraan Korporat · 2026", m, H - m - 40, split_w - 220, 30, 15, sub_ink)
        rect(s1, m + split_w - 200, H - m - 50, 200, 44, primary_col)
        text(s1, "PITCH PROPOSAL", m + split_w - 200, H - m - 42, 200, 30, 13, "#000000" if not dark else "#FFFFFF",
             bold=True, align=PP_ALIGN.CENTER)

        # Slide 2: Market Problem (2x2 Grid with high-contrast tinted card backgrounds)
        s2 = slide()
        line2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(m * 0.7), px(W - 2 * m), px(1))
        line2.fill.solid()
        line2.fill.fore_color.rgb = _rgb(border_col)
        line2.line.fill.background()

        text(s2, "01 / MARKET PAIN POINTS", m, m * 0.7 + 16, 400, 30, 14, accent_col, bold=True)
        text(s2, "Inefisiensi Struktural yang Dihadapi Industri", m, H * 0.16, W * 0.75, 70, 38, ink, bold=True)
        text(s2, "Kesenjangan tajam antara tuntutan kecepatan pasar dan infrastruktur warisan yang berjalan saat ini.",
             m, H * 0.24, W * 0.7, 45, 17, sub_ink)

        card_bg = "#162032" if dark else "#F1F5F9"
        problems = [
            ("01", "Fragmentasi Sistem Warisan", "Integrasi lintas kanal terhambat arsitektur silo yang lambat dan rentan inkonsistensi data."),
            ("02", "Beban Operasional Tinggi", "Proses manual berulang meningkatkan biaya tenaga kerja serta resiko kesalahan manusia."),
            ("03", "Keterlambatan Siklus Rilis", "Waktu peluncuran fitur baru membutuhkan hitungan minggu tanpa otomasi validasi data."),
            ("04", "Keterbatasan Visibilitas Real-Time", "Pimpinan kekurangan akses dasbor analitik terpadu untuk keputusan strategis cepat.")
        ]
        grid_w = (W - 2 * m - 30) / 2
        grid_h = H * 0.26
        for idx, (p_num, p_title, p_desc) in enumerate(problems):
            row, col = idx // 2, idx % 2
            gx = m + col * (grid_w + 30)
            gy = H * 0.35 + row * (grid_h + 24)
            card = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(gx), px(gy), px(grid_w), px(grid_h))
            card.fill.solid()
            card.fill.fore_color.rgb = _rgb(card_bg)
            card.line.color.rgb = _rgb(border_col)
            card.line.width = px(1)

            c_top = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(gx), px(gy), px(grid_w), px(3))
            c_top.fill.solid()
            c_top.fill.fore_color.rgb = _rgb(primary_col if idx % 2 == 0 else accent_col)
            c_top.line.fill.background()

            n_badge = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(gx + 24), px(gy + 20), px(44), px(32))
            n_badge.fill.solid()
            n_badge.fill.fore_color.rgb = _rgb(primary_col if idx % 2 == 0 else accent_col)
            n_badge.line.fill.background()
            text(s2, p_num, gx + 24, gy + 24, 44, 28, 14, "#000000" if not dark else "#FFFFFF", bold=True, align=PP_ALIGN.CENTER)

            text(s2, p_title, gx + 80, gy + 22, grid_w - 100, 35, 20, ink, bold=True)
            d_line = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(gx + 24), gy + 66, px(grid_w - 48), px(1))
            d_line.fill.solid()
            d_line.fill.fore_color.rgb = _rgb(border_col)
            d_line.line.fill.background()
            text(s2, p_desc, gx + 24, gy + 78, grid_w - 48, 80, 15, sub_ink)

        # Slide 3: Solution Architecture
        s3 = slide()
        line3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(m * 0.7), px(W - 2 * m), px(1))
        line3.fill.solid()
        line3.fill.fore_color.rgb = _rgb(border_col)
        line3.line.fill.background()

        text(s3, "02 / VALUE PROPOSITION", m, m * 0.7 + 16, 400, 30, 14, primary_col, bold=True)
        split_x = W * 0.46
        text(s3, "Solusi Terintegrasi Berbasis Arsitektur Cerdas", m, H * 0.22, split_x - m - 40, 110, 36, ink, bold=True)
        text(s3, "Menggabungkan pemrosesan throughput tinggi, keandalan 99.95% uptime, dan orkestrasi otomatis.",
             m, H * 0.44, split_x - m - 40, 90, 17, sub_ink)

        s_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(H * 0.65), px(split_x - m - 40), px(54))
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = _rgb(card_bg)
        s_box.line.color.rgb = _rgb(primary_col)
        s_box.line.width = px(2)
        text(s3, "REDUKSI BIAYA INFRASTRUKTUR HINGGA 42%", m, H * 0.65 + 16, split_x - m - 40, 30, 14, primary_col,
             bold=True, align=PP_ALIGN.CENTER)

        v_div = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(split_x), px(H * 0.2), px(1), px(H * 0.65))
        v_div.fill.solid()
        v_div.fill.fore_color.rgb = _rgb(border_col)
        v_div.line.fill.background()

        pillars = [
            ("01", "Skalabilitas Awan Elastis", "Infrastruktur kontainer terdistribusi yang menyesuaikan kapasitas lalu lintas dinamis secara mulus."),
            ("02", "Enkripsi & Tata Kelola Standar Global", "Protokol perlindungan data berstandar enterprise dengan jejak audit komprehensif."),
            ("03", "Konektor API Instan", "Integrasi modular yang mudah disematkan pada sistem yang sedang beroperasi tanpa penghentian layanan.")
        ]
        for idx, (p_num, p_title, p_desc) in enumerate(pillars):
            py = H * 0.22 + idx * (H * 0.22)
            rx = split_x + 40
            rw = W - rx - m

            p_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(rx), px(py), px(rw), px(H * 0.18))
            p_box.fill.solid()
            p_box.fill.fore_color.rgb = _rgb(card_bg)
            p_box.line.color.rgb = _rgb(border_col)
            p_box.line.width = px(1)

            text(s3, p_num, rx + 20, py + 16, 45, 30, 22, accent_col, bold=True)
            text(s3, p_title, rx + 75, py + 16, rw - 95, 30, 21, ink, bold=True)
            text(s3, p_desc, rx + 75, py + 52, rw - 95, 60, 15, sub_ink)

        # Slide 4: Key Traction Metrics (Giant Display Numbers & High-Contrast Tinted Cards)
        s4 = slide()
        line4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(m * 0.7), px(W - 2 * m), px(1))
        line4.fill.solid()
        line4.fill.fore_color.rgb = _rgb(border_col)
        line4.line.fill.background()

        text(s4, "03 / TRACTION & FINANCIAL EFFICIENCY", m, m * 0.7 + 16, 450, 30, 14, primary_col, bold=True)
        text(s4, "Pertumbuhan Eksponensial & Metrik Kinerja Teruji", m, H * 0.16, W * 0.75, 70, 38, ink, bold=True)

        kpis = [
            ("+240%", "PERTUMBUHAN TAHUNAN (YoY)", "Pertumbuhan pendapatan berulang murni tanpa pembengkakan biaya akuisisi pengguna.", primary_col),
            ("89.4%", "RETENSI PENGGUNA 12 BULAN", "Retensi tingkat tinggi berkat ketergantungan workflow harian yang efisien.", accent_col),
            ("Rp 65 M", "TOTAL VOLUME TRANSAKSI", "Volume transaksi bruto yang telah diproses secara aman dalam periode pelaporan.", primary_col)
        ]
        kpi_w = (W - 2 * m - 40) / 3
        for idx, (k_num, k_lbl, k_desc, k_col) in enumerate(kpis):
            kx = m + idx * (kpi_w + 20)
            k_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(kx), px(H * 0.32), px(kpi_w), px(H * 0.52))
            k_box.fill.solid()
            k_box.fill.fore_color.rgb = _rgb(card_bg)
            k_box.line.color.rgb = _rgb(border_col)
            k_box.line.width = px(1)

            top_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(kx), px(H * 0.32), px(kpi_w), px(5))
            top_bar.fill.solid()
            top_bar.fill.fore_color.rgb = _rgb(k_col)
            top_bar.line.fill.background()

            text(s4, k_num, kx + 24, H * 0.38, kpi_w - 48, 80, 54, k_col, bold=True)
            text(s4, k_lbl, kx + 24, H * 0.53, kpi_w - 48, 30, 14, ink, bold=True)
            text(s4, k_desc, kx + 24, H * 0.62, kpi_w - 48, 90, 15, sub_ink)

        # Slide 5: The Ask & Closing
        s5 = slide()
        line5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(m * 0.7), px(W - 2 * m), px(1))
        line5.fill.solid()
        line5.fill.fore_color.rgb = _rgb(border_col)
        line5.line.fill.background()

        text(s5, "04 / STRATEGIC INVESTMENT & PARTNERSHIP", m, m * 0.7 + 16, 450, 30, 14, accent_col, bold=True)
        text(s5, "Membangun Ekosistem Bersama", m, H * 0.22, W * 0.65, 80, 48, ink, bold=True)
        text(s5, "Alokasi Rencana Pendanaan: 45% Riset & Rekayasa Produk · 35% Ekspansi Penetrasi Pasar · 20% Cadangan Operasional.",
             m, H * 0.36, W * 0.72, 60, 18, sub_ink)

        # Contact card
        c_card = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(m), px(H * 0.54), px(W - 2 * m), px(H * 0.32))
        c_card.fill.solid()
        c_card.fill.fore_color.rgb = _rgb(card_bg)
        c_card.line.color.rgb = _rgb(border_col)
        c_card.line.width = px(1)

        text(s5, "KANTOR PUSAT & JALUR KEMITRAAN RESMI", m + 32, H * 0.58, 400, 26, 14, primary_col, bold=True)
        text(s5, "Konsorsium Ekosistem Cipta Digital Nusantara\nSurat Elektronik: kemitraan@digitalnusantara.id",
             m + 32, H * 0.64, W * 0.45, 60, 18, ink, bold=True)
        text(s5, "Dokumen ini disiapkan khusus untuk mitra strategis dan dilindungi kerahasiaan korporasi.",
             m + 32, H * 0.76, W * 0.45, 30, 13, sub_ink)

        btn = rect(s5, W - m - 340, H * 0.64, 300, 56, primary_col)
        text(s5, "JADWALKAN DISKUSI STRATEGIS", W - m - 340, H * 0.64 + 16, 300, 30, 13,
             "#000000" if not dark else "#FFFFFF", bold=True, align=PP_ALIGN.CENTER)

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
