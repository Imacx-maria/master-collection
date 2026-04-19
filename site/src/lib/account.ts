import { createHash } from "node:crypto";
import { getProductById, getProductVersion } from "@/lib/products";

export type Order = {
  id: string;
  userId: string;
  provider: "stripe" | "manual" | "other";
  providerSessionId?: string;
  providerPaymentId?: string;
  status: "pending" | "paid" | "failed" | "refunded";
  amountCents: number;
  currency: string;
  createdAt: string;
  paidAt?: string;
};

export type Entitlement = {
  id: string;
  userId: string;
  productId: string;
  orderId: string;
  status: "active" | "revoked" | "refunded";
  createdAt: string;
};

export type InstallCode = {
  id: string;
  codeHash: string;
  entitlementId: string;
  productVersionId: string;
  status: "active" | "used" | "expired" | "revoked";
  maxUses: number;
  useCount: number;
  expiresAt?: string;
  createdAt: string;
  mockPlainCode?: string;
};

const mockCode = "MC-ATLAS-READY-42";

export const fixtureUserId = "user_local_fixture";

export const orders: Order[] = [
  {
    id: "order_fixture_atlas",
    userId: fixtureUserId,
    provider: "stripe",
    providerSessionId: "cs_test_fixture_atlas",
    status: "paid",
    amountCents: 14900,
    currency: "USD",
    createdAt: "2026-04-19T10:20:00.000Z",
    paidAt: "2026-04-19T10:22:00.000Z",
  },
];

export const entitlements: Entitlement[] = [
  {
    id: "ent_fixture_atlas",
    userId: fixtureUserId,
    productId: "prod-atlas-studio",
    orderId: "order_fixture_atlas",
    status: "active",
    createdAt: "2026-04-19T10:22:00.000Z",
  },
];

export const installCodes: InstallCode[] = [
  {
    id: "code_fixture_atlas",
    codeHash: hashInstallCode(mockCode),
    entitlementId: "ent_fixture_atlas",
    productVersionId: "ver-atlas-studio-1",
    status: "active",
    maxUses: 5,
    useCount: 0,
    expiresAt: "2026-05-19T10:22:00.000Z",
    createdAt: "2026-04-19T10:22:00.000Z",
    mockPlainCode: mockCode,
  },
];

export function hashInstallCode(code: string) {
  return createHash("sha256").update(normalizeInstallCode(code)).digest("hex");
}

export function normalizeInstallCode(code: string) {
  return code.trim().toUpperCase().replace(/\s+/g, "");
}

export function getLibraryItems(userId = fixtureUserId) {
  return entitlements
    .filter((entitlement) => entitlement.userId === userId)
    .map((entitlement) => {
      const product = getProductById(entitlement.productId);
      const order = orders.find((item) => item.id === entitlement.orderId);
      const installCode = installCodes.find((item) => item.entitlementId === entitlement.id);
      const version = installCode ? getProductVersion(installCode.productVersionId) : undefined;

      return {
        entitlement,
        product,
        order,
        installCode,
        version,
        purchaseId: entitlement.id,
      };
    })
    .filter((item) => item.product && item.order);
}

export function getLibraryItem(purchaseId: string, userId = fixtureUserId) {
  return getLibraryItems(userId).find((item) => item.purchaseId === purchaseId);
}

export function findInstallCodeByPlainCode(code: string) {
  const codeHash = hashInstallCode(code);
  return installCodes.find((item) => item.codeHash === codeHash);
}
