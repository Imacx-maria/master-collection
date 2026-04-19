import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import Stripe from "stripe";
import { z } from "zod";
import { getProductById, getProductBySlug } from "@/lib/products";

const requestSchema = z.object({
  productId: z.string().optional(),
  slug: z.string().optional(),
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = requestSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid checkout request", issues: parsed.error.flatten() }, { status: 400 });
  }

  if (!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY || !process.env.CLERK_SECRET_KEY) {
    return NextResponse.json({ error: "Clerk credentials are required before checkout can start" }, { status: 503 });
  }

  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: "Authentication required" }, { status: 401 });
  }

  if (!process.env.STRIPE_SECRET_KEY) {
    return NextResponse.json({ error: "Stripe secret key is required before checkout can start" }, { status: 503 });
  }

  const product = parsed.data.productId
    ? getProductById(parsed.data.productId)
    : parsed.data.slug
      ? getProductBySlug(parsed.data.slug)
      : undefined;

  if (!product?.currentVersion) {
    return NextResponse.json({ error: "Product or current version not found" }, { status: 404 });
  }

  const orderId = `order_${crypto.randomUUID()}`;
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    success_url: `${siteUrl}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${siteUrl}/${product.type === "template" ? "templates" : "components"}/${product.slug}`,
    client_reference_id: orderId,
    metadata: {
      userId,
      productId: product.id,
      productVersionId: product.currentVersion.id,
      orderId,
    },
    line_items: [
      product.stripePriceId
        ? {
            price: product.stripePriceId,
            quantity: 1,
          }
        : {
            price_data: {
              currency: product.currency.toLowerCase(),
              product_data: {
                name: product.title,
                description: product.summary,
              },
              unit_amount: product.priceCents,
            },
            quantity: 1,
          },
    ],
  });

  return NextResponse.json({ checkoutUrl: session.url, orderId });
}
