# -*- coding: utf-8 -*-
"""Pass 2: more concise natural Indonesian copy."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("frontend/public/locales/id/translation.json")

EXACT = {
    "loginCinematic.second.title": "Dari ide ke proyek",
    "loginCinematic.second.subtitle": "Di ProyekDrama, kreasi tidak berhenti di satu prompt dan satu hasil.",
    "loginCinematic.third.title": "Mulai dari cerita",
    "loginCinematic.third.subtitle": "Impor novel, naskah, atau teks per episode—sistem mengurai dasar untuk aset, episode, dan adegan.",
    "loginCinematic.fifth.heading": "Ubah ide jadi aset",
    "loginCinematic.fifth.lead1": "ProyekDrama menaruhnya di perpustakaan aset proyek,",
    "loginCinematic.fifth.lead2": "supaya bidikan berikutnya bisa merujuk, menyimpan, dan mengembalikan versi lama.",
    "loginCinematic.sixth.heading": "Episode demi episode, sampai potongan akhir",
    "loginCinematic.sixth.lead": "Kanvas bebas untuk multi-referensi dan multi-versi; setelah dikonfirmasi, hasil kembali ke jalur utama.",
    "loginCinematic.seventh.heading": "Dari undian ke jalur kerja",
    "loginCinematic.seventh.lead": "ProyekDrama memecah ketidakpastian video AI menjadi teks, aset, bidikan, dan tugas.",
    "loginCinematic.seventh.steps.01.title": "Premis masuk",
    "loginCinematic.seventh.steps.01.body": "Satu kalimat jadi karakter, latar, dan batas narasi.",
    "loginCinematic.seventh.steps.02.title": "Kunci karakter",
    "loginCinematic.seventh.steps.02.body": "Identitas, motif, dan hubungan dikunci dulu—generasi tidak mengembara.",
    "loginCinematic.seventh.steps.03.title": "Konflik",
    "loginCinematic.seventh.steps.03.body": "Dorong peristiwa sampai ada pilihan yang harus diambil.",
    "loginCinematic.seventh.steps.04.title": "Rencana bidikan",
    "loginCinematic.seventh.steps.04.body": "Sudut, ritme, dan framing dalam satu jalur yang terkendali.",
    "loginCinematic.seventh.steps.05.title": "Klip terbentuk",
    "loginCinematic.seventh.steps.05.body": "Ide berlanjut jadi adegan, trailer, dan klip bersambung.",
    "loginCinematic.seventh.steps.06.title": "Karya tumbuh",
    "loginCinematic.seventh.steps.06.body": "Tiap hasil bisa kembali ke proses dan membuka cabang baru.",
    "loginCinematic.eighth.heading": "Untuk produksi utuh",
    "loginCinematic.eighth.lead": "Teks masuk, karakter konsisten, adegan dipakai ulang, bidikan maju, tim mengirim.",
    "loginCinematic.eighth.statementTitle": "Protokol perjalanan malam · Urutan 08",
    "loginCinematic.eighth.statementBody": "Kapal kargo tak terdaftar menarik rahasia kota ke dalam malam.",
    "loginCinematic.eighth.decisions.KEEP.title": "Simpan",
    "loginCinematic.eighth.decisions.KEEP.body": "Kunci karakter, bidikan, atau klip ini sebagai dasar langkah berikutnya.",
    "loginCinematic.eighth.decisions.REWRITE.title": "Tulis ulang",
    "loginCinematic.eighth.decisions.REWRITE.body": "Ganti konflik, dialog, atau arah bidikan tanpa merusak dunia yang sudah jalan.",
    "loginCinematic.eighth.decisions.EXTEND.title": "Perpanjang",
    "loginCinematic.eighth.decisions.EXTEND.body": "Lanjut dari klip ini ke adegan berikutnya, trailer, atau cabang penuh.",
    "loginCinematic.eighth.decisions.REJECT.title": "Tolak",
    "loginCinematic.eighth.decisions.REJECT.body": "Mundur satu simpul, ambil jalur lain, kembalikan cerita ke arah yang tepat.",
    "loginCinematic.ninth.headingTop": "Satu garis, lurus ke",
    "loginCinematic.ninth.headingAccent": "bidikan",
    "loginCinematic.ninth.lead": "Naskah lengkap tidak wajib. Beri arah—ProyekDrama pecah jadi karakter, konflik, latar, dan rantai adegan.",
    "loginCinematic.ninth.steps.01.title": "Satu premis",
    "loginCinematic.ninth.steps.01.body": "Kota gelap menyala lagi; setiap penyintas mendengar hitungan yang sama.",
    "loginCinematic.ninth.steps.02.title": "Ke struktur",
    "loginCinematic.ninth.steps.02.body": "Tokoh, konflik, latar, dan batas narasi jadi node yang bisa didorong.",
    "loginCinematic.ninth.steps.03.title": "Ke bidikan",
    "loginCinematic.ninth.steps.03.body": "Urutan, catatan adegan, dan tempo terkunci—klip punya arah.",
    "loginCinematic.ninth.steps.04.title": "Potong",
    "loginCinematic.ninth.steps.04.body": "Cuplikan yang bisa diperpanjang, dipotong ulang, atau dikirim ke meja kerja.",
    "loginCinematic.twelfth.heading": "Dorong satu garis jadi alam semesta yang bisa ditonton",
    "loginCinematic.twelfth.lead": "Beri konflik karakter atau dunia—ProyekDrama pecah jadi node adegan dan terus tumbuh.",
    "loginCinematic.twelfth.primaryCta": "Mulai buat",
    "loginCinematic.twelfth.secondaryCta": "Minta akun",
    "loginCinematic.watchCommunity": "Tonton komunitas",
    "loginCinematic.watchNow": "Tonton sekarang",
    "loginCinematic.backToTop": "Ke atas",
    "auth.stage.eyebrow": "Platform kreasi drama",
    "auth.stage.headline": "Buat alam semesta DC Anda",
    "auth.stage.headlines.createUniverse": "Buka alam semesta kreatif Anda",
    "auth.stage.headlines.dramaUniverse": "Buka alam semesta drama Anda",
    "auth.stage.headlines.storyWorld": "Bangun dunia cerita Anda",
    "auth.stage.headlinePrefix": "Buat",
    "auth.stage.headlineSuffix": "Universe",
    "auth.stage.subtitlePrefix": "Buat",
    "auth.stage.start": "Saat inspirasi datang",
    "auth.stage.sub": "Setiap gelombang ide bertemu kekuatan kreasi AI yang ringan",
    "auth.stage.changelog": "Catatan rilis",
    "downloadPage.preview.lede": "Jalur utama: episode → karakter → storyboard → frame → video → komposit. Freezone edit di kanvas node, lalu sync. Aset dipakai bersama.",
    "downloadPage.hero.subtitle": "Dari novel ke potongan akhir lewat jalur utama. Freezone bebas di kanvas—asetnya sama.",
    "episode.workbench.aspectSwitch.desc": "Ganti rasio aspek tidak meregangkan sketsa, referensi, atau video lama—mereka tetap di rasio aslinya.",
    "errorDialog.stillRunningMessage": "Lebih lama dari biasanya. Halaman berhenti menunggu, tapi pekerjaan masih jalan di latar—segarkan nanti.",
    "common.generationChannelPolicyBlocked": "Diblokir kebijakan saluran model (bukan rate limit). Regenerasi sketsa berkualitas rendah ditolak.",
    "node.videoNode.generation.faceBlockedMessage": "Aset berisi wajah manusia nyata dan diblokir. Nyalakan “Tinjauan aset orang nyata” di bawah, lalu coba lagi.",
    "settings.modelConfig.featureModels.removeChannelConfirm": "Hapus “{{provider}}”? Pemetaan fitur {{featureCount}}, media {{mediaCount}}, dan embedding terkait ikut hilang.",
    "settings.modelConfig.custom.setupAlreadyInitializedPasswordIgnored": "NewAPI sudah diinisialisasi. Ini tidak memanggil setup ulang dan tidak mengubah password admin.",
    "settings.mediaStorage.fieldsHint": "Disimpan di database CE lokal. AccessKey lengkap tidak dikembalikan. Kosong = pakai tersimpan; isi baru = ganti.",
    "settings.mediaStorage.providerHint": "Untuk penyedia ini, sebaiknya jangan aktifkan “Unggah aset sepenuhnya dikelola”—paket gratis punya kuota bandwidth.",
    "settings.providerGuideText": "Penyedia beda di kemampuan, antrean, stabilitas, dan harga. Pilih sesuai tugas.",
    "ingest.reuploadConfirm.description": "Impor ulang membangun ulang graf dan bisa memengaruhi karakter, episode, skrip, serta video di hilir. Lanjut?",
    "ingest.novelFormat.ruleDialogue": "Dialog: “JI-WON: Ada orang di sini?” — nama kapital di baris sendiri tanpa titik dua tidak dihitung pembicara.",
    "ingest.novelFormat.ruleTimeTokens": "Slot waktu hanya: HARI, MALAM, PAGI, SIANG, SORE, SUBUH, SENJA. Selain itu ditolak.",
    "ingest.novelFormat.ruleClockTime": "Jangan taruh jam di nama lokasi. Pakai baris terpisah “Waktu: 11:47 PM” di bawah judul.",
    "ingest.novelFormat.ruleScene": "Tiap adegan: INT./EXT. + lokasi + “ — ” + waktu, mis. “INT. STASIUN METRO SEOUL — MALAM”.",
    "ingest.formatCheck.issue.missingSceneHeaders.fix": "Format: “EPISODE N”, lalu “INT./EXT. lokasi — WAKTU”, daftar karakter, baru badan adegan.",
    "ingest.sceneHeaders.repairable": "Batas adegan terbaca, tapi beberapa judul kurang waktu/lokasi/INT-EXT. Impor tetap boleh; metadata dilengkapi nanti.",
    "freezone.commit.batch.hint": "Tiap gambar kembali ke slot asalnya. Impor jalur utama ditulis ulang ke slot asli; unggahan/buatan baru butuh pilih slot.",
    "freezone.canvases.restoreConfirm": "Sync tampilan utama membangun ulang lapisan preset dari fakta proyek. Node non-preset di lapisan ini hilang.",
    "characters.voices.firstPersonNarratedMissingMain": "Proyek narasi orang pertama butuh karakter utama sebagai narator dulu, baru unggah suaranya.",
    "canvas.capabilities.video_start_frame_candidate.description": "Buat kandidat frame awal video dari render/ekstrak/referensi, lalu commit ke slot frame.",
}


def set_path(obj, path: str, value: str) -> None:
    parts = path.split(".")
    cur = obj
    for i, key in enumerate(parts):
        if i == len(parts) - 1:
            cur[key] = value
            return
        cur = cur[key]


def main() -> None:
    data = json.loads(ROOT.read_text(encoding="utf-8"))
    miss = 0
    for path, value in EXACT.items():
        try:
            set_path(data, path, value)
        except Exception as exc:
            miss += 1
            print("MISS", path, exc)
    ROOT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(ROOT.read_text(encoding="utf-8"))
    print("updated", len(EXACT) - miss, "miss", miss)


if __name__ == "__main__":
    main()
