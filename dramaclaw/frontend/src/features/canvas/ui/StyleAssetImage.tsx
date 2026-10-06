// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab
import { useState } from 'react';
import { ImageOff } from 'lucide-react';

import { resolveStyleAssetUrl } from '@/features/canvas/nodes/styleAssetUrl';
import { styleCategoryToneClass } from '@/features/canvas/domain/styleGalleryI18n';

export interface StyleAssetImageProps {
  /** 清单里的相对路径,由 resolveStyleAssetUrl 决定落到本地还是 OSS。 */
  rel: string;
  assetBase: string;
  alt: string;
  className?: string;
  loading?: 'lazy' | 'eager';
  draggable?: boolean;
  /** Optional Chinese category — colors the broken/missing placeholder. */
  category?: string;
  /** Optional short label drawn on the placeholder (localized display name). */
  placeholderLabel?: string;
}

/**
 * 风格封面/示例图。
 *
 * 提示词清单和图片可以分别换代(清单走 STYLE_GALLERY_MANIFEST、图片走
 * STYLE_GALLERY_ASSET_BASE),两边对不上时图会 404 —— 这里兜一个占位块,
 * 免得图墙里散落浏览器默认的碎图标。
 */
export function StyleAssetImage({
  rel,
  assetBase,
  alt,
  className = '',
  loading,
  draggable,
  category,
  placeholderLabel,
}: StyleAssetImageProps) {
  const [failedSrc, setFailedSrc] = useState<string | null>(null);
  const src = resolveStyleAssetUrl(rel, assetBase);
  const tone = styleCategoryToneClass(category);

  // 比较地址而不是存布尔:换了清单/换了前缀就自动重试一次。
  if (!src || failedSrc === src) {
    return (
      <div
        role="img"
        aria-label={alt}
        className={`relative flex min-h-10 overflow-hidden bg-gradient-to-br ${tone} ${
          placeholderLabel ? 'items-end justify-start' : 'items-center justify-center'
        } ${className}`}
      >
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              'radial-gradient(ellipse at 30% 20%, rgb(0 189 207 / 0.22), transparent 55%), radial-gradient(ellipse at 80% 90%, rgb(255 255 255 / 0.06), transparent 50%)',
          }}
        />
        {placeholderLabel ? (
          <div className="relative z-[1] flex w-full items-center gap-2 p-3">
            <ImageOff className="size-3.5 shrink-0 text-white/45" />
            <span className="truncate text-[11px] font-medium tracking-wide text-white/72">
              {placeholderLabel}
            </span>
          </div>
        ) : (
          <ImageOff className="relative z-[1] size-5 text-white/35" />
        )}
      </div>
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      loading={loading}
      draggable={draggable}
      onError={() => setFailedSrc(src)}
      className={className}
    />
  );
}
