import { NextResponse } from "next/server";
import { findInstallCodeByPlainCode } from "@/lib/account";
import { canAccessPackage, getEntitlementForInstallCode, getFixturePackage } from "@/lib/package-access";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ packageId: string; assetKey: string }> },
) {
  const { packageId, assetKey } = await params;
  const url = new URL(request.url);
  const plainCode = url.searchParams.get("installCode");
  const installCode = plainCode ? findInstallCodeByPlainCode(plainCode) : undefined;
  const entitlement = installCode ? getEntitlementForInstallCode(installCode) : undefined;

  if (!canAccessPackage({ packageId, installCode, entitlement })) {
    return NextResponse.json({ error: "Asset access requires an active entitlement or install code" }, { status: 403 });
  }

  const packageData = getFixturePackage(packageId);
  const asset = packageData?.assets.find((item) => item.assetKey === assetKey);

  if (!asset) {
    return NextResponse.json({ error: "Asset not found" }, { status: 404 });
  }

  return NextResponse.json({
    asset,
    content: `Fixture asset placeholder for ${asset.assetKey}. Real storage is pending package storage credentials.`,
  });
}
