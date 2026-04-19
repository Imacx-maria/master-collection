import { describe, expect, it } from "vitest";
import { findInstallCodeByPlainCode, hashInstallCode, normalizeInstallCode } from "@/lib/account";

describe("install-code helpers", () => {
  it("normalizes codes before hashing", () => {
    expect(normalizeInstallCode(" mc-atlas-ready-42 ")).toBe("MC-ATLAS-READY-42");
    expect(hashInstallCode("mc-atlas-ready-42")).toBe(hashInstallCode(" MC-ATLAS-READY-42 "));
  });

  it("resolves fixture codes by hash without exposing hash input coupling", () => {
    const installCode = findInstallCodeByPlainCode("mc-atlas-ready-42");

    expect(installCode?.status).toBe("active");
    expect(installCode?.codeHash).toBe(hashInstallCode("MC-ATLAS-READY-42"));
  });
});
