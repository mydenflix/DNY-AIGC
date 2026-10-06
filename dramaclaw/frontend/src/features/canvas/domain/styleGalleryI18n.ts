// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab
/**
 * Freezone style-gallery display copy.
 *
 * Backend manifest (`style_templates.json`) keeps Chinese `label` / `category`
 * as the stable data contract (and Chinese `style_prompt` for the model).
 * UI shows localized names via these maps keyed by id / Chinese category.
 */
import type { FreezoneStyleTemplate } from "@/api/ops";
import type { TFn } from "@/lib/i18n-types";

/** Chinese category string from the manifest → i18n key suffix. */
export const STYLE_CATEGORY_KEYS: Readonly<Record<string, string>> = {
  古装: "period",
  都市: "urban",
  年代: "era",
  生活: "lifestyle",
  科幻: "scifi",
  类型: "genre",
  写意: "lyrical",
  动画: "animation",
  绘画: "painting",
  神话: "myth",
};

/** Cover placeholder gradient (Tailwind-friendly stops) per Chinese category. */
export const STYLE_CATEGORY_TONE: Readonly<Record<string, string>> = {
  古装: "from-[#3d2a18] via-[#24180f] to-[#12100e]",
  都市: "from-[#1a2a38] via-[#121820] to-[#0c1014]",
  年代: "from-[#3a2e22] via-[#221c16] to-[#12100e]",
  生活: "from-[#1e3328] via-[#142018] to-[#0e1210]",
  科幻: "from-[#12343a] via-[#0e1e24] to-[#0a1014]",
  类型: "from-[#3a1c22] via-[#221014] to-[#120c0e]",
  写意: "from-[#2a2438] via-[#18141f] to-[#100e14]",
  动画: "from-[#1a3040] via-[#122028] to-[#0c1418]",
  绘画: "from-[#2a3220] via-[#181c12] to-[#10120e]",
  神话: "from-[#3a3020] via-[#221c12] to-[#12100c]",
};

export function localizeStyleCategory(category: string, t: TFn): string {
  const trimmed = category.trim();
  if (!trimmed) return t("canvas.styleGallery.other");
  const key = STYLE_CATEGORY_KEYS[trimmed];
  if (!key) return trimmed;
  return t(`canvas.styleGallery.categories.${key}`, { defaultValue: trimmed });
}

export function localizeStyleTemplateLabel(
  template: Pick<FreezoneStyleTemplate, "id" | "label">,
  t: TFn,
): string {
  return t(`canvas.styleGallery.templates.${template.id}`, {
    defaultValue: template.label,
  });
}

export function styleCategoryToneClass(category: string | undefined): string {
  const trimmed = (category ?? "").trim();
  return STYLE_CATEGORY_TONE[trimmed] ?? "from-[#1e242c] via-[#14181e] to-[#0e1014]";
}
