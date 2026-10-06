<!-- lang-switch -->
[English](../../en/getting-started/installation.md) · [简体中文](../../zh/getting-started/installation.md) · **Bahasa Indonesia**

# Panduan Instalasi

> Siapkan lingkungan runtime DNY CE di macOS / Windows / Linux. Jika Anda hanya ingin jalur tercepat untuk menjalankannya, langsung ke [Mulai Cepat](quickstart.md); panduan ini mencakup prasyarat per platform dan dua metode instalasi (Docker dan pengembangan lokal).

DNY CE adalah layanan satu mesin yang **tidak membutuhkan PostgreSQL / Redis**. Docker menjalankan `api` + gateway `newapi` bawaan + `web`; model dilayani lewat gateway resmi DNY (RelayClaw) secara default, atau lewat gateway bawaan setelah Anda beralih ke mode Custom di Pengaturan. Tidak ada yang menjalankan model di mesin Anda, jadi mesin biasa sudah cukup.

## Pilih salah satu dari dua metode instalasi

| Metode | Cocok untuk | Prasyarat |
|---|---|---|
| **Docker (disarankan)** | Deployment, uji coba, self-hosting produksi | Cukup Docker; ffmpeg dan sejenisnya sudah di dalam image |
| **Pengembangan lokal (uv)** | Mengedit kode, debugging | Python 3.11–3.12, uv, ffmpeg (diinstal sendiri) |

> ffmpeg/ffprobe adalah **dependensi sistem**; CE tidak mendistribusikan binary-nya (lihat [ADR-0002](../../adr/0002-ffmpeg-system-dependency.md) untuk alasannya). Image Docker sudah membundle keduanya; untuk pengembangan lokal Anda menginstalnya sendiri — lihat [panduan ffmpeg](../../en/guides/ffmpeg.md).

---

## A. Docker (disarankan)

Prasyarat: Docker + `docker compose`.

| Platform | Instalasi |
|---|---|
| **macOS** | [Docker Desktop](https://www.docker.com/products/docker-desktop/) (berjalan di Apple Silicon dan Intel) |
| **Windows** | Docker Desktop dengan backend **WSL2** diaktifkan (Settings → General → Use WSL2) |
| **Linux** | Docker Engine + `docker-compose-plugin` (dari package manager distro) — Docker Compose **≥ 2.24** (`docker compose version`; file compose memakai sintaks panjang `env_file`) |

Setelah terinstal:

```bash
git clone https://github.com/mydenflix/DNY-AIGC.git
cd DNY-AIGC/app
# Opsional: checkout gateway di ../gateway (atau set DNY_AIGC_GATEWAY_SRC di .env)
cp .env.example .env        # setidaknya, ubah PROMPT_EXPORT_PASSWORD ke nilai non-default
docker compose up -d --build    # membangun api, web, dan gateway dari sumber
# tanpa build? docker compose -f docker-compose.release.yml up -d   # menarik image terpublikasi, tidak perlu clone gateway
```

Setelah naik, buka **`http://localhost:8080`** di browser (UI aplikasi); REST API ada di `http://localhost:8780`. Masuk ke Pengaturan → Konfigurasi Model → Saluran Official, tempel DC key Anda, simpan, dan siap digunakan. Untuk panduan lengkap lihat [Mulai Cepat](quickstart.md); untuk start/stop/backup lihat [Buku Panduan Self-Hosting](../../en/guides/self-hosting.md).

> Pengguna Windows sebaiknya clone dan menjalankan di dalam **terminal WSL2** (tetap di filesystem Linux, bukan di bawah `/mnt/c/...`) untuk menghindari masalah performa volume-mount dan line-ending.

---

## B. Pengembangan lokal (uv + Python 3.11–3.12)

### 1. Instal prasyarat

| Platform | Python 3.11/3.12 | uv | ffmpeg |
|---|---|---|---|
| **macOS** | `brew install python@3.12` | `brew install uv` | `brew install ffmpeg` |
| **Windows** | [python.org](https://www.python.org/downloads/) atau `winget install Python.Python.3.12` | `winget install astral-sh.uv` | `winget install Gyan.FFmpeg` (atau gunakan WSL2 dan ikuti alur Linux) |
| **Linux (Debian/Ubuntu)** | `apt install python3.12` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `apt install ffmpeg` |

> Python harus dalam rentang **3.11–3.12** (`requires-python = ">=3.11,<3.13"`). uv mengunci versi dependensi menurut `uv.lock`.

### 2. Instal dependensi dan jalankan

```bash
git clone https://github.com/mydenflix/DNY-AIGC.git
cd DNY-AIGC/app

uv sync                                  # instal dependensi ke .venv menurut uv.lock
cp .env.example .env && $EDITOR .env     # atur gateway dan key

uv run novelvideo api --host 0.0.0.0 --port 8780
```

CE default ke `ST_EDITION=ce`, pengguna lokal tunggal tanpa login, dan eksekusi tugas inline in-process (tanpa Ray/Redis/Celery).

### 3. Verifikasi

```bash
curl http://localhost:8780/api/v1/config   # respons 200 berarti berfungsi
```

### 4. Gateway (hanya untuk mode Custom / Local + Official Hybrid)

Mode Official tidak membutuhkan apa pun lagi. Untuk dua mode lainnya API mengharapkan gateway di `127.0.0.1:3000` (default `NEWAPI_ADMIN_BASE_URL` di `.env`) dengan file SQLite `./state/newapi/one-api.db`, yang ditulis oleh **Inisialisasi** di Pengaturan. Jalankan image terpublikasi dengan direktori itu di-mount:

```bash
mkdir -p state/newapi
docker run -d --name dramaclaw-gateway -p 127.0.0.1:3000:3000 \
  -v "$PWD/state/newapi:/data" \
  claymorelab/dramaclaw-gateway:v1.0.0-rc.24-dramaclaw.1
```

atau bangun dan jalankan gateway dari checkout saudara `dramaclaw-gateway` dengan `SQLITE_PATH` mengarah ke file itu. Lihat [Mengonfigurasi Model](configuring-models.md) untuk pengaturan mode.

---

## Opsional: fitur world (3DGS / kedalaman SHARP)

Fitur berat seperti voxel/panorama-ke-3D ada di ekstra opsional `world`; fitur ini **membutuhkan GPU dan toolchain tambahan** dan tidak diinstal secara default:

```bash
uv sync --extra world                       # menginstal torch / ml-sharp / da2 dan lainnya
npm install -g @playcanvas/splat-transform  # alat kompresi PLY→SOG
```

Docker: `INSTALL_WORLD=1 docker compose up -d --build`. Basis slim hanya CPU; akselerasi GPU membutuhkan basis CUDA + runtime nvidia. Bobot model diunduh otomatis saat runtime, tidak dibake ke dalam image.

> Jika Anda tidak melakukan alur kerja 3D/voxel apa pun, bagian ini bisa diabaikan; text→video jadi tidak membutuhkannya.

---

## Langkah berikutnya

- Dapatkan hasil pertama yang berfungsi: [Mulai Cepat](quickstart.md)
- Hubungkan gateway model Anda sendiri: [Mengonfigurasi Model](configuring-models.md)
- Instal/verifikasi ffmpeg: [panduan ffmpeg](../../en/guides/ffmpeg.md)
- Menemui masalah: [Pemecahan Masalah](../../en/guides/troubleshooting.md)
