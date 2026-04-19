import { NextResponse } from "next/server";
import { z } from "zod";
import { findInstallCodeByPlainCode } from "@/lib/account";
import { getEntitlementForInstallCode, getFixturePackage } from "@/lib/package-access";
import { getProductById, getProductVersion } from "@/lib/products";

const requestSchema = z.object({
  code: z.string().min(6),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = requestSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid install code request", issues: parsed.error.flatten() }, { status: 400 });
  }

  const installCode = findInstallCodeByPlainCode(parsed.data.code);

  if (!installCode) {
    return NextResponse.json({ error: "Install code not found" }, { status: 404 });
  }

  if (installCode.status !== "active" || installCode.useCount >= installCode.maxUses) {
    return NextResponse.json({ error: "Install code is not active" }, { status: 403 });
  }

  const entitlement = getEntitlementForInstallCode(installCode);
  const version = getProductVersion(installCode.productVersionId);
  const product = entitlement ? getProductById(entitlement.productId) : undefined;
  const packagePreview = version ? getFixturePackage(version.packageId) : undefined;

  if (!entitlement || !version || !product || !packagePreview) {
    return NextResponse.json({ error: "Install code does not map to a package" }, { status: 404 });
  }

  return NextResponse.json({
    installCode: {
      id: installCode.id,
      status: installCode.status,
      maxUses: installCode.maxUses,
      useCount: installCode.useCount,
    },
    entitlementId: entitlement.id,
    product: {
      id: product.id,
      slug: product.slug,
      type: product.type,
      title: product.title,
    },
    package: {
      packageId: version.packageId,
      schemaVersion: version.packageSchemaVersion,
      assets: packagePreview.assets,
    },
  });
}
