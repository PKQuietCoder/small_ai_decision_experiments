import { Link } from "wouter";
import { format } from "date-fns";
import type { PostSummary } from "@/lib/api";
import { VerdictBadge } from "@/components/verdict-badge";

function safeDate(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : format(parsed, "MMM d, yyyy");
}

interface PostCardProps {
  post: PostSummary;
  author: string;
  index?: number;
}

// Editorial list item (Nature PoV): flat cream surface, hairline rule, sharp corners,
// no shadow. Each entry is a full-width box of uniform height; hierarchy comes from
// type and whitespace, not decoration. The author photo lives once in the page header,
// so it is intentionally omitted here — only the byline name and date remain.
export function PostCard({ post, author, index = 0 }: PostCardProps) {
  return (
    <article
      className="group relative flex min-h-44 flex-col border border-border bg-card p-6 transition-colors duration-200 hover:border-foreground animate-in fade-in slide-in-from-bottom-4 fill-mode-both md:flex-row md:items-start md:gap-8"
      style={{ animationDelay: `${index * 90}ms` }}
    >
      <Link href={`/posts/${post.slug}`} className="absolute inset-0 z-10">
        <span className="sr-only">Read {post.title}</span>
      </Link>

      <div className="flex-1">
        <div className="flex items-center gap-2">
          {post.type && <span className="eyebrow">{post.type}</span>}
          {post.type && post.category && (
            <span className="text-muted-foreground" aria-hidden="true">·</span>
          )}
          <span className="eyebrow">{post.category || "Article"}</span>
        </div>

        <h3 className="mt-3 font-serif text-xl font-semibold leading-snug text-foreground">
          {post.title}
        </h3>

        <p className="mt-3 line-clamp-3 font-serif text-base leading-relaxed text-muted-foreground">
          {post.excerpt}
        </p>
      </div>

      <div className="mt-6 flex shrink-0 items-center gap-3 text-sm md:mt-0 md:w-44 md:flex-col md:items-end md:gap-4 md:text-right">
        {post.verdict && <VerdictBadge verdict={post.verdict} compact />}
        <div className="leading-tight md:mt-auto">
          <div className="font-medium text-foreground">{author}</div>
          <time className="font-mono text-xs text-muted-foreground" dateTime={post.date}>
            {safeDate(post.date)}
          </time>
        </div>
      </div>
    </article>
  );
}
