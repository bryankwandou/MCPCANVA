# mcp-canva — MCP server untuk Canva + editor web "Rakit Desain"

Repo ini berdiri sendiri, terpisah dari MCP CapCut ([bryankwandou/MCPCAPCUT](https://github.com/bryankwandou/MCPCAPCUT)).

| Bagian | Isi |
|---|---|
| **Server MCP** | Tool `canva_*` lewat Canva Connect API resmi (OAuth): list/buat desain, upload aset, export, brand template + autofill, resize; `catalog`; `desktop_*` (kontrol layar, opsional) |
| **Editor web** | `src/creative_mcp/editor/`: editor desain bergaya Canva (template, elemen, teks, animasi, presentasi, export PNG/JPG/PDF/PPTX). Dideploy ke Vercel sebagai situs statis |
| **Daftar fitur** | `FEATURES.md` / `features.html`: fitur Canva Free vs Pro dan status di editor ini |

Elemen/fitur Pro Canva tidak dibuka tanpa langganan; tidak ada aset Canva yang disalin.

## Instalasi
```bash
git clone https://github.com/bryankwandou/MCPCANVA && cd MCPCANVA
pip install -e ".[desktop]"
mcp-canva login        # sekali: browser terbuka ke Canva, klik Allow
```
App Canva dibuat di https://www.canva.com/developers/apps (Outside Canva), Redirect URL
`http://127.0.0.1:3001/oauth/redirect`. Client ID/Secret ditanyakan saat `login` dan disimpan di `.env`.

Tambahkan ke Claude Desktop (`claude_desktop_config.json`):
```json
{ "mcpServers": { "canva": { "command": "mcp-canva" } } }
```

## Cek koneksi
```bash
python scripts/verify_connection.py --write
```
Berhasil bila muncul `[OK ] Canva: akun terhubung` dengan nama akun Anda dan desain "Tes MCP …" muncul di Canva.

## Deploy editor ke Vercel
Import repo ini di Vercel; `vercel.json` sudah menyetel output `src/creative_mcp/editor` tanpa build.
