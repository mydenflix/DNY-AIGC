# Catatan Setup PC Lokal (DNY)

Dokumen ini menyelaraskan [README](../../readme/README_id.md) / [Mulai Cepat](./quickstart.md) dengan spesifikasi PC Anda (`D:\My PC DATA.txt`).

## Ringkasan audit

| Syarat README | PC Anda | Status |
|---|---|---|
| ≥ 2 vCPU / 4 GB RAM | i5-13400F · **32 GB DDR5** | Melebihi |
| GPU (opsional, hanya fitur `world`) | **RTX 4070 12 GB** · driver NVIDIA + CUDA 12.8 | Siap untuk world/3DGS |
| Disk beberapa GB | 2× SSD ADATA ~931 GB · D: ~356 GB bebas | Cukup |
| Windows + Docker Desktop WSL2 | Windows 11 Pro · WSL `docker-desktop` v2 | OK |
| Docker + Compose | Docker 29.8 · Compose v5.5.1 | OK |
| Port 8080 / 8780 / 3000 | web · api · newapi | Berjalan |
| Sibling `dramaclaw-gateway` | `D:\storyboard\dramaclaw-gateway` | Ada |
| `.env` (PROMPT_EXPORT_PASSWORD non-default) | `dramaclaw/.env` | Ada |
| Git / Node 20+ / pnpm / uv / ffmpeg | Terpasang | OK |
| Python 3.11–3.12 (hanya jalur lokal uv) | Dipasang **3.12** (selain 3.14 sistem) | Dilengkapi |
| Locale UI Indonesia | `frontend/public/locales/id` · default `id` | OK |
| Mode model (Settings) | Hybrid · Official DC key tersimpan · Custom NewAPI siap | OK |

## Mode yang disarankan di PC ini

1. **Docker (utama)** — sesuai README: sudah `docker compose up -d --build`. Buka http://localhost:8080  
2. **Official / Hybrid** — DC Key sudah terkonfigurasi (`relayclaw.cdnfg.com`). Tidak perlu mapping model manual.  
3. **Fitur world (3DGS / SHARP)** — GPU Anda memenuhi syarat. Aktifkan hanya jika perlu:

```bash
cd D:\storyboard\dramaclaw
INSTALL_WORLD=1 docker compose up -d --build api
```

4. **Pengembangan lokal (opsional)** — setelah Python 3.12 terpasang:

```bash
cd D:\storyboard\dramaclaw
uv python pin 3.12
uv sync
uv run novelvideo api --port 8780
# terminal kedua:
cd frontend && pnpm install && pnpm dev
```

## Perintah cek cepat

```bash
cd D:\storyboard\dramaclaw
docker compose ps
curl http://localhost:8780/api/v1/config
curl -I http://localhost:8080/locales/id/translation.json
```

## Yang harus Anda lakukan di UI

1. Hard refresh http://localhost:8080 (`Ctrl+Shift+R`) — pastikan bahasa **Bahasa Indonesia**.  
2. **Pengaturan → Konfigurasi Model** — mode Hybrid/Official sudah aktif; cek lencana **Aktif**.  
3. Buat proyek baru dan uji alur singkat (sesuai [Mengonfigurasi Model](./configuring-models.md) jika menambah saluran Custom).

## Catatan Windows

README menyarankan clone di filesystem Linux WSL untuk performa volume. Checkout Anda di `D:\storyboard` tetap dipakai (sudah berjalan). Jika build Docker terasa lambat, pertimbangkan memindahkan repo ke `\\wsl$\docker-desktop\...` atau distro WSL.

Sumber spek: `D:\My PC DATA.txt` (B760M PROJECT ZERO · i5-13400F · 32 GB · RTX 4070).
