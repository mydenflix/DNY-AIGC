# Audit SKILL.md (PC lokal)

Sumber: [`.hermes/skills/dramaclaw/SKILL.md`](../../.hermes/skills/dramaclaw/SKILL.md)  
Identik dengan `Downloads/SKILL.md`.

| Item SKILL.md | Status | Catatan |
|---------------|--------|---------|
| File skill + frontmatter (`requires.env`) | OK | `DRAMACLAW_API_URL` / `AGENT_TOKEN` / `PROJECT_ID` diinjeksikan runtime oleh chat Hermes |
| Playbooks `init` / `episode` / `resume` | OK | `.hermes/skills/dramaclaw/playbooks/` |
| References (7 wajib) | OK | + ekstra `run-modes.md` |
| Plugin tools `dramaclaw_*` | OK | 27 tool yang disebut di SKILL semuanya terdaftar; 7 tool ekstra di plugin |
| Identitas “我是虾导” | OK | `SOUL.md` / `MEMORY.md` default di `hermes_workspace.py` |
| Rute ingest hanya upload+start | OK | `src/novelvideo/api/routes/ingest.py` |
| `GET …/pipeline/status` | OK | OpenAPI + `pipeline.py` |
| `POST …/beats/{beat}/video` (single_video) | OK | OpenAPI |
| Default video `huimeng_seedance-1.0-pro-fast` | OK | Digunakan di kode/tes backend |
| Tes workspace Hermes | OK | `tests/test_hermes_workspace.py` + `test_mcp_ce_owner.py` → 37 passed |
| API hidup | OK | `/healthz` ok; OpenAPI 200 |

## Perintah verifikasi

```bash
cd D:/storyboard/dramaclaw
cmp -s ".hermes/skills/dramaclaw/SKILL.md" "/c/Users/DNY  PC/Downloads/SKILL.md" && echo identical
uv run pytest tests/test_hermes_workspace.py tests/test_mcp_ce_owner.py -q
curl -s http://127.0.0.1:8780/healthz
```

Env skill (bukan `.env` root statis): diisi otomatis saat sesi chat Hermes — lihat `src/novelvideo/chat/service.py` (`DRAMACLAW_API_URL`, `DRAMACLAW_AGENT_TOKEN`, `DRAMACLAW_PROJECT_ID`).

## Gap yang dilengkapi

1. Tes Hermes di Windows gagal membaca `SOUL.md` (cp1252) → semua `read_text`/`write_text` relevan memakai `encoding="utf-8"`.
2. Audit dokumentasi skill → `docs/id/audit-skill.md`.
