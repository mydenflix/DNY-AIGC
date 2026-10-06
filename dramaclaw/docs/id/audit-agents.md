# Audit kepatuhan AGENTS.md (PC lokal)

Checklist operasional terhadap [AGENTS.md](../../AGENTS.md) / [AGENTS_id.md](../../AGENTS_id.md)
dan sumber asli `Downloads/AGENTS.md`.

| Item AGENTS | Status | Catatan |
|-------------|--------|---------|
| Struktur repo (`src/novelvideo`, `tests`, `docs`, `frontend`, `LICENSES`, `sbom.spdx.json`) | OK | Path kepatuhan aktual: `scripts/compliance/`, `tests/compliance/` (bukan `docs/compliance/`) |
| Python 3.11–3.12 + `uv` | OK | Pin lokal: `.python-version` → 3.12 |
| `uv sync --group dev` | OK | Group `dev` di `.venv` |
| Pre-commit + gitleaks | OK | Hook terpasang; `gitleaks` + `banned-words` Passed |
| `uv run pytest tests/test_api_assets.py` (fokus) | OK | Assertion path Windows diperbaiki; tes sog Passed |
| `scripts/acceptance/run.sh` | OK | File ada |
| `DESIGN.md` | OK | Ada |
| Docker CE (`api` 8780, `web` 8080, `newapi` 3000) | OK | Container healthy / 200 |
| Health API | OK | Endpoint: `GET /healthz` → `{"status":"ok"}` |
| UI default Bahasa Indonesia | OK | Locale `id` |
| Docs ID | OK | `docs/id/` |

## Perintah verifikasi

```bash
cd D:/storyboard/dramaclaw
uv sync --group dev
pre-commit install
pre-commit run --all-files
uv run pytest tests/test_api_assets.py -q
docker compose ps
curl -s http://127.0.0.1:8780/healthz
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/
```

## Gap yang dilengkapi

1. **Pre-commit belum di PATH / hook** → `uv tool install pre-commit` + `pre-commit install`.
2. **Hook `banned-words` gagal di Windows** (`python3` / encoding cp1252) → entry memakai `uv run` + UTF-8; pesan sukses ASCII-safe.
3. **Referensi `docs/compliance/` di AGENTS** tidak ada di repo → AGENTS mengarah ke `scripts/compliance/` + `tests/compliance/`.
4. **Tes path Windows** (`endswith("/master_sharp.sog")`) → memakai `Path(...).name`.
5. **Health check** → dokumentasikan `/healthz` (bukan `/api/health`).
