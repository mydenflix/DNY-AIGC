<!-- lang-switch -->
[English](../../en/getting-started/quickstart.md) · [简体中文](../../zh/getting-started/quickstart.md) · **Bahasa Indonesia**

# Mulai Cepat

> Jalankan DNY secara lokal dan hasilkan hasil pertama Anda.

DNY adalah Community Edition (CE): berjalan di satu mesin tanpa PostgreSQL / Redis. Secara default `docker compose` menjalankan tiga layanan: `api` (backend kreasi, :8780), `newapi` (gateway bawaan, idle sampai Anda beralih ke mode Custom atau Local + Official Hybrid), dan `web` (UI browser, :8080). Model dilayani lewat **gateway resmi DNY (RelayClaw)** secara default — tempel DC key dan siap digunakan.

## Prasyarat

- Docker (Desktop atau Engine) dengan dukungan `docker compose`.
- **DC key** — daftar / beli di <https://relayclaw.cdnfg.com>; atau gunakan NewAPI lokal yang dibundle dengan CE.

## Langkah

```bash
# 1. Ambil kode — DNY dan gateway bawaan, berdampingan
git clone https://github.com/dramaclaw/dramaclaw.git
git clone https://github.com/dramaclaw/dramaclaw-gateway.git
cd dramaclaw

# 2. Siapkan konfigurasi
cp .env.example .env
#    Buka .env dan setidaknya ubah PROMPT_EXPORT_PASSWORD ke nilai non-default.
#    Konfigurasi saluran model dan key di UI web, bukan di .env.

# 3. Mulai — menjalankan api / newapi / web
docker compose up -d --build   # membangun api, web (checkout ini) dan gateway (../dramaclaw-gateway) dari sumber
# tanpa build? docker compose -f docker-compose.release.yml up -d   # menarik image terpublikasi, tidak perlu clone gateway

# 4. Pastikan sudah naik
docker compose ps   # api, newapi, dan web harus semuanya running
```

## Masukkan DC key Anda (sekali, wajib)

1. Buka **`http://localhost:8080`** di browser — ini adalah UI DNY.
2. Masuk ke Pengaturan → **Konfigurasi Model → Saluran Official**. Alamat gateway sudah terisi sebagai `https://relayclaw.cdnfg.com/v1`.
3. **Tempel DC key Anda** lalu klik "Simpan dan Aktifkan". Langsung berfungsi, **tanpa pemetaan model** (RelayClaw sudah mengonfigurasi semuanya di backend).

> CE default tanpa login, pengguna lokal tunggal (`ST_EDITION=ce`, dipaksa oleh compose). REST API ada di `http://localhost:8780` (browser hanya berbicara ke `web`, yang reverse-proxy ke `api`).

## Ingin memakai saluran model sendiri?

NewAPI bawaan mulai bersama `docker compose up -d`. Inisialisasi dan konfigurasi key upstream serta pemetaan model di Pengaturan → Konfigurasi Model → Custom. Alamat dan runtime token-nya disimpan di `settings.db` lokal, bukan `.env`. Lihat [Mengonfigurasi Model](configuring-models.md).

## Langkah berikutnya

- Setup diselaraskan dengan spek PC Anda: [Setup PC Lokal](setup-pc-lokal.md)
- Deployment/upgrade/backup lengkap: [Buku Panduan Self-Hosting](../../en/guides/self-hosting.md)
- Hubungkan model Anda sendiri: [Mengonfigurasi Model](configuring-models.md)
- Instalasi per platform: [Panduan Instalasi](installation.md)
