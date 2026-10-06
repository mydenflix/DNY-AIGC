// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { StyleAssetImage } from "@/features/canvas/ui/StyleAssetImage";

describe("StyleAssetImage", () => {
  it("resolves the relative path against the asset base", () => {
    render(
      <StyleAssetImage
        rel="golden_age/cover.webp"
        assetBase="https://cdn.example.com/styles"
        alt="黄金时代"
      />,
    );

    expect(screen.getByAltText("黄金时代")).toHaveAttribute(
      "src",
      "https://cdn.example.com/styles/golden_age/cover.webp",
    );
  });

  it("shows a placeholder immediately when no CDN base is configured", () => {
    render(
      <StyleAssetImage
        rel="gone/cover.webp"
        assetBase=""
        alt="已下架风格"
        placeholderLabel="已下架风格"
      />,
    );

    // 没配 CDN 就不发请求 —— 直接占位，别先露碎图标再等 onError
    const placeholder = screen.getByRole("img", { name: "已下架风格" });
    expect(placeholder.tagName).toBe("DIV");
    expect(screen.getByText("已下架风格")).toBeInTheDocument();
  });

  it("falls back to a placeholder when the asset 404s", () => {
    render(
      <StyleAssetImage
        rel="gone/cover.webp"
        assetBase="https://cdn.example.com/styles"
        alt="已下架风格"
      />,
    );

    fireEvent.error(screen.getByAltText("已下架风格"));

    // 图没了也要留个占位块，别露浏览器的碎图标
    const placeholder = screen.getByRole("img", { name: "已下架风格" });
    expect(placeholder.tagName).toBe("DIV");
  });

  it("renders the placeholder when the manifest has no cover", () => {
    render(<StyleAssetImage rel="" assetBase="" alt="无封面" />);

    expect(screen.getByRole("img", { name: "无封面" }).tagName).toBe("DIV");
  });
});
