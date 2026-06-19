import { Link } from "wouter";
import { format } from "date-fns";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import type { PostSummary } from "@/lib/api";

const GRADIENTS = [
  "from-indigo-500 via-blue-500 to-cyan-400",
  "from-emerald-400 via-teal-500 to-cyan-500",
  "from-violet-500 via-purple-500 to-fuchsia-400",
  "from-amber-400 via-orange-400 to-rose-400",
  "from-rose-400 via-pink-400 to-purple-400",
];

function hashString(value: string): number {
  let hash = 0;
  for (let i = 0; i < value.length; i++) {
    hash = (hash * 31 + value.charCodeAt(i)) >>> 0;
  }
  return hash;
}

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
  return Number.isNaN(parsed.getTime()) ? value : format(parsed, "EEE MMM d yyyy");
}

interface PostCardProps {
  post: PostSummary;
  author: string;
  index?: number;
}

export function PostCard({ post, author, index = 0 }: PostCardProps) {
  const gradient = post.featured
    ? "from-slate-100 via-indigo-100 to-sky-200"
    : GRADIENTS[hashString(post.category || post.slug) % GRADIENTS.length];
  const coverDark = !post.featured;

  return (
    <article
      className="group relative flex flex-col overflow-hidden rounded-2xl border border-card-border bg-card shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl animate-in fade-in slide-in-from-bottom-4 fill-mode-both"
      style={{ animationDelay: `${index * 90}ms` }}
    >
      <Link href={`/posts/${post.slug}`} className="absolute inset-0 z-10">
        <span className="sr-only">Read {post.title}</span>
      </Link>

      <div className={`relative aspect-[16/10] overflow-hidden bg-gradient-to-br ${gradient}`}>
        <div
          className={`absolute inset-0 ${coverDark ? "text-white/30" : "text-primary/20"}`}
          style={{
            backgroundImage:
              "radial-gradient(currentColor 1px, transparent 1px)",
            backgroundSize: "18px 18px",
            opacity: 0.5,
          }}
        />
        <div className="absolute inset-0 flex items-end p-5">
          <span
            className={`font-serif text-2xl font-bold uppercase tracking-tight leading-none ${
              coverDark ? "text-white/90" : "text-primary/70"
            }`}
          >
            {post.category || "Article"}
          </span>
        </div>
      </div>

      <div className="flex flex-1 flex-col gap-4 p-6">
        <div className="flex flex-wrap items-center gap-2">
          {post.featured ? (
            <span className="rounded-md bg-primary/10 px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-primary">
              Featured
            </span>
          ) : (
            <span className="rounded-md bg-muted px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
              {post.category}
            </span>
          )}
        </div>

        <h3 className="font-serif text-xl font-bold leading-snug text-foreground transition-colors duration-300 group-hover:text-primary">
          {post.title}
        </h3>

        <div className="flex items-center gap-3">
          <Avatar className="h-9 w-9 border border-border">
            <AvatarFallback className="bg-primary/10 text-xs font-semibold text-primary">
              {getInitials(author)}
            </AvatarFallback>
          </Avatar>
          <div className="text-sm leading-tight">
            <div className="font-semibold text-foreground">{author}</div>
            <time className="font-mono text-xs text-muted-foreground" dateTime={post.date}>
              {safeDate(post.date)}
            </time>
          </div>
        </div>

        <p className="line-clamp-3 text-sm leading-relaxed text-muted-foreground">
          {post.excerpt}
        </p>
      </div>
    </article>
  );
}
