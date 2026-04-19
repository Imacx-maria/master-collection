import { describe, expect, it } from "vitest";
import { fulfillCheckoutSession, type FulfillmentState } from "@/lib/fulfillment";

const input = {
  userId: "user_123",
  productId: "prod-atlas-studio",
  productVersionId: "ver-atlas-studio-1",
  orderId: "order_123",
  providerSessionId: "cs_test_123",
  amountCents: 14900,
  currency: "USD",
  now: "2026-04-19T12:00:00.000Z",
  plainInstallCode: "MC-TEST-123",
};

describe("fulfillCheckoutSession", () => {
  it("creates order, entitlement, and install code for a paid checkout", () => {
    const state: FulfillmentState = { orders: [], entitlements: [], installCodes: [] };
    const result = fulfillCheckoutSession(state, input);

    expect(result.createdEntitlement).toBe(true);
    expect(result.createdInstallCode).toBe(true);
    expect(result.state.orders).toHaveLength(1);
    expect(result.state.entitlements).toHaveLength(1);
    expect(result.state.installCodes).toHaveLength(1);
    expect(result.state.installCodes[0].codeHash).not.toContain(input.plainInstallCode);
  });

  it("is idempotent for repeated webhook calls with the same checkout session", () => {
    const first = fulfillCheckoutSession({ orders: [], entitlements: [], installCodes: [] }, input);
    const second = fulfillCheckoutSession(first.state, input);

    expect(second.createdEntitlement).toBe(false);
    expect(second.createdInstallCode).toBe(false);
    expect(second.state.orders).toHaveLength(1);
    expect(second.state.entitlements).toHaveLength(1);
    expect(second.state.installCodes).toHaveLength(1);
  });
});
