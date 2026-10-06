<!-- lang-switch -->
[English](../../en/getting-started/configuring-models.md) · [简体中文](../../zh/getting-started/configuring-models.md) · **Bahasa Indonesia**

# Mengonfigurasi Model

DNY CE memakai gateway yang kompatibel dengan NewAPI untuk model teks, vision, embedding, gambar, video, dan audio. Pengaturan model disimpan di `settings.db` lokal CE. Rahasia tidak pernah dikirim ke browser; yang ditampilkan hanya pratinjau status tersimpan yang sudah disamarkan.

Setelah startup, buka `http://localhost:8080` lalu masuk ke **Pengaturan → Model & Saluran**. Lencana **Aktif** di bagian atas menunjukkan mode runtime yang benar-benar berlaku, bukan sekadar tab yang sedang dilihat.

## Pilih mode gateway

| Mode | Kegunaan | Yang dikonfigurasi |
|---|---|---|
| Official | Memakai model yang disediakan RelayClaw | Hanya DC Key |
| Custom | Mengarahkan semua model lewat konfigurasi NewAPI Anda | Inisialisasi NewAPI, provider, model fitur, embedding, dan model media |
| Local + Official Hybrid | Mempertahankan model resmi sambil menambah model video Local ComfyUI, atau menimpa model resmi dengan ID yang sama | DC Key resmi, Local NewAPI, URL ComfyUI, dan workflow |

Aktifkan mode yang diinginkan setelah dikonfigurasi. Pekerjaan baru membaca mode, key, dan pemetaan terbaru. Pekerjaan yang sudah berjalan tidak berpindah gateway di tengah jalan.

## Mode Official

Mode Official adalah jalur pengaturan paling singkat:

1. Buka **Official**.
2. Masukkan RelayClaw DC Key Anda.
3. Klik **Simpan & Aktifkan**.

DNY mengelola URL gateway resmi. RelayClaw sudah menyediakan pemetaan `DC-*-LLM`, `DC-cognee-embedding`, dan model media resmi, sehingga pemetaan upstream di sisi CE tidak diperlukan.

Daftar gambar/video resmi beserta resolusi, rasio aspek, durasi, dan kemampuan media referensi berasal dari `src/novelvideo/official_media_models.json` yang dibundle.

### Memperbarui katalog model media resmi

Mode Official dan Local + Official Hybrid menampilkan versi katalog saat ini, jumlah model, dan sumbernya:

- Klik **Periksa Pembaruan** untuk mengambil katalog terbaru dari URL publikasi resmi DNY dan menerapkannya segera.
- **Perbarui katalog model resmi secara otomatis** nonaktif secara default. Saat diaktifkan, backend memeriksa setiap lima menit secara default, dan juga memeriksa segera saat panel pengaturan terkait dibuka.
- Katalog yang diunduh disimpan lokal di `state/local/official_media_models.json` dan tetap aktif setelah restart.
- DNY menolak katalog remote yang lebih lama dari versi aktif. Setelah upgrade aplikasi, katalog bawaan yang lebih baru mengungguli cache lokal yang lebih lama.
- Setelah pembaruan berhasil, browser XiaHua yang terbuka mengamati status katalog setiap menit selama pembaruan otomatis aktif, dan menyegarkan daftar model gambar serta video saat SHA256 konten berubah.
- API status melaporkan SHA256 konten aktif, revisi Git publikasi, waktu publikasi, URL remote, dan error pembaruan terakhir agar setiap instance dapat diaudit.

Pembaruan katalog resmi tidak mengubah saluran provider, pemetaan model, atau kemampuan yang dikelola di mode Custom.

Katalog resmi default memakai bucket `dramaclaw-dl` di Chengdu: `https://dramaclaw-dl.oss-cn-chengdu.aliyuncs.com/official-media-catalog/manifest.json`. Manifest menunjuk ke snapshot katalog beralamat SHA256 yang tidak pernah ditimpa. Backend memvalidasi manifest, versi katalog, dan SHA256 konten, serta memakai revalidasi ETag. Timpa default dengan `OFFICIAL_MEDIA_CATALOG_MANIFEST_URL`; `OFFICIAL_MEDIA_CATALOG_URL` tetap ada sebagai sumber JSON langsung warisan. Atur `OFFICIAL_MEDIA_CATALOG_POLL_SECONDS` untuk mengubah interval polling; minimum 60 detik.

Workflow repositori `publish-official-media-catalog` mengunggah `catalogs/<sha256>.json` dengan kebijakan cache immutable jangka panjang, lalu memublikasikan `manifest.json` dengan kebijakan cache 60 detik. Konfigurasi berikut sebagai secret repositori atau di environment GitHub `official-media-catalog`:

- Variabel bersifat opsional: default-nya `oss-cn-chengdu.aliyuncs.com`, `dramaclaw-dl`, dan `official-media-catalog`; timpa dengan `OFFICIAL_CATALOG_OSS_ENDPOINT`, `OFFICIAL_CATALOG_OSS_BUCKET`, dan `OFFICIAL_CATALOG_OSS_PREFIX`.
- Secret: `OFFICIAL_CATALOG_OSS_ACCESS_KEY_ID` dan `OFFICIAL_CATALOG_OSS_ACCESS_KEY_SECRET` diutamakan; jika tidak, workflow memakai `OSS_RELAY_AK` dan `OSS_RELAY_SK` tingkat organisasi.

Jaga `dramaclaw-dl` tetap privat dan berikan `GetObject` anonim hanya untuk prefix `official-media-catalog/*`. Identitas CI hanya perlu akses tulis ke prefix itu. Pull request Git tetap menjadi sumber kebenaran; mengaktifkan versioning OSS disarankan untuk pemulihan infrastruktur.

Untuk mendapatkan DC Key, kunjungi <https://relayclaw.cdnfg.com>.

## Mode Custom

### 1. Jalankan stack lokal

Gunakan file compose repositori (NewAPI bawaan selalu ikut):

```bash
docker compose up -d
```

Ini menjalankan API DNY, frontend web, dan NewAPI bawaan. DNY biasanya mencapai NewAPI lewat jaringan container. Port host yang dihadapi browser bisa berbeda dan tidak perlu mengganti URL internal.

File compose repositori mengaktifkan fitur setup dan manajemen saluran yang dibutuhkan UI pengaturan. Database SQLite NewAPI bawaan disimpan di volume Compose `newapi-data`. Path-nya `/data/one-api.db` di dalam container NewAPI, sementara API DNY mengelolanya lewat mount bersama `/newapi-data/one-api.db`. Biasanya Anda tidak perlu memasukkan path SQLite atau DSN secara manual.

### 2. Inisialisasi Local NewAPI

Buka **Custom**. Saat menampilkan “Inisialisasi diperlukan”:

1. Atur dan konfirmasi kata sandi akun root minimal delapan karakter untuk instance NewAPI baru.
2. Klik **Inisialisasi Local NewAPI**.

Inisialisasi:

- Membuat akun root NewAPI pertama hanya untuk instance baru.
- Membuat atau memakai ulang token `dramaclaw-ce-runtime`.
- Menyimpan URL runtime dan token di pengaturan lokal CE.
- Memverifikasi database SQLite dan akses manajemen.

DNY tidak menyimpan kata sandi root. Simpan sendiri untuk masuk ke NewAPI. Memasukkan kata sandi untuk instance yang sudah diinisialisasi tidak mereset kata sandi yang ada.

### 3. Terapkan profil yang direkomendasikan

Setelah inisialisasi, mulai dengan **Recommended**. Satu profil mengonfigurasi:

- Saluran provider dan key upstream.
- Pemetaan model fitur DNY.
- Model embedding Cognee, dimensi, dan ukuran batch.
- Pemetaan model gambar, video, dan audio.

Masukkan setiap key provider secara terpisah, lalu klik **Simpan & Terapkan Semua**. Key disimpan terpisah dan tidak pernah ditulis ke JSON profil. Biarkan kosong jika key sudah tersimpan; memasukkan nilai baru akan menggantikannya.

Template rekomendasi saat ini mencakup OpenRouter, VolcEngine, fal.ai, dan DoubaoAudio. Pemetaan speech yang direkomendasikan mempertahankan `index-tts-2` sebagai Model ID DNY sambil mengarahkannya lewat saluran DoubaoAudio ke model upstream `seed-audio-1.0`.

Profil rekomendasi bawaan bersifat read-only. Beralih ke **My Config** untuk mengedit dan menyimpan JSON Anda sendiri. Bentuk utamanya:

```json
{
  "version": 2,
  "name": "My CE profile",
  "channels": [
    {
      "id": "openrouter",
      "provider": "openrouter",
      "baseUrl": "",
      "priority": 0,
      "settings": {}
    }
  ],
  "featureModels": {
    "text": {"channel": "openrouter", "model": "upstream-text-model"},
    "vision": {"channel": "openrouter", "model": "upstream-vision-model"},
    "overrides": {}
  },
  "embedding": {
    "channel": "openrouter",
    "model": "upstream-embedding-model",
    "dimension": 1024,
    "batchSize": 10
  },
  "mediaModels": {
    "my-video-model": {
      "channel": "openrouter",
      "model": "upstream-video-model",
      "mediaType": "video",
      "label": "My Video Model",
      "enabled": true,
      "sortOrder": 100,
      "config": {}
    }
  }
}
```

Setiap `channel` merujuk ke `channels[].id`. Saat ini profil hanya mendukung satu entri per `provider`. Mengganti profil atau melihat JSON hanya mengubah template yang menunggu; tidak menimpa Advanced Settings yang aktif. Klik **Simpan & Terapkan Semua** untuk menulis saluran provider, model fitur, embedding, dan model media ke backend serta memperbarui daftar di bawahnya. Menyimpan Advanced Settings menyinkronkannya ke My Config agar tidak ada dua konfigurasi yang saling bersaing. Setelah profil rekomendasi bawaan berubah, terapkan ulang jika Advanced Settings masih menampilkan saluran atau model lama. Menghapus data browser tidak diperlukan.

Profil rekomendasi tidak membuat saluran ComfyUI secara default. Untuk memakai MiniMax H3 lokal, buka **Kelola Saluran** di Advanced Settings, tambahkan ComfyUI, lalu muat template dari area **ComfyUI Workflows** saluran tersebut. Template menambah workflow dan membuat draf model media `MiniMax-H3-local` yang sesuai.

### 4. Advanced Settings

Gunakan Advanced Settings untuk menyesuaikan hasil individual setelah menerapkan profil.

#### Saluran provider

Klik **Kelola Saluran** untuk membuka katalog provider yang didukung instance NewAPI saat ini. Tipe dan kemampuan provider dimuat dinamis dari `/api/channel/types`, dan setiap provider hanya bisa ditambahkan sekali. Cari berdasarkan nama provider atau filter menurut kemampuan teks, vision, embedding, gambar, video, dan audio. Provider yang baru ditambahkan muncul pertama di daftar saluran terkonfigurasi. Jika katalog gagal dimuat, pastikan RelayClaw CE berjalan lalu klik **Muat Ulang**.

Pemilih provider untuk model fitur, embedding, dan media difilter menurut tujuannya. Misalnya, model video menampilkan provider berkemampuan video, sementara fitur teks menampilkan provider berkemampuan teks. Seleksi yang sudah ada dan provider dengan metadata kemampuan yang sementara tidak tersedia tetap terlihat untuk diperiksa dan diperbaiki, bukan menghilang setelah upgrade.

- **Simpan Saluran** menyimpan preset saluran lokal CE.
- **Perbarui Saluran NewAPI** segera mengganti key dan Base URL saluran NewAPI yang cocok.
- **Override Base URL** biasanya kosong. Atur hanya untuk proxy kustom atau jika diminta provider.

Sebelum menghapus provider biasa, konfirmasi menampilkan berapa banyak pemetaan model fitur, model media, dan embedding yang terdampak. Menghapus provider tersimpan segera menyimpan daftar provider yang tersisa. Jika permintaan itu gagal, konfigurasi lokal dipertahankan. Menghapus provider biasa terakhir menyimpan daftar kosong, sehingga tidak kembali setelah refresh. ComfyUI memakai konfirmasi pembersihan khusus yang dijelaskan di bawah.

Setelah profil disimpan, key saluran harus menampilkan “Tersimpan” dan pratinjau yang disamarkan. Titik kata sandi tanpa lencana “Tersimpan” menandakan draf browser yang belum dikomit.

#### Model fitur

DNY memakai nama logis yang stabil seperti `DC-character-builder-LLM`, `DC-scene-builder-LLM`, dan `DC-freezone-vision-LLM`. Di mode Custom, pertahankan nama internal itu dan petakan ke model upstream nyata di NewAPI.

- Fitur teks dapat memakai model khusus teks.
- Fitur vision mengirim gambar atau video dan membutuhkan model multimodal yang sesuai.
- Pengisian massal hanya mengubah draf; klik Simpan Pemetaan setelahnya.
- Hermes dapat memakai model terpisah. Pemetaan `DC-*-LLM` lain dapat berbagi satu model upstream atau diganti satu per satu.
- Setelah upgrade yang menambah baris fitur (misalnya `DC-character-builder-LLM` di v2.0.3), baris baru mulai kosong dan tidak ditulis ke NewAPI sampai Anda memilih model lalu klik Simpan Pemetaan, atau menerapkan ulang profil cepat. Sampai saat itu fitur tersebut gagal dengan `No available channel for model DC-...`.

#### Embedding

`DC-cognee-embedding` mendukung knowledge graph novel dan pencarian semantik. Konfigurasi:

- Model embedding upstream.
- Dimensi keluarannya.
- Ukuran batch, default 10.

Model dan dimensi terikat saat proyek dibuat. Perubahan berikutnya otomatis hanya memengaruhi proyek baru. Bersihkan dan bangun ulang graph sebelum mengubah nilai ini untuk proyek yang sudah ada.

Untuk error embedding HTTP 400/422, pastikan model mendukung dimensi yang dikonfigurasi dan ukuran batch tidak melebihi batas `input` upstream.

#### Model gambar, video, dan audio

Konfigurasi model media mengontrol:

- Apakah model muncul di XiaHua.
- Label dan urutan.
- Model upstream yang dikirim ke NewAPI.
- Kontrol resolusi, rasio aspek, kualitas gambar, dan durasi.
- Mode text-to-video, frame pertama, frame pertama/terakhir, referensi gambar, all-reference, dan edit video.
- Batas referensi gambar/video/audio.
- Visibilitas kontrol human-review.
- Parameter permintaan spesifik model.

Model mainline bawaan menyediakan baseline kemampuan default dan tidak dapat dihapus dari konfigurasi. My Config dapat menambah model gambar atau video dan mengedit kemampuan model kustom. Simpan konfigurasi lengkap lalu refresh XiaHua untuk memuat katalog dan kontrol terbaru.

**Model ID** adalah pengenal stabil DNY. **Upstream Model** adalah model aktual yang dipakai saluran NewAPI; keduanya boleh berbeda.

### 5. Konfigurasi ComfyUI

Di mode **Custom**, tambahkan ComfyUI lewat **Advanced Settings → Saluran Provider**. Di **Local + Official Hybrid**, tambahkan lewat bagian **Konfigurasi ComfyUI** terpisah. Kedua mode memakai Local NewAPI dan data SQLite yang sama serta editor saluran yang sama.

Klik **Kelola Saluran** dan tambahkan ComfyUI dari katalog provider untuk menampilkan area **ComfyUI Workflows** di bawah saluran itu. **Muat Template MiniMax H3** hanya muncul di sana, sehingga pengguna yang tidak menambah ComfyUI tidak melihat pintasan itu. Memuat template menambah tiga workflow awal dan mengisi `http://127.0.0.1:8188` jika Base URL kosong. Tidak menimpa URL yang sudah terisi atau workflow yang sudah ada dengan ID yang sama. Simpan konfigurasi saluran dan model video setelahnya agar hasilnya tersimpan ke Local NewAPI.

Setiap konfigurasi saluran ComfyUI membutuhkan:

- Satu nama model yang dipakai DNY. Nama ini didaftarkan di Local NewAPI dan ditampilkan di XiaHua.
- URL layanan ComfyUI; default lokal `http://127.0.0.1:8188`.
- Satu atau lebih workflow. Setiap workflow punya **Workflow ID** unik dan ekspor **API Format Workflow JSON** ComfyUI; JSON workflow browser tidak diterima.
- Kemampuan media untuk model, termasuk mode, rasio, resolusi, durasi, dan batas media referensi.

Instance ComfyUI lokal biasa tidak membutuhkan API key, jadi biarkan kosong. Autentikasi relevan hanya jika ComfyUI berada di belakang proxy terotentikasi.

Satu nama model dapat mengikat beberapa workflow. DNY menyimpan nama model, Workflow ID, dan Workflow JSON ke NewAPI, sementara RelayClaw memilih workflow untuk setiap permintaan. XiaHua menampilkan satu model terpadu, bukan satu model per workflow.

Template MiniMax H3 memakai nama model `MiniMax-H3-local` dan mencakup workflow text-to-video, first-frame, serta all-reference. Kemampuan media awalnya mengaktifkan tiga mode itu, resolusi `480p`, `768p`, dan `1080p`, serta rasio `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, dan `9:16`. Ini nilai awal dan tetap dapat diedit di kemampuan model media.

Menghapus satu workflow hanya menghapus rute itu; tidak otomatis menghapus model terpadu. Untuk menghapus semuanya, gunakan **Hapus konfigurasi ComfyUI**, yang hanya muncul setelah ComfyUI dikonfigurasi. Setelah konfirmasi, itu menghapus saluran ComfyUI, workflow, dan pemetaan model media terkait dari pengaturan lokal dan NewAPI. Proyek dan media yang sudah dihasilkan tetap dipertahankan.

## Mode Local + Official Hybrid

Mode Hybrid mempertahankan RelayClaw sambil menghasilkan model video tertentu lewat Local ComfyUI:

1. Simpan DC Key di bawah **Official**.
2. Inisialisasi NewAPI sekali di bawah **Custom**; database SQLite yang sama dipakai ulang.
3. Buka **Local + Official Hybrid**.
4. Buka bagian **Konfigurasi ComfyUI** terpisah, klik **Kelola Saluran**, dan tambahkan ComfyUI dari katalog.
5. Muat template MiniMax H3 dari area **ComfyUI Workflows** saluran itu. Atau masukkan nama model video lokal dan tambahkan satu atau lebih Workflow ID beserta **API Format Workflow JSON**. URL default lokal adalah `http://127.0.0.1:8188`.
6. Simpan konfigurasi video dan aktifkan mode Hybrid.

API key ComfyUI bersifat opsional. Workflow harus memakai Format API, bukan format workflow browser. Mode Custom dan Hybrid berbagi saluran ComfyUI, workflow, dan kemampuan media; menyimpannya di salah satu mode memperbarui konfigurasi yang sama.

Selama saluran ComfyUI ada, tombol template MiniMax H3 tetap di area **ComfyUI Workflows** saluran itu agar template yang hilang dapat dipulihkan. Memuat lagi menggabungkan template ke workflow yang ada dan mempertahankan workflow yang dikonfigurasi pengguna dengan Workflow ID yang sama. Jika URL ComfyUI kosong, UI mengisi `http://127.0.0.1:8188`; tidak menimpa URL kustom yang sudah terisi.

Routing berdasarkan Model ID. Model Local ComfyUI dapat muncul di XiaHua sebagai model baru; jika berbagi ID dengan model video resmi, model lokal menimpa model resmi itu. Semua model lain tetap lewat RelayClaw. Menyimpan konfigurasi video menyimpan saluran ComfyUI terlebih dahulu lalu model medianya. DNY tidak otomatis jatuh kembali ke model resmi setelah kegagalan lokal. Pengguna memilih apakah akan mencoba ulang atau mengganti model. Mode Hybrid hanya mengelola model video Local ComfyUI, sehingga tidak membutuhkan pengaturan provider upstream resmi seperti OpenRouter atau VolcEngine.

## Penyimpanan media referensi

Edit gambar, frame pertama/terakhir video, gambar referensi, dan gambar identitas membutuhkan layanan upstream untuk membaca file lokal. Buka **Pengaturan → Penyimpanan Media** dan konfigurasikan relay media sementara yang dapat dijangkau publik.

### Aliyun OSS

Sediakan Bucket dan AccessKey dengan izin baca/tulis untuk Bucket itu. Sub-akun RAM dengan cakupan sempit direkomendasikan.

| Field UI | Variabel lingkungan | Contoh atau catatan |
|---|---|---|
| Endpoint | `OSS_RELAY_ENDPOINT` | `oss-cn-chengdu.aliyuncs.com`, tanpa `https://` |
| Bucket | `OSS_RELAY_BUCKET` | Bucket media sementara |
| AccessKey ID | `OSS_RELAY_AK` | AK terbatas Bucket |
| AccessKey Secret | `OSS_RELAY_SK` | SK yang cocok |
| TTL | `MEDIA_RELAY_TTL_SECONDS` | Default: 1800 detik |

Bucket tidak perlu akses public-read. DNY membuat URL bertanda tangan sementara untuk akses upstream.

### Cloudinary

Masukkan Cloud name, API Key, API Secret, dan folder opsional. Temukan di **Product environment settings → API Keys** di Cloudinary. Pengaturan database yang tersimpan mengungguli variabel lingkungan, dan rahasia penuh tidak pernah dikembalikan ke frontend.

## Pemecahan masalah

| Gejala | Yang diperiksa |
|---|---|
| Tidak ada lencana “Tersimpan” setelah menyimpan key | Nilai mungkin masih draf browser. Simpan/perbarui saluran itu atau terapkan ulang profil lengkap, dan pastikan image yang berjalan berisi kode terbaru. |
| Menambah model media bilang key providernya hilang | Saluran provider belum tersimpan ke NewAPI. Simpan/perbarui saluran sebelum menyimpan model media. |
| NewAPI melaporkan `No available channel for model ...` | Periksa pemetaan logis, status saluran, nama model upstream, dan grup. |
| Langkah terstruktur gagal dengan `Exceeded maximum output retries` di belakang relay berbasis Codex (Codex2API dll.) | Relay menghilangkan `tool_calls` pada `/v1/chat/completions`. Aktifkan **ChatCompletions → Responses Compatibility** untuk saluran itu di admin NewAPI. Lihat [panduan pemecahan masalah](../../en/guides/troubleshooting.md#model--gateway). |
| Inisialisasi Local NewAPI gagal | Periksa layanan NewAPI, mount SQLite, izin direktori, dan `NEWAPI_PROVISIONER_ENABLED`. |
| Model baru tidak ada di XiaHua | Pastikan diaktifkan, tipe media benar, konfigurasi lengkap disimpan, dan halaman di-refresh. |
| Kontrol tidak cocok dengan kemampuan model | Periksa `config` model media, terutama resolusi, rasio, mode, dan batas referensi. |
| Embedding knowledge-graph gagal | Periksa key, model upstream, dimensi, dan ukuran batch. HTTP 429 berarti rate limiting upstream. |
| Media referensi tidak dapat dibaca | Verifikasi penyimpanan media dan bahwa layanan upstream dapat menjangkau URL publik sementara. |
| Video lokal Hybrid gagal tanpa fallback resmi | Diharapkan: mode Hybrid tidak punya fallback kegagalan otomatis. |
| ComfyUI tidak dapat terhubung ke `127.0.0.1:8188` | `127.0.0.1` berarti lingkungan yang menjalankan backend DNY. Untuk container atau deployment remote, gunakan alamat host atau LAN yang dapat dijangkau dari backend itu. |
| Workflow MiniMax H3 melaporkan node atau model hilang | Pasang custom node dan file model yang dirujuk workflow rekomendasi, lalu sesuaikan workflow untuk nama file dan versi lokal. |

## File terkait

- `src/novelvideo/official_media_models.json`: model media resmi CE dan kemampuannya.
- `.env.example`: referensi variabel lingkungan.
- `docker-compose.yml` (build sumber) / `docker-compose.release.yml` (image): file deployment (api + NewAPI bawaan + web); mode gateway dipilih di Pengaturan.
- [Buku Panduan Self-Hosting](../../en/guides/self-hosting.md)
- [Referensi Variabel Lingkungan](../../en/reference/environment-variables.md)
