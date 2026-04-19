import { NextResponse } from "next/server";
import { z } from "zod";
import { getProducts } from "@/lib/products";

const querySchema = z.object({
  type: z.enum(["template", "component"]).optional(),
});

export function GET(request: Request) {
  const url = new URL(request.url);
  const parsed = querySchema.safeParse({ type: url.searchParams.get("type") ?? undefined });

  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid product query", issues: parsed.error.flatten() }, { status: 400 });
  }

  return NextResponse.json({ products: getProducts(parsed.data.type) });
}
