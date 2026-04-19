import type { ReactNode } from "react";

export function PageHeading({
  eyebrow,
  title,
  description,
  actions,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
}) {
  return (
    <div className="mx-auto flex max-w-[1400px] flex-col gap-4 border-b border-border bg-background px-6 py-6 sm:px-10 lg:flex-row lg:items-end lg:justify-between lg:px-14">
      <div className="max-w-3xl">
        {eyebrow ? <p className="font-mono text-[11px] uppercase text-muted-foreground">{eyebrow}</p> : null}
        <h1 className="mt-1 text-2xl font-semibold">{title}</h1>
        {description ? <p className="mt-2 text-sm leading-6 text-muted-foreground">{description}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap gap-2">{actions}</div> : null}
    </div>
  );
}
