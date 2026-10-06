<!-- lang-switch -->
[English](./AGENTS.md) · **Bahasa Indonesia**

# Panduan Repositori (AGENTS)

## Struktur Proyek & Organisasi Modul

Repositori ini berisi backend SuperTale Community Edition dan pipeline video. Kode Python ada di `src/novelvideo/`, dengan area utama seperti `api/` untuk rute FastAPI, `task_backend/` untuk eksekusi pekerjaan, `generators/` untuk generasi media, `verification/` untuk quality gate, `ports/` untuk batas antarmuka, dan `assets/` untuk media bawaan. Tes ada di `tests/`, dengan tes kontrak di `tests/contract/`, tes berfokus port di `tests/ports/`, dan tes kepatuhan di `tests/compliance/`. Skrip operasional di `scripts/` (termasuk `scripts/compliance/` dan `scripts/acceptance/`). Dokumentasi di `docs/` (Bahasa Indonesia di `docs/id/`), contoh di `examples/`, dan artefak kepatuhan di `LICENSES/`, `sbom.spdx.json`, serta `frontend/THIRD-PARTY-LICENSES.txt`. Frontend SPA ada di `frontend/` (locale UI: `id` / `en` / `zh` / `vi`).

## Perintah Build, Tes, dan Pengembangan

- `uv sync --group dev`: instal dependensi runtime dan pengembangan dari `uv.lock`.
- `uv run novelvideo api --port 8780`: jalankan REST API lokal.
- `uv run pytest`: jalankan suite tes default; `pyproject.toml` mengecualikan marker `ee` dan `e2e` secara default.
- `uv run pytest tests/test_api_assets.py`: jalankan satu file tes saat iterasi.
- `scripts/acceptance/run.sh`: jalankan pemeriksaan acceptance saat memvalidasi perilaku API yang lebih luas.
- `pre-commit run --all-files`: jalankan hook repositori, saat ini termasuk pemindaian rahasia `gitleaks`.

Jalur Docker (disarankan untuk menjalankan CE penuh sesuai README):

```bash
cp .env.example .env   # setidaknya ubah PROMPT_EXPORT_PASSWORD
docker compose up -d --build   # api :8780 · newapi :3000 · web :8080
```

Dokumentasi setup lokal: [Mulai Cepat](docs/id/getting-started/quickstart.md) · [Instalasi](docs/id/getting-started/installation.md) · [Mengonfigurasi Model](docs/id/getting-started/configuring-models.md) · [Setup PC Lokal](docs/id/getting-started/setup-pc-lokal.md).

## Gaya Kode & Konvensi Penamaan

Gunakan kode yang kompatibel dengan Python 3.11–3.12 dan jaga impor/path paket berakar di `src/novelvideo`. Ikuti gaya yang ada: indentasi 4 spasi, type hint untuk antarmuka publik serta model dataclass/Pydantic, snake_case untuk fungsi dan modul, PascalCase untuk kelas, dan nama huruf besar untuk konstanta. Jaga handler rute tetap tipis dan pindahkan perilaku yang dapat digunakan ulang ke service, port, atau task runner yang selaras dengan modul di sekitarnya. Jangan commit media hasil generate atau state runtime lokal.

Untuk setiap perubahan visual frontend, baca `DESIGN.md` terlebih dahulu — itu sumber kebenaran untuk warna, tipografi, spasi, radius, elevasi, dan motion, serta mencerminkan variabel CSS di `frontend/src/index.css`. Saat variabel itu berubah, perbarui `DESIGN.md` dalam commit yang sama dan jaga `npx @google/design.md lint DESIGN.md` tetap 0 error.

## Panduan Pengujian

Tes memakai `pytest` dengan `pytest-asyncio` mode auto. Namai file tes `test_*.py` dan kolokasikan fixture di `tests/conftest.py` kecuali cakupannya sempit. Tandai tes khusus enterprise atau end-to-end penuh dengan `@pytest.mark.ee` atau `@pytest.mark.e2e` agar jalankan default tetap ramah community edition. Tambahkan tes regresi terfokus untuk kontrak API, perubahan siklus hidup tugas, migrasi storage, dan penanganan error provider.

## Panduan Commit & Pull Request

Riwayat terkini memakai prefix konvensional singkat seperti `fix:`, `feat(scope):`, `refactor(scope):`, dan `chore(scope):`; jaga subjek tetap imperatif dan spesifik. PR harus mendeskripsikan perubahan yang terlihat pengguna, mencantumkan perintah verifikasi, menautkan isu terkait, dan menyertakan screenshot atau sampel keluaran API untuk perubahan kontrak UI/API. Catat secara eksplisit dampak migrasi, konfigurasi, model-provider, atau kepatuhan.

## Tip Keamanan & Konfigurasi

Jangan commit key provider, signed URL, kredensial, atau secret hasil generate. Konfigurasi akses model lewat UI **Pengaturan → Konfigurasi Model** (Official / Custom / Hybrid) dan variabel lingkungan bila diperlukan (misalnya di `.env`, yang sudah di-gitignore). Jalankan hook pre-commit gitleaks sebelum membagikan perubahan yang menyentuh konfigurasi, provisioning, backup, atau kode gateway.
