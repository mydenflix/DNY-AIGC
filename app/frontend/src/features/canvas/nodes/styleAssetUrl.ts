// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab

/**
 * 风格图片地址的唯一解析点。
 *
 * 图片不随仓库发布:后端配 STYLE_GALLERY_ASSET_BASE(OSS/CDN 域名)后由接口
 * 下发前缀,这里直接拼。assetBase 为空时返回空串 —— 仓库没有内置预览图,
 * StyleAssetImage 直接显示分类色占位块,避免去拉不存在的 /style-gallery/ 碎图标。
 */
export function resolveStyleAssetUrl(rel: string, assetBase: string): string {
  if (!rel) return '';
  const base = assetBase.trim();
  if (!base) return '';
  return `${base.replace(/\/+$/, '')}/${rel}`;
}
