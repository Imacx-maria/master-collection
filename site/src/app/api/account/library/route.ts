import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { fixtureUserId, getLibraryItems } from "@/lib/account";

const clerkReady = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY && process.env.CLERK_SECRET_KEY);

export async function GET() {
  const userId = clerkReady ? (await auth()).userId : fixtureUserId;

  if (!userId) {
    return NextResponse.json({ error: "Authentication required" }, { status: 401 });
  }

  return NextResponse.json({ items: getLibraryItems(userId), mode: clerkReady ? "live" : "fixture" });
}
