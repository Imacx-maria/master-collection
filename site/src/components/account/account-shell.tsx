import Link from "next/link";
import type { ReactNode } from "react";

const accountNav = [
  { href: "/account", label: "Dashboard" },
  { href: "/account/library", label: "Library" },
  { href: "/account/installations", label: "Installations" },
  { href: "/account/billing", label: "Billing" },
];

export function AccountShell({ children }: { children: ReactNode }) {
  return (
    <div className="grid gap-0 lg:grid-cols-[220px_minmax(0,1fr)]">
      <aside className="border-b border-border bg-muted/30 p-4 lg:min-h-[calc(100svh-89px)] lg:border-b-0 lg:border-r">
        <p className="font-mono text-[11px] uppercase text-muted-foreground">Account</p>
        <nav className="mt-4 flex gap-2 overflow-x-auto lg:flex-col" aria-label="Account navigation">
          {accountNav.map((item) => (
            <Link
              className="shrink-0 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-foreground"
              href={item.href}
              key={item.href}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
