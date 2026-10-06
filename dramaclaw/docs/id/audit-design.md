# Audit DESIGN.md (PC lokal)

Sumber kebenaran: [DESIGN.md](../../DESIGN.md) (identik dengan `Downloads/DESIGN.md`).

| Item DESIGN.md | Status | Catatan |
|----------------|--------|---------|
| `npx @google/design.md lint` | OK | **0 errors**, 15 warnings (baseline resmi) |
| Token canvas gelap (`#0a0c12`…`#5ba0ff`) | OK | `--*-rgb` di `.dark` cocok |
| Token motion / radius | OK | 150/220/320ms; node 14px; panel 16px |
| Kelas `.tap-*` / `.ui-scrollbar` / `.backdrop-blur-tap` | OK | Ada di `frontend/src/index.css` |
| Default tema gelap | OK | `app-store` + bootstrap `index.html` → `dark` |
| Font Inter + CJK | OK | `--font-sans` → `Inter Variable` + Noto/PingFang/YaHei |
| PikoCountdownPixel | OK | `/fonts/piko-countdown-pixel.woff` |
| Exception `/download` | OK | lazy + `download.module.css` + Geist + zinc/rust |
| Exception `/login` | OK | `login.module.css` + `light-rays.css` (tanpa Geist) |
| Rute live | OK | `/` `/download` `/login` → 200 |

## Perintah

```bash
cd D:/storyboard/dramaclaw
# dari repo root (via frontend script):
cd frontend && pnpm design:lint
# atau:
node "$(npm root -g 2>/dev/null)/@google/design.md/dist/index.js" lint DESIGN.md
# praktis:
npx --yes -p @google/design.md design.md lint DESIGN.md
```

Baseline yang diharapkan: **0 errors / 15 warnings** (4 contrast debt + 11 orphaned-tokens). Jangan hapus token orphan hanya untuk membersihkan warning.

## Gap yang dilengkapi

1. Stack font produk tidak memuat face `@fontsource-variable/inter` (`Inter Variable`) dan tanpa fallback CJK di `--font-sans` → diselaraskan ke Typography DESIGN.md.
2. Bootstrap FOUC di `index.html` memakai default `system` → diganti `dark` agar selaras dengan DESIGN + `app-store`.
3. Script `pnpm design:lint` ditambahkan di `frontend/package.json` agar gate AGENTS mudah dijalankan.
