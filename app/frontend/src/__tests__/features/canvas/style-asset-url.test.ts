// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab
import { describe, expect, it } from "vitest";

import { resolveStyleAssetUrl } from "@/features/canvas/nodes/styleAssetUrl";

describe("resolveStyleAssetUrl", () => {
  it("returns empty when no CDN base is configured (placeholders, no broken imgs)", () => {
    expect(resolveStyleAssetUrl("golden_age/cover.webp", "")).toBe("");
    expect(resolveStyleAssetUrl("golden_age/cover.webp", "   ")).toBe("");
  });

  it("uses the configured base and collapses duplicate slashes", () => {
    expect(
      resolveStyleAssetUrl("golden_age/cover.webp", "https://cdn.example.com/styles/"),
    ).toBe("https://cdn.example.com/styles/golden_age/cover.webp");
  });

  it("returns empty string for an empty relative path", () => {
    expect(resolveStyleAssetUrl("", "https://cdn.example.com/styles")).toBe("");
  });
});
