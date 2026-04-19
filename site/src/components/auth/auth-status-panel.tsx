import { SignIn, SignUp } from "@clerk/nextjs";
import { Badge } from "@/components/ui/badge";

const clerkReady = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY);

export function AuthStatusPanel({ mode }: { mode: "sign-in" | "sign-up" }) {
  if (clerkReady) {
    return mode === "sign-in" ? (
      <SignIn routing="path" path="/sign-in" signUpUrl="/sign-up" />
    ) : (
      <SignUp routing="path" path="/sign-up" signInUrl="/sign-in" />
    );
  }

  return (
    <div className="rounded-md border border-border bg-card p-5">
      <Badge variant="outline">local development</Badge>
      <h2 className="mt-4 text-xl font-semibold">Clerk is not configured yet</h2>
      <p className="mt-2 text-sm leading-6 text-muted-foreground">
        Add Clerk keys to `.env.local` to enable live sign-in. Public catalog, mock account pages, and API
        boundaries remain buildable without secrets.
      </p>
      <dl className="mt-4 grid gap-2 text-sm">
        <div className="flex justify-between gap-3">
          <dt className="text-muted-foreground">Publishable key</dt>
          <dd className="font-mono">NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY</dd>
        </div>
        <div className="flex justify-between gap-3">
          <dt className="text-muted-foreground">Secret key</dt>
          <dd className="font-mono">CLERK_SECRET_KEY</dd>
        </div>
      </dl>
    </div>
  );
}
