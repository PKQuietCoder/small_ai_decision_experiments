import { Link } from "wouter";
import { format } from "date-fns";
import type { PostSummary } from "@/lib/api";
import authorPhoto from "@assets/PK Photo.jpg";

function safeDate(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : format(parsed, "MMM d, yyyy");
}

interface PostCardProps {
  post: PostSummary;
  author: string;
  authorUrl?: string;
  index?: number;
}

// Editorial card (Nature PoV): flat cream surface, hairline rule, sharp corners,
// no shadow. Hierarchy comes from type and whitespace, not decoration.
export function PostCard({ post, author, authorUrl, index = 0 }: PostCardProps) {
  return (
    <article
      className="group relative flex flex-col border border-border bg-card p-6 transition-colors duration-200 hover:border-foreground animate-in fade-in slide-in-from-bottom-4 fill-mode-both"
      style={{ animationDelay: `${index * 90}ms` }}
    >
      <Link href={`/posts/${post.slug}`} className="absolute inset-0 z-10">
        <span className="sr-only">Read {post.title}</span>
      </Link>

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

      <div className="mt-auto flex items-center gap-3 pt-6 text-sm">
        <img
          src={authorPhoto}
          alt={author}
          className="h-9 w-9 shrink-0 rounded-none object-cover"
        />
        <div className="leading-tight">
          {authorUrl ? (
            <a
              href={authorUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="relative z-20 font-medium text-foreground hover:underline"
            >
              {author}
            </a>
          ) : (
            <div className="font-medium text-foreground">{author}</div>
          )}
          <time className="font-mono text-xs text-muted-foreground" dateTime={post.date}>
            {safeDate(post.date)}
          </time>
        </div>
      </div>
    </article>
  );
}
