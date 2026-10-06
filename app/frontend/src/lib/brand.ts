// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab

/** Product display name — keep UI + meta strings in sync via this constant. */
export const PRODUCT_NAME = "DNY";

/** Short mark used in tight chrome (favicon alt, aria when space is limited). */
export const PRODUCT_MARK = "DNY";

/** Primary brand mark asset (SVG preferred; PNG fallbacks live alongside). */
export const PRODUCT_LOGO_SRC = "/brand/aigc-dny-mark.svg";
export const PRODUCT_LOGO_PNG = "/brand/aigc-dny-mark.png";

/**
 * Replace legacy upstream product names in user-visible copy.
 * Does not touch protocol tags, package names, CDN paths, or env keys —
 * only strings already destined for toasts, logs, and UI text.
 */
export function rebrandUserFacingText(text: string): string {
  return text
    .replace(/\bDramaClawAPI\b/gi, PRODUCT_NAME)
    .replace(/\bDramaClaw\b/gi, PRODUCT_NAME)
    .replace(/\bDRAMACLAW\b/g, PRODUCT_NAME);
}
