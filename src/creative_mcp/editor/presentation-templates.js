// Rakit Desain / Canva Desktop — High-End Editorial Presentation Engine (210+ Templates)
// Pure Swiss & Editorial Grid, Zero AI-ish decorative clutter, stark architectural typography.
'use strict';

if (typeof LAYOUTS !== 'undefined') {
  // Hairline stroke divider helper
  const HLine = (x, y, w, col, op = 0.2) => Sh('line', x, y, w, 2, col, {opacity: op});
  const VLine = (x, y, h, col, op = 0.2) => R(x, y, 2, h, col, {opacity: op});

  // 1. Investor Pitch Deck (5 Slides: Executive Pitch, Problem Context, Solution Architecture, Traction & Unit Economics, The Ask)
  LAYOUTS.deck_pitch = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .09, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg.startsWith('#0') || p.bg.startsWith('#1');
    const ink = dark ? '#F8FAFC' : '#0F172A', subInk = dark ? '#94A3B8' : '#475569';
    const borderCol = dark ? '#334155' : '#CBD5E1';
    const splitX = W * .48;

    // Slide 1: Editorial Cover (Asymmetric Split with Clean Hairline Rule)
    const s1 = {
      bg: p.bg, title: '01 · Sampul Pitch Deck', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.35),
        Tx((t.kicker || 'VENTURE PITCH DECK').toUpperCase(), m, m * .7 + S * .02, W * .5, S * .025, p.primary, {bold: true, spacing: 5, font: t.bf}),
        Tx('2026 // CONFIDENTIAL', W - m - S * .3, m * .7 + S * .02, S * .3, S * .022, subInk, {align: 'right', spacing: 2, font: t.bf}),

        Tx(t.title, m, H * .3, W * .65, fitFs(t.title, W * .65, S * .11, 2, .6), ink, {bold: true, font: t.hf, lh: 1.08}),
        VLine(m, H * .58, H * .14, p.primary, 0.8),
        Tx(t.sub, m + S * .03, H * .58, W * .58, S * .036, subInk, {font: t.bf, lh: 1.45}),

        HLine(m, H - m - S * .06, W - 2 * m, borderCol, 0.25),
        Tx(t.info || 'Direktorat Strategis & Kemitraan', m, H - m - S * .03, W * .5, S * .026, subInk, {font: t.bf}),
        R(W - m - S * .28, H - m - S * .05, S * .28, S * .055, p.primary, {radius: 4}),
        Tx('PITCH PROPOSAL', W - m - S * .28, H - m - S * .038, S * .28, S * .022, '#FFFFFF', {bold: true, align: 'center', spacing: 2, font: t.bf})
      ]
    };

    // Slide 2: Problem & Market Inefficiency (2x2 Clean Hairline Grid)
    const s2 = {
      bg: p.bg, title: '02 · Permasalahan Pasar', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('01 / MARKET PAIN POINTS', m, m * .7 + S * .02, W * .4, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),
        Tx('Inefisiensi Struktural yang Dihadapi Industri', m, H * .18, W * .75, S * .07, ink, {bold: true, font: t.hf}),
        Tx('Kesenjangan antara kebutuhan pelanggan modern dengan infrastruktur warisan yang ada saat ini.', m, H * .26, W * .7, S * .03, subInk, {font: t.bf}),

        ...items.map((it, idx) => {
          const colW = (W - 2 * m - S * .05) / 2, row = Math.floor(idx / 2), col = idx % 2;
          const x = m + col * (colW + S * .05), y = H * .36 + row * (H * .27);
          const parts = it.split('—');
          return [
            R(x, y, colW, H * .23, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            Tx('0' + (idx + 1), x + S * .03, y + S * .03, S * .08, S * .04, p.primary, {bold: true, font: t.hf}),
            Tx(parts[0].trim(), x + S * .11, y + S * .03, colW - S * .14, S * .034, ink, {bold: true, font: t.hf}),
            HLine(x + S * .03, y + S * .085, colW - S * .06, borderCol, 0.2),
            Tx(parts[1] ? parts[1].trim() : 'Hambatan utama yang menurunkan produktivitas dan meningkatkan beban biaya tahunan.', x + S * .03, y + S * .11, colW - S * .06, S * .028, subInk, {font: t.bf, lh: 1.4})
          ];
        }).flat()
      ]
    };

    // Slide 3: Solution Architecture (Asymmetric Left-Right Layout)
    const s3 = {
      bg: p.bg, title: '03 · Arsitektur Solusi', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('02 / PROPOSISI NILAI', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),

        // Left Column (Bold Statement)
        Tx('Solusi Berbasis Teknologi Mandiri', m, H * .22, splitX - m - S * .04, S * .08, ink, {bold: true, font: t.hf, lh: 1.1}),
        Tx(t.body, m, H * .42, splitX - m - S * .04, S * .032, subInk, {font: t.bf, lh: 1.5}),
        R(m, H * .65, splitX - m - S * .04, S * .09, null, {stroke: p.primary, strokeW: 2, radius: 6}),
        Tx('EFISIENSI BIAYA HINGGA 40%', m, H * .68, splitX - m - S * .04, S * .026, p.primary, {bold: true, align: 'center', spacing: 2, font: t.bf}),

        VLine(splitX, H * .2, H * .65, borderCol, 0.35),

        // Right Column (3 Pillar Specs)
        ...[
          {num: '01', title: 'Skalabilitas Awan Tinggi', desc: 'Arsitektur modular siap menangani jutaan permintaan per detik.'},
          {num: '02', title: 'Keamanan Data Berlapis', desc: 'Protokol enkripsi data end-to-end berstandar kepatuhan internasional.'},
          {num: '03', title: 'Integrasi API Terbuka', desc: 'Konektivitas instan ke sistem enterprise yang telah berjalan tanpa migrasi rumit.'}
        ].flatMap((feat, idx) => {
          const y = H * .22 + idx * (H * .21), rx = splitX + S * .05, rw = W - rx - m;
          return [
            Tx(feat.num, rx, y, S * .08, S * .04, p.accent, {bold: true, font: t.hf}),
            Tx(feat.title, rx + S * .08, y, rw - S * .08, S * .036, ink, {bold: true, font: t.hf}),
            Tx(feat.desc, rx + S * .08, y + S * .05, rw - S * .08, S * .028, subInk, {font: t.bf, lh: 1.4}),
            HLine(rx, y + S * .16, rw, borderCol, 0.2)
          ];
        })
      ]
    };

    // Slide 4: Traction & High-Impact Metrics (Giant Display Numbers)
    const s4 = {
      bg: p.bg, title: '04 · Traksi & Pertumbuhan', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('03 / KEY TRACTION METRICS', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Pertumbuhan Konsisten & Efisiensi Unit Ekonomi', m, H * .18, W * .75, S * .07, ink, {bold: true, font: t.hf}),

        ...[
          {big: '+240%', label: 'PERTUMBUHAN TAHUNAN (YoY)', desc: 'Pertumbuhan pendapatan berulang organik tanpa kenaikan biaya akuisisi.'},
          {big: '89.4%', label: 'RETENSI PENGGUNA 12 BULAN', desc: 'Loyalitas pengguna tinggi berkat nilai tambah berkelanjutan pada produk.'},
          {big: 'Rp 65 M', label: 'VOLUME TRANSAKSI TAHUNAN', desc: 'Volume bruto yang telah diproses secara aman dalam 12 bulan terakhir.'}
        ].flatMap((kpi, idx) => {
          const colW = (W - 2 * m - S * .06) / 3, x = m + idx * (colW + S * .03);
          return [
            R(x, H * .32, colW, H * .52, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            HLine(x, H * .32, colW, p.primary, 1),
            Tx(kpi.big, x + S * .03, H * .38, colW - S * .06, S * .095, p.primary, {bold: true, font: t.hf}),
            Tx(kpi.label, x + S * .03, H * .52, colW - S * .06, S * .026, ink, {bold: true, spacing: 2, font: t.bf}),
            Tx(kpi.desc, x + S * .03, H * .61, colW - S * .06, S * .028, subInk, {font: t.bf, lh: 1.45})
          ];
        })
      ]
    };

    // Slide 5: The Ask & Leadership (Executive Closing)
    const s5 = {
      bg: p.bg, title: '05 · Pendanaan & Kemitraan', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('04 / INVESTMENT & NEXT STEPS', m, m * .7 + S * .02, W * .4, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),

        Tx('Mari Menghadirkan Dampak Bersama', m, H * .25, W * .65, S * .09, ink, {bold: true, font: t.hf}),
        Tx('Alokasi Pendanaan: 45% Ekspansi Riset & Produk · 35% Penetrasi Pasar Nasional · 20% Cadangan Operasional.', m, H * .39, W * .7, S * .032, subInk, {font: t.bf, lh: 1.5}),

        HLine(m, H * .52, W - 2 * m, borderCol, 0.25),

        Tx('KONTOR PUSAT & INFORMASI RESMI', m, H * .58, W * .4, S * .024, p.primary, {bold: true, spacing: 3, font: t.bf}),
        Tx(t.info || 'Kantor Manajemen Pusat · Hubungi Tim Kemitraan', m, H * .64, W * .45, S * .034, ink, {bold: true, font: t.bf}),
        Tx('Dokumen presentasi ini disiapkan khusus dan dilindungi kerahasiaan korporasi.', m, H * .72, W * .45, S * .026, subInk, {font: t.bf}),

        R(W - m - S * .36, H * .62, S * .36, S * .075, p.primary, {radius: 6}),
        Tx((t.cta || 'KIRIM UNDANGAN DISKUSI').toUpperCase(), W - m - S * .36, H * .645, S * .36, S * .024, '#FFFFFF', {bold: true, align: 'center', spacing: 2, font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 2. Executive Corporate Report
  LAYOUTS.deck_report = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .09, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg.startsWith('#0') || p.bg.startsWith('#1');
    const ink = dark ? '#F8FAFC' : '#0F172A', subInk = dark ? '#94A3B8' : '#475569';
    const borderCol = dark ? '#334155' : '#CBD5E1';

    const s1 = {
      bg: p.bg, title: '01 · Sampul Laporan Eksekutif', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.35),
        Tx('LAPORAN KINERJA RESMI // TAHUNAN', m, m * .7 + S * .02, W * .5, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx(t.title, m, H * .28, W * .72, fitFs(t.title, W * .72, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx(t.sub, m, H * .46, W * .65, S * .036, subInk, {font: t.bf, lh: 1.4}),
        HLine(m, H - m - S * .06, W - 2 * m, borderCol, 0.25),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .028, subInk, {font: t.bf})
      ]
    };

    const s2 = {
      bg: p.bg, title: '02 · Ringkasan Kinerja & KPI', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('EXECUTIVE KPI SUMMARY', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Realisasi Indikator Finansial & Operasional', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...[
          {k: 'Pencapaian Target Pendapatan', v: '+118%', s: 'Melampaui target RKAP tahunan.'},
          {k: 'Rasio Efisiensi Beban Pokok', v: '-22%', s: 'Penurunan biaya pasca otomatisasi.'},
          {k: 'Indeks Kepuasan Pengguna (NPS)', v: '94.6', s: 'Kategori kepuasan prima.'},
          {k: 'Kepatuhan Audit & Tata Kelola', v: '100%', s: 'Nol temuan pelanggaran kritis.'}
        ].flatMap((card, idx) => {
          const colW = (W - 2 * m - S * .09) / 4, x = m + idx * (colW + S * .03);
          return [
            R(x, H * .32, colW, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            Tx(card.v, x + S * .02, H * .38, colW - S * .04, S * .075, p.primary, {bold: true, font: t.hf}),
            HLine(x + S * .02, H * .48, colW - S * .04, borderCol, 0.2),
            Tx(card.k, x + S * .02, H * .51, colW - S * .04, S * .03, ink, {bold: true, font: t.hf}),
            Tx(card.s, x + S * .02, H * .61, colW - S * .04, S * .026, subInk, {font: t.bf, lh: 1.35})
          ];
        })
      ]
    };

    const s3 = {
      bg: p.bg, title: '03 · Realisasi Inisiatif Strategis', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('STRATEGIC INITIATIVES', m, m * .7 + S * .02, W * .4, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),
        Tx('Pencapaian Sasaran Utama Lintas Departemen', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const y = H * .3 + idx * (H * .135);
          return [
            R(m, y, W - 2 * m, H * .11, null, {stroke: borderCol, strokeW: 1, radius: 4}),
            Tx('0' + (idx + 1), m + S * .03, y + S * .03, S * .05, S * .036, p.primary, {bold: true, font: t.hf}),
            Tx(it, m + S * .09, y + S * .032, W - 2 * m - S * .12, S * .034, ink, {bold: true, font: t.bf})
          ];
        }).flat()
      ]
    };

    const s4 = {
      bg: p.bg, title: '04 · Analisis Tantangan & Solusi', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('RISK & OPERATIONS', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Mitigasi Risiko & Rekomendasi Alokasi', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W * .48, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Tinjauan Risiko Eksternal', m + S * .03, H * .36, W * .42, S * .038, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .03, H * .43, W * .42, S * .03, subInk, {font: t.bf, lh: 1.5}),
        R(W * .52, H * .32, W * .48 - m, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Arahan Dewan Direksi', W * .52 + S * .03, H * .36, W * .42 - m, S * .038, p.accent, {bold: true, font: t.hf}),
        Tx('Percepat digitalisasi rantai pasok dan lakukan pengawasan belanja modal ketat di setiap kuartal.', W * .52 + S * .03, H * .43, W * .42 - m, S * .03, subInk, {font: t.bf, lh: 1.5})
      ]
    };

    const s5 = {
      bg: p.bg, title: '05 · Penutup & Pengesahan', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('LAPORAN RESMI TELAH DISETUJUI', m, H * .3, W - 2 * m, S * .03, p.primary, {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Pengesahan Kinerja & Komitmen Masa Depan', m, H * .37, W - 2 * m, S * .085, ink, {bold: true, align: 'center', font: t.hf}),
        Tx('Ditandatangani oleh Dewan Direksi dan Komite Audit Perusahaan.', m, H * .48, W - 2 * m, S * .032, subInk, {align: 'center', font: t.bf}),
        HLine(W / 2 - S * .2, H * .65, S * .4, borderCol, 0.5),
        Tx('Sekretariat Dewan Komisaris · 2026', m, H * .68, W - 2 * m, S * .026, subInk, {align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 3. Strategy & Roadmap Deck
  LAYOUTS.deck_strategy = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .09, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg.startsWith('#0') || p.bg.startsWith('#1');
    const ink = dark ? '#F8FAFC' : '#0F172A', subInk = dark ? '#94A3B8' : '#475569';
    const borderCol = dark ? '#334155' : '#CBD5E1';

    const s1 = {
      bg: p.bg, title: '01 · Sampul Rencana Strategis', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.35),
        Tx('PETA JALAN STRATEGIS 2026-2030', m, m * .7 + S * .02, W * .5, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),
        Tx(t.title, m, H * .28, W * .72, fitFs(t.title, W * .72, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx(t.sub, m, H * .46, W * .65, S * .036, subInk, {font: t.bf, lh: 1.4}),
        HLine(m, H - m - S * .06, W - 2 * m, borderCol, 0.25),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .028, subInk, {font: t.bf})
      ]
    };

    const s2 = {
      bg: p.bg, title: '02 · Pilar Keberhasilan', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('CORE STRATEGIC PILLARS', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Empat Landasan Transformasi Berkelanjutan', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const colW = (W - 2 * m - S * .09) / 4, x = m + idx * (colW + S * .03);
          const parts = it.split('—');
          return [
            R(x, H * .32, colW, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            Tx('PILAR 0' + (idx + 1), x + S * .02, H * .36, colW - S * .04, S * .024, p.accent, {bold: true, spacing: 2, font: t.bf}),
            Tx(parts[0].trim(), x + S * .02, H * .43, colW - S * .04, S * .036, ink, {bold: true, font: t.hf}),
            HLine(x + S * .02, H * .53, colW - S * .04, borderCol, 0.2),
            Tx(parts[1] ? parts[1].trim() : 'Fokus utama pencapaian keunggulan kompetitif jangka panjang.', x + S * .02, H * .57, colW - S * .04, S * .026, subInk, {font: t.bf, lh: 1.35})
          ];
        }).flat()
      ]
    };

    const s3 = {
      bg: p.bg, title: '03 · Roadmap Tiga Horison', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('THREE HORIZONS OF GROWTH', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Tahapan Eksekusi Jangka Pendek, Menengah, dan Panjang', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...[
          {h: 'HORISON 1 · TAHUN 2026', t: 'Penguatan Inti Operasi', d: 'Optimalisasi infrastruktur eksisting, reduksi biaya, dan konsolidasi pasar domestik.'},
          {h: 'HORISON 2 · TAHUN 2027-2028', t: 'Ekspansi Lini Baru', d: 'Peluncuran produk komplementer dan penetrasi pasar regional berdaya saing.'},
          {h: 'HORISON 3 · TAHUN 2029-2030', t: 'Inovasi Disruptif', d: 'Membangun ekosistem platform mandiri berbasis teknologi terdepan.'}
        ].flatMap((hor, idx) => {
          const colW = (W - 2 * m - S * .06) / 3, x = m + idx * (colW + S * .03);
          return [
            R(x, H * .32, colW, H * .52, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            R(x, H * .32, colW, S * .06, p.primary, {radius: 4}),
            Tx(hor.h, x + S * .02, H * .338, colW - S * .04, S * .022, '#FFFFFF', {bold: true, align: 'center', spacing: 2, font: t.bf}),
            Tx(hor.t, x + S * .03, H * .43, colW - S * .06, S * .04, ink, {bold: true, font: t.hf}),
            Tx(hor.d, x + S * .03, H * .53, colW - S * .06, S * .03, subInk, {font: t.bf, lh: 1.45})
          ];
        })
      ]
    };

    const s4 = {
      bg: p.bg, title: '04 · Alokasi Sumber Daya', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('CAPITAL ALLOCATION', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Distribusi Anggaran Modal Kerja Strategis', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W - 2 * m, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('R&D & Teknologi: 45%  ·  Pemasaran & Pertumbuhan: 30%  ·  Operasional & SDM: 25%', m + S * .04, H * .38, W - 2 * m - S * .08, S * .036, p.primary, {bold: true, spacing: 1, font: t.bf}),
        HLine(m + S * .04, H * .45, W - 2 * m - S * .08, borderCol, 0.25),
        Tx(t.body, m + S * .04, H * .49, W - 2 * m - S * .08, S * .032, subInk, {font: t.bf, lh: 1.5})
      ]
    };

    const s5 = {
      bg: p.bg, title: '05 · Target Milestone', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('STRATEGIC MILESTONES', m, H * .28, W - 2 * m, S * .028, p.primary, {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Komitmen Eksekusi dengan Hasil Terukur', m, H * .35, W - 2 * m, S * .085, ink, {bold: true, align: 'center', font: t.hf}),
        Tx('Monitoring capaian dilakukan per kuartal bersama jajaran pimpinan eksekutif.', m, H * .46, W - 2 * m, S * .032, subInk, {align: 'center', font: t.bf}),
        HLine(W / 2 - S * .2, H * .6, S * .4, borderCol, 0.4),
        Tx(t.info, m, H * .65, W - 2 * m, S * .026, subInk, {align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 4. Creative Agency & Capabilities Deck
  LAYOUTS.deck_agency = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .09, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg.startsWith('#0') || p.bg.startsWith('#1');
    const ink = dark ? '#F8FAFC' : '#0F172A', subInk = dark ? '#94A3B8' : '#475569';
    const borderCol = dark ? '#334155' : '#CBD5E1';

    const s1 = {
      bg: p.bg, title: '01 · Sampul Agensi Kreatif', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.35),
        Tx('AGENCY CAPABILITIES & WORK PORTFOLIO', m, m * .7 + S * .02, W * .5, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx(t.title, m, H * .28, W * .72, fitFs(t.title, W * .72, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx(t.sub, m, H * .46, W * .65, S * .036, subInk, {font: t.bf, lh: 1.4}),
        HLine(m, H - m - S * .06, W - 2 * m, borderCol, 0.25),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .028, subInk, {font: t.bf})
      ]
    };

    const s2 = {
      bg: p.bg, title: '02 · Layanan Utama', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('CORE EXPERTISE', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Keahlian Desain & Strategi Komunikasi Terpadu', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const colW = (W - 2 * m - S * .06) / 2, row = Math.floor(idx / 2), col = idx % 2;
          const x = m + col * (colW + S * .06), y = H * .32 + row * (H * .27);
          const parts = it.split('—');
          return [
            R(x, y, colW, H * .23, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            Tx('0' + (idx + 1), x + S * .03, y + S * .03, S * .08, S * .038, p.primary, {bold: true, font: t.hf}),
            Tx(parts[0].trim(), x + S * .1, y + S * .03, colW - S * .13, S * .036, ink, {bold: true, font: t.hf}),
            HLine(x + S * .03, y + S * .085, colW - S * .06, borderCol, 0.2),
            Tx(parts[1] ? parts[1].trim() : 'Pendekatan strategis yang menghasilkan diferensiasi merek berdaya saing tinggi.', x + S * .03, y + S * .11, colW - S * .06, S * .028, subInk, {font: t.bf, lh: 1.4})
          ];
        }).flat()
      ]
    };

    const s3 = {
      bg: p.bg, title: '03 · Studi Kasus Dampak', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('FEATURED CASE STUDY', m, m * .7 + S * .02, W * .4, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),
        Tx('Dampak Nyata Kolaborasi Kreatif Kami', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W * .5, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Kampanye Merek Unggulan', m + S * .04, H * .37, W * .42, S * .04, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .04, H * .45, W * .42, S * .032, subInk, {font: t.bf, lh: 1.45}),
        R(W * .54, H * .32, W * .46 - m, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Metrik Keberhasilan Kampanye', W * .54 + S * .04, H * .37, W * .38 - m, S * .04, p.accent, {bold: true, font: t.hf}),
        Tx('+320% Interaksi Sosial · 1.4M Jangkauan Audiens · Rekognisi Industri Bergengsi', W * .54 + S * .04, H * .46, W * .38 - m, S * .032, ink, {font: t.bf, lh: 1.5})
      ]
    };

    const s4 = {
      bg: p.bg, title: '04 · Alur Kerja Empat Tahap', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('WORKFLOW & PROCESS', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Proses Eksekusi Presisi dan Terukur', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...[
          {s: '01', t: 'Discovery', d: 'Riset mendalam identitas, pasar, dan kompetitor.'},
          {s: '02', t: 'Strategy', d: 'Perumusan arah kreatif dan proposisi nilai merek.'},
          {s: '03', t: 'Design', d: 'Eksplorasi visual dan iterasi purwarupa karya.'},
          {s: '04', t: 'Delivery', d: 'Penerapan menyeluruh dan panduan merek resmi.'}
        ].flatMap((step, idx) => {
          const w = (W - 2 * m - S * .09) / 4, x = m + idx * (w + S * .03);
          return [
            R(x, H * .32, w, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            Tx(step.s, x + S * .02, H * .37, w - S * .04, S * .065, p.primary, {bold: true, font: t.hf}),
            Tx(step.t, x + S * .02, H * .46, w - S * .04, S * .038, ink, {bold: true, font: t.hf}),
            Tx(step.d, x + S * .02, H * .54, w - S * .04, S * .028, subInk, {font: t.bf, lh: 1.35})
          ];
        })
      ]
    };

    const s5 = {
      bg: p.bg, title: '05 · Penawaran Kerjasama', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('MULAI KOLABORASI', m, H * .28, W - 2 * m, S * .028, p.primary, {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Wujudkan Karya Ikonik Bersama Kami', m, H * .35, W - 2 * m, S * .085, ink, {bold: true, align: 'center', font: t.hf}),
        Tx('Sesi konsultasi eksplorasi awal dibuka setiap awal pekan.', m, H * .46, W - 2 * m, S * .032, subInk, {align: 'center', font: t.bf}),
        HLine(W / 2 - S * .2, H * .58, S * .4, borderCol, 0.4),
        Tx(t.info, m, H * .63, W - 2 * m, S * .026, subInk, {align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };

  // 5. Training & Workshop Masterclass Deck
  LAYOUTS.deck_workshop = function(W, H, t) {
    const p = t.pal, S = Math.min(W, H), m = S * .09, items = t.items.slice(0, 4);
    const dark = p.text === '#FFFFFF' || p.bg.startsWith('#0') || p.bg.startsWith('#1');
    const ink = dark ? '#F8FAFC' : '#0F172A', subInk = dark ? '#94A3B8' : '#475569';
    const borderCol = dark ? '#334155' : '#CBD5E1';

    const s1 = {
      bg: p.bg, title: '01 · Sampul Workshop Profesional', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.35),
        Tx('PROFESSIONAL WORKSHOP // MODUL RESMI', m, m * .7 + S * .02, W * .5, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),
        Tx(t.title, m, H * .28, W * .72, fitFs(t.title, W * .72, S * .11, 2, .6), ink, {bold: true, font: t.hf}),
        Tx(t.sub, m, H * .46, W * .65, S * .036, subInk, {font: t.bf, lh: 1.4}),
        HLine(m, H - m - S * .06, W - 2 * m, borderCol, 0.25),
        Tx(t.info, m, H - m - S * .03, W * .6, S * .028, subInk, {font: t.bf})
      ]
    };

    const s2 = {
      bg: p.bg, title: '02 · Silabus Modul Pembelajaran', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('LEARNING OBJECTIVES', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Kompetensi Utama yang Akan Dikuasai Peserta', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        ...items.map((it, idx) => {
          const colW = (W - 2 * m - S * .06) / 2, row = Math.floor(idx / 2), col = idx % 2;
          const x = m + col * (colW + S * .06), y = H * .32 + row * (H * .27);
          const parts = it.split('—');
          return [
            R(x, y, colW, H * .23, null, {stroke: borderCol, strokeW: 1, radius: 6}),
            Tx('MODUL 0' + (idx + 1), x + S * .03, y + S * .03, colW - S * .06, S * .024, p.primary, {bold: true, spacing: 2, font: t.bf}),
            Tx(parts[0].trim(), x + S * .03, y + S * .075, colW - S * .06, S * .036, ink, {bold: true, font: t.hf}),
            HLine(x + S * .03, y + S * .12, colW - S * .06, borderCol, 0.2),
            Tx(parts[1] ? parts[1].trim() : 'Pemahaman konsep dasar dan latihan aplikatif di dunia kerja nyata.', x + S * .03, y + S * .145, colW - S * .06, S * .028, subInk, {font: t.bf, lh: 1.35})
          ];
        }).flat()
      ]
    };

    const s3 = {
      bg: p.bg, title: '03 · Kerangka Konseptual', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('FRAMEWORK & THEORY', m, m * .7 + S * .02, W * .4, S * .024, p.accent, {bold: true, spacing: 4, font: t.bf}),
        Tx('Prinsip Fundamental Teruji di Lapangan', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W * .5, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Prinsip Utama Pelatihan', m + S * .04, H * .37, W * .42, S * .04, p.primary, {bold: true, font: t.hf}),
        Tx(t.body, m + S * .04, H * .45, W * .42, S * .032, subInk, {font: t.bf, lh: 1.45}),
        R(W * .54, H * .32, W * .46 - m, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Penerapan Kerja Nyata', W * .54 + S * .04, H * .37, W * .38 - m, S * .04, p.accent, {bold: true, font: t.hf}),
        Tx('Terapkan langsung pada alur kerja tim harian untuk meningkatkan produktivitas terukur.', W * .54 + S * .04, H * .45, W * .38 - m, S * .032, subInk, {font: t.bf, lh: 1.45})
      ]
    };

    const s4 = {
      bg: p.bg, title: '04 · Latihan & Simulasi Kasus', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('INTERACTIVE WORKSHOP', m, m * .7 + S * .02, W * .4, S * .024, p.primary, {bold: true, spacing: 4, font: t.bf}),
        Tx('Simulasi Kasus Kelompok Interaktif (25 Menit)', m, H * .18, W * .7, S * .07, ink, {bold: true, font: t.hf}),
        R(m, H * .32, W - 2 * m, H * .48, null, {stroke: borderCol, strokeW: 1, radius: 6}),
        Tx('Tahapan Latihan:', m + S * .04, H * .37, W - 2 * m - S * .08, S * .036, p.primary, {bold: true, font: t.hf}),
        Tx('1. Analisis skenario studi kasus riil yang dibagikan fasilitator.\n2. Rumuskan 3 inisiatif perbaikan berbasis metodologi yang telah dipelajari.\n3. Presentasikan kesimpulan solusi dalam waktu 3 menit per kelompok.', m + S * .04, H * .44, W - 2 * m - S * .08, S * .032, subInk, {font: t.bf, lh: 1.6})
      ]
    };

    const s5 = {
      bg: p.bg, title: '05 · Kesimpulan & Tanya Jawab', elements: [
        HLine(m, m * .7, W - 2 * m, borderCol, 0.3),
        Tx('SESI TANYA JAWAB', m, H * .28, W - 2 * m, S * .028, p.primary, {bold: true, align: 'center', spacing: 4, font: t.bf}),
        Tx('Rangkuman Materi & Rencana Tindak Lanjut', m, H * .35, W - 2 * m, S * .085, ink, {bold: true, align: 'center', font: t.hf}),
        Tx('Materi tayangan dan sertifikat digital dikirimkan ke email terdaftar seluruh peserta.', m, H * .46, W - 2 * m, S * .032, subInk, {align: 'center', font: t.bf}),
        HLine(W / 2 - S * .2, H * .58, S * .4, borderCol, 0.4),
        Tx(t.info, m, H * .63, W - 2 * m, S * .026, subInk, {align: 'center', font: t.bf})
      ]
    };

    return [s1, s2, s3, s4, s5];
  };
}

// ---------- 42 Authentic Professional Presentation Themes ----------
const PRESENTATION_THEMES = {
  fintech_ai: {
    cat: 'Finansial & FinTech', tags: 'fintech payment gateway perbankan ai investasi',
    pal: {bg: '#0A0E17', primary: '#38BDF8', text: '#FFFFFF', accent: '#0284C7', soft: '#111827'},
    hf: 'Plus Jakarta Sans', bf: 'Roboto',
    kicker: 'FINTECH & PAYMENT GATEWAY', title: 'Ekosistem Pembayaran Digital Cerdas 2026',
    sub: 'Solusi Settlement Real-Time dan Proteksi Transaksi Berbasis Kecerdasan Buatan',
    body: 'Pemrosesan 500+ transaksi per detik dengan latensi rata-rata di bawah 120ms.',
    cta: 'JELAJAHI SOLUSI FINTECH', info: 'Direktorat Teknologi Finansial · PT Solusi Bayar Indonesia',
    st: ['bolt', 'shield', 'sparkle'],
    items: ['Settlement instan antar bank 24/7', 'Deteksi fraud transaksi real-time', 'Integrasi Open Banking API resmi', 'Enkripsi berlapis standar PCI-DSS']
  },
  saas_enterprise: {
    cat: 'Teknologi & SaaS', tags: 'saas b2b automasi korporat cloud software',
    pal: {bg: '#0F172A', primary: '#38BDF8', text: '#FFFFFF', accent: '#818CF8', soft: '#1E293B'},
    hf: 'Bricolage Grotesque', bf: 'Plus Jakarta Sans',
    kicker: 'B2B SAAS WORKFLOW AUTOMATION', title: 'Platform Otomasi Operasional Korporat',
    sub: 'Mengintegrasikan Sistem ERP, CRM, dan Analisis Data dalam Satu Antarmuka',
    body: 'Meningkatkan produktivitas tim lintas divisi hingga 42% sejak bulan pertama.',
    cta: 'JADWALKAN DEMO ENTERPRISE', info: 'Divisi Solusi Korporasi · CloudFlow Enterprise',
    st: ['bulb', 'check', 'bolt'],
    items: ['Sinkronisasi data dua arah multi-platform', 'Mesin automasi tanpa kode terintegrasi', 'Audit log dan kepatuhan ISO 27001', 'Dukungan SLA ketersediaan 99.95%']
  },
  healthtech_telemed: {
    cat: 'Kesehatan & Medis', tags: 'healthtech medis rumah sakit dokter klinik',
    pal: {bg: '#0F1E17', primary: '#22C55E', text: '#FFFFFF', accent: '#38BDF8', soft: '#162C22'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'HEALTHTECH & REKAM MEDIS', title: 'Transformasi Layanan Kesehatan Digital',
    sub: 'Platform Telekonsultasi dan Rekam Medis Elektronik Terintegrasi Standar Kemenkes',
    body: 'Menghubungkan 1.200+ fasilitas kesehatan primer dengan spesialis di seluruh Indonesia.',
    cta: 'KONSULTASI SOLUSI RUMAH SAKIT', info: 'Konsorsium Inovasi Kesehatan Medika Digital',
    st: ['leaf', 'check', 'sparkle'],
    items: ['Rekam Medis Elektronik (RME) terpadu', 'Antrean faskes online dan e-resep', 'Triase pasien berbasis AI klinis', 'Keamanan data privasi pasien terenkripsi']
  },
  edutech_learning: {
    cat: 'Pendidikan & EduTech', tags: 'edutech sekolah kampus pelatihan kursus siswa',
    pal: {bg: '#0F1123', primary: '#6366F1', text: '#FFFFFF', accent: '#F59E0B', soft: '#181C38'},
    hf: 'Bricolage Grotesque', bf: 'Poppins',
    kicker: 'EDUTECH & ADAPTIVE LEARNING', title: 'Kurikulum Digital Masa Depan',
    sub: 'Pembelajaran Personalisasi Berbasis Analisis Minat dan Kecepatan Belajar Siswa',
    body: 'Digunakan oleh 45.000+ pelajar dan mahasiswa di 18 provinsi.',
    cta: 'PELAJARI KURIKULUM LENGKAP', info: 'Lembaga Pengembangan Pendidikan Cerdas Indonesia',
    st: ['graduation', 'bulb', 'sparkle'],
    items: ['Jalur belajar adaptif kecerdasan buatan', 'Dashboard perkembangan murid bagi guru', 'Bank soal kompetensi terstandar nasional', 'Akses materi offline ramah kuota']
  },
  agritech_smartfarm: {
    cat: 'Pertanian & AgriTech', tags: 'agritech tani pangan hidroponik irigasi suplai',
    pal: {bg: '#111A15', primary: '#84CC16', text: '#FFFFFF', accent: '#EAB308', soft: '#1D2A23'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'SMART FARMING & SUPPLY CHAIN', title: 'Modernisasi Rantai Pasok Pangan Nasional',
    sub: 'Sensor Tanah IoT, Prediksi Iklim Mikro, dan Distribusi Panen Langsung ke Pasar',
    body: 'Meningkatkan hasil panen petani mitra sebesar 31% dengan pengurangan limbah pascapanen.',
    cta: 'GABUNG MITRA AGRI DIGITAL', info: 'Inisiatif Kedaulatan Pangan Lestari AgriTech',
    st: ['leaf', 'plant', 'check'],
    items: ['Pemantauan kelembapan tanah otomatis', 'Prediksi cuaca mikro hiperlokal', 'Jalur distribusi langsung tanpa perantara', 'Pendanaan bibit dan sarana produksi tani']
  },
  logistics_fleet: {
    cat: 'Logistik & Rantai Pasok', tags: 'logistik armada kargo pengiriman gudang suplai',
    pal: {bg: '#0A101D', primary: '#2DD4BF', text: '#FFFFFF', accent: '#F97316', soft: '#142036'},
    hf: 'Archivo Black', bf: 'Montserrat',
    kicker: 'SMART FLEET & WAREHOUSING', title: 'Optimasi Logistik Rantai Dingin & Kargo',
    sub: 'Pelacakan Armada Telemetri Real-Time dan Tata Kelola Gudang Otomatis',
    body: 'Efisiensi konsumsi bahan bakar armada hingga 18% dan ketepatan waktu kirim 98.4%.',
    cta: 'OPTIMALKAN LOGISTIK ANDA', info: 'PT Nusantara Ekspedisi Logistik Terpadu',
    st: ['bolt', 'pin', 'check'],
    items: ['Pemetaan rute dinamis berbasis kemacetan', 'Kontrol suhu armada rantai dingin', 'Sistem manajemen gudang barcode terpusat', 'Dashboard utilisasi aset armada real-time']
  },
  clean_energy_solar: {
    cat: 'Energi & Lingkungan', tags: 'energi surya solar plts hijau listrik esg',
    pal: {bg: '#0B1713', primary: '#10B981', text: '#FFFFFF', accent: '#06B6D4', soft: '#152C25'},
    hf: 'Montserrat', bf: 'Roboto',
    kicker: 'RENEWABLE ENERGY & SOLAR POWER', title: 'Transisi Energi Bersih Industri 2026',
    sub: 'Pemasangan PLTS Atap dan Efisiensi Konsumsi Listrik Manufaktur Ramah Lingkungan',
    body: 'Reduksi emisi karbon terukur sebesar 14.000 ton CO2 setara per tahun per fasilitas pabrik.',
    cta: 'SIMULASI PENGHEMATAN ENERGI', info: 'Divisi Energi Baru & Terbarukan · Solaria Indonesia',
    st: ['plant', 'leaf', 'bulb'],
    items: ['Desain PLTS Atap industri bersertifikasi', 'Pembiayaan tanpa investasi awal terencana', 'Sistem pemantauan produksi daya online', 'Sertifikat kredit energi terbarukan (REC)']
  },
  corporate_audit: {
    cat: 'Tata Kelola & Kepatuhan Korporat', tags: 'audit kepatuhan tata kelola risiko manajemen korporat',
    pal: {bg: '#14181E', primary: '#D4AF37', text: '#FFFFFF', accent: '#94A3B8', soft: '#222832'},
    hf: 'Playfair Display', bf: 'Plus Jakarta Sans',
    kicker: 'INTERNAL AUDIT & GOVERNANCE', title: 'Kerangka Kepatuhan & Manajemen Risiko',
    sub: 'Memperkuat Tata Kelola Perusahaan yang Baik (Good Corporate Governance)',
    body: 'Pencegahan risiko operasional dan perlindungan integritas bisnis secara sistemik.',
    cta: 'TINJAU LAPORAN TATA KELOLA', info: 'Komite Audit & Kepatuhan Korporasi',
    st: ['shield', 'check', 'sparkle'],
    items: ['Matriks penilaian risiko divisi menyeluruh', 'Sistem pelaporan pelanggaran terenkripsi', 'Audit kepatuhan standar keuangan internasional', 'Rekomendasi perbaikan berkala dewan direksi']
  },
  esg_sustainability: {
    cat: 'Keberlanjutan & ESG', tags: 'esg emisi karbon keberlanjutan csr sosial hijau',
    pal: {bg: '#0D1A14', primary: '#34D399', text: '#FFFFFF', accent: '#6EE7B7', soft: '#193026'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'ESG REPORTING & IMPACT', title: 'Laporan Keberlanjutan & Dampak Sosial',
    sub: 'Transparansi Kinerja Lingkungan, Kesejahteraan Sosial, dan Integritas Korporasi',
    body: 'Pencapaian target net-zero emisi karbon operasional fase pertama tercapai lebih awal.',
    cta: 'BACA LAPORAN ESG LENGKAP', info: 'Dewan Keberlanjutan Korporasi Hijau Nusantara',
    st: ['leaf', 'plant', 'sparkle'],
    items: ['Penurunan intensitas energi pabrik 22%', 'Program pemberdayaan komunitas sekitar', 'Kesetaraan gender dalam kepemimpinan senior', 'Pengelolaan limbah tanpa pembuangan akhir']
  },
  cybersecurity_soc: {
    cat: 'Keamanan Siber & IT', tags: 'cybersecurity keamanan siber hacker enkripsi server',
    pal: {bg: '#070B12', primary: '#00F0FF', text: '#FFFFFF', accent: '#818CF8', soft: '#111827'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'CYBER DEFENSE & SOC OPERATIONS', title: 'Pertahanan Siber Aktif & Keamanan Cloud',
    sub: 'Pusat Operasi Keamanan 24/7 dan Deteksi Ancaman Siber Berbasis Intelijen Mesin',
    body: 'Menetralkan 100% insiden upaya intrusi tanpa downtime data kritis pelanggan.',
    cta: 'AUDIT POSTUR KEAMANAN ANDA', info: 'Pusat Tanggap Insiden Keamanan Siber Korporat',
    st: ['shield', 'bolt', 'check'],
    items: ['Security Operations Center (SOC) siaga 24/7', 'Uji penetrasi dan simulasi serangan berkala', 'Arsitektur Zero Trust Network Access (ZTNA)', 'Pelatihan kesadaran keamanan bagi seluruh staf']
  },
  proptech_marketplace: {
    cat: 'Properti & Real Estate', tags: 'proptech properti rumah apartemen investasi sewa',
    pal: {bg: '#0E131F', primary: '#F59E0B', text: '#FFFFFF', accent: '#D97706', soft: '#182033'},
    hf: 'Montserrat', bf: 'Plus Jakarta Sans',
    kicker: 'PROPTECH & REAL ESTATE INVESTMENT', title: 'Platform Investasi Properti Digital',
    sub: 'Kepemilikan Fraksional Properti Komersial Prima dengan Legalitas Transparan',
    body: 'Memberikan imbal hasil sewa stabil rata-rata 8.5% per tahun bagi para investor.',
    cta: 'LIHAT DAFTAR PROPERTI PILIHAN', info: 'PT Investasi Properti Digital Indonesia',
    st: ['house', 'pin', 'check'],
    items: ['Verifikasi sertifikat tanah instan online', 'Perhitungan imbal hasil sewa otomatis', 'Pengelolaan operasional penyewa terpadu', 'Likuiditas pasar sekunder bagi pemodal']
  },
  retail_omnichannel: {
    cat: 'Ritel & E-Commerce', tags: 'ritel ecommerce toko kasir pos belanja logistik',
    pal: {bg: '#14110E', primary: '#FB923C', text: '#FFFFFF', accent: '#F59E0B', soft: '#241E1A'},
    hf: 'Bebas Neue', bf: 'Poppins',
    kicker: 'OMNICHANNEL RETAIL EXPERIENCE', title: 'Ekspansi Ritel Terintegrasi Offline-Online',
    sub: 'Menyatukan Pengalaman Belanja di Toko Fisik dan Aplikasi Digital Tanpa Hambatan',
    body: 'Peningkatan nilai rata-rata keranjang belanja (AOV) sebesar 38% lintas saluran.',
    cta: 'PELAJARI SOLUSI RITEL KAMI', info: 'Divisi Inovasi Ritel Terpadu · RetailPro',
    st: ['pricetag', 'hot', 'check'],
    items: ['Sinkronisasi stok inventaris real-time', 'Program loyalitas poin terpusat', 'Layanan Ambil di Toko terintegrasi', 'Analisis arus pengunjung berbasis kamera cerdas']
  },
  biotech_pharma: {
    cat: 'Bioteknologi & Farmasi', tags: 'biotek farmasi obat vaksin uji klinis lab',
    pal: {bg: '#0B1520', primary: '#38BDF8', text: '#FFFFFF', accent: '#2DD4BF', soft: '#152538'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'BIOTECHNOLOGY & CLINICAL TRIALS', title: 'Riset Terapi Presisi & Kemandirian Farmasi',
    sub: 'Inovasi Molekul Obat Baru untuk Penyakit Tropis dengan Uji Klinis Terstandar WHO',
    body: 'Mempercepat fase penemuan obat baru hingga 50% lebih efisien dari metode konvensional.',
    cta: 'TELAAH HASIL UJI KLINIS', info: 'Pusat Riset Bioteknologi Terapan Nusantara',
    st: ['leaf', 'bulb', 'sparkle'],
    items: ['Sintesis molekul obat berbahan baku lokal', 'Uji praklinis dan kepatuhan bioetika', 'Fasilitas laboratorium berstandar GLP', 'Kemitraan riset global institusi terkemuka']
  },
  ev_mobility: {
    cat: 'Otomotif & Mobilitas', tags: 'ev motor listrik baterai spklu transportasi',
    pal: {bg: '#080808', primary: '#00E676', text: '#FFFFFF', accent: '#00B0FF', soft: '#1A1A1A'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'EV ECOSYSTEM & INFRASTRUCTURE', title: 'Jaringan Pengisian Daya Kendaraan Listrik',
    sub: 'Penggelaran Stasiun Pengisian Cepat (Ultra Fast SPKLU) di Koridor Utama Antar Kota',
    body: 'Tersedia di 240+ titik strategis dengan waktu pengisian rata-rata 25 menit.',
    cta: 'PETA JARINGAN SPKLU', info: 'Konsorsium Infrastruktur EV Nusantara Raya',
    st: ['bolt', 'pin', 'check'],
    items: ['Pengisian daya berkecepatan 150 kW DC', 'Aplikasi reservasi stasiun pengisian mobile', 'Pasokan energi bersih bersertifikat', 'Kemitraan armada logistik komersial']
  },
  cloud_devops: {
    cat: 'Cloud & Rekayasa Perangkat Lunak', tags: 'cloud devops kubernetes aws gcp microservices',
    pal: {bg: '#0B0F19', primary: '#60A5FA', text: '#FFFFFF', accent: '#34D399', soft: '#151D2E'},
    hf: 'Bricolage Grotesque', bf: 'Roboto',
    kicker: 'DEVOPS & CLOUD ARCHITECTURE', title: 'Modernisasi Infrastruktur Multi-Cloud',
    sub: 'Otomasi Pipeline CI/CD, Orkestrasi Kontainer, dan Skalabilitas Tanpa Gangguan',
    body: 'Memangkas waktu deployment dari hitungan hari menjadi menit dengan tingkat kegagalan 0.01%.',
    cta: 'KONSULTASI ARSITEKTUR CLOUD', info: 'Tim Rekayasa Keandalan Sistem (SRE)',
    st: ['bolt', 'check', 'sparkle'],
    items: ['Klaster Kubernetes terdistribusi otomatis', 'Pipeline rilis perangkat lunak nir-henti', 'Observabilitas dan telemetri metrik sistem', 'Optimasi biaya komputasi awan (FinOps)']
  },
  growth_marketing: {
    cat: 'Pemasaran & Pertumbuhan', tags: 'marketing iklan ads seo conversion funnel b2b',
    pal: {bg: '#140D1D', primary: '#C084FC', text: '#FFFFFF', accent: '#F472B6', soft: '#221532'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'PERFORMANCE & GROWTH MARKETING', title: 'Strategi Akuisisi & Retensi Pengguna Skala Besar',
    sub: 'Optimalisasi Corong Konversi Multi-Saluran dengan Pendekatan Berbasis Eksperimen Data',
    body: 'Menurunkan Customer Acquisition Cost (CAC) sebesar 34% sambil menaikkan LTV 1.8x.',
    cta: 'MULAI KAMPANYE PERTUMBUHAN', info: 'Agensi Akselerasi Pertumbuhan Digital',
    st: ['megaphone', 'hot', 'sparkle'],
    items: ['Segmentasi audiens prediktif berbasis perilaku', 'Pengujian A/B materi kreatif iklan dinamis', 'Optimasi mesin pencari (SEO) teknikal', 'Automasi retensi email dan notifikasi cerdas']
  },
  brand_identity: {
    cat: 'Identitas Visual & Merek', tags: 'branding logo warna font identitas pedoman visual',
    pal: {bg: '#141414', primary: '#D4AF37', text: '#FFFFFF', accent: '#E5E7EB', soft: '#242424'},
    hf: 'Playfair Display', bf: 'Plus Jakarta Sans',
    kicker: 'BRAND IDENTITY GUIDELINES', title: 'Panduan Merek & Desain Terpadu 2026',
    sub: 'Standar Konsistensi Bahasa Visual, Tipografi, Tone of Voice, dan Penerapan Aset',
    body: 'Memastikan pesan merek tersampaikan secara kohesif di seluruh titik kontak pelanggan.',
    cta: 'LIHAT PANDUAN LENGKAP', info: 'Studio Desain Strategis & Identitas Merek',
    st: ['sparkle', 'bulb', 'check'],
    items: ['Skala tipografi dan hirarki teks resmi', 'Palet warna primer, sekunder, dan aksesibilitas', 'Pedoman fotografi dan ilustrasi editorial', 'Contoh penerapan pada kemasan dan media digital']
  },
  hr_talent: {
    cat: 'SDM & Budaya Kerja', tags: 'hr hrd rekrutmen karyawan budaya kantor talent',
    pal: {bg: '#140E15', primary: '#F472B6', text: '#FFFFFF', accent: '#FB7185', soft: '#241825'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'PEOPLE & CULTURE STRATEGY', title: 'Pengembangan Talenta & Tempat Kerja Idaman',
    sub: 'Membangun Budaya Performa Tinggi, Kesejahteraan Karyawan, dan Jalur Karier Jelas',
    body: 'Tingkat retensi karyawan mencapai 94% dengan indeks kepuasan kerja kategori luar biasa.',
    cta: 'IKUTI PROGRAM ONBOARDING', info: 'Direktorat Sumber Daya Manusia & Organisasi',
    st: ['briefcase', 'check', 'sparkle'],
    items: ['Matriks jenjang karier dan transparansi kompensasi', 'Program pembinaan kepemimpinan berkala', 'Kebijakan kerja fleksibel berbasis output', 'Evaluasi kinerja berbasis OKR objektif']
  },
  legal_tech: {
    cat: 'Administrasi Kontrak & Kepatuhan Bisnis', tags: 'kontrak administrasi kepatuhan operasional perjanjian',
    pal: {bg: '#0F131C', primary: '#94A3B8', text: '#FFFFFF', accent: '#CBD5E1', soft: '#1B2232'},
    hf: 'Cinzel', bf: 'Roboto',
    kicker: 'CONTRACT LIFECYCLE MANAGEMENT', title: 'Manajemen Kontrak Cerdas & Efisiensi Operasional',
    sub: 'Digitalisasi Alur Persetujuan Perjanjian Kerjasama dengan Tanda Tangan Elektronik Sah',
    body: 'Mempercepat siklus penandatanganan kontrak dari rata-rata 14 hari menjadi 4 jam.',
    cta: 'KONSULTASI MITRA KORPORASI', info: 'Konsultan Manajemen Kontrak & Transformasi Digital',
    st: ['shield', 'check', 'sparkle'],
    items: ['Standarisasi draf perjanjian bisnis resmi', 'Tanda tangan digital tersertifikasi resmi', 'Notifikasi pengingat masa perpanjangan kontrak', 'Repositori dokumen perjanjian terpusat dan aman']
  },
  luxury_hospitality: {
    cat: 'Pariwisata & Perhotelan', tags: 'hotel resor liburan vila wisata bali lombok',
    pal: {bg: '#14120F', primary: '#D4AF37', text: '#FFFFFF', accent: '#C5A880', soft: '#24201A'},
    hf: 'Playfair Display', bf: 'Lora',
    kicker: 'LUXURY ECO-RESORT & TOURISM', title: 'Pengalaman Menginap Berkelas Dunia',
    sub: 'Harmoni Kemewahan Fasilitas Bintang Lima dengan Kelestarian Alam Budaya Lokal',
    body: 'Tingkat okupansi tahunan rata-rata 89% dengan penghargaan Best Boutique Resort.',
    cta: 'RESERVASI SUITE EKSKLUSIF', info: 'Manajemen Resor Bintang Lima Nusantara',
    st: ['flower', 'sparkle', 'leaf'],
    items: ['Vila privat dengan kolam renang tanpa batas', 'Pengalaman kuliner hidangan bahan organik lokal', 'Spa relaksasi tradisional berstandar global', 'Komitmen nol plastik dan efisiensi air mandiri']
  },
  fnb_franchise_expansion: {
    cat: 'Kuliner & Waralaba', tags: 'waralaba franchise resto cafe kuliner cabang fnb',
    pal: {bg: '#160E08', primary: '#F97316', text: '#FFFFFF', accent: '#EA580C', soft: '#281B10'},
    hf: 'Archivo Black', bf: 'Poppins',
    kicker: 'FRANCHISE EXPANSION OPPORTUNITY', title: 'Peluang Kemitraan Waralaba Kuliner 2026',
    sub: 'Model Bisnis Teruji dengan Balik Modal Cepat dan Pasokan Bahan Baku Terstandar',
    body: 'Telah membuka 180+ gerai sukses di seluruh kota besar di Indonesia.',
    cta: 'DAFTAR MENJADI MITRA WARALABA', info: 'Divisi Pengembangan Kemitraan · Gerai Rasa Group',
    st: ['mug', 'hot', 'pricetag'],
    items: ['Proyeksi balik modal (ROI) 12-16 bulan terukur', 'Pasokan bumbu dan bahan baku terpusat', 'Pelatihan menyeluruh untuk kru dan manajer', 'Dukungan pemasaran nasional berkelanjutan']
  },
  gaming_interactive: {
    cat: 'Game & Hiburan Digital', tags: 'game studio esports gaming turnamen anime 3d',
    pal: {bg: '#0E071A', primary: '#C084FC', text: '#FFFFFF', accent: '#F43F5E', soft: '#1F1138'},
    hf: 'Bebas Neue', bf: 'Roboto',
    kicker: 'GAME STUDIO & ESPORTS ECOSYSTEM', title: 'Ekspansi IP Game Mobile Berstandar Global',
    sub: 'Pengembangan Permainan Lintas Platform dengan Narasi Lokal dan Grafis Mutakhir',
    body: 'Mencapai 8.5 juta unduhan organik dengan rating pengguna 4.8 bintang di toko aplikasi.',
    cta: 'MAINKAN VERSI ALPHA SEKARANG', info: 'Studio Animasi & Game Interaktif Nusantara',
    st: ['bolt', 'hot', 'sparkle'],
    items: ['Mesin grafis optimal untuk ponsel spesifikasi menengah', 'Turnamen kompetitif liga komunitas resmi', 'Monetisasi ramah pemain berbasis item kosmetik', 'Pembaruan konten cerita musiman berkala']
  },
  digital_agency: {
    cat: 'Agensi Kreatif & Media', tags: 'agensi kreatif studio desain video iklan kampanye',
    pal: {bg: '#0B0D15', primary: '#60A5FA', text: '#FFFFFF', accent: '#F43F5E', soft: '#151928'},
    hf: 'Bricolage Grotesque', bf: 'Plus Jakarta Sans',
    kicker: 'CREATIVE & MEDIA AGENCY', title: 'Kreativitas Berdampak untuk Brand Terdepan',
    sub: 'Menghubungkan Brand dengan Generasi Baru Melalui Cerita Otentik dan Produksi Visual Prima',
    body: 'Pemenang 14 penghargaan kampanye periklanan terbaik tingkat regional.',
    cta: 'DISKUSIKAN PROYEK ANDA', info: 'Agensi Kreatif Lintas Saluran · Kreasi Citra',
    st: ['sparkle', 'megaphone', 'hot'],
    items: ['Strategi komunikasi kampanye merek terpadu', 'Produksi iklan video sinematik berkualitas', 'Manajemen aktivasi media sosial dan kreator', 'Analisis sentimen publik dan jangkauan audiens']
  },
  industry_smart_factory: {
    cat: 'Manufaktur & Industri', tags: 'pabrik industri manufaktur robot iot otomasi mesin',
    pal: {bg: '#141416', primary: '#F59E0B', text: '#FFFFFF', accent: '#E11D48', soft: '#242428'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'INDUSTRY 4.0 & SMART MANUFACTURING', title: 'Digitalisasi Operasi Pabrik Masa Depan',
    sub: 'Penerapan Sensor Mesin Pintar dan Pemeliharaan Prediktif untuk Meminimalisir Downtime',
    body: 'Efisiensi output lini perakitan meningkat 28% dengan penurunan cacat produk di bawah 0.2%.',
    cta: 'JADWALKAN TUR PABRIK CERDAS', info: 'Departemen Teknologi Manufaktur Maju',
    st: ['bolt', 'check', 'bulb'],
    items: ['Sensor pemantauan getaran mesin nirkabel', 'Pemeliharaan prediktif sebelum terjadi kerusakan', 'Integrasi sistem SCADA dengan analisis awan', 'Dasbor keselamatan kerja pekerja pabrik digital']
  },
  circular_economy: {
    cat: 'Ekonomi Sirkular & Daur Ulang', tags: 'daur ulang limbah sampah sirkular plastik ramah lingkungan',
    pal: {bg: '#0C1814', primary: '#10B981', text: '#FFFFFF', accent: '#34D399', soft: '#162C24'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'CIRCULAR ECONOMY & ZERO WASTE', title: 'Ekosistem Pengolahan Sampah Industri Berkelanjutan',
    sub: 'Mengubah Limbah Kemasan Menjadi Material Daur Ulang Berkualitas Tinggi untuk Manufaktur',
    body: 'Mengolah 25.000 ton limbah plastik pascakonsumen per tahun menjadi bahan baku siap pakai.',
    cta: 'GABUNG PROGRAM DAUR ULANG', info: 'Inisiatif Ekonomi Sirkular Bersih Nusantara',
    st: ['leaf', 'plant', 'check'],
    items: ['Sistem pelacakan sumber material daur ulang', 'Standar kemurnian biji plastik daur ulang industri', 'Sertifikasi rantai pasok ramah lingkungan', 'Kemitraan bank sampah komunitas terpadu']
  },
  wealth_management: {
    cat: 'Investasi & Perbankan Swasta', tags: 'wealth saham obligasi reksadana aset portofolio pensiun',
    pal: {bg: '#0B111A', primary: '#D4AF37', text: '#FFFFFF', accent: '#93C5FD', soft: '#152030'},
    hf: 'Cinzel', bf: 'Roboto',
    kicker: 'PRIVATE WEALTH MANAGEMENT', title: 'Pengelolaan Aset Keluarga & Portofolio Strategis',
    sub: 'Perlindungan Nilai Kekayaan Jangka Panjang Melalui Alokasi Multi-Aset Global dan Domestik',
    body: 'Dipercaya mengelola dana nasabah institusi dan individu bernilai kekayaan tinggi.',
    cta: 'HUBUNGI PENASIHAT INVESTASI', info: 'Kantor Pengelolaan Aset Prima · Private Wealth',
    st: ['shield', 'sparkle', 'check'],
    items: ['Alokasi aset defensif dan terukur', 'Perencanaan suksesi waris bisnis keluarga', 'Akses produk investasi eksklusif pasar privat', 'Laporan kinerja portofolio terperinci berkala']
  },
  autonomous_drones: {
    cat: 'Dirgantara & Drone Otonom', tags: 'drone uav udara inspeksi sensor pemetaan kargo',
    pal: {bg: '#0A0F1D', primary: '#06B6D4', text: '#FFFFFF', accent: '#3B82F6', soft: '#15203B'},
    hf: 'Archivo Black', bf: 'Montserrat',
    kicker: 'AUTONOMOUS DRONE SOLUTIONS', title: 'Inspeksi Udara Cerdas & Logistik Tanpa Awak',
    sub: 'Pengawasan Infrastruktur Kelistrikan, Pertambangan, dan Pemetaan Topografi Berakurasi Tinggi',
    body: 'Memangkas waktu survei medan berat hingga 80% dengan tingkat presisi sentimeter.',
    cta: 'JELAJAHI KAPABILITAS SURVEI', info: 'Divisi Teknologi Drone Mandiri Indonesia',
    st: ['bolt', 'pin', 'check'],
    items: ['Kamera termal dan LiDAR resolusi tinggi', 'Penerbangan otonom di luar jangkauan visual', 'Analisis cacat infrastruktur otomatis berbasis AI', 'Sertifikasi pilot dan keselamatan penerbangan resmi']
  },
  media_ott_platform: {
    cat: 'Media & Penyiaran Digital', tags: 'ott streaming media film podcast audio video',
    pal: {bg: '#080808', primary: '#E50914', text: '#FFFFFF', accent: '#F59E0B', soft: '#1A1A1A'},
    hf: 'Bebas Neue', bf: 'Roboto',
    kicker: 'DIGITAL STREAMING & ENTERTAINMENT', title: 'Platform Konten Sinematik Nusantara',
    sub: 'Menghadirkan Film Cerita Asli, Dokumenter Budaya, dan Serial Eksklusif Berkualitas 4K',
    body: '3.2 juta pelanggan aktif bulanan dengan waktu tonton rata-rata 110 menit per hari.',
    cta: 'NIKMATI TAYANGAN UNGGULAN', info: 'Layanan Media Hiburan Berkelanjutan',
    st: ['hot', 'sparkle', 'pricetag'],
    items: ['Kompresi video cerdas hemat kuota pengguna', 'Kurasi konten lokal berdaya saing global', 'Akses tayangan bebas iklan pada paket premium', 'Fitur tonton luring (offline download) di ponsel']
  },
  medical_diagnostics: {
    cat: 'Alat Kesehatan & Diagnostik', tags: 'alkes laboratorium tes darah deteksi medis biosensor',
    pal: {bg: '#0A141E', primary: '#38BDF8', text: '#FFFFFF', accent: '#10B981', soft: '#142638'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'POINT-OF-CARE DIAGNOSTICS', title: 'Perangkat Deteksi Medis Portabel & Cepat',
    sub: 'Hasil Analisis Sampel Darah Akurat dalam 15 Menit untuk Fasilitas Kesehatan Terpencil',
    body: 'Telah digunakan di 340 puskesmas daerah tertinggal, terdepan, dan terluar.',
    cta: 'DAPATKAN SPESIFIKASI ALAT', info: 'Inovasi Alat Kesehatan Diagnostik Medis',
    st: ['check', 'bulb', 'shield'],
    items: ['Akurasi diagnostik setara laboratorium rujukan (98.8%)', 'Desain kokoh dengan baterai tahan hingga 12 jam', 'Pengiriman data otomatis ke sistem rekam medis', 'Biaya per pengujian sangat terjangkau untuk faskes']
  },
  microfinance_umkm: {
    cat: 'Inklusi Keuangan & UMKM', tags: 'umkm mikro modal usaha kredit koperasi warung',
    pal: {bg: '#141108', primary: '#D97706', text: '#FFFFFF', accent: '#10B981', soft: '#262012'},
    hf: 'Archivo Black', bf: 'Poppins',
    kicker: 'MICROFINANCE & INCLUSION', title: 'Pemberdayaan Modal Usaha UMKM Indonesia',
    sub: 'Akses Pendanaan Produktif Cepat, Tanpa Jaminan Rumit, Didampingi Edukasi Bisnis',
    body: 'Telah menyalurkan modal usaha produktif kepada 120.000+ pelaku usaha mikro perempuan.',
    cta: 'AJUKAN PENDAMPINGAN USAHA', info: 'Lembaga Keuangan Mikro Komunitas Berdaya',
    st: ['check', 'bulb', 'sparkle'],
    items: ['Bunga kompetitif dengan skema cicilan mingguan', 'Pelatihan pembukuan keuangan toko digital', 'Pendampingan manajemen inventaris usaha', 'Skoring kredit berbasis rekam jejak komunitas']
  },
  smart_governance: {
    cat: 'Pemerintahan & Pelayanan Publik', tags: 'pemerintah kota smart city pelayanan perizinan ktp kependudukan',
    pal: {bg: '#0B1220', primary: '#3B82F6', text: '#FFFFFF', accent: '#10B981', soft: '#15223C'},
    hf: 'Montserrat', bf: 'Plus Jakarta Sans',
    kicker: 'DIGITAL PUBLIC SERVICES & SMART CITY', title: 'Satu Portal Layanan Terpadu Warga Kota',
    sub: 'Pengurusan Izin, Pelaporan Warga, dan Pembayaran Pajak Daerah dalam Satu Genggaman',
    body: 'Tingkat kepuasan warga atas pelayanan administrasi daerah melonjak menjadi 92.4%.',
    cta: 'JELAJAHI PORTAL WARGA', info: 'Dinas Komunikasi, Informatika & Tata Ruang Kota',
    st: ['shield', 'pin', 'check'],
    items: ['Integrasi seluruh instansi pelayanan kependudukan', 'Pelaporan kendala fasilitas kota secara transparan', 'Pembayaran retribusi nontunai bebas perantara', 'Dasbor komando pengendalian kota (Command Center)']
  },
  pharma_distribution: {
    cat: 'Rantai Pasok Farmasi', tags: 'farmasi obat apotek distribusi rantai dingin vaksin',
    pal: {bg: '#0A1622', primary: '#0284C7', text: '#FFFFFF', accent: '#059669', soft: '#15293E'},
    hf: 'Poppins', bf: 'Roboto',
    kicker: 'PHARMACEUTICAL SUPPLY INTEGRITY', title: 'Jaminan Ketahanan & Distribusi Obat Nasional',
    sub: 'Sistem Rantai Dingin Terakreditasi BPOM Menjangkau 8.000+ Apotek dan Rumah Sakit',
    body: 'Ketepatan distribusi pasokan obat esensial mencapai 99.4% dengan jaminan keaslian 100%.',
    cta: 'KEMITRAAN DISTRIBUSI FARMASI', info: 'Distributor Farmasi Terakreditasi CDOB',
    st: ['check', 'shield', 'leaf'],
    items: ['Sertifikasi Cara Distribusi Obat yang Baik (CDOB)', 'Kontrol suhu gudang dan armada berbasis IoT', 'Pelacakan nomor batch obat terverifikasi resmi', 'Pasokan darurat 24 jam untuk rumah sakit rujukan']
  },
  telecom_network: {
    cat: 'Telekomunikasi & Jaringan', tags: 'telekomunikasi 5g fiber optic sinyal internet tower',
    pal: {bg: '#0A0E1A', primary: '#6366F1', text: '#FFFFFF', accent: '#06B6D4', soft: '#182138'},
    hf: 'Archivo Black', bf: 'Montserrat',
    kicker: 'TELECOMMUNICATION & 5G ROLLOUT', title: 'Penggelaran Jaringan Pita Lebar Berkecepatan Tinggi',
    sub: 'Ekspansi Jaringan Serat Optik dan Menara Pemancar 5G Mendukung Transformasi Digital',
    body: 'Menghubungkan 12 juta rumah tangga dengan latensi ultra rendah untuk aplikasi kritis.',
    cta: 'CEK JANGKAUAN FIBER OPTIK', info: 'Infrastruktur Jaringan Telekomunikasi Prima',
    st: ['bolt', 'pin', 'check'],
    items: ['Jaringan kabel serat optik bawah laut dan darat', 'Penetrasi menara 5G di kawasan industri dan pemukiman', 'Kesiapan infrastruktur edge computing perkotaan', 'Dukungan teknis keandalan transmisi 24/7']
  },
  port_maritime_logistics: {
    cat: 'Maritim & Pelabuhan', tags: 'pelabuhan kapal kontainer logistik laut dermaga ekspor',
    pal: {bg: '#081426', primary: '#64FFDA', text: '#FFFFFF', accent: '#F43F5E', soft: '#112240'},
    hf: 'Archivo Black', bf: 'Roboto',
    kicker: 'MARITIME & SMART PORT LOGISTICS', title: 'Modernisasi Terminal Peti Kemas Maritim',
    sub: 'Otomasi Bongkar Muat Kapal dan Integrasi Ekosistem Logistik Pelabuhan Cerdas',
    body: 'Menurunkan waktu tunggu kapal (dwelling time) di dermaga hingga rata-rata 1.9 hari.',
    cta: 'AKSES JADWAL DERMAGA KAPAL', info: 'Otoritas Pelabuhan & Terminal Maritim Terpadu',
    st: ['pin', 'bolt', 'check'],
    items: ['Derek pemindah kontainer otomatis berteknologi tinggi', 'Pintu gerbang pelabuhan berbasis pemindai digital', 'Sistem manifes pelayaran terintegrasi bea cukai', 'Fasilitas pasokan daya listrik kapal sandar']
  },
  green_construction: {
    cat: 'Konstruksi & Infrastruktur', tags: 'konstruksi bangunan gedung beton arsitektur proyek teknik',
    pal: {bg: '#121618', primary: '#F59E0B', text: '#FFFFFF', accent: '#10B981', soft: '#222A2E'},
    hf: 'Montserrat', bf: 'Roboto',
    kicker: 'GREEN CONSTRUCTION & INFRASTRUCTURE', title: 'Rekayasa Bangunan Gedung Hijau Berkelanjutan',
    sub: 'Desain Konstruksi Efisiensi Energi Tinggi Bersertifikat Greenship Platinum',
    body: 'Penghematan konsumsi energi operasional gedung hingga 35% dibandingkan gedung standar.',
    cta: 'KONSULTASI DESAIN INFRASTRUKTUR', info: 'Kontraktor Rekayasa Bangunan Hijau Indonesia',
    st: ['house', 'plant', 'check'],
    items: ['Material beton rendah karbon dan daur ulang', 'Fasad insulasi termal penahan panas matahari', 'Sistem pemanenan air hujan dan pengolahan mandiri', 'Manajemen keselamatan kerja konstruksi tanpa insiden fatal']
  },
  insurtech_digital: {
    cat: 'Asuransi & Proteksi', tags: 'asuransi polis klaim proteksi jiwa kesehatan kendaraan',
    pal: {bg: '#0D1629', primary: '#3B82F6', text: '#FFFFFF', accent: '#10B981', soft: '#182540'},
    hf: 'Poppins', bf: 'Plus Jakarta Sans',
    kicker: 'INSURTECH & DIGITAL POLICIES', title: 'Proteksi Asuransi Mikro Mudah & Terjangkau',
    sub: 'Pembelian Polis Instan dari Ponsel dengan Pencairan Klaim Otomatis Berbasis Data',
    body: 'Persetujuan klaim asuransi kesehatan sederhana selesai dalam waktu kurang dari 30 menit.',
    cta: 'HITUNG PREMI ANDA SEKARANG', info: 'PT Asuransi Digital Mandiri Indonesia',
    st: ['shield', 'check', 'sparkle'],
    items: ['Pilihan premi mikro harian atau bulanan terjangkau', 'Klaim foto kuitansi online tanpa dokumen fisik', 'Jaringan rekanan ribuan rumah sakit dan klinik', 'Dukungan layanan darurat medis dan ambulans 24 jam']
  },
  architecture_planning: {
    cat: 'Arsitektur & Tata Ruang', tags: 'arsitektur denah interior fasad rumah tata kota',
    pal: {bg: '#141414', primary: '#E5E7EB', text: '#FFFFFF', accent: '#D4AF37', soft: '#242424'},
    hf: 'DM Serif Display', bf: 'Montserrat',
    kicker: 'SUSTAINABLE ARCHITECTURE STUDIO', title: 'Perencanaan Ruang Hidup Bernapas Alami',
    sub: 'Desain Hunian Tropis Modern dengan Ventilasi Silang Maksimal dan Pemanfaatan Cahaya Alami',
    body: 'Meraih pengakuan desain terbaik pada Festival Arsitektur Indonesia 2025.',
    cta: 'JADWALKAN KONSULTASI DESAIN', info: 'Studio Rancang Bangun Arsitektur Tropis',
    st: ['house', 'plant', 'sparkle'],
    items: ['Integrasi taman terbuka di dalam area rumah', 'Sirkulasi udara silang alami minim pendingin udara', 'Pilihan material kayu legal dan batu alam lokal', 'Gambar kerja detail dan simulasi tiga dimensi']
  },
  management_turnaround: {
    cat: 'Konsultasi Manajemen & Strategi', tags: 'konsultan manajemen bisnis strategi turnaround direksi',
    pal: {bg: '#0E131C', primary: '#D4AF37', text: '#FFFFFF', accent: '#38BDF8', soft: '#1B2433'},
    hf: 'Playfair Display', bf: 'Plus Jakarta Sans',
    kicker: 'MANAGEMENT CONSULTING & ADVISORY', title: 'Restrukturisasi Strategis & Lompatan Performa',
    sub: 'Mendampingi Pemimpin Bisnis dalam Menavigasi Disrupsi Pasar dan Efisiensi Organisasi',
    body: 'Membantu 50+ korporasi memulihkan profitabilitas dan menciptakan nilai jangka panjang.',
    cta: 'JADWALKAN SESI STRATEGI EKSEKUTIF', info: 'Kantor Konsultan Manajemen Strategis Reksa',
    st: ['briefcase', 'check', 'bulb'],
    items: ['Diagnostik kesehatan operasional dan keuangan', 'Redesain struktur organisasi ramping dan lincah', 'Program pengendalian biaya terukur', 'Pelaksanaan program manajemen perubahan efektif']
  },
  culinary_specialty_roastery: {
    cat: 'Kuliner & Roastery Kopi', tags: 'kopi roastery biji arabika seduh kafe barista',
    pal: {bg: '#140D0A', primary: '#D4A373', text: '#FFFFFF', accent: '#E76F51', soft: '#251A14'},
    hf: 'DM Serif Display', bf: 'Plus Jakarta Sans',
    kicker: 'SPECIALTY ROASTERY & COFFEE LAB', title: 'Eksplorasi Cita Rasa Kopi Nusantara',
    sub: 'Penyangraian Biji Kopi Single Origin Pilihan dengan Kurva Profil Rasa Presisi Tinggi',
    body: 'Menghubungkan langsung 40+ perkebunan petani kopi lokal dengan kafe terbaik.',
    cta: 'PESAN BIJI KOPI SANGRAI SEGAR', info: 'Laboratorium Sangrai Kopi Autentik Indonesia',
    st: ['coffee', 'mug', 'leaf'],
    items: ['Seleksi biji kopi arabika mutu tertinggi grade 1', 'Kurva sangrai digital terkalibrasi konsisten', 'Pengujian cupping berkala standar SCA', 'Pengiriman segar maksimal 3 hari pasca sangrai']
  },
  film_animation_studio: {
    cat: 'Perfilman & Animasi', tags: 'animasi film bioskop 3d render efek vfx sinema',
    pal: {bg: '#08080C', primary: '#A78BFA', text: '#FFFFFF', accent: '#F43F5E', soft: '#181824'},
    hf: 'Bebas Neue', bf: 'Poppins',
    kicker: 'ANIMATION & VISUAL EFFECTS', title: 'Kisah Sinematik Animasi Generasi Baru',
    sub: 'Produksi Film Animasi Panjang Berkualitas Tinggi dengan Sentuhan Cerita Rakyat Nusantara',
    body: 'Karya kami telah diputar di festival film animasi internasional ternama.',
    cta: 'TONTON REEL KARYA KAMI', info: 'Studio Animasi & Visual Sinema Kreatif',
    st: ['hot', 'sparkle', 'bulb'],
    items: ['Efek visual sinematik berstandar layar lebar', 'Perancangan karakter original dan latar imajinatif', 'Perekaman suara dan tata musik orkestra orisinal', 'Pipeline produksi digital berbasis cloud render farm']
  },
  bigdata_ai_intelligence: {
    cat: 'Data & Intelijen Bisnis', tags: 'data ai analytics machine learning database bi',
    pal: {bg: '#050D1A', primary: '#38BDF8', text: '#FFFFFF', accent: '#A855F7', soft: '#0E1F36'},
    hf: 'Bricolage Grotesque', bf: 'Roboto',
    kicker: 'ENTERPRISE DATA & AI INTELLIGENCE', title: 'Pengambilan Keputusan Berbasis Intelijen Data',
    sub: 'Membangun Gudang Data Modern (Modern Data Stack) dan Model Pembelajaran Mesin Prediktif',
    body: 'Membantu organisasi mentransformasikan data mentah menjadi wawasan bisnis bernilai tinggi.',
    cta: 'KONSULTASI ARSITEKTUR DATA', info: 'Pusat Analisis Data & Kecerdasan Buatan',
    st: ['bulb', 'bolt', 'check'],
    items: ['Data pipeline real-time dengan skalabilitas masif', 'Model prediktif pergerakan tren pasar industri', 'Dasbor intelijen bisnis interaktif untuk pimpinan', 'Tata kelola data dan kepatuhan privasi ketat']
  },
  venture_syndicate_fund: {
    cat: 'Investasi Modal Ventura', tags: 'venture capital modal ventura startup investasi lp seed',
    pal: {bg: '#0F172A', primary: '#10B981', text: '#FFFFFF', accent: '#F59E0B', soft: '#1E293B'},
    hf: 'Montserrat', bf: 'Plus Jakarta Sans',
    kicker: 'VENTURE CAPITAL & SEED FUND', title: 'Investasi pada Pendiri Startup Berdaya Cipta Tinggi',
    sub: 'Mendanai Startup Tahap Awal di Sektor FinTech, Logistik, AgriTech, dan Solusi Iklim',
    body: 'Mengelola portofolio 40+ startup dengan tingkat kelipatan modal (MOIC) konsisten prima.',
    cta: 'AJUKAN PITCH DECK ANDA', info: 'Komite Investasi Ventura Cipta Nusantara',
    st: ['briefcase', 'sparkle', 'check'],
    items: ['Pendanaan tahap Pra-Awal hingga Seri A terstruktur', 'Akses jejaring korporasi dan mitra strategis global', 'Pendampingan tata kelola dan rekrutmen pimpinan kunci', 'Sinergi ekosistem portofolio investasi terintegrasi']
  }
};

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

const targetList = (typeof window !== 'undefined' && window.TEMPLATES) ? window.TEMPLATES : (typeof TEMPLATES !== 'undefined' ? TEMPLATES : null);
if (targetList) {
  PRESENTATION_TEMPLATES.forEach(t => targetList.push(t));
}
if (typeof window !== 'undefined') {
  window.PRESENTATION_TEMPLATES = PRESENTATION_TEMPLATES;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PRESENTATION_THEMES, PRESENTATION_LAYOUT_KEYS, PRESENTATION_TEMPLATES };
}
