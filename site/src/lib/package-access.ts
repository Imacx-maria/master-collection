import { entitlements, type Entitlement, type InstallCode } from "@/lib/account";
import { getProductById, getProductVersionByPackageId } from "@/lib/products";

export type MasterCollectionPackage = {
  schemaVersion: "master-collection-package@1";
  packageId: string;
  productId: string;
  productVersionId: string;
  title: string;
  requiredFonts: string[];
  assets: Array<{
    assetKey: string;
    fileName: string;
    mimeType: string;
    sizeBytes: number;
  }>;
  xscpDataRef: string;
};

export function canAccessPackage({
  packageId,
  entitlement,
  installCode,
}: {
  packageId: string;
  entitlement?: Entitlement;
  installCode?: InstallCode;
}) {
  const version = getProductVersionByPackageId(packageId);

  if (!version) {
    return false;
  }

  if (installCode?.status === "active" && installCode.productVersionId === version.id && installCode.useCount < installCode.maxUses) {
    return true;
  }

  if (entitlement?.status === "active" && entitlement.productId === version.productId) {
    return true;
  }

  return false;
}

export function getEntitlementForInstallCode(installCode: InstallCode) {
  return entitlements.find((entitlement) => entitlement.id === installCode.entitlementId);
}

export function getFixturePackage(packageId: string): MasterCollectionPackage | undefined {
  const version = getProductVersionByPackageId(packageId);
  const product = version ? getProductById(version.productId) : undefined;

  if (!version || !product) {
    return undefined;
  }

  return {
    schemaVersion: "master-collection-package@1",
    packageId,
    productId: product.id,
    productVersionId: version.id,
    title: product.title,
    requiredFonts: product.requiredFonts,
    assets: [
      {
        assetKey: "preview-thumb",
        fileName: `${product.slug}-preview.png`,
        mimeType: "image/png",
        sizeBytes: 184000,
      },
      {
        assetKey: "package-manifest",
        fileName: `${product.slug}-manifest.json`,
        mimeType: "application/json",
        sizeBytes: 12000,
      },
    ],
    xscpDataRef: `fixtures/${product.slug}/xscp-data.json`,
  };
}
