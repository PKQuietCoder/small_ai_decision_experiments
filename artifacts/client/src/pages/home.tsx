import { useMemo, useState } from "react";
import { useSite, usePosts } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { PostCard } from "@/components/post-card";
import authorPhoto from "@assets/PK Photo.jpg";

const ALL = "All Articles";

export default function Home() {
  const { data: site, isLoading: siteLoading } = useSite();
  const { data: posts, isLoading: postsLoading } = usePosts();
  const [active, setActive] = useState(ALL);

  const categories = useMemo(() => {
    if (site?.categories?.length) return [ALL, ...site.categories];
    const seen = new Set<string>();
    for (const post of posts ?? []) {
      if (post.category) seen.add(post.category);
    }
    return [ALL, ...Array.from(seen)];
  }, [site, posts]);

  const visible = useMemo(() => {
    const list = (posts ?? []).filter(
      (post) => active === ALL || post.category === active,
    );
    return [...list].sort(
      (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
    );
  }, [posts, active]);

  const author = site?.author ?? "The Lab";
  const authorUrl = site?.authorUrl;

  return (
    <div className="container mx-auto max-w-6xl px-4 py-12 md:px-6 md:py-16">
      <section className="mb-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {siteLoading ? (
          <div className="space-y-4">
            <Skeleton className="h-10 w-2/3 max-w-md" />
            <Skeleton className="h-6 w-full max-w-2xl" />
          </div>
        ) : (
          <div className="flex flex-col gap-8 sm:flex-row sm:items-stretch sm:justify-between">
            <div className="space-y-4">
              <h1 className="font-serif text-4xl font-bold tracking-tight text-foreground md:text-5xl">
                {site?.title}
              </h1>
              <p className="max-w-3xl text-lg leading-relaxed text-muted-foreground md:text-xl">
                {site?.tagline}
              </p>
            </div>
            <div className="flex shrink-0 flex-col items-center gap-2 sm:justify-between">
              <img
                src={authorPhoto}
                alt={author}
                className="h-20 w-20 shrink-0 rounded-none object-cover"
              />
              <div>
                {authorUrl ? (
                  <a
                    href={authorUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="font-medium text-foreground underline decoration-border underline-offset-4 transition-colors hover:decoration-foreground"
                  >
                    {author}
                  </a>
                ) : (
                  <span className="font-medium text-foreground">{author}</span>
                )}
              </div>
            </div>
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
        <div className="flex flex-col gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded-none border border-border bg-card p-6">
              <div className="space-y-4">
                <Skeleton className="h-4 w-20" />
                <Skeleton className="h-7 w-3/4" />
                <Skeleton className="h-16 w-full" />
                <Skeleton className="h-4 w-32" />
              </div>
            </div>
          ))}
        </div>
      ) : visible.length === 0 ? (
        <div className="rounded-none border border-dashed border-border bg-muted/20 py-16 text-center text-muted-foreground">
          <p>No publications found.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-6">
          {visible.map((post, i) => (
            <PostCard key={post.slug} post={post} author={author} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}
