#!/usr/bin/env python3
"""Polish Indonesian locale chrome to natural, concise Indonesian."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "frontend" / "public" / "locales" / "id" / "translation.json"

VALUE_MAP = {
    "Import": "Impor",
    "Replace": "Ganti",
    "Library": "Perpustakaan",
    "Completed": "Selesai",
    "Done": "Selesai",
    "Cancel": "Batal",
    "Delete": "Hapus",
    "Select": "Pilih",
    "Selected": "Dipilih",
    "Start": "Mulai",
    "Type": "Jenis",
    "Scope": "Cakupan",
    "Progress": "Progres",
    "Connected": "Terhubung",
    "Failed": "Gagal",
    "Complete": "Selesai",
    "Generating": "Menghasilkan",
    "Generating...": "Menghasilkan…",
    "Idle": "Siaga",
    "Logs": "Log",
    "Result": "Hasil",
    "Error": "Kesalahan",
    "Project": "Proyek",
    "Voice": "Suara",
    "References": "Referensi",
    "Sent": "Terkirim",
    "Unused": "Tidak dipakai",
    "Configured": "Siap",
    "Missing": "Kurang",
    "Width": "Lebar",
    "Height": "Tinggi",
    "Crop": "Potong",
    "Script": "Naskah",
    "Shots": "Shot",
    "Compose": "Susun",
    "Sketch": "Sketsa",
    "Aspect": "Aspek",
    "Background": "Latar",
    "Overview": "Ringkasan",
    "Companion": "Teman",
    "Auto": "Otomatis",
    "Accessory": "Aksesori",
    "Energy": "Energi",
    "Pending": "Menunggu",
    "Running": "Berjalan",
    "Imported": "Diimpor",
    "Importing": "Mengimpor",
    "Save": "Simpan",
    "Close": "Tutup",
    "Open": "Buka",
    "Search": "Cari",
    "Loading…": "Memuat…",
    "Loading...": "Memuat…",
    "All": "Semua",
    "Confirm": "Konfirmasi",
    "Back": "Kembali",
    "Next": "Lanjut",
    "Skip": "Lewati",
    "Update": "Perbarui",
    "Refresh": "Segarkan",
    "Copy": "Salin",
    "Download": "Unduh",
    "Upload": "Unggah",
    "Settings": "Pengaturan",
    "Help": "Bantuan",
    "Status": "Status",
    "Name": "Nama",
    "Description": "Deskripsi",
    "Title": "Judul",
    "Actions": "Aksi",
    "Details": "Detail",
    "Dismiss": "Tutup",
}

PATH_MAP = {
    "common.cancel": "Batal",
    "common.delete": "Hapus",
    "common.save": "Simpan",
    "common.refreshDone": "Selesai",
    "aiAssistant.actions.delete": "Hapus",
    "aiAssistant.connected": "Terhubung",
    "aiAssistant.taskCompleteNotice": (
        "✅ {{label}} selesai. Minta saya menampilkan hasilnya, "
        "atau lanjut ke langkah berikutnya."
    ),
    "aiAssistant.taskFailedNotice": (
        "{{label}} gagal: {{reason}}\n"
        "Perbaiki penyebab error sebelum melanjutkan."
    ),
    "myBuddy.companion.entry": "Teman",
    "myBuddy.companion.title": "Pilih teman",
    "myBuddy.companion.importCta": "Impor teman",
    "myBuddy.import.button": "Impor",
    "myBuddy.import.replace": "Ganti",
    "myBuddy.import.confirm": "Impor",
    "myBuddy.import.title": "Impor hewan peliharaan petdex",
    "myBuddy.gallery.tabLibrary": "Perpustakaan",
    "myBuddy.gallery.tabMine": "Milik saya",
    "myBuddy.gallery.select": "Pilih",
    "myBuddy.gallery.selected": "Dipilih",
    "myBuddy.gallery.title": "Pilih teman",
    "myBuddy.gallery.emptyMine": "Belum ada hewan peliharaan — klik Impor untuk menambah",
    "myBuddy.taskRunning": "Berjalan · {{name}}",
    "myBuddy.taskSuccess": "Selesai · {{name}}",
    "myBuddy.taskFailure": "Gagal · {{name}}",
    "myBuddy.debug.states.running": "Gelembung berjalan",
    "myBuddy.debug.states.success": "Gelembung sukses",
    "myBuddy.debug.states.failure": "Gelembung gagal",
    "myBuddy.debug.states.idle": "Gelembung siaga",
    "characters.summary.title": "Ringkasan",
    "characters.tabs.voice": "Suara",
    "characters.stats.strip.voice": "Suara",
    "characters.identities.delete": "Hapus",
    "episode.nav.script": "Naskah",
    "episode.nav.shots": "Shot",
    "episode.nav.compose": "Susun",
    "episode.nav.sketch": "Sketsa",
    "episode.drawer.script": "Naskah",
    "episode.drawer.sketch": "Sketsa",
    "episode.stage.script": "Naskah",
    "episode.stage.compose": "Susun",
    "episode.state.failed": "Gagal",
    "episode.state.generating": "Menghasilkan",
    "episode.state.missing": "Menunggu",
    "episode.list.stats.completedEpisodes": "Selesai",
    "episode.beat.select": "Pilih",
    "episode.beat.selected": "Dipilih",
    "episode.beat.sectionSketch": "Sketsa",
    "episode.beat.sectionRender": "Render",
    "episode.beat.deleteManualShot": "Hapus",
    "episode.beat.badge": "Beat {{n}}",
    "episode.compose.composeCancel": "Batal",
    "episode.sketchSettings.aspectRatio": "Rasio aspek",
    "episode.workbench.cancel": "Batal",
    "episode.workbench.batch.sketch": "Sketsa",
    "episode.workbench.batch.render": "Render",
    "episode.workbench.sketch.chooseBackground": "Latar",
    "episode.workbench.sketch.generating": "Menghasilkan",
    "episode.workbench.sketch.cropWidth": "Lebar",
    "episode.workbench.sketch.cropHeight": "Tinggi",
    "episode.workbench.sketch.poseWidth": "Lebar",
    "episode.workbench.audio.generating": "Menghasilkan…",
    "episode.workbench.video.generating": "Menghasilkan…",
    "episode.workbench.video.preview.sketch": "Sketsa",
    "episode.workbench.video.preview.render": "Render",
    "episode.workbench.video.renderReady": "Render siap",
    "episode.workbench.video.seedance2Ready": "Siap",
    "episode.workbench.video.seedance2Missing": "Belum lengkap",
    "episode.workbench.video.seedance2References": "Referensi",
    "episode.workbench.video.seedance2Voice": "Suara",
    "episode.workbench.video.seedance2ReferenceSent": "Terkirim",
    "episode.workbench.video.seedance2ReferenceUnused": "Tidak dipakai",
    "episode.workbench.video.seedance2AssetDelete": "Hapus",
    "episode.workbench.video.seedance2AssetCrop": "Potong",
    "episode.workbench.video.seedance2CropWidth": "Lebar",
    "episode.workbench.video.seedance2CropHeight": "Tinggi",
    "episode.workbench.video.narratorVoiceDelete": "Hapus",
    "episode.workbench.video.narratorVoiceRecordStart": "Mulai",
    "episode.workbench.video.activeBeat": "Beat {{n}}",
    "episode.workbench.verify.failed": "Gagal",
    "episode.workbench.verify.running": "Berjalan",
    "episode.workbench.insertManual.type": "Jenis",
    "episode.workbench.text.type": "Jenis",
    "freezone.assetPanel.cancel": "Batal",
    "freezone.assetPanel.replace": "Ganti",
    "freezone.assetPanel.roles.current_sketch": "Sketsa",
    "freezone.assetPanel.roles.selected_background": "Latar",
    "freezone.canvases.delete": "Hapus",
    "freezone.commit.batch.done": "Selesai",
    "freezone.commit.batch.status.pending": "Menunggu",
    "freezone.commit.kinds.sketch": "Sketsa",
    "freezone.commit.nodeLabels.sketch": "Sketsa",
    "freezone.commit.shortKinds.sketch": "Sketsa",
    "freezone.canvasOutline.types.script": "Naskah",
    "freezone.nodeContext.kind.sketch": "Sketsa",
    "freezone.nodeContext.kind.voice": "Suara",
    "ingest.selectPlaceholder": "Pilih",
    "ingest.status.completed": "Diimpor",
    "ingest.status.importing": "Mengimpor",
    "pipelineImport.replace": "Ganti",
    "pipelineImport.completed": "Selesai",
    "pipelineImport.submit": "Impor",
    "assets.common.delete": "Hapus",
    "notifications.title": "Pusat pengumuman",
    "header.notifications": "Pengumuman",
    "tasks.cancelRunning.keepRunning": "Biarkan berjalan",
    "tasks.types.sketch_regen": "Regenerasi sketsa",
    "tasks.types.selected_regen": "Regenerasi pilihan",
    "tasks.types.grid_regenerate": "Regenerasi kisi",
    "tasks.chatLabel.beatRange": "Beat {{ranges}}",
    "taskCenter.panel.close": "Tutup",
    "taskCenter.detail.tabs.overview": "Ringkasan",
    "taskCenter.detail.tabs.logs": "Log",
    "taskCenter.detail.result.label": "Hasil",
    "taskCenter.detail.error.label": "Kesalahan",
    "taskCenter.detail.meta.type": "Jenis",
    "taskCenter.detail.meta.project": "Proyek",
    "taskCenter.detail.meta.scope": "Cakupan",
    "taskCenter.detail.meta.progress": "Progres",
    "taskCenter.statusBar.idle": "Siaga",
    "taskCenter.statusBar.connected": "Terhubung",
    "taskCenter.statusBar.generationRunning": "Sedang menghasilkan",
    "taskCenter.statusBar.generationComplete": "Selesai",
    "taskCenter.toast.completed": "{{label}} selesai",
    "taskCenter.toast.failed": "{{label}} gagal: {{error}}",
    "taskCenter.toast.canceled": "{{label}} dibatalkan",
    "pikoMiniGame.start": "Mulai",
    "pikoMiniGame.energy": "Energi",
    "app.updateAvailable.dismiss": "Tutup",
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


def walk_replace(obj: object) -> int:
    changed = 0
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and value in VALUE_MAP and VALUE_MAP[value] != value:
                obj[key] = VALUE_MAP[value]
                changed += 1
            else:
                changed += walk_replace(value)
    elif isinstance(obj, list):
        for item in obj:
            changed += walk_replace(item)
    return changed


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    path_hits = sum(1 for key, value in PATH_MAP.items() if set_path(data, key, value))
    value_hits = walk_replace(data)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(PATH.read_text(encoding="utf-8"))
    print(f"path overrides: {path_hits}")
    print(f"value walk replacements: {value_hits}")
    print("json ok")


if __name__ == "__main__":
    main()
