// Rakit Studio / Canva Desktop Web — Shared helpers: bridge connection, storage, navigation, dialogs, icons, templates, localization.
'use strict';

function ls(k) { try { return localStorage.getItem(k); } catch { return null; } }
function lsSet(k, v) { try { localStorage.setItem(k, v); return true; } catch { return false; } }
const uid = () => (crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36)).toUpperCase();
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

// Page parameters from URL hash or storage
const PARAMS = (() => {
  const h = new URLSearchParams(location.hash.slice(1)), out = {};
  for (const [k, v] of h) out[k] = v;
  if (!Object.keys(out).length) { try { Object.assign(out, JSON.parse(ls('nav') || '{}')); } catch {} }
  return out;
})();

// Localization dictionary
const I18N = {
  id: {
    home: 'Beranda',
    projects: 'Proyek',
    templates: 'Templat',
    brand: 'Merek',
    mcp: 'MCP & Desktop',
    createDesign: 'Buat Desain',
    openCanvaDesktop: 'Buka di Canva Desktop',
    searchPlaceholder: 'Cari templat, proyek, atau format...',
    heroTitle: 'Mau mendesain apa hari ini?',
    heroSubtitle: 'Pilih format siap pakai atau buat dengan ukuran khusus sesuka Anda.',
    recentDesigns: 'Desain Terbaru',
    seeAll: 'Lihat semua',
    trendingTemplates: 'Templat Populer',
    noDesignsYet: 'Belum ada desain tersimpan.',
    startFirstDesign: 'Mulai dengan memilih salah satu format di atas atau buat ukuran khusus.',
    openEditor: 'Buka di Editor',
    duplicate: 'Duplikat',
    download: 'Unduh',
    delete: 'Hapus',
    customSize: 'Ukuran Khusus',
    width: 'Lebar',
    height: 'Tinggi',
    create: 'Buat Baru',
    cancel: 'Batal',
    allTemplates: 'Semua Templat',
    brandKit: 'Brand Kit & Gaya',
    brandPalettes: 'Palet Warna Brand',
    brandFonts: 'Font Brand',
    uploadFont: 'Unggah Font (.ttf/.otf/.woff)',
    mcpTitle: 'Integrasi MCP & Canva Desktop',
    mcpSubtitle: 'Koneksi real-time ke Model Context Protocol dan aplikasi desktop Canva di komputer Anda.',
    mcpStatus: 'Status Server MCP',
    bridgeUrl: 'URL Bridge Lokal',
    token: 'Token Akses',
    connected: 'Terhubung',
    disconnected: 'Tidak Terhubung',
    testConnection: 'Uji Koneksi',
    launchCanvaApp: 'Luncurkan Canva Desktop',
    syncCanvaApp: 'Kirim Desain ke Canva',
    availableTools: 'Daftar Tool MCP Aktif',
    themeLight: 'Mode Terang',
    themeDark: 'Mode Gelap',
    language: 'Bahasa',
  },
  en: {
    home: 'Home',
    projects: 'Projects',
    templates: 'Templates',
    brand: 'Brand Hub',
    mcp: 'MCP & Desktop',
    createDesign: 'Create Design',
    openCanvaDesktop: 'Open in Canva Desktop',
    searchPlaceholder: 'Search templates, projects, or formats...',
    heroTitle: 'What will you design today?',
    heroSubtitle: 'Choose from ready-made formats or create with custom dimensions.',
    recentDesigns: 'Recent Designs',
    seeAll: 'See all',
    trendingTemplates: 'Trending Templates',
    noDesignsYet: 'No saved designs yet.',
    startFirstDesign: 'Start by choosing one of the presets above or create a custom size.',
    openEditor: 'Open in Editor',
    duplicate: 'Duplicate',
    download: 'Download',
    delete: 'Delete',
    customSize: 'Custom Size',
    width: 'Width',
    height: 'Height',
    create: 'Create',
    cancel: 'Cancel',
    allTemplates: 'All Templates',
    brandKit: 'Brand Kit & Styles',
    brandPalettes: 'Brand Color Palettes',
    brandFonts: 'Brand Fonts',
    uploadFont: 'Upload Font (.ttf/.otf/.woff)',
    mcpTitle: 'MCP & Canva Desktop Integration',
    mcpSubtitle: 'Real-time connection to Model Context Protocol and local Canva desktop application.',
    mcpStatus: 'MCP Server Status',
    bridgeUrl: 'Local Bridge URL',
    token: 'Access Token',
    connected: 'Connected',
    disconnected: 'Disconnected',
    testConnection: 'Test Connection',
    launchCanvaApp: 'Launch Canva Desktop',
    syncCanvaApp: 'Send Design to Canva',
    availableTools: 'Active MCP Tools',
    themeLight: 'Light Mode',
    themeDark: 'Dark Mode',
    language: 'Language',
  }
};

const Studio = {
  bridge: PARAMS.bridge || ls('bridge') || (location.protocol === 'http:' && location.hostname === '127.0.0.1' ? location.origin : 'http://127.0.0.1:8765'),
  token: PARAMS.token || ls('token') || '',
  connected: false,
  mcpStatus: null,

  async connect() {
    if (!this.bridge) this.bridge = 'http://127.0.0.1:8765';
    try {
      const headers = {'Content-Type': 'application/json'};
      if (this.token) headers['X-Bridge-Token'] = this.token;
      const res = await fetch(this.bridge + '/api/mcp/status', {
        headers,
        signal: AbortSignal.timeout(1800)
      });
      if (res.ok) {
        this.connected = true;
        this.mcpStatus = await res.json();
        lsSet('bridge', this.bridge);
        if (this.token) lsSet('token', this.token);
        return true;
      }
    } catch {}

    try {
      const headers = {'Content-Type': 'application/json'};
      if (this.token) headers['X-Bridge-Token'] = this.token;
      const res = await fetch(this.bridge + '/api/drafts', {
        headers,
        signal: AbortSignal.timeout(1500)
      });
      if (res.ok) {
        this.connected = true;
        lsSet('bridge', this.bridge);
        if (this.token) lsSet('token', this.token);
        return true;
      }
    } catch {}

    this.connected = false;
    return false;
  },

  async api(path, opt = {}) {
    const headers = {'Content-Type': 'application/json', ...opt.headers};
    if (this.token) headers['X-Bridge-Token'] = this.token;
    const r = await fetch(this.bridge + path, {...opt, headers});
    const j = await r.json();
    if (!r.ok) throw new Error(j.error || r.status);
    return j;
  },

  mediaUrl(p) {
    if (!p || /^(data:|blob:|https?:)/.test(p)) return p;
    return `${this.bridge}/media?token=${encodeURIComponent(this.token)}&path=${encodeURIComponent(p)}`;
  },

  go(page, extra = {}) {
    const params = {...(this.connected ? {bridge: this.bridge, token: this.token} : {}), ...extra};
    lsSet('nav', JSON.stringify(extra));
    const url = new URL(page + (Object.keys(params).length ? '#' + new URLSearchParams(params) : ''), location.href);
    if (url.pathname === location.pathname) { location.hash = url.hash; location.reload(); }
    else location.href = url.href;
  },

  async openCanvaDesktop(designId = '') {
    // If bridge is connected, trigger launch endpoint
    if (this.connected) {
      try {
        const r = await this.api('/api/canva/launch', {
          method: 'POST',
          body: JSON.stringify({url: designId ? `canva://design/${designId}` : 'canva://'})
        });
        if (r.ok) {
          this.toast(r.message || 'Membuka aplikasi Canva Desktop di komputer Anda…');
          return true;
        }
      } catch {}
    }

    // Direct Windows protocol launcher
    try {
      const target = designId ? `canva://design/${designId}` : 'canva://';
      window.location.href = target;
      this.toast('Menghubungkan ke Canva Desktop (' + target + ')…');
      return true;
    } catch (err) {
      this.toast('Gagal meluncurkan Canva Desktop: ' + err.message);
      return false;
    }
  },

  // Designs list: bridge when available, else local storage
  async listDesigns() {
    if (this.connected) {
      try {
        const list = await this.api('/api/designs');
        if (Array.isArray(list)) return list;
      } catch {}
    }
    return Object.values(this._local()).map(({id, title, kind, width, height, updated, thumb}) => ({id, title, kind, width, height, updated, thumb}));
  },

  async getDesign(id) {
    if (this.connected) {
      try { return await this.api('/api/design?id=' + encodeURIComponent(id)); } catch {}
    }
    return this._local()[id] || null;
  },

  async saveDesign(d) {
    d.updated = Date.now();
    let bridgeOk = false;
    if (this.connected) {
      try {
        await this.api('/api/design', {method: 'PUT', body: JSON.stringify(d)});
        bridgeOk = true;
      } catch {}
    }
    const all = this._local();
    all[d.id] = d;
    if (!lsSet('designs', JSON.stringify(all))) {
      if (!bridgeOk) throw new Error('Penyimpanan browser penuh. Hapus desain lama.');
    }
    return {ok: true, bridge: bridgeOk};
  },

  async deleteDesign(id) {
    if (this.connected) {
      try { await this.api('/api/design?id=' + encodeURIComponent(id), {method: 'DELETE'}); } catch {}
    }
    const all = this._local();
    delete all[id];
    lsSet('designs', JSON.stringify(all));
    return {ok: true};
  },

  _local() {
    try { return JSON.parse(ls('designs') || '{}'); } catch { return {}; }
  },

  // Theme Manager
  getTheme() {
    return ls('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  },
  setTheme(theme) {
    lsSet('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.classList.toggle('dark', theme === 'dark');
    document.documentElement.classList.toggle('light', theme === 'light');
    window.dispatchEvent(new CustomEvent('themechange', {detail: theme}));
  },
  toggleTheme() {
    const next = this.getTheme() === 'dark' ? 'light' : 'dark';
    this.setTheme(next);
    return next;
  },

  // Localization Manager
  getLang() {
    return ls('lang') || 'id';
  },
  setLang(lang) {
    lsSet('lang', lang);
    document.documentElement.setAttribute('lang', lang);
    window.dispatchEvent(new CustomEvent('langchange', {detail: lang}));
  },
  toggleLang() {
    const next = this.getLang() === 'id' ? 'en' : 'id';
    this.setLang(next);
    return next;
  },
  t(key) {
    const lang = this.getLang();
    return I18N[lang]?.[key] || I18N['id']?.[key] || key;
  },

  toast(msg, ms = 2800) {
    document.querySelectorAll('.toast').forEach(t => t.remove());
    const t = document.createElement('div');
    t.className = 'toast';
    t.setAttribute('role', 'status');
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), ms);
  },

  modal(html, {onClose} = {}) {
    const back = document.createElement('div');
    back.className = 'modal-back';
    back.innerHTML = `<div class="modal" role="dialog" aria-modal="true">${html}</div>`;
    const close = v => { back.remove(); onClose?.(v); };
    back.addEventListener('pointerdown', e => { if (e.target === back) close(null); });
    back.addEventListener('keydown', e => { if (e.key === 'Escape') close(null); });
    document.body.appendChild(back);
    back.querySelector('button, input, select')?.focus();
    return {el: back.firstElementChild, close};
  },

  confirm(title, msg, ok = 'Lanjutkan', danger = false) {
    return new Promise(res => {
      const m = this.modal(`<h3>${esc(title)}</h3><p>${esc(msg)}</p><div class="actions"><button class="btn" data-v="0">Batal</button><button class="btn primary" data-v="1"${danger ? ' style="background:var(--danger);border-color:var(--danger);color:#fff"' : ''}>${esc(ok)}</button></div>`, {onClose: v => res(!!v)});
      m.el.querySelectorAll('[data-v]').forEach(b => b.onclick = () => m.close(b.dataset.v === '1'));
    });
  },
};

// Apply saved theme at boot
Studio.setTheme(Studio.getTheme());
Studio.setLang(Studio.getLang());

// 24px line SVG icon library
const ICONS = {
  home: 'M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z',
  folder: 'M3 6a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z',
  layout: 'M4 4h16v16H4zM4 10h16M10 10v10',
  palette: 'M12 3a9 9 0 1 0 0 18c1.1 0 1.5-.8 1.5-1.5 0-.9-.6-1.3-.6-2.1 0-.8.7-1.4 1.6-1.4H17a4 4 0 0 0 4-4c0-5-4-9-9-9zM7.5 11.5h.01M10 7.5h.01M15 7.5h.01',
  sparkles: 'M12 3l1.8 4.7 4.7 1.8-4.7 1.8L12 16l-1.8-4.7-4.7-1.8 4.7-1.8zM19 15l.8 2.2 2.2.8-2.2.8L19 21l-.8-2.2-2.2-.8 2.2-.8z',
  list: 'M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01',
  link: 'M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1',
  plus: 'M12 5v14M5 12h14',
  search: 'M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM20 20l-4-4',
  text: 'M5 6V4h14v2M12 4v16M9 20h6',
  shapes: 'M4 13h7v7H4zM17.5 4a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7zM7.5 3l4 7h-8z',
  upload: 'M12 16V4M7 9l5-5 5 5M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3',
  image: 'M4 5h16v14H4zM4 16l5-5 4 4 2-2 5 5M15 9.5h.01',
  fill: 'M5 12l7-7 7 7-7 7zM19 16s2 2.2 2 3.5a2 2 0 0 1-4 0c0-1.3 2-3.5 2-3.5z',
  layers: 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5',
  undo: 'M9 14L4 9l5-5M4 9h10a6 6 0 0 1 0 12h-3',
  redo: 'M15 14l5-5-5-5M20 9H10a6 6 0 0 0 0 12h3',
  download: 'M12 4v12M7 11l5 5 5-5M4 20h16',
  send: 'M4 12l16-8-6 16-3-7z',
  trash: 'M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13',
  copy: 'M8 8h12v12H8zM16 8V4H4v12h4',
  lock: 'M6 11h12v9H6zM8.5 11V8a3.5 3.5 0 0 1 7 0v3',
  unlock: 'M6 11h12v9H6zM8.5 11V8a3.5 3.5 0 0 1 6.8-1',
  eye: 'M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12zM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
  eyeoff: 'M3 3l18 18M10.6 5.1A10 10 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.2 4M6.6 6.6C3.9 8.4 2 12 2 12s3.6 7 10 7a9.6 9.6 0 0 0 5.4-1.6',
  group: 'M4 4h7v7H4zM13 13h7v7h-7zM8 15v3h3M16 9V6h-3',
  alignL: 'M4 3v18M8 7h10v4H8zM8 14h6v4H8z',
  alignC: 'M12 3v18M7 7h10v4H7zM9 14h6v4H9z',
  alignR: 'M20 3v18M6 7h10v4H6zM10 14h6v4h-6z',
  crop: 'M6 2v16h16M2 6h16v16',
  flipH: 'M12 3v18M8 7l-5 5 5 5zM16 7l5 5-5 5z',
  flipV: 'M3 12h18M7 8l5-5 5 5zM7 16l5 5 5-5z',
  wand: 'M4 20L15 9M14 3v3M19 8h3M18 4l1.5-1.5M17.5 12.5L19 14M10 3.5l1 1',
  filter: 'M9 4a5 5 0 1 0 0 10 5 5 0 0 0 0-10zM15 10a5 5 0 1 0 0 10 5 5 0 0 0 0-10z',
  zoomIn: 'M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM20 20l-4-4M8 11h6M11 8v6',
  zoomOut: 'M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM20 20l-4-4M8 11h6',
  back: 'M15 5l-7 7 7 7',
  resize: 'M4 9V4h5M20 15v5h-5M4 4l7 7M20 20l-7-7',
  adjust: 'M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M16 4v4M10 10v4M16 16v4',
  check: 'M5 12l5 5 9-10',
  x: 'M6 6l12 12M18 6L6 18',
  computer: 'M3 5h18v11H3zM8 20h8M12 16v4',
  grid: 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z',
  font: 'M4 20l6-16h1l6 16M6.5 14h8M17 20h4',
  shadow: 'M5 5h11v11H5zM9 19h10V9',
  more: 'M5 12h.01M12 12h.01M19 12h.01',
  bolt: 'M13 3L5 13h6l-1 8 8-10h-6z',
  desktop: 'M2 4h20v13H2zM8 21h8M12 17v4',
  sun: 'M12 3v2M12 19v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M3 12h2M19 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z',
  moon: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z',
  refresh: 'M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15',
  arrowRight: 'M5 12h14M12 5l7 7-7 7',
  chevronDown: 'M6 9l6 6 6-6',
  apps: 'M4 4h4v4H4zM10 4h4v4h-4zM16 4h4v4h-4zM4 10h4v4H4zM10 10h4v4h-4zM16 10h4v4h-4zM4 16h4v4H4zM10 16h4v4h-4zM16 16h4v4h-4z',
  sliders: 'M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6',
};

const icon = (n, cls = '') => `<svg class="i ${cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="${ICONS[n] || ICONS.more}"/></svg>`;

// Built-in color palettes
const PALETTES = {
  kunyit: {bg: '#1B1A17', primary: '#E8B02A', text: '#F7F3E8', accent: '#D95D39'},
  pandan: {bg: '#EAF5EC', primary: '#2F8F5B', text: '#13301F', accent: '#F2A541'},
  batik: {bg: '#F4EDE1', primary: '#7A4A2A', text: '#2A1E16', accent: '#2F5D8A'},
  senja: {bg: '#2A1B3D', primary: '#FF8C5A', text: '#FFF4EC', accent: '#F4C95D'},
  laut: {bg: '#F2F7FB', primary: '#1F6FB2', text: '#0E2236', accent: '#36C5B1'},
};

// Preset design formats
const SIZES = {
  instagram_post: {w: 1080, h: 1350, label: 'Post Instagram', icon: 'image'},
  story: {w: 1080, h: 1920, label: 'Story / Reels', icon: 'video'},
  square: {w: 1080, h: 1080, label: 'Post Persegi', icon: 'shapes'},
  youtube_thumbnail: {w: 1280, h: 720, label: 'Thumbnail YouTube', icon: 'image'},
  presentation: {w: 1920, h: 1080, label: 'Presentasi 16:9', icon: 'computer'},
  a4: {w: 1240, h: 1754, label: 'Poster A4', icon: 'layout'},
  banner: {w: 1500, h: 500, label: 'Banner Web', icon: 'layout'},
  logo: {w: 500, h: 500, label: 'Logo', icon: 'sparkles'},
};

const VIDEO_SIZES = {
  portrait: {w: 1080, h: 1920, label: 'Video 9:16'},
  landscape: {w: 1920, h: 1080, label: 'Video 16:9'},
  square: {w: 1080, h: 1080, label: 'Video 1:1'}
};

const T = (text, x, y, w, h, fontSize, color, o = {}) => ({id: uid(), type: 'text', text, x, y, w, h, fontSize, color, bold: false, italic: false, align: 'left', font: 'Plus Jakarta Sans', rot: 0, opacity: 1, effect: 'none', ...o});
const R = (x, y, w, h, fill, o = {}) => ({id: uid(), type: 'rect', x, y, w, h, fill, radius: 0, rot: 0, opacity: 1, ...o});

function makeDesign(kind, palette = 'kunyit', title) {
  const s = SIZES[kind] || SIZES.square, p = PALETTES[palette] || PALETTES.kunyit, W = s.w, H = s.h, m = Math.round(Math.min(W, H) * 0.06);
  const page = els => ({id: uid(), bg: p.bg, elements: els});
  const head = 'Bricolage Grotesque';
  let pages;
  if (kind === 'youtube_thumbnail' || kind === 'banner') {
    pages = [page([
      R(W * 0.45, 0, W * 0.55, H, p.accent, {name: 'Foto (ganti)'}),
      R(0, 0, W * 0.5, H, p.bg),
      R(W * 0.5 - 10, 0, 20, H, p.primary),
      T('JUDUL YANG MENARIK AUDIENS', m, m, W * 0.44, H * 0.62, Math.round(Math.min(W * 0.065, H * 0.15)), p.text, {bold: true, font: head}),
      R(m, H - m - H * 0.14, W * 0.26, H * 0.14, p.primary, {radius: 14}),
      T('TONTON', m, H - m - H * 0.12, W * 0.26, H * 0.1, Math.round(H * 0.07), p.bg, {bold: true, align: 'center', font: head})
    ])];
  } else if (kind === 'presentation') {
    pages = [
      page([
        R(m, H * 0.3, 14, H * 0.4, p.primary),
        T('Judul Presentasi Strategis', m + 50, H * 0.3, W * 0.48, 220, 92, p.text, {bold: true, font: head}),
        T('Tim Kreatif & Analitik · 2026', m + 50, H * 0.58, W * 0.48, 70, 34, p.text, {opacity: 0.8}),
        R(W * 0.56, 0, W * 0.44, H, p.primary, {name: 'Foto (ganti)'})
      ]),
      page([
        R(0, 0, W, 14, p.primary),
        T('01', m, m * 1.6, 220, 110, 80, p.accent, {bold: true, font: head}),
        T('Gagasan Pokok', m, m * 1.6 + 130, W * 0.48, 100, 64, p.text, {bold: true, font: head}),
        T('Satu gagasan utama per slide menjaga perhatian audiens tetap fokus dan materi mudah dipahami.', m, m * 1.6 + 260, W * 0.42, 260, 32, p.text),
        R(W * 0.55, m * 1.6, W * 0.45 - m, H - 3.2 * m, p.primary, {radius: 24, name: 'Foto (ganti)'})
      ]),
      page([
        T('Terima Kasih', 0, H * 0.4, W, 140, 104, p.primary, {bold: true, align: 'center', font: head}),
        T('kontak@bisnisanda.com', 0, H * 0.58, W, 60, 32, p.text, {align: 'center'})
      ])
    ];
  } else if (kind === 'logo') {
    pages = [page([
      {id: uid(), type: 'ellipse', x: W * 0.2, y: W * 0.12, w: W * 0.6, h: W * 0.6, fill: p.primary, rot: 0, opacity: 1},
      T('C', W * 0.2, W * 0.2, W * 0.6, W * 0.4, Math.round(W * 0.34), p.bg, {bold: true, align: 'center', font: head}),
      T('BRAND IDENTITY', 0, W * 0.78, W, W * 0.1, Math.round(W * 0.07), p.text, {bold: true, align: 'center', spacing: 6})
    ])];
  } else {
    const ph = H * (kind === 'a4' ? 0.5 : 0.56);
    pages = [page([
      R(0, 0, W, ph, p.primary, {name: 'Foto (ganti)'}),
      R(m, ph - 34, W * 0.32, 16, p.accent),
      T('Penawaran Spesial', m, ph + m * 0.7, W - 2 * m, H * 0.13, Math.round(W * 0.08), p.text, {bold: true, font: head}),
      T('Dapatkan pengalaman terbaik dengan desain visual berkualitas tinggi.', m, ph + H * 0.17, W - 2 * m, H * 0.1, Math.round(W * 0.034), p.text, {opacity: 0.85}),
      R(m, H - m - H * 0.07, W * 0.46, H * 0.07, p.primary, {radius: 999}),
      T('Mulai Sekarang', m, H - m - H * 0.07 + H * 0.017, W * 0.46, H * 0.05, Math.round(W * 0.034), p.bg, {bold: true, align: 'center'})
    ])];
  }
  return {id: uid(), title: title || (s.label + ' Baru'), kind, palette, width: W, height: H, pages, fonts: [], updated: Date.now()};
}

function demoImage(label, c1, c2, w = 960, h = 540) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d');
  const g = x.createLinearGradient(0, 0, w, h); g.addColorStop(0, c1); g.addColorStop(1, c2); x.fillStyle = g; x.fillRect(0, 0, w, h);
  x.globalAlpha = 0.18; x.fillStyle = '#fff';
  for (let i = 0; i < 7; i++) { x.beginPath(); x.arc((i * 173) % w, (i * 97 + 60) % h, 40 + i * 18, 0, 7); x.fill(); }
  x.globalAlpha = 1; x.fillStyle = 'rgba(255,255,255,0.92)'; x.textAlign = 'center'; x.textBaseline = 'middle';
  let fs = Math.round(h * 0.11); x.font = `700 ${fs}px "Bricolage Grotesque", sans-serif`;
  const tw = x.measureText(label).width; if (tw > w * 0.84) { fs = Math.floor(fs * w * 0.84 / tw); x.font = `700 ${fs}px "Bricolage Grotesque", sans-serif`; }
  x.fillText(label, w / 2, h / 2);
  return c.toDataURL('image/jpeg', 0.85);
}
