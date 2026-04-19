import { Award, ExternalLink, Globe2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { formatMoney } from "@/lib/format";
import type { Creator } from "@/lib/creators";
import type { ProductWithVersion } from "@/lib/products";

export function CreatorProfile({
  creator,
  products,
}: {
  creator: Creator;
  products: ProductWithVersion[];
}) {
  const featured = products[0];

  return (
    <article className="bg-background pb-16 text-foreground">
      <section className="border-b border-border">
        <div className="mx-auto grid max-w-[1400px] gap-8 px-6 py-12 sm:px-10 lg:grid-cols-[112px_1fr_auto] lg:px-14">
          <div className="flex size-28 items-center justify-center rounded-full border border-border bg-muted text-xl font-semibold">
            {creator.initials}
          </div>
          <div className="grid gap-4">
            <div>
              <h1 className="text-4xl font-semibold tracking-normal">{creator.name}</h1>
              <p className="mt-2 text-base text-muted-foreground">
                {creator.title} . {creator.location}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {creator.badges.map((badge) => (
                <Badge key={badge} variant="outline">
                  {badge}
                </Badge>
              ))}
            </div>
            <div className="flex flex-wrap gap-3">
              <LinkButton href="#templates" variant="outline">
                View templates
              </LinkButton>
              <LinkButton href={creator.websiteUrl} variant="ghost">
                {creator.websiteLabel}
                <ExternalLink aria-hidden="true" className="size-3" />
              </LinkButton>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:min-w-[240px]">
            {creator.stats.map((stat) => (
              <div className="rounded-md border border-border bg-muted/50 p-4 text-center" key={stat.label}>
                <strong className="block text-2xl font-semibold">{stat.value}</strong>
                <span className="mt-1 block text-xs text-muted-foreground">{stat.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="mx-auto grid max-w-[1400px] gap-10 px-6 py-10 sm:px-10 lg:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)] lg:px-14">
          <div>
            <h2 className="text-xl font-semibold">About {creator.shortName}</h2>
            <div className="mt-5 grid gap-4 text-base leading-8 text-muted-foreground">
              {creator.bio.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
          </div>
          <div className="grid gap-6">
            <div>
              <h2 className="text-sm font-semibold">What I do</h2>
              <div className="mt-3 flex flex-wrap gap-2">
                {creator.skills.map((skill) => (
                  <Badge key={skill}>{skill}</Badge>
                ))}
              </div>
            </div>
            <div className="border-t border-border pt-6">
              <h2 className="text-sm font-semibold">Selected clients</h2>
              <p className="mt-3 text-sm leading-7 text-muted-foreground">{creator.clients.join(" . ")}</p>
            </div>
            <div className="border-t border-border pt-6">
              <h2 className="text-sm font-semibold">Short CV</h2>
              <div className="mt-3 grid gap-3">
                {creator.roles.map((role) => (
                  <div className="flex gap-3" key={`${role.title}-${role.company}`}>
                    <span className="mt-2 size-1.5 rounded-full bg-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">{role.title}</p>
                      <p className="text-sm text-muted-foreground">{role.company}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="border-b border-border bg-muted/40">
        <div className="mx-auto max-w-[1400px] px-6 py-10 sm:px-10 lg:px-14">
          <h2 className="text-xl font-semibold">Known for</h2>
          <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {creator.knownFor.map((item) => (
              <div className="flex gap-3 rounded-md border border-border bg-background p-4" key={item}>
                <Award aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
                <p className="text-sm leading-6">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-b border-border" id="templates">
        <div className="mx-auto max-w-[1400px] px-6 py-10 sm:px-10 lg:px-14">
          <div className="mb-6 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold">Templates by {creator.name}</h2>
              <p className="mt-1 text-sm text-muted-foreground">{products.length} published templates</p>
            </div>
            <Badge variant="outline">{products.length} templates</Badge>
          </div>
          <div className="grid auto-rows-fr gap-4 md:grid-cols-2 xl:grid-cols-4">
            {products.map((product) => (
              <article
                className="flex h-full flex-col overflow-hidden rounded-md border border-border bg-background"
                key={product.id}
              >
                <div className="relative flex aspect-square items-center justify-center bg-muted text-xs text-muted-foreground">
                  {featured?.id === product.id ? (
                    <div className="absolute inset-x-0 top-0 bg-foreground px-3 py-1.5 text-center font-mono text-[11px] uppercase text-background">
                      Featured
                    </div>
                  ) : null}
                  Preview
                </div>
                <div className="flex flex-1 flex-col p-4">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-sm font-semibold">{product.title}</h3>
                    <span className="text-sm font-semibold">{formatMoney(product.priceCents, product.currency)}</span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {product.tags.slice(0, 2).map((tag) => (
                      <Badge key={tag}>{tag}</Badge>
                    ))}
                  </div>
                  <LinkButton className="mt-auto w-full" href={`/templates/${product.slug}`} size="sm" variant="outline">
                    View
                  </LinkButton>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-muted/60">
        <div className="mx-auto flex max-w-[1400px] flex-wrap items-center justify-between gap-5 px-6 py-8 sm:px-10 lg:px-14">
          <div>
            <h2 className="text-xl font-semibold">Work with templates by {creator.shortName}.</h2>
            <p className="mt-1 text-sm text-muted-foreground">Start with the featured build, then branch into the creator library.</p>
          </div>
          {featured ? (
            <LinkButton href={`/templates/${featured.slug}`}>
              View featured template
              <Globe2 aria-hidden="true" className="size-3" />
            </LinkButton>
          ) : null}
        </div>
      </section>
    </article>
  );
}
