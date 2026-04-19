# Master Collection Site

Master Collection website/platform built with Next.js App Router, TypeScript, Tailwind v4, shadcn/ui, Clerk-ready auth boundaries, Stripe-ready checkout boundaries, and fixture-backed product/package data for local development.

## Getting Started

Use Bun from this folder:

```bash
bun install
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Checks

```bash
bun run typecheck
bun run lint
bun run test
bun run build
```

## Vercel

Configure the Vercel project with:

```text
Root Directory: site
Install Command: bun install
Build Command: bun run build
Output Directory: default
```

No environment variables are required for the fixture MVP. Live Clerk and Stripe credentials are needed later when switching from fixtures to real auth and payments.
