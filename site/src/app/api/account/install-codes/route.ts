import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { z } from "zod";
import { fixtureUserId, getLibraryItem } from "@/lib/account";

const clerkReady = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY && process.env.CLERK_SECRET_KEY);

const requestSchema = z.object({
  purchaseId: z.string().min(1),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = requestSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid install-code request", issues: parsed.error.flatten() }, { status: 400 });
  }

  const userId = clerkReady ? (await auth()).userId : fixtureUserId;

  if (!userId) {
    return NextResponse.json({ error: "Authentication required" }, { status: 401 });
  }

  const item = getLibraryItem(parsed.data.purchaseId, userId);

  if (!item?.installCode) {
    return NextResponse.json({ error: "Install code not available" }, { status: 404 });
  }

  return NextResponse.json({
    installCode: item.installCode,
    plainCode: item.installCode.mockPlainCode ?? null,
    mode: clerkReady ? "live" : "fixture",
  });
}
