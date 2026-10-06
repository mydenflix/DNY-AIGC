# -*- coding: utf-8 -*-
"""Rewrite Indonesian locale copy to be concise and natural."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path("frontend/public/locales/id/translation.json")

# Exact path → new value (dot paths; lists use [i])
EXACT: dict[str, str] = {
    # —— login cinematic chrome ——
    "loginCinematic.moreInfo": "Info lainnya",
    "loginCinematic.moreInfoShort": "Lainnya",
    "loginCinematic.announcement.open": "Lihat pengumuman",
    "loginCinematic.announcement.label": "Pengumuman",
    "loginCinematic.announcement.title": "Pengumuman",
    "loginCinematic.announcement.close": "Tutup",
    "loginCinematic.announcement.confirm": "Mengerti",
    "loginCinematic.announcement.markAllRead": "Tandai semua dibaca",
    "loginCinematic.announcement.unread": "{{n}} belum dibaca",
    "loginCinematic.announcement.pinned": "Disematkan",
    "loginCinematic.testimonials.heading": "Bukan lagi halaman kosong",
    "loginCinematic.testimonials.subheading": "Dari satu kalimat premis langsung ke jalur produksi.",
    "loginCinematic.testimonials.quotes.shortFilmDirector.name": "Sutradara film pendek",
    "loginCinematic.testimonials.quotes.shortFilmDirector.tag": "Previz konsep",
    "loginCinematic.testimonials.quotes.shortFilmDirector.text": "Konflik dan bidikan terlihat dulu, baru putuskan cabang mana yang diproduksi.",
    "loginCinematic.testimonials.quotes.aiCreator.name": "Kreator video AI",
    "loginCinematic.testimonials.quotes.aiCreator.tag": "Klip bersambung",
    "loginCinematic.testimonials.quotes.aiCreator.text": "Yang berguna bukan satu gambar—tapi mendorong klip terus maju.",
    "loginCinematic.testimonials.quotes.screenwriter.name": "Penulis naskah",
    "loginCinematic.testimonials.quotes.screenwriter.tag": "Tes karakter",
    "loginCinematic.testimonials.quotes.screenwriter.text": "Karakter, konflik, dan latar terpisah—lebih cepat nilai apakah cerita layak ditulis.",
    "loginCinematic.testimonials.quotes.animationTeam.name": "Tim animasi",
    "loginCinematic.testimonials.quotes.animationTeam.tag": "Cek ritme",
    "loginCinematic.testimonials.quotes.animationTeam.text": "Previz dulu: cek ritme dan bidikan, baru masuk produksi.",
    "loginCinematic.testimonials.quotes.indieProducer.name": "Produser independen",
    "loginCinematic.testimonials.quotes.indieProducer.tag": "Trailer",
    "loginCinematic.testimonials.quotes.indieProducer.text": "Ide jadi sesuatu yang bisa ditonton—diskusi tidak berhenti di catatan.",
    "loginCinematic.testimonials.quotes.visualDirector.name": "Direktur visual",
    "loginCinematic.testimonials.quotes.visualDirector.tag": "Perluasan dunia",
    "loginCinematic.testimonials.quotes.visualDirector.text": "Dunia terus bercabang, tetap terkendali.",
    "loginCinematic.testimonials.quotes.storyPlanner.name": "Perencana cerita",
    "loginCinematic.testimonials.quotes.storyPlanner.tag": "Pilih cabang",
    "loginCinematic.testimonials.quotes.storyPlanner.text": "Buang cabang mati cepat; fokus ke yang ada ketegangannya.",
    "loginCinematic.testimonials.quotes.creativeStudio.name": "Studio kreatif",
    "loginCinematic.testimonials.quotes.creativeStudio.tag": "Contoh nada",
    "loginCinematic.testimonials.quotes.creativeStudio.text": "Dari satu baris premis sampai klip yang bisa dibahas bersama.",
    "loginCinematic.testimonials.quotes.directorAssistant.name": "Asisten sutradara",
    "loginCinematic.testimonials.quotes.directorAssistant.tag": "Susunan bidikan",
    "loginCinematic.testimonials.quotes.directorAssistant.text": "Bidikan tidak berhamburan—tiap generasi kembali ke jalur yang sama.",
    "loginCinematic.faq.heading": "Tanya jawab singkat",
    "loginCinematic.faq.subheading": "Generasi, kontrol, kolaborasi, dan bisnis—yang benar-benar memengaruhi keputusan.",
    "loginCinematic.faq.contactPrompt": "Butuh kerja sama khusus?",
    "loginCinematic.faq.contactOpen": "Buka kontak bisnis",
    "loginCinematic.faq.contactCta": "Hubungi penjualan",
    "loginCinematic.faq.contactLabel": "Kontak bisnis",
    "loginCinematic.faq.qrAlt": "Kode QR WeChat bisnis",
    "loginCinematic.faq.items.difference.question": "Bedanya ProyekDrama dengan generator video AI biasa?",
    "loginCinematic.faq.items.difference.answer": "Alat biasa: satu prompt, satu klip. ProyekDrama: proyek utuh—teks, aset, episode, adegan, sampai komposit—bisa dilacak dan dikerjakan bersama.",
    "loginCinematic.faq.items.gettingStarted.question": "Mulai dari mana?",
    "loginCinematic.faq.items.gettingStarted.answer": "Impor teks di Sumber Cerita → cek karakter/adegan/properti/suara di Perpustakaan Aset → rencanakan episode di Studio Episode → ekspor di komposit. Target pertama: selesaikan satu episode, bukan sempurna.",
    "loginCinematic.faq.items.mirrorVsCanvas.question": "Kapan pakai Studio Episode vs Freezone?",
    "loginCinematic.faq.items.mirrorVsCanvas.answer": "Studio Episode untuk jalur utama: batch, stabil, per episode. Freezone untuk poles adegan sulit dan eksplorasi versi. Adegan biasa lewat Studio Episode; yang rumit ke Freezone.",
    "loginCinematic.faq.items.canvasOverwrite.question": "Hasil Freezone otomatis menimpa aset utama?",
    "loginCinematic.faq.items.canvasOverwrite.answer": "Tidak. Hasil Freezone adalah kandidat. Baru masuk jalur utama setelah Anda konfirmasi dan pilih slot (karakter, adegan, properti, sketsa, frame pertama, atau video).",
    "loginCinematic.faq.items.whyAssetsFirst.question": "Kenapa aset dulu sebelum video?",
    "loginCinematic.faq.items.whyAssetsFirst.answer": "Rework biasanya dari hulu: karakter goyah, adegan kabur, properti tanpa referensi, suara tidak konsisten. Rapikan di Perpustakaan Aset dulu—tahap bidikan jauh lebih tenang.",
    "loginCinematic.faq.items.contentTypes.question": "Konten apa yang cocok?",
    "loginCinematic.faq.items.contentTypes.answer": "Drama pendek, komik, promo novel, iklan, pelatihan, dan serial IP. Solo bisa jalan sendiri; tim bisa kolaborasi.",
    "loginCinematic.faq.items.teamRoles.question": "Cara bagi kerja di tim?",
    "loginCinematic.faq.items.teamRoles.answer": "Pemilik: proyek & biaya. Penulis: teks. Seni: karakter/adegan/properti. Sutradara: performa adegan. Operator: frame, video, komposit. Izin: penonton → editor → admin → pemilik.",
    "loginCinematic.faq.items.unstableResults.question": "Hasil tidak konsisten—cek apa dulu?",
    "loginCinematic.faq.items.unstableResults.answer": "Cari tahap yang gagal: teks, identitas karakter, referensi adegan/properti, sketsa, frame pertama, atau audio. Jangan ulangi video terus—perbaiki hulu dulu.",
    "loginCinematic.faq.items.dcUniverse.question": "Arti “Buat alam semesta DC Anda”?",
    "loginCinematic.faq.items.dcUniverse.answer": "DC = ProyekDrama, sekaligus dunia konten Anda. Dari satu cerita, bangun karakter, dunia, aset, lalu produksi berseri.",
    "loginCinematic.faq.items.afterLogin.question": "Setelah masuk ke mana?",
    "loginCinematic.faq.items.afterLogin.answer": "Ke pusat proyek. Buka yang ada atau buat baru. Tiap proyek menyimpan teks, aset, episode, video, dan hasil komposit.",
    # —— download ——
    "downloadPage.hero.subtitle": "Dari novel ke potongan akhir: episode, karakter, storyboard, frame pertama, video, komposit. Jalur utama langkah demi langkah; Freezone bebas di kanvas node—asetnya sama.",
    "downloadPage.preview.lede": "Jalur utama memecah novel menjadi episode → karakter → storyboard → frame → video → komposit. Freezone memproyeksikan bidikan ke kanvas node untuk diedit, lalu sync balik. Aset dipakai bersama.",
    "downloadPage.preview.windowTitle": "ProyekDrama — Episode 03 · Kanvas",
    "downloadPage.preview.caption": "Sketsa (tampilan Freezone)",
    "downloadPage.preview.alt": "Sketsa kanvas desktop: tab episode, outline adegan, kanvas node, panel parameter.",
    "downloadPage.faq.items.storage.answer": "Data proyek di cloud akun Anda. Perangkat yang login melihat episode yang sama. Ekspor bisa diunduh lokal.",
    "downloadPage.faq.items.offline.answer": "Ya untuk orkestrasi lokal. Render skrip, frame, dan video tetap di cloud.",
    # —— auth / assistant ——
    "aiAssistant.title": "Direktur Xia",
    "aiAssistant.upgrading": "Direktur Xia sedang ditingkatkan.",
    "aiAssistant.description": "Buka Direktur Xia di samping halaman ini.",
    "aiAssistant.toggle": "Buka/tutup Direktur Xia",
    "aiAssistant.close": "Tutup Direktur Xia",
    "aiAssistant.iframeTitle": "Direktur Xia",
    "aiAssistant.chatTitle": "Direktur Xia",
    "aiAssistant.syncingHistoryDescription": "Menyambung Direktur Xia dan memuat riwayat…",
    "aiAssistant.disclaimer": "Direktur Xia bisa salah. Cek cerita, karakter, dan aset penting.",
    "aiAssistant.placeholder": "Setelah unggah naskah, minta maju episode, visual, audio, atau video final",
    "aiAssistant.waitingResponse": "Menunggu Direktur Xia…",
    "aiAssistant.ingestAutomationNoProject": "Buka proyek dulu sebelum unggah novel lewat Direktur Xia.",
    "freezone.chat.title": "Direktur Xia",
    "freezone.chat.description": "Buka Direktur Xia di samping Freezone.",
    "freezone.chat.toggle": "Buka Direktur Xia",
    "freezone.chat.close": "Tutup Direktur Xia",
    "freezone.chat.resize": "Seret untuk ubah lebar",
    # —— login fourth ——
    "loginCinematic.fourth.sets.s1.titleTop": "Cerita Anda masuk",
    "loginCinematic.fourth.sets.s1.titleBottom": "produksi",
    "loginCinematic.fourth.sets.s1.lead": "Mulai dari satu baris. Karakter, konflik, latar, dan adegan jadi aset yang bisa dilanjutkan.",
    "loginCinematic.fourth.sets.s2.titleTop": "Satu dunia,",
    "loginCinematic.fourth.sets.s2.titleBottom": "satu arah",
    "loginCinematic.fourth.sets.s2.lead": "Karakter konsisten, bidikan tetap di jalur. Tiap generasi kembali ke narasi yang sama.",
    "loginCinematic.fourth.sets.s3.titleTop": "Ide yang didorong",
    "loginCinematic.fourth.sets.s3.titleBottom": "jadi gambar",
    "loginCinematic.fourth.sets.s3.lead": "Bukan satu gambar selesai—lanjut ke storyboard, klip, trailer, sampai karya yang bisa dipublikasikan.",
    "loginCinematic.fourth.cards.breakdown.title": "Uraian cerita",
    "loginCinematic.fourth.cards.breakdown.body": "Pecah ide jadi karakter, konflik, latar, dan adegan—jangan berhenti di satu kalimat.",
    "loginCinematic.fourth.cards.lock.title": "Kunci visual",
    "loginCinematic.fourth.cards.lock.body": "Jaga karakter, latar, dan bidikan dalam satu register agar hasil tidak acak.",
    "loginCinematic.fourth.cards.advance.title": "Maju ke gambar",
    "loginCinematic.fourth.cards.advance.body": "Dorong ide jadi klip, trailer, dan karya yang lebih utuh.",
    # —— download FAQ ——
    "downloadPage.faq.items.macGatekeeper.question": "macOS bilang pengembang tidak terverifikasi. Lanjut?",
    "downloadPage.faq.items.macGatekeeper.answer": "Finder → Aplikasi → klik kanan → Buka → konfirmasi. Cukup sekali.",
    "downloadPage.faq.items.winSmartScreen.question": "Windows SmartScreen memblokir. Lanjut?",
    "downloadPage.faq.items.winSmartScreen.answer": "Info selengkapnya → Jalankan tetap. Biasa untuk installer baru.",
    "downloadPage.faq.items.offline.question": "Perlu internet?",
    "downloadPage.faq.items.offline.answer": "Ya. Skrip, frame, dan video dijalankan di cloud; aplikasi mengorkestrasi dan mengelola media.",
    "downloadPage.faq.items.update.question": "Cara memperbarui?",
    "downloadPage.faq.items.update.answer": "Otomatis saat diluncurkan: unduh di latar, siap saat restart.",
    "downloadPage.faq.items.storage.question": "Proyek dan ekspor di mana?",
    "downloadPage.faq.items.storage.answer": "Proyek di cloud akun Anda. Perangkat yang login melihat episode yang sama. Ekspor bisa diunduh.",
    "downloadPage.faq.items.openSource.question": "Apakah open source?",
    "downloadPage.faq.items.openSource.answer": "Lisensi Elastic-2.0: boleh pakai, ubah, dan self-host; batasan komersial tertentu berlaku.",
    # —— settings long hints ——
    "settings.modelConfig.custom.setupPasswordOnlyOnce": "Username & password hanya dikirim saat membuat admin pertama NewAPI baru. Jika sudah diinisialisasi, input di sini tidak mengubah password lama. ProyekDrama tidak menyimpan password—simpan sendiri untuk konsol NewAPI.",
    "settings.modelConfig.featureModels.channelsSaveHint": "Hanya menyimpan preset saluran lokal CE. Pemetaan model berikutnya yang memperbarui saluran NewAPI.",
    "settings.mediaStorage.cloudinaryFieldsHint": "Disimpan di database CE lokal. Key/Secret lengkap tidak dikembalikan. Kosongkan = pakai yang tersimpan; isi baru = ganti.",
    "settings.modelConfig.embeddingModel.dimensionWarning": "Dimensi mengikat model saat proyek dibuat. Perubahan hanya untuk proyek baru. Bangun ulang graf pengetahuan jika perlu.",
    "settings.mediaStorage.notConfiguredImpact": "Penyimpanan media referensi belum diatur. Teks-saja biasanya aman; unggah referensi gambar (XiaHua, karakter, identitas, I2I, frame video) akan gagal. Atur OSS atau Cloudinary.",
    # —— ingest ——
    "ingest.novelFormat.intro": "Naskah drama butuh batas episode dan adegan yang jelas. ProyekDrama memotong per header adegan sebelum visual, dialog, dan audio.",
    "ingest.novelFormat.repairableHint": "Kedua adegan di bawah bisa dipahami, tapi kurang lengkap: satu tanpa waktu/INT-EXT, satu INT/EXT tidak terbaca.",
}

# Phrase replacements applied to ALL string leaves (order matters)
PHRASES: list[tuple[str, str]] = [
    ("Shrimp Feed", "Sumber Cerita"),
    ("Shrimp Pond", "Perpustakaan Aset"),
    ("Shrimp Lens", "Studio Episode"),
    ("Shrimp Canvas", "Freezone"),
    ("Xia Director", "Direktur Xia"),
    ("Direktur Zona Bebas Collapse Xia", "Tutup Direktur Xia"),
    ("Buka Direktur Freezone Xia", "Buka Direktur Xia"),
    ("Freezone Xia Director", "Direktur Xia"),
    ("Silakan coba lagi", "Coba lagi"),
    ("silakan coba lagi", "coba lagi"),
    ("Harap tunggu.", "Tunggu sebentar."),
    ("Harap tunggu", "Tunggu sebentar"),
    ("Anda dapat ", "Bisa "),
    ("Anda bisa ", "Bisa "),
    ("Anda harus ", "Perlu "),
    ("secara otomatis", "otomatis"),
    ("secara eksplisit", "eksplisit"),
    ("berikut ini", "ini"),
    ("dalam rangka ", "untuk "),
    ("oleh karena itu, ", "Jadi "),
    ("oleh karena itu ", "jadi "),
    ("dengan demikian, ", "Jadi "),
    ("dengan demikian ", "jadi "),
    ("pada saat ini", "sekarang"),
]

# Soft cleanup after phrase pass
def tidy(s: str) -> str:
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r" +([,.!?;:])", r"\1", s)
    s = re.sub(r"\s+—\s+", " — ", s)
    s = re.sub(r"\s+-\s+", " — ", s)
    # collapse double spaces again
    s = re.sub(r" {2,}", " ", s)
    return s.strip()


def set_path(obj, path: str, value: str) -> None:
    parts = re.split(r"\.(?![^\[]*\])", path)
    cur = obj
    for i, part in enumerate(parts):
        m = re.fullmatch(r"([^\[\]]+)(?:\[(\d+)\])?", part)
        if not m:
            raise KeyError(path)
        key, idx = m.group(1), m.group(2)
        if i == len(parts) - 1 and idx is None:
            cur[key] = value
            return
        cur = cur[key]
        if idx is not None:
            idx_i = int(idx)
            if i == len(parts) - 1:
                cur[idx_i] = value
                return
            cur = cur[idx_i]


def walk_mutate(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                orig = v
                for a, b in PHRASES:
                    if a in v:
                        v = v.replace(a, b)
                v = tidy(v)
                # trim overly long generic fluff sentences: "yang benar-benar" etc.
                v = v.replace("yang benar-benar ", "")
                v = v.replace("yang sangat ", "")
                v = tidy(v)
                if v != orig:
                    obj[k] = v
            else:
                walk_mutate(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                orig = v
                for a, b in PHRASES:
                    if a in v:
                        v = v.replace(a, b)
                v = tidy(v)
                if v != orig:
                    obj[i] = v
            else:
                walk_mutate(v)


def main() -> None:
    data = json.loads(ROOT.read_text(encoding="utf-8"))
    before = json.dumps(data, ensure_ascii=False)

    for path, value in EXACT.items():
        try:
            set_path(data, path, value)
        except Exception as exc:
            print(f"MISS {path}: {exc}")

    walk_mutate(data)

    # Fix remaining English leftovers in high-traffic chrome
    nav = data.get("nav", {})
    nav_updates = {
        "creation": "Kreasi",
        "production": "Produksi",
        "tools": "Alat",
        "characters": "Karakter",
        "script": "Naskah",
        "sketches": "Sketsa",
        "compose": "Komposit",
        "freezone": "Freezone",
        "xiaji": "Serial",
    }
    for k, v in nav_updates.items():
        if k in nav:
            nav[k] = v

    chars = data.get("characters", {})
    if isinstance(chars.get("title"), str):
        chars["title"] = "Karakter"
    if isinstance(chars.get("subtitle"), str):
        chars["subtitle"] = "Kelola pemeran proyek ini."
    tabs = chars.get("assetTabs") or {}
    for k, v in {
        "characters": "Karakter",
        "voices": "Suara",
        "scenes": "Adegan",
        "props": "Properti",
    }.items():
        if k in tabs:
            tabs[k] = v

    after = json.dumps(data, ensure_ascii=False)
    ROOT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # validate
    json.loads(ROOT.read_text(encoding="utf-8"))
    print("bytes", len(before), "->", len(after), "delta", len(after) - len(before))
    print("DramaClaw left", after.count("DramaClaw"))
    print("Shrimp left", after.count("Shrimp "))
    print("ProyekDrama", after.count("ProyekDrama"))


if __name__ == "__main__":
    main()
