// Rakit Desain / Canva Desktop — 200+ Authentic Professional Presentation Templates
// Multi-page 16:9 widescreen decks across 42 authentic business, tech, creative, and institutional domains.
'use strict';

// ---------- 5 Specialized Multi-page Presentation Deck Layouts ----------
if (typeof LAYOUTS !== 'undefined') {
  // 1. Investor Pitch Deck (5 Slides: Problem, Solution, Market, Traction, Team/Ask)
  LAYOUTS.deck_pitch = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .08, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg === '#111111' || p.bg === '#0B3D2E';
    const ink = dark ? p.text : p.text, cardBg = dark ? (p.soft || '#1E1E1E') : '#FFFFFF';

    const s1_cover = {
      bg: p.bg, title: 'Sampul Pitch Deck', elements: [
        R(m, H * .22, S * .015, H * .45, p.primary),
        Sh('ring', W - S * .35, -S * .1, S * .6, S * .6, p.primary, {opacity: .25}),
        Sh('blob', W - S * .5, H - S * .5, S * .7, S * .7, p.accent, {opacity: .18}),
        Tx('INVESTOR PITCH DECK · 2026', m + S * .04, H * .22, W * .6, S * .035, p.primary, {bold: true, spacing: 3, font: t.bf}),
        Tx(t.title, m + S * .04, H * .28, W * .62, fitFs(t.title, W * .62, S * .12, 2, .6), ink, {bold: true, font: t.hf, lh: 1.05}),
        Tx(t.sub, m + S * .04, H * .48, W * .55, S * .04, ink, {opacity: .85, font: t.bf, lh: 1.3}),
        R(m + S * .04, H * .62, S * .32, S * .065, p.primary, {radius: S * .015}),
        Tx(t.cta || 'PELAJARI PELUANG INVESTASI', m + S * .04, H * .638, S * .32, S * .024, '#FFFFFF', {bold: true, align: 'center', font: t.bf}),
        Tx(t.info, m + S * .04, H - m - S * .04, W * .6, S * .03, ink, {opacity: .7, font: t.bf})
      ]
    };

    const s2_problem = {
      bg: p.soft || '#F8F9FA', title: 'Masalah & Peluang Pasar', elements: [
        Tx('01 / PERMASALAHAN PASAR', m, m * .7, W * .5, S * .032, p.primary, {bold: true, spacing: 2, font: t.bf}),
        Tx('Tantangan Kritis Industri yang Perlu Solusi Baru', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...items.map((it, i) => {
          const colW = (W - 2 * m - S * .06) / 2, row = Math.floor(i / 2), col = i % 2;
          const x = m + col * (colW + S * .06), y = H * .32 + row * (H * .3);
          return [
            R(x, y, colW, H * .25, cardBg, {radius: S * .02, shadow: {on: true, x: 0, y: 8, blur: 20, color: '#00000015'}}),
            Sh('hexagon', x + S * .03, y + S * .03, S * .045, S * .045, p.accent),
            Tx('0' + (i + 1), x + S * .03, y + S * .038, S * .045, S * .024, '#FFFFFF', {bold: true, align: 'center', font: t.hf}),
            Tx(it.split('—')[0].trim(), x + S * .09, y + S * .035, colW - S * .11, S * .036, ink, {bold: true, font: t.hf}),
            Tx(it.includes('—') ? it.split('—')[1].trim() : 'Faktor kritis yang menghambat pertumbuhan efisiensi dan profitabilitas.', x + S * .03, y + S * .1, colW - S * .06, S * .028, ink, {opacity: .8, font: t.bf, lh: 1.3})
          ];
        }).flat()
      ]
    };

    const s3_solution = {
      bg: p.bg, title: 'Solusi & Arsitektur Nilai', elements: [
        Tx('02 / PROPOSISI NILAI', m, m * .7, W * .5, S * .032, p.accent, {bold: true, spacing: 2, font: t.bf}),
        Tx('Inovasi Terintegrasi dengan Skalabilitas Tinggi', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W * .48, H * .52, cardBg, {radius: S * .03}),
        Tx('Keunggulan Kompetitif Utama', m + S * .04, H * .36, W * .4, S * .045, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .04, H * .43, W * .4, S * .032, ink, {opacity: .85, font: t.bf, lh: 1.4}),
        Sh('diamond', W * .75 - S * .12, H * .45 - S * .12, S * .24, S * .24, p.primary, {opacity: .3}),
        Sh('ring', W * .75 - S * .15, H * .45 - S * .15, S * .3, S * .3, p.accent, {opacity: .4}),
        Tx('99.9%', W * .6, H * .65, W * .3, S * .08, p.primary, {bold: true, align: 'center', font: t.hf}),
        Tx('Keandalan & Efisiensi Teruji', W * .6, H * .75, W * .3, S * .03, ink, {align: 'center', font: t.bf})
      ]
    };

    const s4_traction = {
      bg: p.soft || '#F1F3F5', title: 'Traksi & Finansial', elements: [
        Tx('03 / PERTUMBUHAN & METRIK', m, m * .7, W * .5, S * .032, p.primary, {bold: true, spacing: 2, font: t.bf}),
        Tx('Traksi Pengguna Kuat dan Proyeksi Pendapatan', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...[
          {lbl: 'Pertumbuhan Tahunan (YoY)', val: '+240%', desc: 'Kenaikan adopsi organik'},
          {lbl: 'Retensi Pengguna 12 Bulan', val: '88.5%', desc: 'Tingkat kepuasan tinggi'},
          {lbl: 'Gross Merchandise Value', val: 'Rp45 Miliar', desc: 'Volume transaksi diproses'}
        ].flatMap((stat, idx) => {
          const w = (W - 2 * m - S * .06) / 3, x = m + idx * (w + S * .03);
          return [
            R(x, H * .34, w, H * .48, cardBg, {radius: S * .02, shadow: {on: true, x: 0, y: 10, blur: 24, color: '#00000010'}}),
            Tx(stat.val, x + S * .03, H * .42, w - S * .06, S * .085, p.primary, {bold: true, font: t.hf}),
            Tx(stat.lbl, x + S * .03, H * .53, w - S * .06, S * .036, ink, {bold: true, font: t.hf}),
            Tx(stat.desc, x + S * .03, H * .62, w - S * .06, S * .028, ink, {opacity: .75, font: t.bf})
          ];
        })
      ]
    };

    const s5_close = {
      bg: G(p.primary, p.accent, 140), title: 'Pendanaan & Kontak', elements: [
        Tx('PELUANG PENDANAAN', m, H * .26, W - 2 * m, S * .04, '#FFFFFF', {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Mari Membangun Masa Depan Bersama', m, H * .33, W - 2 * m, fitFs('Mari Membangun Masa Depan Bersama', W - 2 * m, S * .11, 1, .6), '#FFFFFF', {bold: true, align: 'center', font: t.hf}),
        Tx('Target Pendanaan Seri Lanjutan: Akselerasi R&D dan Penetrasi Pasar Global', m, H * .46, W - 2 * m, S * .04, '#FFFFFF', {opacity: .9, align: 'center', font: t.bf}),
        R(W / 2 - S * .24, H * .56, S * .48, S * .07, '#FFFFFF', {radius: 999}),
        Tx(t.cta || 'HUBUNGI TIM INVESTASI KAMI', W / 2 - S * .24, H * .58, S * .48, S * .026, p.primary, {bold: true, align: 'center', font: t.bf}),
        Tx(t.info + ' · Dokumen Rahasia Perusahaan', m, H - m - S * .03, W - 2 * m, S * .026, '#FFFFFF', {opacity: .8, align: 'center', font: t.bf})
      ]
    };

    return [s1_cover, s2_problem, s3_solution, s4_traction, s5_close];
  };

  // 2. Executive Corporate Report (5 Slides: Executive Summary, KPI Dashboard, Strategic Achievements, Financial Review, Next Steps)
  LAYOUTS.deck_report = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .08, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg === '#111111';
    const ink = dark ? p.text : p.text, cardBg = dark ? (p.soft || '#1E1E1E') : '#FFFFFF';

    const s1 = {
      bg: p.bg, title: 'Sampul Laporan Kinerja', elements: [
        R(0, 0, W, S * .015, p.primary),
        Tx('LAPORAN KINERJA EKSEKUTIF', m, H * .24, W * .7, S * .035, p.primary, {bold: true, spacing: 3, font: t.bf}),
        Tx(t.title, m, H * .3, W * .7, fitFs(t.title, W * .7, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx('Periode Kinerja Tahunan & Evaluasi Pencapaian Strategis Perusahaan', m, H * .46, W * .65, S * .038, ink, {opacity: .8, font: t.bf}),
        Sh('ring', W - S * .3, H * .5 - S * .2, S * .4, S * .4, p.primary, {opacity: .2}),
        Tx(t.info, m, H - m - S * .04, W * .6, S * .03, ink, {opacity: .7, font: t.bf})
      ]
    };

    const s2 = {
      bg: p.soft || '#F8F9FA', title: 'Ringkasan Eksekutif & KPI', elements: [
        Tx('RINGKASAN EKSEKUTIF', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Indikator Kinerja Utama Melampaui Target', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...[
          {t: 'Pendapatan Bersih', v: '+118%', sub: 'Target kuartal tercapai'},
          {t: 'Efisiensi Operasional', v: '-24%', sub: 'Optimalisasi biaya'},
          {t: 'Indeks Kepuasan Klien', v: '96.2%', sub: 'NPS level prima'},
          {t: 'Kepatuhan Regulasi', v: '100%', sub: 'Zero non-compliance'}
        ].flatMap((kpi, idx) => {
          const w = (W - 2 * m - S * .09) / 4, x = m + idx * (w + S * .03);
          return [
            R(x, H * .32, w, H * .45, cardBg, {radius: S * .018, shadow: {on: true, x: 0, y: 6, blur: 16, color: '#00000010'}}),
            Tx(kpi.v, x + S * .02, H * .38, w - S * .04, S * .075, p.primary, {bold: true, font: t.hf}),
            Tx(kpi.t, x + S * .02, H * .48, w - S * .04, S * .032, ink, {bold: true, font: t.hf}),
            Tx(kpi.sub, x + S * .02, H * .57, w - S * .04, S * .026, ink, {opacity: .75, font: t.bf})
          ];
        })
      ]
    };

    const s3 = {
      bg: p.bg, title: 'Pilar Capaian Strategis', elements: [
        Tx('CAPAIAN STRATEGIS', m, m * .7, W * .5, S * .032, p.accent, {bold: true, font: t.bf}),
        Tx('Realisasi Inisiatif Kunci di Seluruh Lini', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const y = H * .3 + idx * (H * .13);
          return [
            R(m, y, W - 2 * m, H * .1, cardBg, {radius: S * .015}),
            Sh('hexagon', m + S * .025, y + S * .025, S * .04, S * .04, p.primary),
            Tx('0' + (idx + 1), m + S * .025, y + S * .032, S * .04, S * .022, '#FFFFFF', {bold: true, align: 'center', font: t.hf}),
            Tx(it, m + S * .08, y + S * .03, W - 2 * m - S * .1, S * .036, ink, {bold: true, font: t.bf})
          ];
        }).flat()
      ]
    };

    const s4 = {
      bg: p.soft || '#F8F9FA', title: 'Tinjauan Finansial & Data', elements: [
        Tx('ANALISIS DATA & KEUANGAN', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Struktur Biaya dan Imbal Hasil Investasi Sehat', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        R(m, H * .3, W * .52, H * .52, cardBg, {radius: S * .02}),
        Tx('Pertumbuhan Aliran Kas Bebas', m + S * .04, H * .35, W * .45, S * .04, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .04, H * .42, W * .45, S * .032, ink, {opacity: .85, font: t.bf, lh: 1.4}),
        R(W * .62, H * .3, W * .38 - m, H * .52, cardBg, {radius: S * .02}),
        Tx('Rekomendasi Utama', W * .62 + S * .04, H * .35, W * .3, S * .04, p.accent, {bold: true, font: t.hf}),
        Tx('Pertahankan disiplin alokasi belanja modal dan perluas otomatisasi proses inti.', W * .62 + S * .04, H * .43, W * .3, S * .032, ink, {font: t.bf, lh: 1.4})
      ]
    };

    const s5 = {
      bg: p.bg, title: 'Rekomendasi & Tindak Lanjut', elements: [
        Tx('TINDAK LANJUT STRATEGIS', m, H * .28, W - 2 * m, S * .035, p.primary, {bold: true, align: 'center', spacing: 3, font: t.bf}),
        Tx('Fokus Eksekusi Menuju Kuartal Mendatang', m, H * .35, W - 2 * m, S * .085, ink, {bold: true, align: 'center', font: t.hf}),
        Tx('Pengawasan berkala dilakukan dewan komisaris dan komite audit setiap akhir bulan.', m, H * .46, W - 2 * m, S * .035, ink, {opacity: .8, align: 'center', font: t.bf}),
        R(W / 2 - S * .22, H * .58, S * .44, S * .065, p.primary, {radius: S * .015}),
        Tx(t.cta || 'UNDUH LAPORAN LENGKAP PDF', W / 2 - S * .22, H * .598, S * .44, S * .024, '#FFFFFF', {bold: true, align: 'center', font: t.bf}),
        Tx('Sekretariat Perusahaan · Kantor Manajemen Pusat', m, H - m - S * .03, W - 2 * m, S * .026, ink, {opacity: .6, align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 3. Strategic Roadmap & Expansion Deck (5 Slides: Vision, Strategic Pillars, 3-Horizon Roadmap, Resource Allocation, Milestones)
  LAYOUTS.deck_strategy = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .08, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg === '#111111';
    const ink = dark ? p.text : p.text, cardBg = dark ? (p.soft || '#1E1E1E') : '#FFFFFF';

    const s1 = {
      bg: p.bg, title: 'Sampul Peta Jalan Strategis', elements: [
        R(0, 0, S * .03, H, p.accent),
        Tx('PETA JALAN STRATEGIS 2026-2030', m, H * .25, W * .7, S * .035, p.accent, {bold: true, spacing: 3, font: t.bf}),
        Tx(t.title, m, H * .31, W * .72, fitFs(t.title, W * .72, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx('Navigasi Pertumbuhan Berkelanjutan dan Kepemimpinan Pasar', m, H * .47, W * .65, S * .036, ink, {opacity: .85, font: t.bf}),
        Sh('burst', W - S * .35, H * .3, S * .4, S * .4, p.primary, {opacity: .18}),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .03, ink, {opacity: .7, font: t.bf})
      ]
    };

    const s2 = {
      bg: p.soft || '#F8F9FA', title: 'Visi & Landasan Strategis', elements: [
        Tx('PILAR STRATEGIS', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Fondasi Keberhasilan Menuju Transformasi Penuh', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const w = (W - 2 * m - S * .09) / 4, x = m + idx * (w + S * .03);
          return [
            R(x, H * .32, w, H * .48, cardBg, {radius: S * .02, shadow: {on: true, x: 0, y: 6, blur: 18, color: '#00000010'}}),
            Sh('star4', x + S * .03, H * .36, S * .04, S * .04, p.primary),
            Tx(it.split('—')[0].trim(), x + S * .03, H * .43, w - S * .06, S * .038, ink, {bold: true, font: t.hf}),
            Tx(it.includes('—') ? it.split('—')[1].trim() : 'Inisiatif fundamental yang mempercepat penguasaan pangsa pasar.', x + S * .03, H * .52, w - S * .06, S * .028, ink, {opacity: .8, font: t.bf, lh: 1.3})
          ];
        }).flat()
      ]
    };

    const s3 = {
      bg: p.bg, title: 'Roadmap Tiga Horison', elements: [
        Tx('ROADMAP EKSEKUSI', m, m * .7, W * .5, S * .032, p.accent, {bold: true, font: t.bf}),
        Tx('Tahapan Implementasi Terukur 3 Horison', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...[
          {h: 'Horison 1 (Tahun 1)', focus: 'Penguatan Bisnis Inti', d: 'Optimalisasi operasi eksisting dan penguatan margin.'},
          {h: 'Horison 2 (Tahun 2-3)', focus: 'Ekspansi Segmen Baru', d: 'Peluncuran produk komplementer dan penetrasi pasar regional.'},
          {h: 'Horison 3 (Tahun 4-5)', focus: 'Peluang Transformasional', d: 'Penciptaan model bisnis inovatif berbasis teknologi masa depan.'}
        ].flatMap((hor, idx) => {
          const w = (W - 2 * m - S * .06) / 3, x = m + idx * (w + S * .03);
          return [
            R(x, H * .32, w, H * .5, cardBg, {radius: S * .025}),
            R(x, H * .32, w, S * .05, p.primary, {radius: S * .025}),
            Tx(hor.h, x + S * .02, H * .332, w - S * .04, S * .026, '#FFFFFF', {bold: true, align: 'center', font: t.bf}),
            Tx(hor.focus, x + S * .03, H * .42, w - S * .06, S * .042, p.primary, {bold: true, font: t.hf}),
            Tx(hor.d, x + S * .03, H * .52, w - S * .06, S * .032, ink, {opacity: .85, font: t.bf, lh: 1.4})
          ];
        })
      ]
    };

    const s4 = {
      bg: p.soft || '#F8F9FA', title: 'Alokasi Sumber Daya', elements: [
        Tx('ALOKASI ANGGARAN & KAPABILITAS', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Penyelarasan Modal Kerja dengan Sasaran Strategis', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W - 2 * m, H * .48, cardBg, {radius: S * .02}),
        Tx('R&D & Inovasi: 40%  ·  Pemasaran & Penjualan: 30%  ·  Operasional & Infrastruktur: 30%', m + S * .04, H * .38, W - 2 * m - S * .08, S * .036, p.primary, {bold: true, font: t.bf}),
        Tx(t.body, m + S * .04, H * .46, W - 2 * m - S * .08, S * .032, ink, {opacity: .85, font: t.bf, lh: 1.5})
      ]
    };

    const s5 = {
      bg: G(p.primary, p.accent, 135), title: 'Milestones & Target Kunci', elements: [
        Tx('TARGET KEBERHASILAN', m, H * .26, W - 2 * m, S * .035, '#FFFFFF', {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Komitmen Eksekusi dengan Hasil Teruji', m, H * .34, W - 2 * m, S * .09, '#FFFFFF', {bold: true, align: 'center', font: t.hf}),
        Tx('Monitoring capaian dilakukan per kuartal bersama dewan direksi dan pemangku kepentingan.', m, H * .46, W - 2 * m, S * .036, '#FFFFFF', {opacity: .9, align: 'center', font: t.bf}),
        R(W / 2 - S * .2, H * .58, S * .4, S * .065, '#FFFFFF', {radius: 999}),
        Tx(t.cta || 'AKSES DASHBOARD STRATEGIS', W / 2 - S * .2, H * .598, S * .4, S * .024, p.primary, {bold: true, align: 'center', font: t.bf}),
        Tx(t.info, m, H - m - S * .03, W - 2 * m, S * .026, '#FFFFFF', {opacity: .8, align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 4. Creative Agency & Capabilities Deck (5 Slides: About, Services, Case Studies, Framework, Investment)
  LAYOUTS.deck_agency = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .08, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg === '#111111';
    const ink = dark ? p.text : p.text, cardBg = dark ? (p.soft || '#1E1E1E') : '#FFFFFF';

    const s1 = {
      bg: p.bg, title: 'Sampul Portofolio & Agensi', elements: [
        Sh('ring', W * .75 - S * .25, H * .5 - S * .25, S * .5, S * .5, p.primary, {opacity: .25}),
        Sh('arch', W - S * .3, 0, S * .3, H * .8, p.accent, {opacity: .15}),
        Tx('PROFIL AGENSI & PORTOFOLIO KARYA', m, H * .26, W * .65, S * .035, p.primary, {bold: true, spacing: 3, font: t.bf}),
        Tx(t.title, m, H * .32, W * .65, fitFs(t.title, W * .65, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx(t.sub, m, H * .48, W * .6, S * .038, ink, {opacity: .85, font: t.bf}),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .03, ink, {opacity: .7, font: t.bf})
      ]
    };

    const s2 = {
      bg: p.soft || '#F8F9FA', title: 'Layanan & Keahlian Utama', elements: [
        Tx('LAYANAN UNGGULAN', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Solusi Desain & Strategi Komunikasi Terpadu', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const colW = (W - 2 * m - S * .06) / 2, row = Math.floor(idx / 2), col = idx % 2;
          const x = m + col * (colW + S * .06), y = H * .32 + row * (H * .3);
          return [
            R(x, y, colW, H * .25, cardBg, {radius: S * .02, shadow: {on: true, x: 0, y: 6, blur: 16, color: '#00000010'}}),
            Sh('hexagon', x + S * .03, y + S * .035, S * .045, S * .045, p.primary),
            Tx(it.split('—')[0].trim(), x + S * .09, y + S * .04, colW - S * .11, S * .038, ink, {bold: true, font: t.hf}),
            Tx(it.includes('—') ? it.split('—')[1].trim() : 'Pendekatan strategis yang menghasilkan diferensiasi merek berdaya saing tinggi.', x + S * .03, y + S * .11, colW - S * .06, S * .028, ink, {opacity: .8, font: t.bf, lh: 1.3})
          ];
        }).flat()
      ]
    };

    const s3 = {
      bg: p.bg, title: 'Studi Kasus Klien', elements: [
        Tx('STUDI KASUS KARYA', m, m * .7, W * .5, S * .032, p.accent, {bold: true, font: t.bf}),
        Tx('Dampak Nyata Kolaborasi Kreatif Kami', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W * .52, H * .5, cardBg, {radius: S * .025}),
        Tx('Kampanye Merek Unggulan', m + S * .04, H * .37, W * .44, S * .044, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .04, H * .45, W * .44, S * .032, ink, {opacity: .85, font: t.bf, lh: 1.4}),
        R(W * .62, H * .32, W * .38 - m, H * .5, cardBg, {radius: S * .025}),
        Tx('Hasil Kinerja Kampanye', W * .62 + S * .04, H * .37, W * .3, S * .04, p.accent, {bold: true, font: t.hf}),
        Tx('+320% Interaksi Sosial · 1.4M Jangkauan Audiens · Rekognisi Industri Nasional', W * .62 + S * .04, H * .46, W * .3, S * .032, ink, {font: t.bf, lh: 1.5})
      ]
    };

    const s4 = {
      bg: p.soft || '#F8F9FA', title: 'Metodologi & Alur Kerja', elements: [
        Tx('METODOLOGI EKSEKUSI', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Empat Langkah Menghasilkan Karya Berkualitas', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...[
          {s: '01', t: 'Discovery', d: 'Riset mendalam identitas dan kompetitor.'},
          {s: '02', t: 'Strategy', d: 'Perumusan arah kreatif dan proposisi nilai.'},
          {s: '03', t: 'Design', d: 'Eksplorasi visual dan iterasi purwarupa.'},
          {s: '04', t: 'Delivery', d: 'Penerapan menyeluruh dan panduan merek.'}
        ].flatMap((step, idx) => {
          const w = (W - 2 * m - S * .09) / 4, x = m + idx * (w + S * .03);
          return [
            R(x, H * .32, w, H * .48, cardBg, {radius: S * .02}),
            Tx(step.s, x + S * .03, H * .36, w - S * .06, S * .065, p.primary, {bold: true, font: t.hf}),
            Tx(step.t, x + S * .03, H * .46, w - S * .06, S * .038, ink, {bold: true, font: t.hf}),
            Tx(step.d, x + S * .03, H * .54, w - S * .06, S * .028, ink, {opacity: .8, font: t.bf, lh: 1.3})
          ];
        })
      ]
    };

    const s5 = {
      bg: p.bg, title: 'Kolaborasi & Penawaran', elements: [
        Tx('KOLABORASI KREATIF', m, H * .28, W - 2 * m, S * .035, p.primary, {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Mari Wujudkan Ide Hebat Bersama Kami', m, H * .35, W - 2 * m, S * .09, ink, {bold: true, align: 'center', font: t.hf}),
        Tx('Konsultasi awal gratis untuk mendiskusikan kebutuhan komunikasi merek Anda.', m, H * .46, W - 2 * m, S * .036, ink, {opacity: .8, align: 'center', font: t.bf}),
        R(W / 2 - S * .2, H * .58, S * .4, S * .065, p.primary, {radius: 999}),
        Tx(t.cta || 'MULAI PROYEK BERSAMA', W / 2 - S * .2, H * .598, S * .4, S * .024, '#FFFFFF', {bold: true, align: 'center', font: t.bf}),
        Tx(t.info, m, H - m - S * .03, W - 2 * m, S * .026, ink, {opacity: .7, align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 5. Training & Workshop Masterclass Deck (5 Slides: Objectives, Framework, Case Analysis, Exercises, Summary)
  LAYOUTS.deck_workshop = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .08, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg === '#111111';
    const ink = dark ? p.text : p.text, cardBg = dark ? (p.soft || '#1E1E1E') : '#FFFFFF';

    const s1 = {
      bg: p.bg, title: 'Sampul Workshop & Pelatihan', elements: [
        R(0, 0, W, S * .02, p.accent),
        Tx('MODUL PELATIHAN & WORKSHOP PROFESIONAL', m, H * .26, W * .7, S * .035, p.accent, {bold: true, spacing: 3, font: t.bf}),
        Tx(t.title, m, H * .32, W * .72, fitFs(t.title, W * .72, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx(t.sub, m, H * .48, W * .65, S * .038, ink, {opacity: .85, font: t.bf}),
        Sh('ring', W - S * .3, H * .3, S * .4, S * .4, p.primary, {opacity: .2}),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .03, ink, {opacity: .7, font: t.bf})
      ]
    };

    const s2 = {
      bg: p.soft || '#F8F9FA', title: 'Tujuan Pembelajaran', elements: [
        Tx('TUJUAN PEMBELAJARAN', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Kompetensi Utama yang Akan Dikuasai Peserta', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const colW = (W - 2 * m - S * .06) / 2, row = Math.floor(idx / 2), col = idx % 2;
          const x = m + col * (colW + S * .06), y = H * .32 + row * (H * .3);
          return [
            R(x, y, colW, H * .25, cardBg, {radius: S * .02, shadow: {on: true, x: 0, y: 6, blur: 16, color: '#00000010'}}),
            Tx('Modul ' + (idx + 1), x + S * .03, y + S * .035, colW - S * .06, S * .028, p.primary, {bold: true, font: t.bf}),
            Tx(it.split('—')[0].trim(), x + S * .03, y + S * .08, colW - S * .06, S * .038, ink, {bold: true, font: t.hf}),
            Tx(it.includes('—') ? it.split('—')[1].trim() : 'Pemahaman konsep dasar dan latihan aplikatif di dunia kerja nyata.', x + S * .03, y + S * .14, colW - S * .06, S * .028, ink, {opacity: .8, font: t.bf, lh: 1.3})
          ];
        }).flat()
      ]
    };

    const s3 = {
      bg: p.bg, title: 'Kerangka Konseptual', elements: [
        Tx('KERANGKA TEORI & PRAKTIK', m, m * .7, W * .5, S * .032, p.accent, {bold: true, font: t.bf}),
        Tx('Prinsip Fundamental yang Teruji di Lapangan', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W * .5, H * .5, cardBg, {radius: S * .025}),
        Tx('Prinsip Utama Pelatihan', m + S * .04, H * .37, W * .42, S * .042, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .04, H * .45, W * .42, S * .032, ink, {opacity: .85, font: t.bf, lh: 1.4}),
        R(W * .6, H * .32, W * .4 - m, H * .5, cardBg, {radius: S * .025}),
        Tx('Aplikasi di Tempat Kerja', W * .6 + S * .04, H * .37, W * .32, S * .04, p.accent, {bold: true, font: t.hf}),
        Tx('Terapkan langsung pada alur kerja tim harian untuk meningkatkan produktivitas secara signifikan.', W * .6 + S * .04, H * .45, W * .32, S * .032, ink, {font: t.bf, lh: 1.4})
      ]
    };

    const s4 = {
      bg: p.soft || '#F8F9FA', title: 'Latihan & Simulasi Studi Kasus', elements: [
        Tx('SIMULASI KASUS NYATA', m, m * .7, W * .5, S * .032, p.primary, {bold: true, font: t.bf}),
        Tx('Latihan Kelompok Interaktif (25 Menit)', m, m * .7 + S * .05, W * .7, S * .075, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W - 2 * m, H * .48, cardBg, {radius: S * .02}),
        Tx('Instruksi Latihan:', m + S * .04, H * .37, W - 2 * m - S * .08, S * .038, p.primary, {bold: true, font: t.hf}),
        Tx('1. Bentuk kelompok 3-4 orang dan analisis skenario yang diberikan fasilitator.\n2. Terapkan kerangka kerja yang telah dipelajari untuk merumuskan 3 solusi prioritas.\n3. Presentasikan hasil diskusi kelompok dalam waktu 3 menit per tim.', m + S * .04, H * .45, W - 2 * m - S * .08, S * .032, ink, {font: t.bf, lh: 1.6})
      ]
    };

    const s5 = {
      bg: G(p.primary, p.accent, 140), title: 'Rangkuman & Sesi Tanya Jawab', elements: [
        Tx('KESIMPULAN PELATIHAN', m, H * .26, W - 2 * m, S * .035, '#FFFFFF', {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Sesi Tanya Jawab & Rencana Tindak Lanjut', m, H * .34, W - 2 * m, S * .085, '#FFFFFF', {bold: true, align: 'center', font: t.hf}),
        Tx('Materi tayangan dan sertifikat digital akan dikirimkan ke email terdaftar seluruh peserta.', m, H * .46, W - 2 * m, S * .035, '#FFFFFF', {opacity: .9, align: 'center', font: t.bf}),
        R(W / 2 - S * .2, H * .58, S * .4, S * .065, '#FFFFFF', {radius: 999}),
        Tx(t.cta || 'UNDUH MATERI WORKSHOP', W / 2 - S * .2, H * .598, S * .4, S * .024, p.primary, {bold: true, align: 'center', font: t.bf}),
        Tx(t.info, m, H - m - S * .03, W - 2 * m, S * .026, '#FFFFFF', {opacity: .8, align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };
}

// ---------- 42 Authentic Professional Presentation Themes ----------
const PRESENTATION_THEMES = {
  fintech_ai: {
    cat: 'Finansial & FinTech', tags: 'fintech payment gateway perbankan ai investasi',
    pal: {bg: '#0D1B2A', primary: '#00B4D8', text: '#E0E1DD', accent: '#90E0EF', soft: '#1B263B'},
    hf: 'Plus Jakarta Sans', bf: 'Roboto',
    kicker: 'FINTECH & PAYMENT GATEWAY', title: 'Ekosistem Pembayaran Digital Cerdas 2026',
    sub: 'Solusi Settlement Real-Time dan Proteksi Transaksi Berbasis Kecerdasan Buatan',
    body: 'Pemrosesan 500+ transaksi per detik dengan latensi rata-rata di bawah 120ms.',
    cta: 'JELAJAHI SOLUSI FINTECH', info: 'Direktorat Teknologi Finansial · PT Solusi Bayar Indonesia',
    st: ['bolt', 'shield', 'sparkle'],
    items: [' Settlement instan antar bank 24/7', ' Deteksi fraud transaksi real-time', ' Integrasi Open Banking API resmi', ' Enkripsi berlapis standar PCI-DSS']
  },
  saas_enterprise: {
    cat: 'Teknologi & SaaS', tags: 'saas b2b automasi korporat cloud software',
    pal: {bg: '#0F172A', primary: '#38BDF8', text: '#F8FAFC', accent: '#818CF8', soft: '#1E293B'},
    hf: 'Bricolage Grotesque', bf: 'Plus Jakarta Sans',
    kicker: 'B2B SAAS WORKFLOW AUTOMATION', title: 'Platform Otomasi Operasional Korporat',
    sub: 'Mengintegrasikan Sistem ERP, CRM, dan Analisis Data dalam Satu Antarmuka',
    body: 'Meningkatkan produktivitas tim lintas divisi hingga 42% sejak bulan pertama.',
    cta: 'JADWALKAN DEMO ENTERPRISE', info: 'Divisi Solusi Korporasi · CloudFlow Enterprise',
    st: ['bulb', 'check', 'bolt'],
    items: [' Sinkronisasi data dua arah multi-platform', ' Mesin automasi tanpa kode (no-code)', ' Audit log dan kepatuhan ISO 27001', ' Dukungan SLA ketersediaan 99.95%']
  },
  healthtech_telemed: {
    cat: 'Kesehatan & Medis', tags: 'healthtech medis rumah sakit dokter klinik',
    pal: {bg: '#F0FDF4', primary: '#16A34A', text: '#14532D', accent: '#38BDF8', soft: '#DCFCE7'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'HEALTHTECH & REKAM MEDIS', title: 'Transformasi Layanan Kesehatan Digital',
    sub: 'Platform Telekonsultasi dan Rekam Medis Elektronik Terintegrasi Standar Kemenkes',
    body: 'Menghubungkan 1.200+ fasilitas kesehatan primer dengan spesialis di seluruh Indonesia.',
    cta: 'KONSULTASI SOLUSI RUMAH SAKIT', info: 'Konsorsium Inovasi Kesehatan Medika Digital',
    st: ['leaf', 'check', 'sparkle'],
    items: [' Rekam Medis Elektronik (RME) terpadu', ' Antrean faskes online dan e-resep', ' Triase pasien berbasis AI klinis', ' Keamanan data privasi pasien terenkripsi']
  },
  edutech_learning: {
    cat: 'Pendidikan & EduTech', tags: 'edutech sekolah kampus pelatihan kursus siswa',
    pal: {bg: '#EEF2FF', primary: '#4F46E5', text: '#1E1B4B', accent: '#F59E0B', soft: '#E0E7FF'},
    hf: 'Bricolage Grotesque', bf: 'Poppins',
    kicker: 'EDUTECH & ADAPTIVE LEARNING', title: 'Kurikulum Digital Masa Depan',
    sub: 'Pembelajaran Personalisasi Berbasis Analisis Minat dan Kecepatan Belajar Siswa',
    body: 'Digunakan oleh 45.000+ pelajar dan mahasiswa di 18 provinsi.',
    cta: 'PELAJARI KURIKULUM LENGKAP', info: 'Lembaga Pengembangan Pendidikan Cerdas Indonesia',
    st: ['graduation', 'bulb', 'sparkle'],
    items: [' Jalur belajar adaptif kecerdasan buatan', ' Dashboard perkembangan murid bagi guru', ' Bank soal kompetensi terstandar nasional', ' Akses materi offline ramah kuota']
  },
  agritech_smartfarm: {
    cat: 'Pertanian & AgriTech', tags: 'agritech tani pangan hidroponik irigasi suplai',
    pal: {bg: '#1C2826', primary: '#A3E635', text: '#F7FEE7', accent: '#FACC15', soft: '#2D3A37'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'SMART FARMING & SUPPLY CHAIN', title: 'Modernisasi Rantai Pasok Pangan Nasional',
    sub: 'Sensor Tanah IoT, Prediksi Iklim Mikro, dan Distribusi Panen Langsung ke Pasar',
    body: 'Meningkatkan hasil panen petani mitra sebesar 31% dengan pengurangan limbah pascapanen.',
    cta: 'GABUNG MITRA AGRI DIGITAL', info: 'Inisiatif Kedaulatan Pangan Lestari AgriTech',
    st: ['leaf', 'plant', 'check'],
    items: [' Pemantauan kelembapan tanah otomatis', ' Prediksi cuaca mikro hiperlokal', ' Jalur distribusi langsung tanpa perantara', ' Pendanaan bibit dan sarana produksi tani']
  },
  logistics_fleet: {
    cat: 'Logistik & Rantai Pasok', tags: 'logistik armada kargo pengiriman gudang suplai',
    pal: {bg: '#0B132B', primary: '#48E5C2', text: '#FFFFFF', accent: '#F39237', soft: '#1C2541'},
    hf: 'Archivo Black', bf: 'Montserrat',
    kicker: 'SMART FLEET & WAREHOUSING', title: 'Optimasi Logistik Rantai Dingin & Kargo',
    sub: 'Pelacakan Armada Telemetri Real-Time dan Tata Kelola Gudang Otomatis',
    body: 'Efisiensi konsumsi bahan bakar armada hingga 18% dan ketepatan waktu kirim 98.4%.',
    cta: 'OPTIMALKAN LOGISTIK ANDA', info: 'PT Nusantara Ekspedisi Logistik Terpadu',
    st: ['bolt', 'pin', 'check'],
    items: [' Pemetaan rute dinamis berbasis kemacetan', ' Kontrol suhu armada rantai dingin', ' Sistem manajemen gudang barcode terpusat', ' Dashboard utilisasi aset armada real-time']
  },
  clean_energy_solar: {
    cat: 'Energi & Lingkungan', tags: 'energi surya solar plts hijau listrik esg',
    pal: {bg: '#0F2027', primary: '#20BF55', text: '#F1F2F6', accent: '#01BAEF', soft: '#203A43'},
    hf: 'Montserrat', bf: 'Roboto',
    kicker: 'RENEWABLE ENERGY & SOLAR POWER', title: 'Transisi Energi Bersih Industri 2026',
    sub: 'Pemasangan PLTS Atap dan Efisiensi Konsumsi Listrik Manufaktur Ramah Lingkungan',
    body: 'Reduksi emisi karbon terukur sebesar 14.000 ton CO2 setara per tahun per fasilitas pabrik.',
    cta: 'SIMULASI PENGHEMATAN ENERGI', info: 'Divisi Energi Baru & Terbarukan · Solaria Indonesia',
    st: ['plant', 'leaf', 'bulb'],
    items: [' Desain PLTS Atap industri bersertifikasi', ' Pembiayaan nol investasi awal (Capex-free)', ' Sistem pemantauan produksi daya online', ' Sertifikat kredit energi terbarukan (REC)']
  },
  corporate_audit: {
    cat: 'Hukum & Tata Kelola', tags: 'audit kepatuhan legal tata kelola risiko perbankan',
    pal: {bg: '#1A1E24', primary: '#C5A880', text: '#F4F4F5', accent: '#533E2D', soft: '#292F38'},
    hf: 'Playfair Display', bf: 'Plus Jakarta Sans',
    kicker: 'INTERNAL AUDIT & GOVERNANCE', title: 'Kerangka Kepatuhan & Manajemen Risiko',
    sub: 'Memperkuat Tata Kelola Perusahaan yang Baik (Good Corporate Governance)',
    body: 'Pencegahan risiko fraud dan perlindungan integritas operasional secara sistemik.',
    cta: 'TINJAU LAPORAN TATA KELOLA', info: 'Komite Audit & Kepatuhan Korporasi',
    st: ['shield', 'check', 'sparkle'],
    items: [' Matriks penilaian risiko divisi menyeluruh', ' Sistem pelaporan pelanggaran (Whistleblowing)', ' Audit kepatuhan standar keuangan internasional', ' Rekomendasi perbaikan operasional dewan direksi']
  },
  esg_sustainability: {
    cat: 'Keberlanjutan & ESG', tags: 'esg emisi karbon keberlanjutan csr sosial hijau',
    pal: {bg: '#14281D', primary: '#52B788', text: '#D8F3DC', accent: '#B7E4C7', soft: '#1B4332'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'ESG REPORTING & IMPACT', title: 'Laporan Keberlanjutan & Dampak Sosial',
    sub: 'Transparansi Kinerja Lingkungan, Kesejahteraan Sosial, dan Integritas Korporasi',
    body: 'Pencapaian target net-zero emisi karbon operasional fase pertama tercapai lebih awal.',
    cta: 'BACA LAPORAN ESG LENGKAP', info: 'Dewan Keberlanjutan Korporasi Hijau Nusantara',
    st: ['leaf', 'plant', 'sparkle'],
    items: [' Penurunan intensitas energi pabrik 22%', ' Program pemberdayaan komunitas sekitar', ' Kesetaraan gender dalam kepemimpinan senior', ' Pengelolaan limbah tanpa tempat pembuangan (Zero Waste)']
  },
  cybersecurity_soc: {
    cat: 'Keamanan Siber & IT', tags: 'cybersecurity keamanan siber hacker enkripsi server',
    pal: {bg: '#0A0E17', primary: '#00F0FF', text: '#E2E8F0', accent: '#7000FF', soft: '#161F30'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'CYBER DEFENSE & SOC OPERATIONS', title: 'Pertahanan Siber Aktif & Keamanan Cloud',
    sub: 'Pusat Operasi Keamanan 24/7 dan Deteksi Ancaman Siber Berbasis Intelijen Mesin',
    body: 'Menetralkan 100% insiden upaya intrusi tanpa downtime data kritis pelanggan.',
    cta: 'AUDIT POSTUR KEAMANAN ANDA', info: 'Pusat Tanggap Insiden Keamanan Siber Korporat',
    st: ['shield', 'bolt', 'check'],
    items: [' Security Operations Center (SOC) siaga 24/7', ' Uji penetrasi dan simulasi serangan berkala', ' Arsitektur Zero Trust Network Access (ZTNA)', ' Pelatihan kesadaran keamanan bagi seluruh staf']
  },
  proptech_marketplace: {
    cat: 'Properti & Real Estate', tags: 'proptech properti rumah apartemen investasi sewa',
    pal: {bg: '#F8FAFC', primary: '#0F172A', text: '#334155', accent: '#D97706', soft: '#E2E8F0'},
    hf: 'Montserrat', bf: 'Plus Jakarta Sans',
    kicker: 'PROPTECH & REAL ESTATE INVESTMENT', title: 'Platform Investasi Properti Digital',
    sub: 'Kepemilikan Fraksional Properti Komersial Prima dengan Legalitas Transparan',
    body: 'Memberikan imbal hasil sewa stabil rata-rata 8.5% per tahun bagi para investor.',
    cta: 'LIHAT DAFTAR PROPERTI PILIHAN', info: 'PT Investasi Properti Digital Indonesia',
    st: ['house', 'pin', 'check'],
    items: [' Verifikasi sertifikat tanah instan online', ' Perhitungan imbal hasil sewa otomatis', ' Pengelolaan operasional penyewa terpadu', ' Likuiditas pasar sekunder bagi pemodal']
  },
  retail_omnichannel: {
    cat: 'Ritel & E-Commerce', tags: 'ritel ecommerce toko kasir pos belanja logistik',
    pal: {bg: '#FFFBEB', primary: '#B45309', text: '#451A03', accent: '#F59E0B', soft: '#FEF3C7'},
    hf: 'Bebas Neue', bf: 'Poppins',
    kicker: 'OMNICHANNEL RETAIL EXPERIENCE', title: 'Ekspansi Ritel Terintegrasi Offline-Online',
    sub: 'Menyatukan Pengalaman Belanja di Toko Fisik dan Aplikasi Digital Tanpa Hambatan',
    body: 'Peningkatan nilai rata-rata keranjang belanja (AOV) sebesar 38% lintas saluran.',
    cta: 'PELAJARI SOLUSI RITEL KAMI', info: 'Divisi Inovasi Ritel Terpadu · RetailPro',
    st: ['pricetag', 'hot', 'check'],
    items: [' Sinkronisasi stok inventaris real-time', ' Program loyalitas poin terpusat', ' Layanan Ambil di Toko (Click and Collect)', ' Analisis arus pengunjung toko berbasis kamera pintar']
  },
  biotech_pharma: {
    cat: 'Bioteknologi & Farmasi', tags: 'biotek farmasi obat vaksin uji klinis lab',
    pal: {bg: '#F8FAFC', primary: '#0284C7', text: '#0F172A', accent: '#0D9488', soft: '#E0F2FE'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'BIOTECHNOLOGY & CLINICAL TRIALS', title: 'Riset Terapi Presisi & Kemandirian Farmasi',
    sub: 'Inovasi Molekul Obat Baru untuk Penyakit Tropis dengan Uji Klinis Terstandar WHO',
    body: 'Mempercepat fase penemuan obat baru hingga 50% lebih efisien dari metode konvensional.',
    cta: 'TELAAH HASIL UJI KLINIS', info: 'Pusat Riset Bioteknologi Terapan Nusantara',
    st: ['leaf', 'bulb', 'sparkle'],
    items: [' Sintesis molekul obat berbahan lokal', ' Uji praklinis dan kepatuhan bioetika', ' Fasilitas laboratorium berstandar GLP', ' Kemitraan riset global institusi terkemuka']
  },
  ev_mobility: {
    cat: 'Otomotif & Mobilitas', tags: 'ev motor listrik baterai spklu transportasi',
    pal: {bg: '#0A0A0A', primary: '#00E676', text: '#EDEDED', accent: '#00B0FF', soft: '#1E1E1E'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'EV ECOSYSTEM & INFRASTRUCTURE', title: 'Jaringan Pengisian Daya Kendaraan Listrik',
    sub: 'Penggelaran Stasiun Pengisian Cepat (Ultra Fast SPKLU) di Koridor Utama Antar Kota',
    body: 'Tersedia di 240+ titik strategis dengan waktu pengisian rata-rata 25 menit.',
    cta: 'PETA JARINGAN SPKLU', info: 'Konsorsium Infrastruktur EV Nusantara Raya',
    st: ['bolt', 'pin', 'check'],
    items: [' Pengisian daya berkecepatan 150 kW DC', ' Aplikasi reservasi stasiun pengisian mobile', ' Pasokan energi bersih bersertifikat', ' Kemitraan armada logistik komersial']
  },
  cloud_devops: {
    cat: 'Cloud & Rekayasa Perangkat Lunak', tags: 'cloud devops kubernetes aws gcp microservices',
    pal: {bg: '#0D1117', primary: '#58A6FF', text: '#C9D1D9', accent: '#7EE787', soft: '#161B22'},
    hf: 'Bricolage Grotesque', bf: 'Roboto',
    kicker: 'DEVOPS & CLOUD ARCHITECTURE', title: 'Modernisasi Infrastruktur Multi-Cloud',
    sub: 'Otomasi Pipeline CI/CD, Orkestrasi Kontainer, dan Skalabilitas Tanpa Gangguan',
    body: 'Memangkas waktu deployment dari hitungan hari menjadi menit dengan tingkat kegagalan 0.01%.',
    cta: 'KONSULTASI ARSITEKTUR CLOUD', info: 'Tim Rekayasa Keandalan Sistem (SRE)',
    st: ['bolt', 'check', 'sparkle'],
    items: [' Klaster Kubernetes terdistribusi otomatis', ' Pipeline rilis perangkat lunak nir-henti', ' Observabilitas dan telemetri metrik sistem', ' Optimasi biaya komputasi awan (FinOps)']
  },
  growth_marketing: {
    cat: 'Pemasaran & Pertumbuhan', tags: 'marketing iklan ads seo conversion funnel b2b',
    pal: {bg: '#FAF5FF', primary: '#7E22CE', text: '#3B0764', accent: '#EC4899', soft: '#F3E8FF'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'PERFORMANCE & GROWTH MARKETING', title: 'Strategi Akuisisi & Retensi Pengguna Skala Besar',
    sub: 'Optimalisasi Corong Konversi Multi-Saluran dengan Pendekatan Berbasis Eksperimen Data',
    body: 'Menurunkan Customer Acquisition Cost (CAC) sebesar 34% sambil menaikkan LTV 1.8x.',
    cta: 'MULAI KAMPANYE PERTUMBUHAN', info: 'Agensi Akselerasi Pertumbuhan Digital',
    st: ['megaphone', 'hot', 'sparkle'],
    items: [' Segmentasi audiens prediktif berbasis perilaku', ' Pengujian A/B kreatif iklan dinamis', ' Optimasi mesin pencari (SEO) teknikal', ' Automasi retensi email dan notifikasi push']
  },
  brand_identity: {
    cat: 'Identitas Visual & Merek', tags: 'branding logo warna font identitas pedoman visual',
    pal: {bg: '#FAF9F6', primary: '#1C1917', text: '#292524', accent: '#EA580C', soft: '#F5F5F4'},
    hf: 'Playfair Display', bf: 'Plus Jakarta Sans',
    kicker: 'BRAND IDENTITY GUIDELINES', title: 'Panduan Merek & Desain Terpadu 2026',
    sub: 'Standar Konsistensi Bahasa Visual, Tipografi, Tone of Voice, dan Penerapan Aset',
    body: 'Memastikan pesan merek tersampaikan secara kohesif di seluruh titik kontak pelanggan.',
    cta: 'LIHAT PANDUAN LENGKAP', info: 'Studio Desain Strategis & Identitas Merek',
    st: ['sparkle', 'bulb', 'check'],
    items: [' Skala tipografi dan hirarki teks resmi', ' Palet warna primer, sekunder, dan aksesibilitas', ' Pedoman fotografi dan ilustrasi editorial', ' Contoh penerapan pada kemasan dan media digital']
  },
  hr_talent: {
    cat: 'SDM & Budaya Kerja', tags: 'hr hrd rekrutmen karyawan budaya kantor talent',
    pal: {bg: '#FDF2F8', primary: '#BE185D', text: '#831843', accent: '#F472B6', soft: '#FCE7F3'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'PEOPLE & CULTURE STRATEGY', title: 'Pengembangan Talenta & Tempat Kerja Idaman',
    sub: 'Membangun Budaya Performa Tinggi, Kesejahteraan Karyawan, dan Jalur Karier Jelas',
    body: 'Tingkat retensi karyawan mencapai 94% dengan indeks kepuasan kerja kategori luar biasa.',
    cta: 'IKUTI PROGRAM ONBOARDING', info: 'Direktorat Sumber Daya Manusia & Organisasi',
    st: ['briefcase', 'check', 'sparkle'],
    items: [' Matriks jenjang karier dan transparansi kompensasi', ' Program pembinaan kepemimpinan berkala', ' Kebijakan kerja fleksibel berbasis output', ' Evaluasi kinerja berbasis OKR objektif']
  },
  legal_tech: {
    cat: 'Layanan Hukum & Regulasi', tags: 'hukum legal kontrak izin advokat kepatuhan',
    pal: {bg: '#0F172A', primary: '#E2E8F0', text: '#F8FAFC', accent: '#94A3B8', soft: '#1E293B'},
    hf: 'Cinzel', bf: 'Roboto',
    kicker: 'LEGALTECH & CONTRACT LIFECYCLE', title: 'Manajemen Kontrak Cerdas & Kepatuhan Bisnis',
    sub: 'Digitalisasi Alur Persetujuan Perjanjian Kerjasama dengan Tanda Tangan Elektronik Sah',
    body: 'Mempercepat siklus penandatanganan kontrak dari rata-rata 14 hari menjadi 4 jam.',
    cta: 'KONSULTASI MITRA HUKUM KAMI', info: 'Firma Hukum Korporasi & Teknologi Digital',
    st: ['shield', 'check', 'sparkle'],
    items: [' Standarisasi draf perjanjian bisnis resmi', ' Tanda tangan digital tersertifikasi Kominfo', ' Notifikasi pengingat masa perpanjangan kontrak', ' Repositori dokumen legal terpusat dan aman']
  },
  luxury_hospitality: {
    cat: 'Pariwisata & Perhotelan', tags: 'hotel resor liburan vila wisata bali lombok',
    pal: {bg: '#1A1815', primary: '#D4AF37', text: '#FDFBF7', accent: '#A67C1E', soft: '#2E2B26'},
    hf: 'Playfair Display', bf: 'Lora',
    kicker: 'LUXURY ECO-RESORT & TOURISM', title: 'Pengalaman Menginap Berkelas Dunia',
    sub: 'Harmoni Kemewahan Fasilitas Bintang Lima dengan Kelestarian Alam Budaya Lokal',
    body: 'Tingkat okupansi tahunan rata-rata 89% dengan penghargaan Best Boutique Resort.',
    cta: 'RESERVASI SUITE EKSKLUSIF', info: 'Manajemen Resor Bintang Lima Nusantara',
    st: ['flower', 'sparkle', 'leaf'],
    items: [' Vila privat dengan kolam renang tanpa batas', ' Pengalaman kuliner hidangan bahan organik lokal', ' Spa relaksasi tradisional berstandar global', ' Komitmen nol plastik dan efisiensi air mandiri']
  },
  fnb_franchise_expansion: {
    cat: 'Kuliner & Waralaba', tags: 'waralaba franchise resto cafe kuliner cabang fnb',
    pal: {bg: '#FFF7ED', primary: '#EA580C', text: '#7C2D12', accent: '#F97316', soft: '#FFEDD5'},
    hf: 'Archivo Black', bf: 'Poppins',
    kicker: 'FRANCHISE EXPANSION OPPORTUNITY', title: 'Peluang Kemitraan Waralaba Kuliner 2026',
    sub: 'Model Bisnis Teruji dengan Balik Modal Cepat dan Pasokan Bahan Baku Terstandar',
    body: 'Telah membuka 180+ gerai sukses di seluruh kota besar di Indonesia.',
    cta: 'DAFTAR MENJADI MITRA WARALABA', info: 'Divisi Pengembangan Kemitraan · Gerai Rasa Group',
    st: ['mug', 'hot', 'pricetag'],
    items: [' Proyeksi balik modal (ROI) 12-16 bulan', ' Pasokan bumbu dan bahan baku terpusat', ' Pelatihan menyeluruh untuk kru dan manajer', ' Dukungan pemasaran nasional berkelanjutan']
  },
  gaming_interactive: {
    cat: 'Game & Hiburan Digital', tags: 'game studio esports gaming turnamen anime 3d',
    pal: {bg: '#0F051D', primary: '#A855F7', text: '#FAF5FF', accent: '#EC4899', soft: '#240E44'},
    hf: 'Bebas Neue', bf: 'Roboto',
    kicker: 'GAME STUDIO & ESPORTS ECOSYSTEM', title: 'Ekspansi IP Game Mobile Berstandar Global',
    sub: 'Pengembangan Permainan Lintas Platform dengan Narasi Lokal dan Grafis Mutakhir',
    body: 'Mencapai 8.5 juta unduhan organik dengan rating pengguna 4.8 bintang di toko aplikasi.',
    cta: 'MAINKAN VERSI ALPHA SEKARANG', info: 'Studio Animasi & Game Interaktif Nusantara',
    st: ['bolt', 'hot', 'sparkle'],
    items: [' Mesin grafis optimal untuk ponsel spesifikasi menengah', ' Turnamen kompetitif liga komunitas resmi', ' Monetisasi ramah pemain berbasis item kosmetik', ' Pembaruan konten cerita musiman berkala']
  },
  digital_agency: {
    cat: 'Agensi Kreatif & Media', tags: 'agensi kreatif studio desain video iklan kampanye',
    pal: {bg: '#090A0F', primary: '#3B82F6', text: '#F3F4F6', accent: '#F43F5E', soft: '#181C2A'},
    hf: 'Bricolage Grotesque', bf: 'Plus Jakarta Sans',
    kicker: 'CREATIVE & MEDIA AGENCY', title: 'Kreativitas Berdampak untuk Brand Terdepan',
    sub: 'Menghubungkan Brand dengan Generasi Baru Melalui Cerita Otentik dan Produksi Visual Prima',
    body: 'Pemenang 14 penghargaan kampanye periklanan terbaik tingkat regional.',
    cta: 'DISUSKIKAN PROYEK ANDA', info: 'Agensi Kreatif Lintas Saluran · Kreasi Citra',
    st: ['sparkle', 'megaphone', 'hot'],
    items: [' Strategi komunikasi kampanye merek terpadu', ' Produksi iklan video sinematik berkualitas', ' Manajemen aktivasi media sosial dan kreator', ' Analisis sentimen publik dan jangkauan audiens']
  },
  industry_smart_factory: {
    cat: 'Manufaktur & Industri', tags: 'pabrik industri manufaktur robot iot otomasi mesin',
    pal: {bg: '#18181B', primary: '#F59E0B', text: '#FAFAFA', accent: '#E11D48', soft: '#27272A'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'INDUSTRY 4.0 & SMART MANUFACTURING', title: 'Digitalisasi Operasi Pabrik Masa Depan',
    sub: 'Penerapan Sensor Mesin Pintar dan Pemeliharaan Prediktif untuk Meminimalisir Downtime',
    body: 'Efisiensi output lini perakitan meningkat 28% dengan penurunan cacat produk di bawah 0.2%.',
    cta: 'JADWALKAN TUR PABRIK CERDAS', info: 'Departemen Teknologi Manufaktur Maju',
    st: ['bolt', 'check', 'bulb'],
    items: [' Sensor pemantauan getaran mesin nirkabel', ' Pemeliharaan prediktif sebelum terjadi kerusakan', ' Integrasi sistem SCADA dengan cloud analytics', ' Dasbor keselamatan kerja pekerja pabrik digital']
  },
  circular_economy: {
    cat: 'Ekonomi Sirkular & Daur Ulang', tags: 'daur ulang limbah sampah sirkular plastik ramah lingkungan',
    pal: {bg: '#0E1F1A', primary: '#10B981', text: '#ECFDF5', accent: '#34D399', soft: '#19382F'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'CIRCULAR ECONOMY & ZERO WASTE', title: 'Ekosistem Pengolahan Sampah Industri Berkelanjutan',
    sub: 'Mengubah Limbah Kemasan Menjadi Material Daur Ulang Berkualitas Tinggi untuk Manufaktur',
    body: 'Mengolah 25.000 ton limbah plastik pascakonsumen per tahun menjadi bahan baku siap pakai.',
    cta: 'GABUNG PROGRAM DAUR ULANG', info: 'Inisiatif Ekonomi Sirkular Bersih Nusantara',
    st: ['leaf', 'plant', 'check'],
    items: [' Sistem pelacakan sumber material daur ulang', ' Standar kemurnian biji plastik daur ulang industri', ' Sertifikasi rantai pasok ramah lingkungan', ' Kemitraan bank sampah komunitas terpadu']
  },
  wealth_management: {
    cat: 'Investasi & Perbankan Swasta', tags: 'wealth saham obligasi reksadana aset portofolio pensiun',
    pal: {bg: '#0C131F', primary: '#D4AF37', text: '#F8FAFC', accent: '#93C5FD', soft: '#1A2333'},
    hf: 'Cinzel', bf: 'Roboto',
    kicker: 'PRIVATE WEALTH MANAGEMENT', title: 'Pengelolaan Aset Keluarga & Portofolio Strategis',
    sub: 'Perlindungan Nilai Kekayaan Jangka Panjang Melalui Alokasi Multi-Aset Global dan Domestik',
    body: 'Dipercaya mengelola dana nasabah institusi dan individu bernilai kekayaan tinggi.',
    cta: 'HUBUNGI PENASIHAT INVESTASI', info: 'Kantor Pengelolaan Aset Prima · Private Wealth',
    st: ['shield', 'sparkle', 'check'],
    items: [' Alokasi aset defensif dan terukur', ' Perencanaan suksesi waris bisnis keluarga', ' Akses produk investasi eksklusif pasar privat', ' Laporan kinerja portofolio terperinci berkala']
  },
  autonomous_drones: {
    cat: 'Dirgantara & Drone Otonom', tags: 'drone uav udara inspeksi sensor pemetaan kargo',
    pal: {bg: '#0A0F1D', primary: '#06B6D4', text: '#E2E8F0', accent: '#3B82F6', soft: '#15203B'},
    hf: 'Archivo Black', bf: 'Montserrat',
    kicker: 'AUTONOMOUS DRONE SOLUTIONS', title: 'Inspeksi Udara Cerdas & Logistik Tanpa Awak',
    sub: 'Pengawasan Infrastruktur Kelistrikan, Pertambangan, dan Pemetaan Topografi Berakurasi Tinggi',
    body: 'Memangkas waktu survei medan berat hingga 80% dengan tingkat presisi sentimeter.',
    cta: 'JELAJAHI KAPABILITAS SURVEI', info: 'Divisi Teknologi Drone Mandiri Indonesia',
    st: ['bolt', 'pin', 'check'],
    items: [' Kamera termal dan LiDAR resolusi tinggi', ' Penerbangan otonom di luar jangkauan visual (BVLOS)', ' Analisis cacat infrastruktur otomatis berbasis AI', ' Sertifikasi pilot dan keselamatan penerbangan resmi']
  },
  media_ott_platform: {
    cat: 'Media & Penyiaran Digital', tags: 'ott streaming media film podcast audio video',
    pal: {bg: '#050505', primary: '#E50914', text: '#F5F5F5', accent: '#FFA00A', soft: '#1F1F1F'},
    hf: 'Bebas Neue', bf: 'Roboto',
    kicker: 'DIGITAL STREAMING & ENTERTAINMENT', title: 'Platform Konten Sinematik Nusantara',
    sub: 'Menghadirkan Film Cerita Asli, Dokumenter Budaya, dan Serial Eksklusif Berkualitas 4K',
    body: '3.2 juta pelanggan aktif bulanan dengan waktu tonton rata-rata 110 menit per hari.',
    cta: 'NIKMATI TAYANGAN UNGGULAN', info: 'Layanan Media Hiburan Berkelanjutan',
    st: ['hot', 'sparkle', 'pricetag'],
    items: [' Kompresi video cerdas hemat kuota pengguna', ' Kurasi konten lokal berdaya saing global', ' Akses tayangan bebas iklan pada paket premium', ' Fitur tonton luring (offline download) di ponsel']
  },
  medical_diagnostics: {
    cat: 'Alat Kesehatan & Diagnostik', tags: 'alkes laboratorium tes darah deteksi medis biosensor',
    pal: {bg: '#F8FAFC', primary: '#0284C7', text: '#1E293B', accent: '#10B981', soft: '#E2E8F0'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'POINT-OF-CARE DIAGNOSTICS', title: 'Perangkat Deteksi Medis Portabel & Cepat',
    sub: 'Hasil Analisis Sampel Darah Akurat dalam 15 Menit untuk Fasilitas Kesehatan Terpencil',
    body: 'Telah digunakan di 340 puskesmas daerah tertinggal, terdepan, dan terluar.',
    cta: 'DAPATKAN SPESIFIKASI ALAT', info: 'Inovasi Alat Kesehatan Diagnostik Medis',
    st: ['check', 'bulb', 'shield'],
    items: [' Akurasi diagnostik setara laboratorium rujukan (98.8%)', ' Desain kokoh dengan baterai tahan hingga 12 jam', ' Pengiriman data otomatis ke sistem rekam medis', ' Biaya per pengujian sangat terjangkau untuk faskes']
  },
  microfinance_umkm: {
    cat: 'Inklusi Keuangan & UMKM', tags: 'umkm mikro modal usaha kredit koperasi warung',
    pal: {bg: '#FFFBEB', primary: '#D97706', text: '#451A03', accent: '#10B981', soft: '#FEF3C7'},
    hf: 'Archivo Black', bf: 'Poppins',
    kicker: 'MICROFINANCE & INCLUSION', title: 'Pemberdayaan Modal Usaha UMKM Indonesia',
    sub: 'Akses Pendanaan Produktif Cepat, Tanpa Jaminan Rumit, Didampingi Edukasi Bisnis',
    body: 'Telah menyalurkan modal usaha produktif kepada 120.000+ pelaku usaha mikro perempuan.',
    cta: 'AJUKAN PENDAMPINGAN USAHA', info: 'Lembaga Keuangan Mikro Komunitas Berdaya',
    st: ['check', 'bulb', 'sparkle'],
    items: [' Bunga kompetitif dengan skema cicilan mingguan', ' Pelatihan pembukuan keuangan toko digital', ' Pendampingan manajemen inventaris usaha', ' Skoring kredit berbasis rekam jejak komunitas']
  },
  smart_governance: {
    cat: 'Pemerintahan & Pelayanan Publik', tags: 'pemerintah kota smart city pelayanan perizinan ktp kependudukan',
    pal: {bg: '#0F172A', primary: '#3B82F6', text: '#F8FAFC', accent: '#10B981', soft: '#1E293B'},
    hf: 'Montserrat', bf: 'Plus Jakarta Sans',
    kicker: 'DIGITAL PUBLIC SERVICES & SMART CITY', title: 'Satu Portal Layanan Terpadu Warga Kota',
    sub: 'Pengurusan Izin, Pelaporan Warga, dan Pembayaran Pajak Daerah dalam Satu Genggaman',
    body: 'Tingkat kepuasan warga atas pelayanan administrasi daerah melonjak menjadi 92.4%.',
    cta: 'JELAJAHI PORTAL WARGA', info: 'Dinas Komunikasi, Informatika & Tata Ruang Kota',
    st: ['shield', 'pin', 'check'],
    items: [' Integrasi seluruh instansi pelayanan kependudukan', ' Pelaporan kendala fasilitas kota dengan status transparan', ' Pembayaran retribusi nontunai bebas pungli', ' Dasbor komando pengendalian kota (Command Center)']
  },
  pharma_distribution: {
    cat: 'Rantai Pasok Farmasi', tags: 'farmasi obat apotek distribusi rantai dingin vaksin',
    pal: {bg: '#F0F9FF', primary: '#0369A1', text: '#0C4A6E', accent: '#059669', soft: '#E0F2FE'},
    hf: 'Poppins', bf: 'Roboto',
    kicker: 'PHARMACEUTICAL SUPPLY INTEGRITY', title: 'Jaminan Ketahanan & Distribusi Obat Nasional',
    sub: 'Sistem Rantai Dingin Terakreditasi BPOM Menjangkau 8.000+ Apotek dan Rumah Sakit',
    body: 'Ketepatan distribusi pasokan obat esensial mencapai 99.4% dengan jaminan keaslian 100%.',
    cta: 'KEMITRAAN DISTRIBUSI FARMASI', info: 'Distributor Farmasi Terakreditasi CDOB',
    st: ['check', 'shield', 'leaf'],
    items: [' Sertifikasi Cara Distribusi Obat yang Baik (CDOB)', ' Kontrol suhu gudang dan armada berbasis IoT', ' Pelacakan nomor batch obat terverifikasi resmi', ' Pasokan darurat 24 jam untuk rumah sakit rujukan']
  },
  telecom_network: {
    cat: 'Telekomunikasi & Jaringan', tags: 'telekomunikasi 5g fiber optic sinyal internet tower',
    pal: {bg: '#0A0E1A', primary: '#6366F1', text: '#F1F5F9', accent: '#06B6D4', soft: '#182138'},
    hf: 'Archivo Black', bf: 'Montserrat',
    kicker: 'TELECOMMUNICATION & 5G ROLLOUT', title: 'Penggelaran Jaringan Pita Lebar Berkecepatan Tinggi',
    sub: 'Ekspansi Jaringan Serat Optik dan Menara Pemancar 5G Mendukung Transformasi Digital',
    body: 'Menghubungkan 12 juta rumah tangga dengan latensi ultra rendah untuk aplikasi kritis.',
    cta: 'CEK JANGKAUAN FIBER OPTIK', info: 'Infrastruktur Jaringan Telekomunikasi Prima',
    st: ['bolt', 'pin', 'check'],
    items: [' Jaringan kabel serat optik bawah laut dan darat', ' Penetrasi menara 5G di kawasan industri dan pemukiman', ' Kesiapan infrastruktur edge computing perkotaan', ' Dukungan teknis keandalan transmisi 24/7']
  },
  port_maritime_logistics: {
    cat: 'Maritim & Pelabuhan', tags: 'pelabuhan kapal kontainer logistik laut dermaga ekspor',
    pal: {bg: '#0A192F', primary: '#64FFDA', text: '#CCD6F6', accent: '#FF70A6', soft: '#112240'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'MARITIME & SMART PORT LOGISTICS', title: 'Modernisasi Terminal Peti Kemas Maritim',
    sub: 'Otomasi Bongkar Muat Kapal dan Integrasi Ekosistem Logistik Pelabuhan Cerdas',
    body: 'Menurunkan waktu tunggu kapal (dwelling time) di dermaga hingga rata-rata 1.9 hari.',
    cta: 'AKSES JADWAL DERMAGA KAPAL', info: 'Otoritas Pelabuhan & Terminal Maritim Terpadu',
    st: ['pin', 'bolt', 'check'],
    items: [' Derek pemindah kontainer otomatis berteknologi tinggi', ' Pintu gerbang pelabuhan berbasis pemindai digital', ' Sistem manifes pelayaran terintegrasi bea cukai', ' Fasilitas pasokan daya listrik kapal sandar (Shore Power)']
  },
  green_construction: {
    cat: 'Konstruksi & Infrastruktur', tags: 'konstruksi bangunan gedung beton arsitektur proyek teknik',
    pal: {bg: '#171B1D', primary: '#E5A93B', text: '#ECEFF1', accent: '#379683', soft: '#242C30'},
    hf: 'Montserrat', bf: 'Roboto',
    kicker: 'GREEN CONSTRUCTION & INFRASTRUCTURE', title: 'Rekayasa Bangunan Gedung Hijau Berkelanjutan',
    sub: 'Desain Konstruksi Efisiensi Energi Tinggi Bersertifikat Greenship Platinum',
    body: 'Penghematan konsumsi energi operasional gedung hingga 35% dibandingkan gedung standar.',
    cta: 'KONSULTASI DESAIN INFRASTRUKTUR', info: 'Kontraktor Rekayasa Bangunan Hijau Indonesia',
    st: ['house', 'plant', 'check'],
    items: [' Material beton rendah karbon dan daur ulang', ' Fasad insulasi termal penahan panas matahari', ' Sistem pemanenan air hujan dan pengolahan daur ulang', ' Manajemen keselamatan kerja konstruksi tanpa insiden fatal']
  },
  insurtech_digital: {
    cat: 'Asuransi & Proteksi', tags: 'asuransi polis klaim proteksi jiwa kesehatan kendaraan',
    pal: {bg: '#F8FAFC', primary: '#2563EB', text: '#0F172A', accent: '#059669', soft: '#DBEAFE'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'INSURTECH & DIGITAL POLICIES', title: 'Proteksi Asuransi Mikro Mudah & Terjangkau',
    sub: 'Pembelian Polis Instan dari Ponsel dengan Pencairan Klaim Otomatis Berbasis Data',
    body: 'Persetujuan klaim asuransi kesehatan sederhana selesai dalam waktu kurang dari 30 menit.',
    cta: 'HITUNG PREMI ANDA SEKARANG', info: 'PT Asuransi Digital Mandiri Indonesia',
    st: ['shield', 'check', 'sparkle'],
    items: [' Pilihan premi mikro harian atau bulanan terjangkau', ' Klaim foto kuitansi online tanpa dokumen fisik', ' Jaringan rekanan ribuan rumah sakit dan klinik', ' Dukungan layanan darurat medis dan ambulans 24 jam']
  },
  architecture_planning: {
    cat: 'Arsitektur & Tata Ruang', tags: 'arsitektur denah interior fasad rumah tata kota',
    pal: {bg: '#F4F1EA', primary: '#2C3539', text: '#2A2E33', accent: '#C86D51', soft: '#E5DFD3'},
    hf: 'DM Serif Display', bf: 'Montserrat',
    kicker: 'SUSTAINABLE ARCHITECTURE STUDIO', title: 'Perencanaan Ruang Hidup Bernapas Alami',
    sub: 'Desain Hunian Tropis Modern dengan Ventilasi Silang Maksimal dan Pemanfaatan Cahaya Alami',
    body: 'Meraih pengakuan desain terbaik pada Festival Arsitektur Indonesia 2025.',
    cta: 'JADWALKAN KONSULTASI DESAIN', info: 'Studio Rancang Bangun Arsitektur Tropis',
    st: ['house', 'plant', 'sparkle'],
    items: [' Integrasi taman terbuka di dalam area rumah', ' Sirkulasi udara silang alami minim pendingin udara', ' Pilihan material kayu legal dan batu alam lokal', ' Gambar kerja detail dan simulasi tiga dimensi']
  },
  management_turnaround: {
    cat: 'Konsultasi Manajemen & Strategi', tags: 'konsultan manajemen bisnis strategi turnaround direksi',
    pal: {bg: '#0F172A', primary: '#C5A880', text: '#F8FAFC', accent: '#38BDF8', soft: '#1E293B'},
    hf: 'Playfair Display', bf: 'Plus Jakarta Sans',
    kicker: 'MANAGEMENT CONSULTING & ADVISORY', title: 'Restrukturisasi Strategis & Lompatan Performa',
    sub: 'Mendampingi Pemimpin Bisnis dalam Menavigasi Disrupsi Pasar dan Efisiensi Organisasi',
    body: 'Membantu 50+ korporasi memulihkan profitabilitas dan menciptakan nilai jangka panjang.',
    cta: 'JADWALKAN SESI STRATEGI EKSEKUTIF', info: 'Kantor Konsultan Manajemen Strategis Reksa',
    st: ['briefcase', 'check', 'bulb'],
    items: [' Diagnostik kesehatan operasional dan keuangan', ' Redesain struktur organisasi ramping dan lincah', ' Program pengendalian biaya terukur', ' Pelaksanaan program manajemen perubahan (Change Management)']
  },
  culinary_specialty_roastery: {
    cat: 'Kuliner & Roastery Kopi', tags: 'kopi roastery biji arabika seduh kafe barista',
    pal: {bg: '#140D09', primary: '#D4A373', text: '#FDFBF7', accent: '#E76F51', soft: '#2A1D16'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'SPECIALTY ROASTERY & COFFEE LAB', title: 'Eksplorasi Cita Rasa Kopi Nusantara',
    sub: 'Penyangraian Biji Kopi Single Origin Pilihan dengan Kurva Profil Rasa Presisi Tinggi',
    body: 'Menghubungkan langsung 40+ perkebunan petani kopi lokal dengan kafe terbaik.',
    cta: 'PESAN BIJI KOPI SANGRAI SEGAR', info: 'Laboratorium Sangrai Kopi Autentik Indonesia',
    st: ['coffee', 'mug', 'leaf'],
    items: [' Seleksi biji kopi arabika mutu tertinggi grade 1', ' Kurva sangrai digital terkalibrasi konsisten', ' Pengujian cupping berkala standar SCA', ' Pengiriman segar maksimal 3 hari setelah disangrai']
  },
  film_animation_studio: {
    cat: 'Perfilman & Animasi', tags: 'animasi film bioskop 3d render efek vfx sinema',
    pal: {bg: '#08080C', primary: '#8B5CF6', text: '#F5F3FF', accent: '#F43F5E', soft: '#181824'},
    hf: 'Bebas Neue', bf: 'Poppins',
    kicker: 'ANIMATION & VISUAL EFFECTS', title: 'Kisah Sinematik Animasi Generasi Baru',
    sub: 'Produksi Film Animasi Panjang Berkualitas Tinggi dengan Sentuhan Cerita Rakyat Nusantara',
    body: 'Karya kami telah diputar di festival film animasi internasional ternama.',
    cta: 'TONTON REEL KARYA KAMI', info: 'Studio Animasi & Visual Sinema Kreatif',
    st: ['hot', 'sparkle', 'bulb'],
    items: [' Visual visual effect (VFX) sinematik berstandar layar lebar', ' Perancangan karakter original dan latar dunia imajinatif', ' Perekaman suara dan tata musik orkestra orisinal', ' Pipeline produksi digital berbasis cloud render farm']
  },
  bigdata_ai_intelligence: {
    cat: 'Data & Intelijen Bisnis', tags: 'data ai analytics machine learning database bi',
    pal: {bg: '#050D1A', primary: '#38BDF8', text: '#F0F9FF', accent: '#A855F7', soft: '#0F223D'},
    hf: 'Bricolage Grotesque', bf: 'Roboto',
    kicker: 'ENTERPRISE DATA & AI INTELLIGENCE', title: 'Pengambilan Keputusan Berbasis Intelijen Data',
    sub: 'Membangun Gudang Data Modern (Modern Data Stack) dan Model Pembelajaran Mesin Prediktif',
    body: 'Membantu organisasi mentransformasikan data mentah menjadi wawasan bisnis bernilai tinggi.',
    cta: 'KONSULTASI ARSITEKTUR DATA', info: 'Pusat Analisis Data & Kecerdasan Buatan',
    st: ['bulb', 'bolt', 'check'],
    items: [' Data pipeline real-time dengan skalabilitas masif', ' Model prediktif churn nasabah dan tren pasar', ' Dasbor intelijen bisnis interaktif untuk pimpinan', ' Tata kelola data dan kepatuhan privasi ketat']
  },
  venture_syndicate_fund: {
    cat: 'Investasi Modal Ventura', tags: 'venture capital modal ventura startup investasi lp seed',
    pal: {bg: '#0F172A', primary: '#10B981', text: '#F8FAFC', accent: '#F59E0B', soft: '#1E293B'},
    hf: 'Montserrat', bf: 'Plus Jakarta Sans',
    kicker: 'VENTURE CAPITAL & SEED FUND', title: 'Investasi pada Pendiri Startup Berdaya Cipta Tinggi',
    sub: 'Mendanai Startup Tahap Awal di Sektor FinTech, Logistik, AgriTech, dan Solusi Iklim',
    body: 'Mengelola portofolio 40+ startup dengan tingkat kelipatan modal (MOIC) konsisten prima.',
    cta: 'AJUKAN PITCH DECK ANDA', info: 'Komite Investasi Ventura Cipta Nusantara',
    st: ['briefcase', 'sparkle', 'check'],
    items: [' Pendanaan tahap Pra-Awal hingga Seri A (Seed to Series A)', ' Akses jejaring korporasi dan mitra strategis global', ' Pendampingan tata kelola dan rekrutmen pimpinan kunci', ' Sinergi ekosistem portofolio investasi terintegrasi']
  }
};

// Generate 42 themes × 5 deck layouts = 210 distinct authentic presentation templates!
const PRESENTATION_LAYOUT_KEYS = ['deck_pitch', 'deck_report', 'deck_strategy', 'deck_agency', 'deck_workshop'];
const PRESENTATION_LAYOUT_LABELS = {
  deck_pitch: 'Investor Pitch Deck',
  deck_report: 'Laporan Kinerja Eksekutif',
  deck_strategy: 'Peta Jalan & Roadmap',
  deck_agency: 'Portofolio & Agensi',
  deck_workshop: 'Workshop & Pelatihan'
};

const PRESENTATION_TEMPLATES = [];
let _ptIndex = 0;

Object.entries(PRESENTATION_THEMES).forEach(([themeKey, th]) => {
  PRESENTATION_LAYOUT_KEYS.forEach(layoutKey => {
    const layoutLabel = PRESENTATION_LAYOUT_LABELS[layoutKey];
    const templateObj = {
      id: `pt${_ptIndex++}`,
      theme: themeKey,
      kind: 'presentation',
      layout: layoutKey,
      cat: th.cat,
      name: `${th.cat} · ${layoutLabel}`,
      search: `${th.cat} ${th.tags} ${th.title} presentasi ${layoutLabel} 16:9 ${themeKey}`.toLowerCase(),
      t: th
    };
    PRESENTATION_TEMPLATES.push(templateObj);
  });
});

// Append to global TEMPLATES array in the editor
const targetList = (typeof window !== 'undefined' && window.TEMPLATES) ? window.TEMPLATES : (typeof TEMPLATES !== 'undefined' ? TEMPLATES : null);
if (targetList) {
  PRESENTATION_TEMPLATES.forEach(t => targetList.push(t));
  console.log(`[Rakit Presentation Engine] Berhasil memuat ${PRESENTATION_TEMPLATES.length} templat presentasi resmi! Total templat aktif: ${targetList.length}`);
}
if (typeof window !== 'undefined') {
  window.PRESENTATION_TEMPLATES = PRESENTATION_TEMPLATES;
}
