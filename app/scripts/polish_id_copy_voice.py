#!/usr/bin/env python3
"""Tighten Indonesian chrome: natural, short, no fluff."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "frontend" / "public" / "locales" / "id" / "translation.json"

PATH_MAP: dict[str, str] = {
    "common.novelImportRequired": "Impor novel dulu",
    "common.insufficientCredits": "Kredit kurang. Hubungi admin untuk isi ulang.",
    "common.billingRuleNotConfigured": "Aturan penagihan belum diatur. Hubungi admin.",
    "freezone.canvasSync.needsMigration": "Data kanvas perlu migrasi. Hubungi admin.",
    "characters.voiceSamples.recordInsecureContext": (
        "Mikrofon hanya aktif di HTTPS atau localhost."
    ),
    "characters.voiceSamples.recordNoDevice": "Mikrofon tidak terdeteksi. Cek perangkat.",
    "auth.businessWechat.note": "Untuk kemitraan, tulis catatan singkat — kami prioritaskan.",
    "ingest.uploadingHint": "Tetap di halaman ini sampai unggahan selesai.",
    "episode.renderPlan.stale.input": "Input berubah (karakter atau teks beat). Konfirmasi ulang.",
    "episode.renderPlan.stale.plan": "Perencana diperbarui. Konfirmasi ulang.",
    "node.imageEdit.promptRequired": "Masukkan prompt",
    "node.audio.uploadTypeError": "Unggah file audio",
    "node.videoNode.submitBusy": "Sedang menghasilkan…",
    "settings.modelConfig.official.missingFields": "Isi kunci API.",
    "errorDialog.openRouterConfigMessage": (
        "Model ini butuh OpenRouter, tetapi kunci API belum dikonfigurasi. Hubungi admin."
    ),
    "productSurface.misconfigured": (
        "Ketersediaan fitur belum lengkap. Hubungi admin."
    ),
    "common.loading": "Memuat…",
    "auth.signingIn": "Sedang masuk…",
    "taskCenter.statusBar.connecting": "Menghubungkan…",
    "taskCenter.statusBar.reconnecting": "Menyambung ulang…",
    "taskCenter.statusBar.polling": "Memeriksa status…",
    "myBuddy.dragHint": "Seret untuk pindah",
    "myBuddy.bubbles.running.holdOn": "Sebentar.",
    "myBuddy.bubbles.running.keepWindowOpen": "Jaga jendela ini terbuka.",
    "myBuddy.bubbles.idle.standingBy": "Siap dipanggil.",
    "myBuddy.bubbles.idle.noRush": "Tidak perlu buru-buru.",
    "header.account.phoneBinding.description": (
        "Verifikasi kata sandi dan telepon untuk tautkan ke akun. "
        "Lalu bisa masuk dengan kode."
    ),
    "episode.compose.composeHint": (
        "Pastikan semua beat punya sketsa, audio, dan video. "
        "Klik Compose Episode untuk menghasilkan."
    ),
    "freezone.shell.conflict.detail": (
        "Kanvas diubah di jendela lain. Segarkan akan buang perubahan lokal yang belum disimpan."
    ),
}


def set_path(root: dict, dotted: str, value: str) -> bool:
    parts = dotted.split(".")
    cur: dict = root
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            return False
        cur = nxt
    if parts[-1] not in cur:
        return False
    cur[parts[-1]] = value
    return True


def strip_fluff(text: str) -> str:
    """Light regex-free trims for leftover courtesy openers."""
    replacements = (
        ("Silakan ", ""),
        ("silakan ", ""),
        ("Harap ", ""),
        ("harap ", ""),
        ("mohon tunggu", "tunggu sebentar"),
        ("Mohon tunggu", "Tunggu sebentar"),
        (", mohon tunggu", "…"),
        ("dengan senang hati", ""),
    )
    out = text
    for old, new in replacements:
        if old in out:
            out = out.replace(old, new)
    # collapse double spaces from removals
    while "  " in out:
        out = out.replace("  ", " ")
    return out.strip()


def walk_strip(obj: object) -> int:
    changed = 0
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if isinstance(value, str):
                new = strip_fluff(value)
                if new != value:
                    obj[key] = new
                    changed += 1
            else:
                changed += walk_strip(value)
    elif isinstance(obj, list):
        for item in obj:
            changed += walk_strip(item)
    return changed


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    path_hits = sum(1 for key, value in PATH_MAP.items() if set_path(data, key, value))
    strip_hits = walk_strip(data)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    missing = [k for k in PATH_MAP if not _exists(data, k)]
    print(f"path overrides: {path_hits}/{len(PATH_MAP)}")
    print(f"fluff strips: {strip_hits}")
    if missing:
        print(f"missing: {missing[:10]}")
    print("json ok")


def _exists(root: dict, dotted: str) -> bool:
    cur: object = root
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


if __name__ == "__main__":
    main()
