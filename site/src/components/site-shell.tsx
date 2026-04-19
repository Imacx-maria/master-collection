"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { LinkButton } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const primaryNav = [
  { href: "/", label: "Catalog" },
  { href: "/templates", label: "Templates" },
  { href: "/components", label: "Components" },
  { href: "/creators/joseph-berry", label: "Creators" },
  { href: "/account", label: "Account" },
];

const tabNav = [
  { href: "/", label: "01 Public Catalog" },
  { href: "/templates/jb-studio-ldn", label: "02 Product Detail" },
  { href: "/creators/joseph-berry", label: "Creator Profile" },
  { href: "/sign-in", label: "03 Auth + Checkout" },
  { href: "/account/library", label: "04 Account + Library" },
];

export function SiteShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-svh bg-background text-foreground">
      <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur">
        <div className="mx-auto flex min-h-12 max-w-[1400px] items-center gap-3 px-6 sm:px-10 lg:px-14">
          <Link className="shrink-0 text-sm font-semibold" href="/">
            Master Collection
          </Link>
          <p className="hidden font-mono text-[11px] text-muted-foreground md:block">
            Catalog · Account · Install codes · Package access
          </p>
          <nav className="ml-auto hidden items-center gap-1 md:flex" aria-label="Primary navigation">
            {primaryNav.map((item) => (
              <Link
                className={cn(
                  "rounded-md px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
                  pathname === item.href && "bg-muted text-foreground",
                )}
                href={item.href}
                key={item.href}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <LinkButton href="/sign-in" size="sm" variant="outline">
            Sign in
          </LinkButton>
        </div>
        <div className="border-t border-border">
          <nav className="mx-auto flex max-w-[1400px] overflow-x-auto px-6 sm:px-10 lg:px-14" aria-label="Workflow navigation">
            {tabNav.map((item) => {
              const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);

              return (
                <Link
                  className={cn(
                    "shrink-0 border-b-2 border-transparent px-3 py-2 text-xs text-muted-foreground transition-colors hover:text-foreground",
                    active && "border-foreground text-foreground",
                  )}
                  href={item.href}
                  key={item.href}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>
      <main>{children}</main>
      <footer className="border-t border-border bg-zinc-100">
        <div className="mx-auto flex max-w-[1400px] flex-wrap items-center justify-between gap-4 px-6 py-8 text-sm text-muted-foreground sm:px-10 lg:px-14">
          <span>Master Collection</span>
          <span>Templates, components, install codes, package access.</span>
        </div>
      </footer>
    </div>
  );
}
