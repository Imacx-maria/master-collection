import { hashInstallCode, type Entitlement, type InstallCode, type Order } from "@/lib/account";

export type FulfillmentInput = {
  userId: string;
  productId: string;
  productVersionId: string;
  orderId: string;
  providerSessionId: string;
  providerPaymentId?: string;
  amountCents: number;
  currency: string;
  now: string;
  plainInstallCode: string;
};

export type FulfillmentState = {
  orders: Order[];
  entitlements: Entitlement[];
  installCodes: InstallCode[];
};

export type FulfillmentResult = {
  state: FulfillmentState;
  orderId: string;
  entitlementId: string;
  installCodeId: string;
  createdEntitlement: boolean;
  createdInstallCode: boolean;
};

export function fulfillCheckoutSession(
  currentState: FulfillmentState,
  input: FulfillmentInput,
): FulfillmentResult {
  const state: FulfillmentState = {
    orders: [...currentState.orders],
    entitlements: [...currentState.entitlements],
    installCodes: [...currentState.installCodes],
  };

  const existingOrderIndex = state.orders.findIndex(
    (order) => order.providerSessionId === input.providerSessionId || order.id === input.orderId,
  );

  if (existingOrderIndex >= 0) {
    state.orders[existingOrderIndex] = {
      ...state.orders[existingOrderIndex],
      status: "paid",
      providerPaymentId: input.providerPaymentId ?? state.orders[existingOrderIndex].providerPaymentId,
      paidAt: state.orders[existingOrderIndex].paidAt ?? input.now,
    };
  } else {
    state.orders.push({
      id: input.orderId,
      userId: input.userId,
      provider: "stripe",
      providerSessionId: input.providerSessionId,
      providerPaymentId: input.providerPaymentId,
      status: "paid",
      amountCents: input.amountCents,
      currency: input.currency,
      createdAt: input.now,
      paidAt: input.now,
    });
  }

  const order = state.orders.find((item) => item.providerSessionId === input.providerSessionId || item.id === input.orderId);
  const orderId = order?.id ?? input.orderId;
  const existingEntitlement = state.entitlements.find(
    (entitlement) =>
      entitlement.userId === input.userId &&
      entitlement.productId === input.productId &&
      entitlement.orderId === orderId,
  );

  let entitlementId = existingEntitlement?.id;
  let createdEntitlement = false;

  if (!entitlementId) {
    entitlementId = `ent_${orderId}_${input.productId}`;
    createdEntitlement = true;
    state.entitlements.push({
      id: entitlementId,
      userId: input.userId,
      productId: input.productId,
      orderId,
      status: "active",
      createdAt: input.now,
    });
  }

  const existingInstallCode = state.installCodes.find(
    (installCode) =>
      installCode.entitlementId === entitlementId &&
      installCode.productVersionId === input.productVersionId,
  );

  let installCodeId = existingInstallCode?.id;
  let createdInstallCode = false;

  if (!installCodeId) {
    installCodeId = `code_${orderId}_${input.productVersionId}`;
    createdInstallCode = true;
    state.installCodes.push({
      id: installCodeId,
      codeHash: hashInstallCode(input.plainInstallCode),
      entitlementId,
      productVersionId: input.productVersionId,
      status: "active",
      maxUses: 5,
      useCount: 0,
      createdAt: input.now,
    });
  }

  return {
    state,
    orderId,
    entitlementId,
    installCodeId,
    createdEntitlement,
    createdInstallCode,
  };
}
