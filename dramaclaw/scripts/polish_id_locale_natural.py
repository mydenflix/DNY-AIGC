#!/usr/bin/env python3
"""Second pass: natural, concise Indonesian chrome (no fluff, no leftover English)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "frontend" / "public" / "locales" / "id" / "translation.json"

PATH_MAP: dict[str, str] = {
    # common
    "common.loading": "Memuat…",
    "common.success": "Berhasil",
    "common.error": "Terjadi kesalahan",
    "common.novelImportRequired": "Impor novel dulu",
    "common.insufficientCredits": "Kredit kurang. Hubungi admin untuk isi ulang.",
    "common.billingRuleNotConfigured": "Aturan penagihan belum diatur. Hubungi admin.",
    "common.billingRuleNotConfiguredShort": "Atur",
    "common.cancel": "Batal",
    "common.delete": "Hapus",
    "common.save": "Simpan",
    "common.confirm": "Konfirmasi",
    "common.back": "Kembali",
    "common.refreshDone": "Selesai",
    # nav
    "nav.home": "Beranda",
    "nav.collapse": "Ciutkan",
    "nav.creation": "Kreasi",
    "nav.production": "Produksi",
    "nav.tools": "Alat",
    "nav.creationMode": "Mode kreasi",
    "nav.xiaji": "Serial",
    "nav.xiajiMenu": "Menu serial",
    "nav.ingest": "Sumber cerita",
    "nav.assets": "Perpustakaan aset",
    "nav.characters": "Karakter",
    "nav.episodes": "Studio episode",
    "nav.script": "Naskah",
    "nav.literalScript": "Naskah literal",
    "nav.sketches": "Sketsa",
    "nav.audio": "Audio",
    "nav.video": "Video",
    "nav.compose": "Komposit",
    "nav.styles": "Gaya visual",
    "nav.tasks": "Pusat tugas",
    "nav.taskCenter": "Pusat tugas",
    "nav.aiAssistant": "Direktur Xia",
    "nav.freezone": "Freezone",
    "nav.switchProject": "Ganti proyek",
    "nav.allProjects": "Semua proyek",
    # auth
    "auth.login": "Masuk",
    "auth.logout": "Keluar",
    "auth.username": "Nama pengguna",
    "auth.account": "Akun",
    "auth.accountPlaceholder": "Masukkan akun",
    "auth.accountOrPhone": "Akun atau telepon",
    "auth.accountOrPhonePlaceholder": "Masukkan akun atau nomor telepon",
    "auth.password": "Kata sandi",
    "auth.passwordTab": "Kata sandi",
    "auth.loginMethod": "Pilih cara masuk",
    "auth.loginButton": "Masuk",
    "auth.loginFailed": "Nama pengguna atau kata sandi salah",
    "auth.welcomeBack": "Selamat datang kembali",
    "auth.signInSubtitle": "Masuk untuk lanjut bekerja",
    "auth.signInEyebrow": "Masuk",
    "auth.welcomeSub": "Dunia menunggu ceritamu.",
    "auth.usernamePlaceholder": "nama.akun",
    "auth.passwordPlaceholder": "••••••••",
    "auth.forgot": "Lupa?",
    "auth.forgotHint": "Hubungi admin ruang kerja untuk reset kata sandi.",
    "auth.remember": "Tetap masuk di perangkat ini",
    "auth.showPassword": "Tampilkan kata sandi",
    "auth.hidePassword": "Sembunyikan kata sandi",
    "auth.signingIn": "Sedang masuk…",
    "auth.language": "Bahasa",
    "auth.contactUs": "Hubungi kami",
    "auth.learnMore": "Pelajari lebih lanjut",
    "auth.openManual": "Buka panduan",
    "auth.learnMoreToast": "Panduan resmi masih disusun — nanti ya.",
    "auth.closeLogin": "Tutup dialog masuk",
    "auth.privacy": "Privasi",
    "auth.terms": "Ketentuan",
    "auth.docs": "Dokumen",
    "auth.tagline": "Ubah novel jadi drama",
    # settings
    "settings.title": "Pengaturan",
    "settings.close": "Tutup",
    "settings.navigationLabel": "Kategori pengaturan",
    "settings.statusConfigured": "{{page}} sudah dikonfigurasi",
    "settings.statusNotConfigured": "{{page}} belum dikonfigurasi",
    "settings.secretSavedBadge": "Tersimpan",
    "settings.secretSavedPlaceholder": "Tersimpan · {{preview}} (isi ulang untuk ganti)",
    "settings.pages.models": "Model & saluran",
    "settings.pages.storage": "Penyimpanan media",
    "settings.modelConfig.title": "Konfigurasi model",
    "settings.modelConfig.description": (
        "Pilih gateway resmi, atur NewAPI sendiri, atau gabungkan keduanya."
    ),
    "settings.modelConfig.baseUrlHint": "Runtime CE mengatur URL NewAPI lokal otomatis.",
    "settings.modelConfig.effectiveBadge": "Aktif: {{channel}}",
    "settings.modelConfig.guide": "Panduan konfigurasi",
    "settings.modelConfig.loading": "Memuat…",
    "settings.modelConfig.requestFailed": "Permintaan gagal, coba lagi.",
    "settings.modelConfig.activateMode": "Jadikan aktif",
    "settings.modelConfig.configureBeforeActivate": "Atur mode ini dulu sebelum diaktifkan.",
    # task center / leftover English
    "tasks.status.cancelled": "Dibatalkan",
    "canvas.shortcuts.groups.create": "Buat",
    "taskCenter.panel.open": "Buka pusat tugas",
    "taskCenter.panel.selectPrompt": "Pilih tugas untuk lihat detail.",
    "taskCenter.statusBar.connecting": "Menghubungkan…",
    "taskCenter.statusBar.reconnecting": "Menyambung ulang…",
    "taskCenter.statusBar.polling": "Memeriksa status…",
    "taskCenter.statusBar.offline": "Offline",
    "taskCenter.detail.logs.placeholder": "Belum ada log.",
    "taskCenter.relative.justNow": "baru saja",
    "notifications.title": "Pengumuman",
    "header.notifications": "Pengumuman",
    # myBuddy — ringkas, natural, tanpa basa-basi
    "myBuddy.dragHint": "Seret untuk pindah posisi",
    "myBuddy.companion.entry": "Teman",
    "myBuddy.companion.title": "Pilih teman",
    "myBuddy.companion.titleBadgeAlt": "Oke, temanku",
    "myBuddy.companion.importCta": "Impor teman",
    "myBuddy.companion.toggleVisibility": "Tampilkan teman",
    "myBuddy.import.button": "Impor",
    "myBuddy.import.title": "Impor hewan peliharaan petdex",
    "myBuddy.import.desc": (
        "Pilih spritesheet.webp (wajib) dan pet.json (opsional) dari petdex."
    ),
    "myBuddy.import.spritesheetTitle": "Klik atau seret spritesheet.webp",
    "myBuddy.import.spritesheetHint": "Wajib · spritesheet webp / png",
    "myBuddy.import.jsonTitle": "Klik atau lepas pet.json",
    "myBuddy.import.jsonHint": "Opsional · untuk nama",
    "myBuddy.import.choose": "Pilih berkas",
    "myBuddy.import.replace": "Ganti",
    "myBuddy.gallery.title": "Pilih teman",
    "myBuddy.gallery.tabLibrary": "Perpustakaan",
    "myBuddy.gallery.tabMine": "Milik saya",
    "myBuddy.gallery.select": "Pilih",
    "myBuddy.gallery.selected": "Dipilih",
    "myBuddy.gallery.search": "Cari nama…",
    "myBuddy.gallery.loading": "Memuat…",
    "myBuddy.gallery.officialGroup": "Teman resmi",
    "myBuddy.gallery.peripheralGroup": "Koleksi teman",
    "myBuddy.bubbles.walkBy": "Lewat diam-diam~",
    "myBuddy.bubbles.running.queued": "Siap, aku kerjakan.",
    "myBuddy.bubbles.running.working": "Sedang dikerjakan.",
    "myBuddy.bubbles.running.holdOn": "Sebentar ya.",
    "myBuddy.bubbles.running.gears": "Mesinnya lagi berputar.",
    "myBuddy.bubbles.running.onIt": "Aku yang urus.",
    "myBuddy.bubbles.running.readingRoom": "Membaca situasinya.",
    "myBuddy.bubbles.running.keepWindowOpen": "Biarkan jendela ini terbuka.",
    "myBuddy.bubbles.running.checkingEdges": "Memeriksa detailnya.",
    "myBuddy.bubbles.running.smallSteps": "Satu langkah demi satu.",
    "myBuddy.bubbles.running.movingPieces": "Bagiannya sedang bergerak.",
    "myBuddy.bubbles.success.done": "Selesai.",
    "myBuddy.bubbles.success.nice": "Berhasil.",
    "myBuddy.bubbles.success.landed": "Hasilnya rapi.",
    "myBuddy.bubbles.success.tidy": "Semua siap.",
    "myBuddy.bubbles.success.flag": "Langkah ini oke.",
    "myBuddy.bubbles.success.cleared": "Sudah bersih.",
    "myBuddy.bubbles.success.goodShape": "Bagusnya bagus.",
    "myBuddy.bubbles.success.savedTrip": "Lebih hemat langkah.",
    "myBuddy.bubbles.success.noDrama": "Tanpa drama kali ini.",
    "myBuddy.bubbles.success.oneLessThing": "Satu tugas kurang.",
    "myBuddy.bubbles.failure.stuck": "Macet di sini.",
    "myBuddy.bubbles.failure.checking": "Aku cek dulu.",
    "myBuddy.bubbles.failure.retry": "Ditandai untuk dicek lagi.",
    "myBuddy.bubbles.failure.noted": "Sudah kulihat.",
    "myBuddy.bubbles.failure.box": "Kotaknya berkedip.",
    "myBuddy.bubbles.failure.hitSnag": "Ada kendala.",
    "myBuddy.bubbles.failure.needsLook": "Perlu dicek.",
    "myBuddy.bubbles.failure.leftClue": "Ada petunjuk di situ.",
    "myBuddy.bubbles.failure.tryAgainLater": "Bisa coba lagi nanti.",
    "myBuddy.bubbles.failure.notClean": "Belum bersih.",
    "myBuddy.bubbles.idle.watching": "Aku di sini.",
    "myBuddy.bubbles.idle.quiet": "Tenang di sini.",
    "myBuddy.bubbles.idle.standingBy": "Panggil saja.",
    "myBuddy.bubbles.idle.idea": "Ide butuh sebentar.",
    "myBuddy.bubbles.idle.tinyBreak": "Istirahat sebentar.",
    "myBuddy.bubbles.idle.noRush": "Tidak perlu buru-buru.",
    "myBuddy.bubbles.idle.roomBreathes": "Biarkan halaman bernapas.",
    "myBuddy.bubbles.idle.stillHere": "Masih online.",
    "myBuddy.bubbles.idle.goodPause": "Jeda sebentar tidak apa-apa.",
    "myBuddy.bubbles.idle.mindingTop": "Jaga sudut ini.",
    "myBuddy.bubbles.idle.keepRhythm": "Jaga ritmenya.",
    "myBuddy.bubbles.idle.littleCorner": "Di pojokan ini.",
    "myBuddy.bubbles.idle.online": "Siaga, tetap online.",
    "myBuddy.bubbles.idle.nextStep": "Menunggu langkah berikutnya.",
    "myBuddy.bubbles.idle.smallPatrol": "Patroli kecil.",
    "myBuddy.bubbles.idle.softPause": "Sedang menahan.",
    "myBuddy.bubbles.dragonBoat.leafScent": "Aroma daun zongzi di udara.",
    "myBuddy.bubbles.dragonBoat.tightWrap": "Bungkus pelan-pelan.",
    "myBuddy.bubbles.dragonBoat.waterQuiet": "Anginnya tenang.",
    "myBuddy.bubbles.dragonBoat.goodStroke": "Daun kecil lagi bertugas.",
    "myBuddy.bubbles.dragonBoat.steadyBoat": "Aroma daunnya bersih hari ini.",
}


def set_path(root: dict, dotted: str, value: str) -> bool:
    parts = dotted.split(".")
    cur: dict = root
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            return False
        cur = nxt
    leaf = parts[-1]
    if leaf not in cur:
        return False
    cur[leaf] = value
    return True


def fix_mojibake_ellipsis(obj: object) -> int:
    """Replace broken '…' (U+2026) encodings and ASCII '...' with proper ellipsis."""
    changed = 0
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if isinstance(value, str):
                new = value.replace("...", "…")
                # common mojibake when UTF-8 … was read as latin-1 then re-encoded
                for bad in ("â€¦", "Ã¢â‚¬Â¦", "\ufffd"):
                    if bad in new:
                        new = new.replace(bad, "…")
                # trailing lone replacement often from truncated …
                if new.endswith("Memuat") or new.endswith("menghubungkan"):
                    pass
                if new != value:
                    obj[key] = new
                    changed += 1
            else:
                changed += fix_mojibake_ellipsis(value)
    elif isinstance(obj, list):
        for item in obj:
            changed += fix_mojibake_ellipsis(item)
    return changed


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    path_hits = sum(1 for key, value in PATH_MAP.items() if set_path(data, key, value))
    ellipsis_hits = fix_mojibake_ellipsis(data)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(PATH.read_text(encoding="utf-8"))
    missing = [k for k in PATH_MAP if not _path_exists(data, k)]
    print(f"path overrides: {path_hits}/{len(PATH_MAP)}")
    print(f"ellipsis fixes: {ellipsis_hits}")
    if missing:
        print(f"missing keys ({len(missing)}): {missing[:20]}")
    print("json ok")


def _path_exists(root: dict, dotted: str) -> bool:
    cur: object = root
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


if __name__ == "__main__":
    main()
