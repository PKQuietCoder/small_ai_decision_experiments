import { useMemo, useState } from "react";
import { useSite, usePosts } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { PostCard } from "@/components/post-card";

const ALL = "All Articles";

export default function Home() {
  const { data: site, isLoading: siteLoading } = useSite();
  const { data: posts, isLoading: postsLoading } = usePosts();
  const [active, setActive] = useState(ALL);

  const categories = useMemo(() => {
    const seen = new Set<string>();
    for (const post of posts ?? []) {
      if (post.category) seen.add(post.category);
    }
    return [ALL, ...Array.from(seen)];
  }, [posts]);

  const visible = useMemo(() => {
    const list = (posts ?? []).filter(
      (post) => active === ALL || post.category === active,
    );
    return [...list].sort((a, b) => Number(b.featured) - Number(a.featured));
  }, [posts, active]);

  const author = site?.author ?? "The Lab";

  return (
    <div className="container mx-auto max-w-6xl px-4 py-12 md:px-6 md:py-16">
      {!siteLoading && site?.intro && (
        <section className="mb-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div className="rounded-none border border-border bg-card p-6 md:p-8">
            <h2 className="eyebrow mb-3">
              About
            </h2>
            <p className="max-w-3xl text-base leading-relaxed text-foreground/80 md:text-lg">
              {site.intro}
            </p>
          </div>
        </section>
      )}

      <section className="mb-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {siteLoading ? (
          <div className="space-y-4">
            <Skeleton className="h-10 w-2/3 max-w-md" />
            <Skeleton className="h-6 w-full max-w-2xl" />
          </div>
        ) : (
          <div className="space-y-4">
            <h1 className="font-serif text-4xl font-bold tracking-tight text-foreground md:text-5xl">
              {site?.title}
            </h1>
            <p className="max-w-3xl text-lg leading-relaxed text-muted-foreground md:text-xl">
              {site?.tagline}
            </p>
          </div>
        )}
      </section>

      {!postsLoading && categories.length > 1 && (
        <nav className="mb-10 flex flex-wrap gap-2 border-b border-border/60 pb-6">
          {categories.map((category) => {
            const isActive = active === category;
            return (
              <button
                key={category}
                type="button"
                onClick={() => setActive(category)}
                className={`rounded-none border px-4 py-1.5 text-xs font-semibold uppercase tracking-wider transition-colors ${
                  isActive
                    ? "border-foreground bg-foreground text-background"
                    : "border-border bg-transparent text-muted-foreground hover:border-foreground hover:text-foreground"
                }`}
              >
                {category}
              </button>
            );
          })}
        </nav>
      )}

      {postsLoading ? (
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded-none border border-border bg-card p-6">
              <div className="space-y-4">
                <Skeleton className="h-4 w-20" />
                <Skeleton className="h-7 w-3/4" />
                <Skeleton className="h-16 w-full" />
                <div className="flex items-center gap-3 pt-2">
                  <Skeleton className="h-9 w-9 rounded-none" />
                  <Skeleton className="h-8 w-32" />
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : visible.length === 0 ? (
        <div className="rounded-xl border border-dashed border-border bg-muted/20 py-16 text-center text-muted-foreground">
          <p>No publications found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {visible.map((post, i) => (
            <PostCard key={post.slug} post={post} author={author} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}
