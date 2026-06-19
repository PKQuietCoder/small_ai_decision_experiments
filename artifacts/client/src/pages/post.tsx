import { useRoute } from "wouter";
import { usePost, useSite } from "@/hooks/use-api";
import { format } from "date-fns";
import { Skeleton } from "@/components/ui/skeleton";
import { ExperimentAnalysis } from "@/components/charts/analysis-charts";
import { Link } from "wouter";
import { ArrowLeft } from "lucide-react";
import authorPhoto from "@assets/PK Photo.jpg";

export default function Post() {
  const [match, params] = useRoute("/posts/:slug");
  const slug = params?.slug || "";

  const { data: post, isLoading, error } = usePost(slug);
  const { data: site } = useSite();
  const author = site?.author ?? "P.K. Mishra";

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
          
          <div className="flex items-center gap-3 text-sm text-muted-foreground font-mono mb-6">
            {post.type && (
              <>
                <span className="uppercase tracking-wider text-primary font-bold">{post.type}</span>
                <span>&middot;</span>
              </>
            )}
            <span className="uppercase tracking-wider text-primary font-bold">{post.category}</span>
            <span>&middot;</span>
            <time dateTime={post.date}>
              {format(new Date(post.date), "MMMM d, yyyy")}
            </time>
            <span>&middot;</span>
            <span>{post.readingMinutes} min read</span>
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight font-serif text-foreground leading-[1.1] mb-6">
            {post.title}
          </h1>
          
          <p className="text-xl text-muted-foreground leading-relaxed">
            {post.excerpt}
          </p>

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
        <div 
          className="prose prose-lg dark:prose-invert prose-headings:font-serif prose-h2:text-3xl prose-h3:text-2xl prose-p:leading-relaxed prose-a:text-primary prose-a:no-underline hover:prose-a:underline prose-pre:bg-muted prose-pre:text-foreground prose-pre:border prose-pre:border-border max-w-none"
          dangerouslySetInnerHTML={{ __html: post.bodyHtml }}
        />
        
        {/* Analysis Charts injected below the content */}
        {post.experimentId && (
          <ExperimentAnalysis analysis={post.analysis} />
        )}
      </div>
    </article>
  );
}
