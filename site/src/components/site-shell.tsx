"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { ThemeToggle } from "@/components/theme-toggle";
import { LinkButton } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const primaryNav = [
  { href: "/", label: "Catalog" },
  { href: "/templates", label: "Templates" },
  { href: "/components", label: "Components" },
  { href: "/account", label: "Account" },
];

const tabNav = [
  { href: "/", label: "01 Public Catalog" },
  { href: "/templates/atlas-studio", label: "02 Product Detail" },
  { href: "/sign-in", label: "03 Auth + Checkout" },
  { href: "/account/library", label: "04 Account + Library" },
];

export function SiteShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-svh bg-background">
      <header className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950 text-zinc-50">
        <div className="flex min-h-12 items-center gap-3 px-4 sm:px-6">
          <Link className="shrink-0 text-sm font-semibold" href="/">
            Master Collection
          </Link>
          <p className="hidden font-mono text-[11px] text-zinc-500 md:block">
            Catalog · Account · Install codes · Package access
          </p>
          <nav className="ml-auto hidden items-center gap-1 md:flex" aria-label="Primary navigation">
            {primaryNav.map((item) => (
              <Link
                className={cn(
                  "rounded-md px-3 py-1.5 text-xs text-zinc-400 transition-colors hover:bg-zinc-900 hover:text-zinc-50",
                  pathname === item.href && "bg-zinc-900 text-zinc-50",
                )}
                href={item.href}
                key={item.href}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <ThemeToggle />
          <LinkButton href="/sign-in" size="sm" variant="secondary">
            Sign in
          </LinkButton>
        </div>
        <div className="flex overflow-x-auto border-t border-zinc-800 px-4 sm:px-6" aria-label="Workflow navigation">
          {tabNav.map((item) => {
            const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);

            return (
              <Link
                className={cn(
                  "shrink-0 border-b-2 border-transparent px-3 py-2 text-xs text-zinc-500 transition-colors hover:text-zinc-50",
                  active && "border-zinc-50 text-zinc-50",
                )}
                href={item.href}
                key={item.href}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
