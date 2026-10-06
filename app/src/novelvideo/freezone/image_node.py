"""Freezone image-node helpers."""

from __future__ import annotations

from pathlib import Path

from novelvideo.freezone.vision_gateway import (
    FREEZONE_IMAGE_REVERSE_PROMPT_TIMEOUT_SECONDS,
    VisionInput,
    call_freezone_vision_model,
    image_media_type,
)
from novelvideo.egress_context import TrustedEgressContext
from novelvideo.official_defaults import DEFAULT_FREEZONE_VISION_MODEL

DEFAULT_IMAGE_REVERSE_PROMPT_INSTRUCTION = (
    "Dari gambar, buat prompt terstruktur berbahasa Indonesia: subjek, lingkungan, "
    "cahaya, bahasa kamera, kata kunci gaya."
)


def build_image_reverse_prompt_task(instruction: str = "") -> str:
    lines = [
        "Kamu asisten reverse-prompt untuk node gambar.",
        "Aku beri satu gambar. Balikkan menjadi prompt Indonesia yang langsung "
        "bisa dipakai untuk text-to-image atau image-to-image.",
        "Aturan:",
        "- Keluarkan hanya prompt akhir. Tanpa penjelasan, markdown, atau tanda kutip.",
        "- Prompt harus memuat: subjek, adegan, komposisi/ukuran bidikan, cahaya, "
        "warna, material/detail, suasana, gaya.",
        "- Tulis seperti kreator menulis prompt — natural, singkat, padat. Bukan laporan analisis.",
        "- Jangan mengarang subjek atau aksi yang tidak ada di gambar.",
        "- Bahasa default: Bahasa Indonesia natural, singkat, tanpa basa-basi.",
    ]
    clean_instruction = str(instruction or "").strip()
    if clean_instruction:
        lines.extend(["Permintaan tambahan pengguna:", clean_instruction])
    return "\n".join(lines)


async def reverse_prompt_from_image(
    *,
    image_path: Path,
    instruction: str = "",
    egress_context: TrustedEgressContext | None = None,
) -> str:
    prompt = build_image_reverse_prompt_task(instruction)
    image_bytes = image_path.read_bytes()
    from novelvideo.freezone.presets import (
        complete_freezone_vision_egress,
        prepare_freezone_vision_egress,
    )

    vision_egress = await prepare_freezone_vision_egress(
        egress_context=egress_context,
        model_name=DEFAULT_FREEZONE_VISION_MODEL,
        prompt=prompt,
        images=[image_bytes],
        timeout_seconds=FREEZONE_IMAGE_REVERSE_PROMPT_TIMEOUT_SECONDS,
    )
    _model, prompt_text = await call_freezone_vision_model(
        prompt=prompt,
        images=[
            VisionInput(
                data=image_bytes,
                media_type=image_media_type(image_path.name),
            )
        ],
        timeout_seconds=FREEZONE_IMAGE_REVERSE_PROMPT_TIMEOUT_SECONDS,
        transport_context=vision_egress.transport_context if vision_egress else None,
    )
    prompt_text = prompt_text.strip()
    if prompt_text.startswith("```"):
        prompt_text = "\n".join(
            line for line in prompt_text.splitlines() if not line.strip().startswith("```")
        ).strip()
    if not prompt_text:
        raise RuntimeError("reverse prompt model returned empty prompt")
    await complete_freezone_vision_egress(vision_egress, result=prompt_text)
    return prompt_text
