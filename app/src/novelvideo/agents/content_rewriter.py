# ruff: noqa: E501 - the long prompt is intentionally kept readable for prompt editing.

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator
from pydantic_ai import Agent

from novelvideo.config import (
    get_newapi_structured_output_model_settings,
    get_newapi_text_pydantic_model,
)
from novelvideo.model_gateway_runtime import model_gateway_output_retries


class AdaptedContentOutput(BaseModel):
    """Baris narasi hasil tulis ulang untuk workflow literal."""

    lines: list[str] = Field(
        default_factory=list,
        description="Baris narasi; tiap baris jadi satu beat di workflow literal",
    )

    @model_validator(mode="after")
    def normalize_lines(self) -> "AdaptedContentOutput":
        normalized: list[str] = []
        for line in self.lines:
            text = str(line or "").strip()
            if text:
                normalized.append(text)
        if not normalized:
            raise ValueError("lines tidak boleh kosong")
        self.lines = normalized
        return self


REWRITE_PROMPT = """Kamu penulis adaptasi novel ke narasi video pendek.

Tugas: tulis ulang teks sumber menjadi baris-baris narasi. Setiap baris = satu beat video di workflow hilir.
Teks akan dibaca TTS bersama gambar, jadi **irama & daya dengar adalah prioritas**.

## Bahasa (wajib)
- Default: Bahasa Indonesia natural, singkat, tanpa basa-basi.
- Pertahankan nama tokoh/tempat persis; jangan diterjemahkan.
- Dialog: format `Nama + cara bicara + : + “kalimat”` (kutip lengkung).

## Tujuan inti
- Ceritakan jalur utama episode agar orang yang tidak baca novel tetap paham
- Pertahankan ritme, emosi, dan kait narasi
- Bukan ringkasan kasar, bukan hanya cuplikan klimaks

## Disiplin panjang baris (target)
- Ideal ~14–20 kata per baris agar TTS stabil
- Prioritaskan ekspresi utuh & dialog kunci
- Hindari baris 2–4 kata yang memecah ritme
- Pecah baris panjang kecuali memecah merusak dialog inti
- Info terlalu pendek: gabung dengan baris sebelum/sesudah

## Irama
- Setiap baris harus enak dibaca keras
- Selang-seling panjang/pendek; dialog dan narasi bergantian
- Hindari tiga baris beruntun dengan pola kalimat sama

## Gaya
- Nada narator novel, bukan berita atau template
- Pertahankan kepadatan emosi sumber
- Jangan menambah aksi/lingkungan kosong yang tidak ada di sumber
- Lebih tajam & maju cerita, bukan lebih “indah”

## Aturan dialog
Format: `NamaTokoh + cara bicara + : + “kalimat asli”`
- Isi kutipan setia ke sumber; normalisasi kutip ke “”
- Dialog eksplisit di sumber harus tetap format dialog lengkap (ada pembicara)
- Jangan keluarkan kutipan tanpa nama pembicara
- Cara bicara singkat & bergambar (tersenyum dingin, membentak, berbisik…)

## Satu baris = satu gambar
Setiap baris harus termasuk salah satu:
1. Aksi baru yang terlihat
2. Informasi baru bagi pendengar
3. Pergeseran konflik/pertahanan
Larang: mengulang penilaian/emosi yang sama dengan kata berbeda.

## Jumlah baris
- Dekati target_beats; kalau kurang, tambah node aksi/konflik; kalau lebih, padatkan pengulangan
- Jaga konsistensi orang pertama/ketiga
- Awal: tegakkan siapa/apa/konflik; akhir: counter/perubahan situasi/kait baru
- Hanya keluarkan baris teks berurutan — tanpa nomor, tanpa penjelasan
"""


async def rewrite_episode_content(
    raw_content: str,
    *,
    episode_title: str = "",
    protagonist_name: str = "",
    target_beats: int = 18,
    beat_chars_range: tuple[int, int] = (14, 20),
    narration_style: str = "first_person",
) -> str:
    """Tulis ulang teks sumber menjadi baris untuk workflow literal."""
    source_text = (raw_content or "").strip()
    if not source_text:
        return ""

    min_chars, max_chars = beat_chars_range
    task = f"""## Info episode
- Judul: {episode_title or "Tanpa judul"}
- Tokoh narasi (aku / I): {protagonist_name or "Belum terikat"}
- Gaya: {narration_style}
- Target baris: {target_beats}
- Panjang baris: {min_chars}-{max_chars} kata
- Tujuan: narasi jalur utama untuk video pendek — natural, singkat, tanpa basa-basi

## Teks sumber
{source_text}

Keluarkan baris hasil tulis ulang saja."""

    agent = Agent(
        get_newapi_text_pydantic_model(
            "CONTENT_REWRITER_MODEL",
            "gpt-5.4-mini",
            capability="text.generate",
        ),
        system_prompt=REWRITE_PROMPT,
        output_type=AdaptedContentOutput,
        output_retries=model_gateway_output_retries(3),
        model_settings=get_newapi_structured_output_model_settings(),
        name="Content Rewriter",
    )
    result = await agent.run(task)
    output: AdaptedContentOutput = result.output
    return "\n".join(output.lines)
