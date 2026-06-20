import { useSite } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";

export default function About() {
  const { data: site, isLoading } = useSite();

  return (
    <div className="container mx-auto px-4 md:px-6 py-12 md:py-20 max-w-3xl">
      <header className="mb-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground font-serif mb-6">
          About Borrowed Intuitions
        </h1>
      </header>

      {isLoading ? (
        <div className="space-y-6">
          <Skeleton className="h-6 w-full" />
          <Skeleton className="h-6 w-full" />
          <Skeleton className="h-6 w-5/6" />
          <div className="pt-8">
            <Skeleton className="h-4 w-32 mb-4" />
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-6 w-4/5" />
          </div>
        </div>
      ) : site ? (
        <div className="animate-in fade-in duration-1000 delay-200 fill-mode-both prose prose-lg dark:prose-invert prose-headings:font-serif prose-p:leading-relaxed max-w-none text-muted-foreground">
          <p className="text-xl text-foreground font-medium mb-8">
            {site.description}
          </p>
          
          <div 
            dangerouslySetInnerHTML={{ __html: site.aboutHtml ?? "" }} 
          />

          <hr className="my-12 border-border" />
          
          <div>
            <h3 className="text-foreground font-serif">Methodology Notes</h3>
            <p>
              All data published here is drawn from actual API calls to production model endpoints. 
              We do not rely on simulated or hand-picked examples. The exact prompts, temperatures, and seeds 
              (where applicable) are recorded for every trial. Statistical significance is computed 
              using standard decision science techniques (e.g., Chi-Square for categorical shifts, 
              ANOVA for broader interactions) with α = 0.05.
            </p>
          </div>
        </div>
      ) : (
        <div className="py-12 text-center text-muted-foreground">
          <p>Information unavailable.</p>
        </div>
      )}
    </div>
  );
}
