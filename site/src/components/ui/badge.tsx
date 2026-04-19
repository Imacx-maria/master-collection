import type { ComponentPropsWithoutRef } from "react";
import { cn } from "@/lib/utils";

type BadgeProps = ComponentPropsWithoutRef<"span"> & {
  variant?: "default" | "muted" | "outline" | "success" | "warning";
};

const variants = {
  default: "border-transparent bg-foreground text-background",
  muted: "border-transparent bg-muted text-muted-foreground",
  outline: "border-border bg-background text-foreground",
  success: "border-border bg-background text-foreground",
  warning: "border-border bg-background text-foreground",
};

export function Badge({ className, variant = "muted", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex h-6 items-center rounded-md border px-2 font-mono text-[11px] leading-none",
        variants[variant],
        className,
      )}
      {...props}
    />
  );
}
