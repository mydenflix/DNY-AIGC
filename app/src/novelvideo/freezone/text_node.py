"""Freezone 文本工具辅助逻辑。

当前包含：
- 中英文提示词互译
- 自由文本生成
- 故事脚本生成
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from novelvideo.egress_context import TrustedEgressContext
from novelvideo.model_gateway_runtime import (
    current_model_gateway_context,
    model_gateway_output_retries,
)

from novelvideo.official_defaults import (
    DEFAULT_FREEZONE_STORY_SCRIPT_MODEL,
    DEFAULT_FREEZONE_TEXT_WRITER_MODEL,
    DEFAULT_FREEZONE_TRANSLATION_MODEL,
)

FREEZONE_TRANSLATION_PROVIDER = "newapi"
FREEZONE_TRANSLATION_MODEL = DEFAULT_FREEZONE_TRANSLATION_MODEL
FREEZONE_TEXT_WRITER_MODEL = DEFAULT_FREEZONE_TEXT_WRITER_MODEL
FREEZONE_STORY_SCRIPT_MODEL = {
    "id": DEFAULT_FREEZONE_STORY_SCRIPT_MODEL,
    "provider": "newapi",
    "model": DEFAULT_FREEZONE_STORY_SCRIPT_MODEL,
    "label": "DramaClawAPI Story Script",
}
LEGACY_FREEZONE_STORY_SCRIPT_MODEL_IDS = {
    "newapi_gemini_flash",
    "openrouter_gemini_flash",
    "OpenRouter Gemini 2.5 Flash",
}

FREEZONE_TRANSLATION_SYSTEM_PROMPT = """# Freezone Prompt Translator

You translate prompting text between Simplified Chinese and English for creative nodes.

## Goal
- First determine the dominant natural language of the source text.
- If the dominant natural language is English, translate natural-language content into Simplified Chinese.
- If the dominant natural language is Simplified Chinese, translate natural-language content into English.
- Translate accurately while preserving prompting intent.
- Keep the output concise, directly usable as a prompt.
- Preserve cinematic, visual, audio, and motion terminology naturally.

## Rules
1. For mixed-language prompts, use the dominant natural language to decide the opposite target language.
2. Translate all natural-language content that should be user-readable into the target language.
3. Preserve line breaks, list structure, tags, and prompt segmentation when possible.
4. Keep IDs, asset markers, variable names, file names, model names, color codes, bracket tags, and technical tokens intact.
   Examples: [CM_6932], [YZSZ_974d], #00FFFF, 16:9, v2.0, fal.ai.
5. Do not add new details not present in the source.
6. For image/video/audio/text prompting, prefer natural creator-facing wording over literal textbook translation.
7. Only return the source directly when the detected source_language is exactly the same as the target_language.
8. If source_language and target_language differ, copying the original prose is a failure.
9. When translating English into Chinese, keep technical tokens intact but translate every English instruction sentence, rule sentence, heading, and description into Simplified Chinese.
10. When translating Chinese into English, keep technical tokens intact but translate every Chinese instruction sentence, rule sentence, heading, and description into English.
11. Return structured data matching the requested schema. Do not wrap with markdown.
"""

FREEZONE_TEXT_WRITER_SYSTEM_PROMPT = """# Freezone AI Text Writer

You create polished, creator-ready text from a user's instruction.

## Goal
- Write the requested story, scene, character setting, dialogue, outline, or creative prompt.
- Follow the user's requested language, structure, tone, length, and formatting.
- If the user does not specify a language, write in natural Indonesian (Bahasa Indonesia).
- Make the result concrete and directly usable in a creative workflow.

## Rules
1. Preserve names, IDs, technical tokens, ratios, and other constraints supplied by the user.
2. Do not invent constraints that conflict with the user's instruction.
3. Return only the finished text. Do not explain your process.
4. Do not wrap the result in a markdown code fence.
"""

FREEZONE_STORY_SCRIPT_SYSTEM_PROMPT = """# Freezone Story Script Generator

You generate a structured story-script table from an uploaded script excerpt.

## Goal
- Turn the source script into a complete, production-oriented story script.
- Output rows that are directly usable by downstream image and video nodes.
- Keep the result cinematic, concrete, and structured.

## Output language (mandatory)
- Write EVERY user-visible prose field in natural Indonesian (Bahasa Indonesia).
- Short and direct — no fluff, no courtesy padding (*Silakan*, *Harap*, filler openers).
- This includes: title, visual_description, character names when inventing labels,
  character descriptions, shot, character_action, emotion, scene_tags,
  lighting_mood, sound, dialogue, shot_prompt, and video_motion_prompt.
- Keep character names supplied by the user verbatim; never translate proper names.
- Keep technical tokens intact (ratios, hex colors, model names, bracket IDs).
- Empty dialogue or empty optional prose must be exactly: `Tidak ada`
  (never Chinese `无`, never English `None` / `N/A`).

## Requirements
1. Break the story into clear numbered shots with sequential `shot_no`, starting from 1.
2. Each row must include all schema fields. Do not omit fields.
3. Prefer concrete visual language over vague abstraction. Every shot should feel filmable.
4. Dialogue should be short and only present when appropriate. If no dialogue is needed, output `Tidak ada`.
5. If a field has no meaningful content, prefer `Tidak ada` instead of vague placeholders.
6. Output only structured data matching the schema. Do not wrap with markdown.

## Table style target
- The result should resemble a production storyboard table, not a prose summary.
- `visual_description` should describe one clear beat of action or state, usually in one concise Indonesian sentence.
- `shot` should use concise combinations like `Medium shot / eye level`, written in Indonesian
  (e.g. `Medium shot / sejajar mata`, `Close-up / sudut rendah`, `Wide / bird's-eye`).
- `emotion` should be compact and specific, often 2-3 short Indonesian phrases joined by `, `.
- `scene_tags`, `lighting_mood`, `sound` should all be concrete and film-facing Indonesian.
- `character_1` should prefer a stable role identifier if inferable, such as `Sari_modern` or `Sari_klasik`.
- `character_description_1` should prefer bracketed character-card format, e.g.
  `[Sari_modern: perempuan 28 tahun, wajah pucat, ekspresi lelah, mengenakan busana kerja modern sederhana…]`.

## Duration guidance
- Default to short cinematic shots.
- Most rows should fall in the 2-5 second range unless the source clearly calls for a longer beat.
- Keep the pacing readable and dramatic rather than mechanically uniform.

## Prompt formatting rules
`shot_prompt` must be image-generation friendly and must be written as a chained bracket structure using ` + ` separators.
All bracket labels and prose inside must be Indonesian.

Preferred order for `shot_prompt`:
1. `[Komposisi gambar: ukuran bidikan, sudut kamera, perspektif, hubungan komposisi]`
2. `[Kartu karakter/subjek: jika ada karakter 1, pakai atau sesuaikan ringan format character_description_1; jika tidak ada, deskripsikan subjek inti]`
3. `[Relasi ruang subjek/tokoh: siapa di foreground, siapa di midground, siapa berinteraksi dengan lingkungan/properti]`
4. `[Detail mikro ekspresi/state/visual kunci: arah pandang, sudut bibir, ketegangan tubuh, kondisi kostum, luka, keringat, darah, dll.]`
5. `[Elemen lingkungan & properti foreground/background: kantor, istana, layar komputer, debu, celah pintu, dll.]`
6. `[Geometri cahaya & atmosfer: arah cahaya utama, suhu warna, rim light, kabut, backlight, top light, volume light]`
7. `[Gaya visual/tekstur: sinematik realistis, dokumenter, tegang dingin, epik sejarah, dll.]`
8. `[Parameter teknis: focal length, aperture, depth of field, shutter feel, grain/resolusi; jangan dihilangkan]`

Example style for `shot_prompt`:
- `[Komposisi gambar: close-up medium, kamera sejajar mata] + [Kartu karakter/subjek: [Sari_modern: perempuan 28 tahun, wajah pucat, ekspresi lelah, busana kerja modern sederhana]] + [Relasi ruang subjek/tokoh: dia duduk sendiri di meja kerja, cahaya biru layar komputer menyinari wajah dari samping depan] + [Detail mikro ekspresi/state/visual kunci: kantung mata kebiruan, jari bergetar tipis, pandangan kosong, bibir sedikit terbuka] + [Elemen lingkungan & properti foreground/background: kantor malam hari, cahaya biru komputer, berkas kertas berantakan, kopi dingin] + [Geometri cahaya & atmosfer: dominan biru dingin, side-light layar menekan bayangan wajah, kabut abu tipis di latar] + [Gaya visual/tekstur: sinematik misteri urban realistis] + [Parameter teknis: lensa 85mm, f/1.8, shallow depth of field]`

`video_motion_prompt` must focus on motion and should also use a chained bracket structure in Indonesian.

Preferred order for `video_motion_prompt`:
1. `[Lintasan & kecepatan kamera: push/pull/pan/truck/follow/crane/handheld — tulis kecepatan, intensitas, stabilitas]`
2. `[Aksi fisik subjek yang sangat konkret: bagaimana tubuh/objek bergerak; jangan hanya tulis perubahan emosi]`
3. `[Dinamis lingkungan: angin, hujan, ujung kain, debu, tirai, kedip layar, api, salju, dll.]`
4. `[Suara & atmosfer: ambient, benda, napas, langkah, guntur, dll.]`
5. `[Dialog & nada: tulis dialog + nada bicara; jika tidak ada tulis Tidak ada]`
6. `[Durasi: 4.0s]`

Example style for `video_motion_prompt`:
- `[Lintasan & kecepatan kamera: dorong sangat lambat, hampir menempel wajah, stabil dengan napas ringan] + [Aksi fisik subjek yang sangat konkret: pandangan Sari sempat kosong, lalu pupil mengecil, ujung jari bergetar di meja, jakun tertelan tertahan] + [Dinamis lingkungan: cahaya dingin layar berkedip tipis, tepi kertas digoyang AC, permukaan kopi bergoyang] + [Suara & atmosfer: ketikan keyboard cepat, notifikasi ponsel beruntun, dengung listrik frekuensi rendah] + [Dialog & nada: Tidak ada] + [Durasi: 4.0s]`

## Quality bar
- Avoid generic outputs like `orang berdiri`, `kamera maju`, `emosi rumit`.
- Prefer highly specific physical action, facial detail, scene detail, and camera-language wording in Indonesian.
- Preserve story logic and character-state progression across rows.

## Asset fields you must NOT invent
- `character_image_1`, `character_image_2`, `reference` are asset URL slots filled in by the
  backend after generation. Always output them as an empty string.
- Never write `Tidak ada`, a file name, or a made-up URL into those three fields.
- When two distinct characters appear in one shot, fill `character_2` /
  `character_description_2` the same way as `character_1` / `character_description_1`.
  Reuse the exact same character identifier across rows so the same person keeps one name.
"""

FREEZONE_VIDEO_STORY_SCRIPT_SYSTEM_PROMPT = FREEZONE_STORY_SCRIPT_SYSTEM_PROMPT + """
## Vision-reference modes
Images may be attached to the request. The task message states which mode applies; follow that
mode and ignore the other one.

### Video-keyframe mode
You are given an ordered set of keyframes sampled from a reference video.
- The story script MUST describe what is actually visible in those frames. Do not invent an
  unrelated story, and do not fall back on the examples in this prompt.
- Read the frames as one continuous clip: identify the real subject(s), setting, wardrobe or
  species, palette, and what physically changes from frame to frame.
- If the subject is not human (animal, object, mascot, animation), say so plainly in
  `character_1` and `character_description_1`. Do not substitute a human character.
- Group consecutive frames into narrative shots rather than describing every frame.
- Set `keyframe_index` on every row to the 1-based index of the input frame that best
  represents that shot. This is how the backend attaches the reference thumbnail.
- Total duration across rows should stay close to the stated video duration.

### Character-reference mode
You are given one portrait-style reference image per character, in the order the task message
lists them. There is no reference video.
- Read every character's real appearance off their image — face, hair, wardrobe, era, species —
  and write `character_description_1` / `character_description_2` from what you actually see.
  Do not describe a character the images do not show.
- Reuse the exact character names given in the task message so the backend can attach each
  character's reference image.
- The story itself comes from the user's request (and the source script, when one is supplied),
  not from the images. The images only fix who the characters are.
- Set `keyframe_index` to 0 on every row: there are no keyframes to attach.
"""

FREEZONE_NODE_TYPE_LABELS: dict[str, str] = {
    "generic": "通用提示词",
    "image": "图片节点提示词",
    "video": "视频节点提示词",
    "audio": "音频节点提示词",
    "text": "文本节点提示词",
}

_translation_agent: Optional[Agent] = None
_text_writer_agent: Optional[Agent] = None
_story_script_agent: Optional[Agent] = None
_video_story_script_agent: Optional[Agent] = None


class FreezoneTranslationResult(BaseModel):
    """Structured translation result produced by the LLM."""

    translated_text: str = Field(description="Translated prompt text.")
    source_language: Literal["zh", "en"] = Field(
        description="Dominant natural language detected from the source text."
    )
    target_language: Literal["zh", "en"] = Field(
        description="Opposite target language used for translation."
    )


def create_freezone_translation_agent() -> Agent:
    """创建 Freezone 中英互译 Agent。"""
    from novelvideo.config import (
        get_newapi_structured_output_model_settings,
        get_newapi_text_pydantic_model,
    )

    model = get_newapi_text_pydantic_model(
        "FREEZONE_TRANSLATION_MODEL",
        FREEZONE_TRANSLATION_MODEL,
        capability="freezone.text.generate",
    )
    return Agent(
        model,
        system_prompt=FREEZONE_TRANSLATION_SYSTEM_PROMPT,
        model_settings=get_newapi_structured_output_model_settings(),
        output_type=FreezoneTranslationResult,
        name="Freezone Prompt Translator",
    )


def get_freezone_translation_agent() -> Agent:
    """获取翻译 Agent 单例。"""
    global _translation_agent
    context = current_model_gateway_context()
    if context is not None and context.is_organization:
        return create_freezone_translation_agent()
    if _translation_agent is None:
        _translation_agent = create_freezone_translation_agent()
    return _translation_agent


def create_freezone_text_writer_agent() -> Agent:
    """创建 Freezone 自由文本生成 Agent。"""
    from novelvideo.config import get_newapi_text_pydantic_model

    model = get_newapi_text_pydantic_model(
        "FREEZONE_TEXT_WRITER_MODEL",
        FREEZONE_TEXT_WRITER_MODEL,
    )
    return Agent(
        model,
        system_prompt=FREEZONE_TEXT_WRITER_SYSTEM_PROMPT,
        output_type=str,
        name="Freezone AI Text Writer",
    )


def get_freezone_text_writer_agent() -> Agent:
    """获取自由文本生成 Agent 单例。"""
    global _text_writer_agent
    if _text_writer_agent is None:
        _text_writer_agent = create_freezone_text_writer_agent()
    return _text_writer_agent


def resolve_freezone_text_writer_model() -> str:
    """返回当前自由文本生成逻辑模型名，供结果与审计记录使用。"""
    from novelvideo.config import get_newapi_text_model_name

    return get_newapi_text_model_name(
        "FREEZONE_TEXT_WRITER_MODEL",
        FREEZONE_TEXT_WRITER_MODEL,
    )


def resolve_freezone_story_script_model(model: str | None) -> dict[str, str]:
    model_text = str(model or "").strip()
    if not model_text:
        return dict(FREEZONE_STORY_SCRIPT_MODEL)
    if model_text == FREEZONE_STORY_SCRIPT_MODEL["id"]:
        return dict(FREEZONE_STORY_SCRIPT_MODEL)
    if model_text.casefold() == FREEZONE_STORY_SCRIPT_MODEL["label"].casefold():
        return dict(FREEZONE_STORY_SCRIPT_MODEL)
    if model_text in LEGACY_FREEZONE_STORY_SCRIPT_MODEL_IDS:
        return dict(FREEZONE_STORY_SCRIPT_MODEL)
    raise ValueError(f"unsupported story script model: {model_text}")


def create_freezone_story_script_agent(model: str | None = None) -> Agent:
    """创建故事脚本生成 Agent。"""
    from novelvideo.api.schemas import FreezoneStoryScriptGenerateData
    from novelvideo.config import (
        get_newapi_structured_output_model_settings,
        get_newapi_text_pydantic_model,
    )

    resolved = resolve_freezone_story_script_model(model)
    llm_model = get_newapi_text_pydantic_model(
        "FREEZONE_STORY_SCRIPT_MODEL",
        resolved["model"],
        capability="freezone.text.generate",
    )
    return Agent(
        llm_model,
        system_prompt=FREEZONE_STORY_SCRIPT_SYSTEM_PROMPT,
        model_settings=get_newapi_structured_output_model_settings(),
        output_type=FreezoneStoryScriptGenerateData,
        # 结构化脚本表字段多、且 shot_no/duration 是严格 int，模型偶尔会把时长写成
        # "2-5"/"3秒" 之类而过不了校验。默认 output_retries=1 只给一次纠正机会不够，
        # 抛 "Exceeded maximum output retries (1)"。对齐本仓其它复杂结构化 agent
        # (episode_planner / content_rewriter)提到 3，让模型按回喂的校验错误自我修正。
        output_retries=model_gateway_output_retries(3),
        name="Freezone Story Script Generator",
    )


def get_freezone_story_script_agent(model: str | None = None) -> Agent:
    """获取故事脚本生成 Agent 单例。"""
    global _story_script_agent
    resolved = resolve_freezone_story_script_model(model)
    context = current_model_gateway_context()
    if context is not None and context.is_organization:
        return create_freezone_story_script_agent(resolved["id"])
    if _story_script_agent is None:
        _story_script_agent = create_freezone_story_script_agent(resolved["id"])
    return _story_script_agent


def build_freezone_translation_task(
    *,
    text: str,
    node_type: Literal["generic", "image", "video", "audio", "text"],
) -> str:
    """构建翻译任务。"""
    node_label = FREEZONE_NODE_TYPE_LABELS[node_type]

    parts = [
        f"Translate the following {node_label}.",
        "You must decide whether the dominant natural language is Simplified Chinese or English.",
        "If dominant language is English, translate into Simplified Chinese.",
        "If dominant language is Simplified Chinese, translate into English.",
        "Do not copy the original prose when translating between different languages.",
        "Preserve IDs, file names, bracket tags, color codes, ratios, and model names exactly, but translate the surrounding natural-language instructions.",
        "Keep it directly usable as a creative prompt.",
    ]
    parts.append(f"Source text:\n{text.strip()}")
    return "\n\n".join(parts)


async def translate_freezone_text(
    *,
    text: str,
    node_type: Literal["generic", "image", "video", "audio", "text"] = "generic",
    egress_context: TrustedEgressContext | None = None,
) -> tuple[str, Literal["zh", "en"], Literal["zh", "en"]]:
    """执行 Freezone 中英互译。"""
    if not text or not text.strip():
        return "", "zh", "en"

    task = build_freezone_translation_task(
        text=text,
        node_type=node_type,
    )
    from novelvideo.model_gateway_runtime import model_gateway_request_scope

    with model_gateway_request_scope(egress_context):
        response = await get_freezone_translation_agent().run(task)
    result = response.output
    target_language: Literal["zh", "en"] = result.target_language
    if target_language == result.source_language:
        target_language = "zh" if result.source_language == "en" else "en"
    return (
        result.translated_text.strip(),
        result.source_language,
        target_language,
    )


async def generate_freezone_text(
    *,
    prompt: str,
    egress_context: TrustedEgressContext | None = None,
) -> tuple[str, str]:
    """根据用户指令生成自由文本，返回逻辑模型名与最终文本。**会出网**。

    形参与 `model_gateway_request_scope` 都照 `translate_freezone_text` 写：
    `runners/freezone.py:FREEZONE_LEAF_EGRESS` 判本函数为 NETWORK 的依据就是它。
    """
    clean_prompt = str(prompt or "").strip()
    if not clean_prompt:
        raise ValueError("prompt is required")

    from novelvideo.model_gateway_runtime import model_gateway_request_scope

    with model_gateway_request_scope(egress_context):
        response = await get_freezone_text_writer_agent().run(clean_prompt)
    generated_text = str(response.output or "").strip()
    if not generated_text:
        raise ValueError("text generation returned empty output")
    return resolve_freezone_text_writer_model(), generated_text


_STORY_SCRIPT_COMMON_RULES = (
    "Field keluaran wajib mencakup: nomor bidikan, durasi, deskripsi visual, karakter 1, "
    "deskripsi karakter 1, gambar karakter 1, karakter 2, deskripsi karakter 2, "
    "gambar karakter 2, referensi, ukuran bidikan, aksi karakter, emosi, tag adegan, "
    "pencahayaan & suasana, sound, dialogue, prompt singkat, prompt gerakan video.",
    "Semua field prosa yang terlihat pengguna WAJIB berbahasa Indonesia natural.",
    "Jika pengguna memberi permintaan tambahan, patuhi juga.",
    "Keluarkan tabel produksi storyboard, bukan ringkasan prosa.",
    "Prompt singkat dan prompt gerakan video wajib memakai format kurung berantai yang dipisah ` + `.",
    "Jika tidak ada dialogue, tulis `Tidak ada`.",
    "Field gambar karakter 1, gambar karakter 2, dan referensi selalu string kosong — "
    "URL diisi backend; jangan tulis `Tidak ada`, nama file, atau URL fiktif.",
    "Prompt singkat harus layak untuk image generation; prompt gerakan video harus layak "
    "untuk video motion, bukan satu kalimat ringkas.",
)

_STORY_SCRIPT_STYLE_HINT = (
    "Poin gaya:\n"
    "- Nomor bidikan naik berurutan\n"
    "- Durasi umumnya 2-5 detik\n"
    "- Ukuran bidikan mirip `Medium shot / sejajar mata`, `Close-up / sudut rendah`\n"
    "- Deskripsi karakter sebaiknya bentuk `[ID_karakter: ...]`\n"
    "- Orang yang sama di semua baris harus memakai nama karakter yang identik\n"
    "- Jika satu bidikan punya dua karakter, isi karakter 2 / deskripsi karakter 2\n"
    "- Prompt singkat idealnya 8 segmen: komposisi, kartu karakter/subjek, relasi ruang, "
    "mikro ekspresi/state, lingkungan & properti, geometri cahaya, gaya visual, parameter teknis\n"
    "- Jika ada karakter 1, segmen kedua prompt singkat sebaiknya memakai/menyesuaikan ringan "
    "deskripsi karakter 1\n"
    "- Segmen parameter teknis jangan dihilangkan\n"
    "- Prompt gerakan video idealnya 6 segmen: lintasan kamera, aksi subjek, dinamis lingkungan, "
    "suara & atmosfer, dialogue & nada, durasi\n"
    "- Aksi subjek harus gerakan fisik yang terlihat, bukan hanya perubahan emosi"
)


def _character_ref_block(
    character_refs: Sequence[Mapping[str, Any]] | None,
) -> str | None:
    """Render character reference cards for the task prompt.

    Only name + description + role are given — images travel as multimodal
    attachments; URLs are filled by the backend after generation.
    """
    if not character_refs:
        return None
    lines: list[str] = []
    for index, ref in enumerate(character_refs, start=1):
        name = str(ref.get("name") or "").strip() or f"Karakter{index}"
        description = str(ref.get("description") or "").strip()
        role = str(ref.get("role") or "").strip()
        detail = ", ".join(part for part in (role, description) if part)
        lines.append(f"{index}. {name}" + (f" ({detail})" if detail else ""))
    return (
        "Referensi karakter yang disediakan (urutannya sesuai gambar terlampir):\n"
        + "\n".join(lines)
        + "\nPakai nama karakter yang sama persis di field karakter 1 / karakter 2 "
        "agar backend bisa mengaitkan gambar referensi."
    )


def build_freezone_story_script_task(
    *,
    source_text: str,
    prompt: str,
    character_refs: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """Bangun tugas generate tabel skrip storyboard."""
    parts = [
        "Dari cuplikan naskah berikut, buat tabel skrip storyboard yang lengkap.",
        "Bahasa keluaran default: Bahasa Indonesia natural untuk semua field prosa.",
        *_STORY_SCRIPT_COMMON_RULES,
    ]
    if prompt.strip():
        parts.append(f"Permintaan pengguna:\n{prompt.strip()}")
    character_block = _character_ref_block(character_refs)
    if character_block:
        parts.append(character_block)
    parts.append(_STORY_SCRIPT_STYLE_HINT)
    parts.append(f"Isi naskah sumber:\n{source_text.strip()}")
    return "\n\n".join(parts)


def build_freezone_video_story_script_task(
    *,
    frame_count: int,
    prompt: str,
    duration_sec: float | None = None,
    character_refs: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """Bangun tugas generate skrip dari keyframe video referensi."""
    duration_hint = (
        f"Durasi total video sekitar {duration_sec:.2f} detik; "
        "jumlah durasi semua bidikan harus mendekati nilai itu."
        if duration_sec and duration_sec > 0
        else "Durasi total video tidak diketahui; perkirakan durasi menurut kepadatan keyframe."
    )
    parts = [
        f"Berikut {frame_count} keyframe berurutan dari video referensi. "
        "Urai menjadi tabel skrip storyboard yang lengkap.",
        "Ini tugas uraian video, bukan cerita orisinal: isi tabel harus menggambarkan "
        "subjek, adegan, aksi, dan gaya yang benar-benar terlihat di keyframe. "
        "Jangan meniru contoh karakter/scene dari system prompt.",
        "Baca semua keyframe dulu untuk menilai kontennya (manusia? hewan? animasi? live-action?), "
        "baru tentukan nama dan deskripsi karakter. Jika subjek bukan manusia, tulis apa adanya.",
        duration_hint,
        "Gabungkan keyframe berurutan menjadi bidikan naratif; jangan daftar mekanis per frame.",
        "Setiap baris wajib mengisi keyframe_index: nomor keyframe input yang paling mewakili "
        f"bidikan itu (bilangan bulat 1 sampai {frame_count}). Backend memakai ini untuk thumbnail.",
        "Bahasa keluaran default: Bahasa Indonesia natural untuk semua field prosa.",
        *_STORY_SCRIPT_COMMON_RULES,
    ]
    if prompt.strip():
        parts.append(f"Permintaan tambahan pengguna:\n{prompt.strip()}")
    character_block = _character_ref_block(character_refs)
    if character_block:
        parts.append(character_block)
    parts.append(_STORY_SCRIPT_STYLE_HINT)
    return "\n\n".join(parts)


def build_freezone_character_story_script_task(
    *,
    image_count: int,
    prompt: str,
    source_text: str = "",
    character_refs: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """Bangun tugas generate skrip dari gambar referensi karakter."""
    parts = [
        f"Berikut {image_count} gambar referensi karakter berurutan. "
        "Buat tabel skrip storyboard yang lengkap.",
        "Mode referensi karakter (tanpa video): tampilan, kostum, era, dan aura karakter 1 / 2 "
        "harus mengikuti gambar referensi yang sesuai; jangan deskripsikan orang yang tidak ada di gambar.",
        "Alur cerita berasal dari permintaan pengguna (dan naskah sumber opsional), "
        "bukan dari contoh di system prompt.",
        "Setiap baris: keyframe_index = 0 (tidak ada keyframe untuk diisi).",
        "Bahasa keluaran default: Bahasa Indonesia natural untuk semua field prosa.",
        *_STORY_SCRIPT_COMMON_RULES,
    ]
    if prompt.strip():
        parts.append(f"Permintaan pengguna:\n{prompt.strip()}")
    else:
        parts.append(
            "Pengguna tidak memberi permintaan tambahan; susun drama pendek yang utuh "
            "mengitari karakter-karakter ini."
        )
    character_block = _character_ref_block(character_refs)
    if character_block:
        parts.append(character_block)
    parts.append(_STORY_SCRIPT_STYLE_HINT)
    if source_text.strip():
        parts.append(f"Isi naskah sumber:\n{source_text.strip()}")
    return "\n\n".join(parts)


async def generate_freezone_story_script(
    *,
    source_text: str,
    prompt: str = "",
    model: str | None = None,
    character_refs: Sequence[Mapping[str, Any]] | None = None,
    egress_context: TrustedEgressContext | None = None,
):
    """执行故事脚本生成（文本 / 角色图模式）。"""
    if not source_text or not source_text.strip():
        raise ValueError("source_text is required")

    task = build_freezone_story_script_task(
        source_text=source_text,
        prompt=prompt,
        character_refs=character_refs,
    )
    from novelvideo.model_gateway_runtime import model_gateway_request_scope

    with model_gateway_request_scope(egress_context):
        response = await get_freezone_story_script_agent(model).run(task)
    return response.output


def create_freezone_video_story_script_agent() -> Agent:
    """创建「视频参考生成分镜脚本」的视觉 Agent。

    走 ``FREEZONE_VISION_MODEL``（``DC-freezone-vision-LLM``）而不是纯文本的
    story-script 别名 —— 带图请求只有视觉渠道能接。
    """
    from novelvideo.api.schemas import FreezoneStoryScriptGenerateData
    from novelvideo.config import (
        get_newapi_structured_output_model_settings,
        get_newapi_text_pydantic_model,
    )
    from novelvideo.official_defaults import DEFAULT_FREEZONE_VISION_MODEL

    return Agent(
        get_newapi_text_pydantic_model(
            "FREEZONE_VISION_MODEL",
            DEFAULT_FREEZONE_VISION_MODEL,
            timeout_seconds_override=300.0,
            capability="vision.analyze",
        ),
        system_prompt=FREEZONE_VIDEO_STORY_SCRIPT_SYSTEM_PROMPT,
        model_settings=get_newapi_structured_output_model_settings(),
        output_type=FreezoneStoryScriptGenerateData,
        output_retries=model_gateway_output_retries(3),
        name="Freezone Video Story Script Generator",
    )


def get_freezone_video_story_script_agent() -> Agent:
    """获取视频分镜脚本 Agent 单例。"""
    global _video_story_script_agent
    context = current_model_gateway_context()
    if context is not None and context.is_organization:
        return create_freezone_video_story_script_agent()
    if _video_story_script_agent is None:
        _video_story_script_agent = create_freezone_video_story_script_agent()
    return _video_story_script_agent


async def generate_freezone_story_script_with_vision(
    *,
    frame_paths: Sequence[str | Path] | None = None,
    character_image_paths: Sequence[str | Path] | None = None,
    source_text: str = "",
    prompt: str = "",
    duration_sec: float | None = None,
    character_refs: Sequence[Mapping[str, Any]] | None = None,
    egress_context: TrustedEgressContext | None = None,
):
    """带图的分镜脚本生成：视频关键帧 / 角色参考图 → 结构化脚本表。

    覆盖两种入口：

    - 「视频参考生成分镜脚本」：``frame_paths`` 是抽出来的关键帧，走视频拆解任务书。
    - 「角色生成分镜脚本」：只有 ``character_image_paths``，走角色参考任务书 ——
      剧情来自 ``prompt``（和可选的 ``source_text``），角色图只负责钉死角色长相。
      这一路不要求 ``source_text``：前端挂了素材时只会发提示词。
    """
    from pydantic_ai import BinaryContent

    from novelvideo.freezone.vision_gateway import load_compact_vision_inputs

    frames = [Path(path) for path in (frame_paths or []) if Path(path).exists()]
    character_images = [
        Path(path) for path in (character_image_paths or []) if Path(path).exists()
    ]
    if not frames and not character_images:
        raise ValueError(
            "vision story script requires at least one keyframe or character image"
        )

    if frames:
        task = build_freezone_video_story_script_task(
            frame_count=len(frames),
            prompt=prompt,
            duration_sec=duration_sec,
            character_refs=character_refs,
        )
    else:
        # 只有角色图：剧情从提示词 / 可选源剧本来，图片只钉角色长相。
        # 这里不能要求 source_text —— 前端在挂了素材时就只发提示词。
        task = build_freezone_character_story_script_task(
            image_count=len(character_images),
            prompt=prompt,
            source_text=source_text,
            character_refs=character_refs,
        )

    vision_inputs = await load_compact_vision_inputs((*frames, *character_images))
    attachments: list[Any] = [
        BinaryContent(data=image.data, media_type=image.media_type)
        for image in vision_inputs
    ]
    from novelvideo.model_gateway_runtime import model_gateway_request_scope

    with model_gateway_request_scope(egress_context):
        response = await get_freezone_video_story_script_agent().run(
            [task, *attachments]
        )
    return response.output


def bind_story_script_assets(
    data: Any,
    *,
    frame_urls: Sequence[str] | None = None,
    character_refs: Sequence[Mapping[str, Any]] | None = None,
) -> Any:
    """把关键帧 / 角色参考图的 URL 回填进生成好的脚本行。

    模型只负责写角色名和 ``keyframe_index``，素材 URL 一律由这里补齐 ——
    这样模型没有机会编造出 404 的链接（issue #207 里角色图列恒为空的另一半原因）。
    """
    frames = [url for url in (frame_urls or []) if url]
    by_name: dict[str, str] = {}
    for ref in character_refs or []:
        name = str(ref.get("name") or "").strip()
        image_url = str(ref.get("image_url") or "").strip()
        if name and image_url:
            by_name[name.casefold()] = image_url
    ordered_images = [
        str(ref.get("image_url") or "").strip()
        for ref in character_refs or []
        if str(ref.get("image_url") or "").strip()
    ]

    def _match(name: str) -> str:
        clean = str(name or "").strip()
        if not clean:
            return ""
        folded = clean.casefold()
        if folded in by_name:
            return by_name[folded]
        # 模型常把角色名写成 `沈昭昭_现代` 这类带状态后缀的稳定 ID，
        # 精确匹配不到时退到包含匹配，仍匹配不到才放弃。
        for candidate, url in by_name.items():
            if candidate in folded or folded in candidate:
                return url
        return ""

    for index, row in enumerate(getattr(data, "rows", []) or []):
        keyframe_index = int(getattr(row, "keyframe_index", 0) or 0)
        if not (1 <= keyframe_index <= len(frames)):
            # 模型没给或给错序号时退回按行号顺序取帧，保证参考列不至于整列为空。
            keyframe_index = index + 1 if index < len(frames) else 0
        row.reference = frames[keyframe_index - 1] if keyframe_index else ""
        row.keyframe_index = keyframe_index

        row.character_image_1 = _match(getattr(row, "character_1", ""))
        row.character_image_2 = _match(getattr(row, "character_2", ""))
        # 只有一张角色图、且模型没写出可匹配的角色名时，直接绑定唯一那张，
        # 否则「角色生成分镜脚本」在模型改写角色名后又会退化成空列。
        if not row.character_image_1 and len(ordered_images) == 1:
            row.character_image_1 = ordered_images[0]

    return data
