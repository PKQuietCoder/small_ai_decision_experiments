import { Link } from "wouter";
import { useSite, usePosts } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { format } from "date-fns";

export default function Home() {
  const { data: site, isLoading: siteLoading } = useSite();
  const { data: posts, isLoading: postsLoading } = usePosts();

  return (
    <div className="container mx-auto px-4 md:px-6 py-12 md:py-20 max-w-4xl">
      <section className="mb-20 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {siteLoading ? (
          <div className="space-y-4">
            <Skeleton className="h-12 w-3/4 max-w-md" />
            <Skeleton className="h-6 w-full max-w-2xl" />
            <Skeleton className="h-6 w-2/3 max-w-xl" />
          </div>
        ) : (
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground font-serif">
              {site?.title}
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground leading-relaxed max-w-3xl">
              {site?.tagline}
            </p>
          </div>
        )}
      </section>

      <section>
        <h2 className="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-8 border-b border-border/50 pb-4">
          Latest Publications
        </h2>
        
        {postsLoading ? (
          <div className="space-y-12">
            {[1, 2, 3].map((i) => (
              <div key={i} className="space-y-4">
                <Skeleton className="h-6 w-32" />
                <Skeleton className="h-8 w-3/4" />
                <Skeleton className="h-20 w-full" />
              </div>
            ))}
          </div>
        ) : !posts || posts.length === 0 ? (
          <div className="py-12 text-center text-muted-foreground bg-muted/20 rounded-xl border border-dashed border-border">
            <p>No publications found.</p>
          </div>
        ) : (
          <div className="space-y-16">
            {posts.map((post, i) => (
              <article 
                key={post.slug} 
                className="group relative animate-in fade-in slide-in-from-bottom-4 duration-700 fill-mode-both"
                style={{ animationDelay: `${(i + 1) * 150}ms` }}
              >
                <Link href={`/posts/${post.slug}`} className="absolute inset-0 z-10">
                  <span className="sr-only">Read {post.title}</span>
                </Link>
                
                <div className="space-y-4">
                  <div className="flex items-center gap-3 text-sm text-muted-foreground font-mono">
                    <time dateTime={post.date}>
                      {format(new Date(post.date), "MMMM d, yyyy")}
                    </time>
                    <span>&middot;</span>
                    <span>{post.readingMinutes} min read</span>
                    {post.featured && (
                      <>
                        <span>&middot;</span>
                        <Badge variant="secondary" className="bg-primary/10 text-primary hover:bg-primary/20 transition-colors">
                          Featured
                        </Badge>
                      </>
                    )}
                  </div>
                  
                  <h3 className="text-2xl md:text-3xl font-bold font-serif text-foreground group-hover:text-primary transition-colors duration-300">
                    {post.title}
                  </h3>
                  
                  <p className="text-lg text-muted-foreground leading-relaxed line-clamp-3">
                    {post.excerpt}
                  </p>
                  
                  <div className="flex items-center gap-2 pt-2">
                    {post.tags.map(tag => (
                      <span key={tag} className="text-xs font-medium text-muted-foreground bg-muted px-2.5 py-1 rounded-md">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
