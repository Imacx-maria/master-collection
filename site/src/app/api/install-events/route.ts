import { NextResponse } from "next/server";
import { z } from "zod";

const requestSchema = z.object({
  installCodeId: z.string().min(1),
  packageId: z.string().min(1),
  status: z.enum(["created", "redeemed_in_app", "assets_uploaded", "payload_copied", "installed", "failed"]),
  webflowSiteId: z.string().optional(),
  webflowSiteName: z.string().optional(),
  webflowPageId: z.string().optional(),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = requestSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid install event", issues: parsed.error.flatten() }, { status: 400 });
  }

  return NextResponse.json({
    accepted: true,
    event: {
      ...parsed.data,
      receivedAt: new Date().toISOString(),
    },
  });
}
