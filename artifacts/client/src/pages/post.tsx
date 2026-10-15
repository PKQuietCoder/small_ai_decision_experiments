import { useLayoutEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useRoute } from "wouter";
import { usePost, useSite } from "@/hooks/use-api";
import { format } from "date-fns";
import { Skeleton } from "@/components/ui/skeleton";
import { ExperimentAnalysis } from "@/components/charts/analysis-charts";
import { VerdictBadge } from "@/components/verdict-badge";
import { WIDGETS } from "@/components/widgets/registry";
import { Link } from "wouter";
import { ArrowLeft } from "lucide-react";
import authorPhoto from "@assets/PK Photo.jpg";

interface WidgetMount {
  node: HTMLElement;
  widget: string;
}

export default function Post() {
  const [match, params] = useRoute("/posts/:slug");
  const slug = params?.slug || "";

  const { data: post, isLoading, error } = usePost(slug);
  const { data: site } = useSite();
  const author = site?.author ?? "P.K. Mishra";

  // In-article widgets. A post marks a slot with `<div data-widget="name">…</div>`
  // whose children are a static fallback (a table + caption that also serve the
  // print/no-JS reading). After the body HTML lands, each registered slot is
  // emptied and a React widget is portalled into it, fed by the analysis JSON.
  // Unregistered names keep their fallback. Hooks sit above the early returns.
  const proseRef = useRef<HTMLDivElement>(null);
  const [mounts, setMounts] = useState<WidgetMount[]>([]);
  const bodyHtml = post?.bodyHtml;
  // Memoised so the prop object is stable: React re-assigns innerHTML whenever
  // the `dangerouslySetInnerHTML` object identity changes, which would wipe the
  // cleared slots (and detach the portals) on every re-render.
  const innerHtml = useMemo(() => ({ __html: bodyHtml ?? "" }), [bodyHtml]);
  useLayoutEffect(() => {
    const root = proseRef.current;
    if (!root || !bodyHtml) {
      setMounts([]);
      return;
    }
    const found: WidgetMount[] = [];
    root.querySelectorAll<HTMLElement>("[data-widget]").forEach((node) => {
      const widget = node.dataset.widget ?? "";
      if (!WIDGETS[widget]) return;
      node.replaceChildren();
      node.classList.add("not-prose");
      found.push({ node, widget });
    });
    setMounts(found);
  }, [bodyHtml]);

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-12 max-w-3xl">
        <Skeleton className="h-4 w-24 mb-8" />
        <Skeleton className="h-12 w-3/4 mb-6" />
        <Skeleton className="h-6 w-1/3 mb-12" />
        <div className="space-y-4">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="container mx-auto px-4 py-32 max-w-3xl text-center">
        <h1 className="text-4xl font-bold mb-4 font-serif">Post not found</h1>
        <p className="text-muted-foreground mb-8">The publication you're looking for doesn't exist or is currently unavailable.</p>
        <Link href="/" className="text-primary hover:underline inline-flex items-center gap-2">
          <ArrowLeft size={16} /> Return to feed
        </Link>
      </div>
    );
  }

  return (
    <article className="pb-24">
      {/* Header */}
      <header className="bg-muted/30 pt-16 pb-12 mb-12 border-b border-border/50">
        <div className="container mx-auto px-4 md:px-6 max-w-3xl animate-in fade-in slide-in-from-bottom-4 duration-700">
          <Link href="/" className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors mb-8 group">
            <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" /> 
            Back to publications
          </Link>
          
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs sm:text-sm text-muted-foreground font-mono mb-6">
            {post.type && (
              <>
                <span className="uppercase tracking-wider text-primary font-bold">{post.type}</span>
                <span aria-hidden="true">&middot;</span>
              </>
            )}
            <span className="uppercase tracking-wider text-primary font-bold">{post.category}</span>
            <span aria-hidden="true">&middot;</span>
            <time dateTime={post.date} className="whitespace-nowrap">
              {format(new Date(post.date), "MMMM d, yyyy")}
            </time>
            <span aria-hidden="true">&middot;</span>
            <span className="whitespace-nowrap">{post.readingMinutes} min read</span>
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight font-serif text-foreground leading-[1.1] mb-6">
            {post.title}
          </h1>
          
          <p className="text-xl text-muted-foreground leading-relaxed">
            {post.excerpt}
          </p>

          {post.verdict && (
            <div className="mt-6">
              <VerdictBadge verdict={post.verdict} />
            </div>
          )}

          <div className="mt-8 flex items-center gap-3 text-sm">
            <img
              src={authorPhoto}
              alt={author}
              className="h-10 w-10 shrink-0 rounded-none object-cover"
            />
            {site?.authorUrl ? (
              <a
                href={site.authorUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-foreground hover:underline"
              >
                {author}
              </a>
            ) : (
              <span className="font-medium text-foreground">{author}</span>
            )}
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="container mx-auto px-4 md:px-6 max-w-3xl animate-in fade-in duration-1000 delay-300 fill-mode-both">
        {/* Recognition / replication controls — the recurring rigor signal: a model
            might just recognize a famous experiment, so every entry states how that
            was ruled out (or, candidly, where it has not yet been). */}
        {post.controls && (
          <aside className="mb-12 border border-border bg-card p-5">
            <p className="eyebrow mb-2">Controls</p>
            <p className="font-serif text-base leading-relaxed text-muted-foreground">
              {post.controls}
            </p>
          </aside>
        )}

        <div
          ref={proseRef}
          className="prose prose-lg dark:prose-invert prose-headings:font-serif prose-h2:text-3xl prose-h3:text-2xl prose-p:leading-relaxed prose-a:text-primary prose-a:no-underline hover:prose-a:underline prose-pre:bg-muted prose-pre:text-foreground prose-pre:border prose-pre:border-border max-w-none"
          dangerouslySetInnerHTML={innerHtml}
        />
        {mounts.map(({ node, widget }) => {
          const Widget = WIDGETS[widget];
          return createPortal(
            <Widget data={post.analysis?.systemone ?? null} />,
            node,
            widget,
          );
        })}

        {/* Generic analysis chart below the content. A systemone_probe post
            renders its figures in-article via the widgets instead. */}
        {post.experimentId && !post.analysis?.systemone && (
          <ExperimentAnalysis analysis={post.analysis} />
        )}

        {/* Author footnote — the byline link lives here at the foot of the piece. */}
        <footer className="mt-16 border-t border-border pt-6 font-sans text-sm text-muted-foreground">
          Written by{" "}
          {site?.authorUrl ? (
            <a
              href={site.authorUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-foreground hover:underline"
            >
              {author}
            </a>
          ) : (
            <span className="font-medium text-foreground">{author}</span>
          )}
          .
        </footer>
      </div>
    </article>
  );
}
