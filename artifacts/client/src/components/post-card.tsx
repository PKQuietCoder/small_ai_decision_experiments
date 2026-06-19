import { Link } from "wouter";
import { format } from "date-fns";
import type { PostSummary } from "@/lib/api";

function getInitials(name: string): string {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase();
}

function safeDate(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : format(parsed, "MMM d, yyyy");
}

interface PostCardProps {
  post: PostSummary;
  author: string;
  index?: number;
}

// Editorial card (Nature PoV): flat cream surface, hairline rule, sharp corners,
// no shadow. Hierarchy comes from type and whitespace, not decoration.
export function PostCard({ post, author, index = 0 }: PostCardProps) {
  return (
    <article
      className="group relative flex flex-col border border-border bg-card p-6 transition-colors duration-200 hover:border-foreground animate-in fade-in slide-in-from-bottom-4 fill-mode-both"
      style={{ animationDelay: `${index * 90}ms` }}
    >
      <Link href={`/posts/${post.slug}`} className="absolute inset-0 z-10">
        <span className="sr-only">Read {post.title}</span>
      </Link>

      <div className="flex items-center gap-2">
        <span className="eyebrow">{post.category || "Article"}</span>
        {post.featured && (
          <>
            <span className="text-muted-foreground" aria-hidden="true">·</span>
            <span className="eyebrow text-foreground">Featured</span>
          </>
        )}
      </div>

      <h3 className="mt-3 font-serif text-xl font-semibold leading-snug text-foreground">
        {post.title}
      </h3>

      <p className="mt-3 line-clamp-3 font-serif text-base leading-relaxed text-muted-foreground">
        {post.excerpt}
      </p>

      <div className="mt-auto flex items-center gap-3 pt-6 text-sm">
        <span
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-none bg-secondary text-xs font-semibold text-foreground"
          aria-hidden="true"
        >
          {getInitials(author)}
        </span>
        <div className="leading-tight">
          <div className="font-medium text-foreground">{author}</div>
          <time className="font-mono text-xs text-muted-foreground" dateTime={post.date}>
            {safeDate(post.date)}
          </time>
        </div>
      </div>
    </article>
  );
}
