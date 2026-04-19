import { describe, expect, it } from "vitest";
import { installCodes } from "@/lib/account";
import { canAccessPackage, getFixturePackage } from "@/lib/package-access";

describe("package access", () => {
  it("returns fixture packages for known package ids", () => {
    const packageData = getFixturePackage("pkg-atlas-studio-v1");

    expect(packageData?.schemaVersion).toBe("master-collection-package@1");
    expect(packageData?.assets.length).toBeGreaterThan(0);
  });

  it("allows active install codes for matching package versions", () => {
    expect(
      canAccessPackage({
        packageId: "pkg-atlas-studio-v1",
        installCode: installCodes[0],
      }),
    ).toBe(true);
  });

  it("rejects mismatched package access", () => {
    expect(
      canAccessPackage({
        packageId: "pkg-pricing-grid-v1",
        installCode: installCodes[0],
      }),
    ).toBe(false);
  });
});
