import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { fixtureUserId, getLibraryItem } from "@/lib/account";

const clerkReady = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY && process.env.CLERK_SECRET_KEY);

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ purchaseId: string }> },
) {
  const { purchaseId } = await params;
  const userId = clerkReady ? (await auth()).userId : fixtureUserId;

  if (!userId) {
    return NextResponse.json({ error: "Authentication required" }, { status: 401 });
  }

  const item = getLibraryItem(purchaseId, userId);

  if (!item) {
    return NextResponse.json({ error: "Library item not found" }, { status: 404 });
  }

  return NextResponse.json({ item, mode: clerkReady ? "live" : "fixture" });
}
