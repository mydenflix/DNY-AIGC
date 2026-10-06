// SPDX-License-Identifier: Elastic-2.0
// Copyright (c) 2026 ClaymoreLab
import { describe, expect, it } from "vitest";
import type { TFunction } from "i18next";

import {
  localizeNodeDisplayName,
  localizeStoredSystemLabel,
} from "@/features/canvas/domain/nodeDisplay";
import { CANVAS_NODE_TYPES } from "@/features/canvas/domain/canvasNodes";

const STRINGS: Record<string, string> = {
  "viewer.threeD.selectedBackgroundOutputLabel": "Latar belakang saat ini",
  "taskCenter.io.directorComposite": "Direktur komposit",
  "taskCenter.io.currentBackground": "Latar belakang saat ini",
  "node.displayName.imageGen": "Node gambar",
};

const t = ((key: string) => STRINGS[key] ?? key) as TFunction;

describe("localizeStoredSystemLabel", () => {
  it("translates Chinese current-background labels with Beat suffix", () => {
    expect(localizeStoredSystemLabel("当前背景 · Beat 11", t)).toBe(
      "Latar belakang saat ini · Beat 11",
    );
    expect(localizeStoredSystemLabel("当前背景 - Beat 11", t)).toBe(
      "Latar belakang saat ini · Beat 11",
    );
    expect(localizeStoredSystemLabel("当前背景", t)).toBe("Latar belakang saat ini");
  });

  it("leaves custom user names alone", () => {
    expect(localizeStoredSystemLabel("TES1 background crop", t)).toBe(
      "TES1 background crop",
    );
  });
});

describe("localizeNodeDisplayName", () => {
  it("localizes stored Chinese displayName on imageGen nodes", () => {
    expect(
      localizeNodeDisplayName(
        CANVAS_NODE_TYPES.imageGen,
        { displayName: "当前背景 · Beat 11" },
        t,
      ),
    ).toBe("Latar belakang saat ini · Beat 11");
  });
});
