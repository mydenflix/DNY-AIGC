# supertale-fe

[English](./README.md) · **Bahasa Indonesia**

SPA React mandiri untuk SuperTale — frontend kreator asli untuk pipeline novel-ke-video. Menggantikan UI NiceGUI in-repo yang dikirim dari [`supertale-be`](https://github.com/claymorelab/SuperTale) dan berbicara ke REST API-nya secara eksklusif.

Ini adalah generasi "UI web tradisional" SuperTale. Pipeline chat-driven generasi berikutnya ada di `superchat` + `dramaclaw`.

## Stack

- **Vite 6** + **React 19** + **TypeScript strict**
- **TanStack Router** — routing berbasis file, lazy child routes untuk halaman fitur berat
- **TanStack Query** + **ky** — state server, query key hierarkis, invalidasi berbasis SSE
- **Zustand** (persisted) — auth + state klien
- **React Hook Form** + **Zod** — form dan validasi
- **shadcn/ui** (base-nova) + **Tailwind CSS 4** — design system
- **react-i18next** — id / en / zh / vi, HTTP backend
- **Native EventSource** — stream progres tugas jangka panjang
- **Vitest** + **MSW** — pengujian

## Prasyarat

- Node 20+
- Backend berjalan lokal: dari root repo `uv run novelvideo api --port 8780` (FastAPI di `:8780`)

## Mulai cepat

```bash
npm install
cp .env.example .env        # default VITE_API_URL sudah mengarah ke :8780
npm run dev                 # Vite dev server di :5173 (mem-proxy /api/v1 + /static ke :8780)
```

Masuk di <http://localhost:5173/login> dengan akun yang disediakan backend.

## Perintah

| Perintah                | Fungsi                                                          |
| ----------------------- | --------------------------------------------------------------- |
| `npm run dev`           | Vite dev server di :5173 dengan proxy `/api/v1` + `/static`     |
| `npm run build`         | `tsc -b && vite build` — bundle produksi di `dist/`             |
| `npm run build:ce`      | Bundle produksi CE source-available dengan env fallback CE      |
| `npm run preview`       | Menyajikan build produksi secara lokal                          |
| `npm test`              | Vitest sekali jalan                                             |
| `npm run test:watch`    | Mode watch Vitest                                               |
| `npx tsc --noEmit`      | Type check saja                                                 |

## Lingkungan

```bash
VITE_API_URL=http://localhost:8780   # proxy dev + origin API produksi
```

Build default dan EE memakai perintah `build` yang ada. Build rilis CE source-available memakai `build:ce`, yang memuat `.env.ce`.

Saat runtime, aplikasi tetap mengutamakan `GET /api/v1/config` dari backend sebagai sumber kebenaran. `VITE_EDITION=ce` hanya menentukan edisi fallback saat permintaan itu tidak tersedia.

Auth berbasis cookie. `AuthStore.login()` POST ke `/api/v1/auth/login` dengan `credentials: "include"`; backend mengatur cookie HttpOnly `st_api_key`, dan SPA hanya menyimpan `{ username, role }` sebagai penanda login. Setiap permintaan `ky` berikutnya memakai `credentials: "include"` agar browser melampirkan cookie. 401 pada permintaan apa pun mengeluarkan pengguna + hard-redirect ke `/login`.

## Peta rute

```
/login                                                    publik
/_app                                                     penjaga auth (sidebar + header)
  /                                                       dasbor proyek
  /projects/$project/ingest                               unggah novel, deteksi bab
  /projects/$project/characters                           CRUD karakter, potret, kostum
  /projects/$project/styles                               lab gaya (preset + kustom)
  /projects/$project/tasks                                monitor tugas (filter + deep-link)
  /projects/$project/episodes                             daftar episode + shell master-detail
    /episodes/$episode/overview                           brief / ringkasan / identitas
    /episodes/$episode/script                             edit beat, toggle ritme
    /episodes/$episode/sketches                           pemilih pool sketsa
    /episodes/$episode/audio                              TTS + penugasan suara
    /episodes/$episode/video                              generasi video per-beat
    /episodes/$episode/compose                            compose MP4 final
```

Semua rute episode di-code-split lewat `.lazy.tsx`.

## Tugas asinkron (SSE)

Operasi jangka panjang (ingest, script, sketch, video, compose) mengikuti pola ini:

1. Mutation mengembalikan `TaskResponse { ok, task_type, message }`
2. `useTaskStream` membuka `EventSource` di `/api/v1/tasks/{type}/{project}/{episode}/stream?api_key=…`
3. Server mendorong event bernama (`pending` / `starting` / `running` / `completed` / `failed`) dengan progres + tugas saat ini + hasil
4. Pada event terminal: stream ditutup, query key target di-invalidate, toast muncul
5. Halaman memakai `useStageTask` (wrapper bersama) untuk reconcile-on-mount, pembatalan nyata lewat `DELETE /tasks/{type}/{project}/{episode}`, dan komponen bersama `<StageProgressPanel>`

## Pengujian

- Unit: `npm test` (auth store, media-url, api client) — Vitest + MSW
- E2E: ad-hoc lewat [`gstack browse`](https://github.com/simonren/skills) (`$B`), belum ada framework otomatis
- **Penjaga biaya**: smoke walk tidak boleh mengklik Generate / Plan / Build / Analyze / Preview / Optimize / Regenerate — itu memicu endpoint LLM / image-gen / TTS / video berbayar

## Deployment

Di-host di Cloudflare Workers lintas empat environment berbasis tag:

| Env | URL | Pemicu |
| --- | --- | --- |
| dev     | <https://tale-dev.dramaclaw.ai>     | push ke `main` |
| test    | <https://tale-test.dramaclaw.ai>    | push tag `vX.Y.Z` |
| preview | <https://tale-preview.dramaclaw.ai> | `gh workflow run deploy.yml -f action=preview -f version=vX.Y.Z` (shadow-prod, digate Zero Trust) |
| prod    | <https://tale.dramaclaw.ai>         | `gh workflow run deploy.yml -f action=promote-prod -f version=vX.Y.Z` (canary 5%, ramp manual) |

Runbook lengkap — setup secret, ramp/rollback canary, konfigurasi Cloudflare Zero Trust, resep version-stamping, catatan — di [`DEPLOY.md`](./DEPLOY.md).

## Bacaan lanjutan

- [`CLAUDE.md`](./CLAUDE.md) — deep-dive arsitektur, alur auth, hierarki query key
- [`DEPLOY.md`](./DEPLOY.md) — runbook operator untuk keempat environment
- [`PROJECT_SPEC.md`](./PROJECT_SPEC.md) — spesifikasi produk lengkap
- [`DESIGN.md`](./DESIGN.md) — design system visual dan pola komponen
- [`docs/todo.md`](./docs/todo.md) — pekerjaan tersisa, item yang diblokir backend, yang baru dikirim

## Repo terkait

- [`claymorelab/SuperTale`](https://github.com/claymorelab/SuperTale) — `supertale-be`, FastAPI + pipeline NovelVideo
- `dramaclaw` / `superchat` — pipeline kreator chat-driven generasi berikutnya (internal)

## Dev multi-region lokal

Untuk melatih mode cluster `multi-region` end-to-end secara lokal:

1. **Jalankan dua instance backend** di port berbeda, misalnya `:8780` (cn-1) dan `:8781` (us-1). Masing-masing harus:
   - Mengatur `SUPERTALE_CORS_ORIGINS=http://localhost:5173` (atau mengeluarkan `Access-Control-Allow-Origin` echo-from-allowlist + `Allow-Credentials: true`)
   - Mengeluarkan cookie `st_api_key` dengan `SameSite=Lax` (same-origin di belakang gateway lokal)

2. **Dirikan edge dispatcher lokal.** Yang paling sederhana adalah Caddy:

   ```caddy
   tale.lingshan.localhost {
     @cn1 header Cookie *server-region=cn-1*
     @us1 header Cookie *server-region=us-1*
     handle @cn1 { reverse_proxy localhost:8780 }
     handle @us1 { reverse_proxy localhost:8781 }
     handle /api/* { respond 400 `{"ok":false,"error":"no_region"}` }
     handle /static/* { respond 400 `{"ok":false,"error":"no_region"}` }
     handle { reverse_proxy localhost:5173 }
   }
   ```

   Sediakan manifest region di origin SPA (edge menyajikannya secara statis — cookie tidak diperlukan):

   ```
   # /cluster-config.json
   { "regions": [ { "id": "cn-1", "displayName": "CN-1" }, { "id": "us-1", "displayName": "US-1" } ] }
   ```

3. **Konfigurasi SPA.** Buat `.env.local`:

   ```
   VITE_CLUSTER_MODE=multi-region
   VITE_CLUSTER_REGIONS_URL=/cluster-config.json
   ```

4. `pnpm dev` (atau `npm run dev`) lalu kunjungi `http://tale.lingshan.localhost`. Anda harus melihat pemilih region di `/login`.

### Checklist smoke-test

- [ ] Masuk ke cn-1, edit beat, buka panel tugas.
- [ ] Klik lencana region → pilih us-1 → konfirmasi. Halaman harus hard-reload ke `/login` dengan us-1 sudah terpilih.
- [ ] DevTools → Application → Local Storage: `st.episode.*`, `supertale-auth`, `supertale-seen-pools` hilang; `supertale-app` dan `i18nextLng` masih ada.
- [ ] DevTools → Application → Cookies: `server-region=us-1`; `st_api_key` diterbitkan oleh us-1 (bukan yang basi dari cn-1).
- [ ] Buka tab kedua yang masuk ke us-1; kembali ke tab pertama; picu aksi apa pun. Tab pertama harus menampilkan banner lockdown dan hard-reload.
- [ ] Hit `/api/*` basi tanpa cookie `server-region`: edge mengembalikan `400 no_region`; FE membersihkan region dan mengalihkan ke `/login`.

## Lisensi

[Elastic License 2.0](../LICENSE) — Copyright (c) 2026 ClaymoreLab. Source available; lihat [LICENSE](../LICENSE) dan [NOTICE](../NOTICE) di root.
