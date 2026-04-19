import { NextResponse } from "next/server";
import Stripe from "stripe";
import { entitlements, installCodes, orders } from "@/lib/account";
import { fulfillCheckoutSession } from "@/lib/fulfillment";
import { getProductById } from "@/lib/products";

export async function POST(request: Request) {
  if (!process.env.STRIPE_SECRET_KEY || !process.env.STRIPE_WEBHOOK_SECRET) {
    return NextResponse.json(
      { error: "Stripe credentials are required before webhook fulfillment can run" },
      { status: 503 },
    );
  }

  const signature = request.headers.get("stripe-signature");

  if (!signature) {
    return NextResponse.json({ error: "Missing Stripe signature" }, { status: 400 });
  }

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  const body = await request.text();
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : "Invalid webhook signature" }, { status: 400 });
  }

  if (event.type !== "checkout.session.completed" && event.type !== "checkout.session.async_payment_succeeded") {
    return NextResponse.json({ received: true, ignored: event.type });
  }

  const session = event.data.object as Stripe.Checkout.Session;
  const metadata = session.metadata ?? {};
  const product = metadata.productId ? getProductById(metadata.productId) : undefined;

  if (!metadata.userId || !metadata.productId || !metadata.productVersionId || !metadata.orderId || !product) {
    return NextResponse.json({ error: "Checkout session metadata is incomplete" }, { status: 400 });
  }

  const result = fulfillCheckoutSession(
    { orders, entitlements, installCodes },
    {
      userId: metadata.userId,
      productId: metadata.productId,
      productVersionId: metadata.productVersionId,
      orderId: metadata.orderId,
      providerSessionId: session.id,
      providerPaymentId: typeof session.payment_intent === "string" ? session.payment_intent : undefined,
      amountCents: session.amount_total ?? product.priceCents,
      currency: (session.currency ?? product.currency).toUpperCase(),
      now: new Date().toISOString(),
      plainInstallCode: `MC-${product.slug.toUpperCase()}-${metadata.orderId.slice(-6)}`,
    },
  );

  return NextResponse.json({
    received: true,
    orderId: result.orderId,
    entitlementId: result.entitlementId,
    installCodeId: result.installCodeId,
    createdEntitlement: result.createdEntitlement,
    createdInstallCode: result.createdInstallCode,
  });
}
