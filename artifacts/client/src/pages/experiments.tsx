import { useExperiments } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Link } from "wouter";
import { format } from "date-fns";

export default function Experiments() {
  const { data: experiments, isLoading } = useExperiments();

  return (
    <div className="container mx-auto px-4 md:px-6 py-12 md:py-20 max-w-5xl">
      <header className="mb-16 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground font-serif mb-6">
          Experiment Index
        </h1>
        <p className="text-xl text-muted-foreground leading-relaxed max-w-3xl">
          A comprehensive registry of all controlled trials conducted by the lab, detailing models tested, sample sizes, and empirical findings.
        </p>
      </header>

      {isLoading ? (
        <div className="grid gap-6">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48 w-full rounded-xl" />
          ))}
        </div>
      ) : !experiments || experiments.length === 0 ? (
        <div className="py-24 text-center text-muted-foreground bg-muted/20 rounded-xl border border-dashed border-border">
          <p>No experiments registered yet.</p>
        </div>
      ) : (
        <div className="grid gap-6 animate-in fade-in duration-1000 delay-200 fill-mode-both">
          {experiments.map((exp) => (
            <Card key={exp.id} className="overflow-hidden group hover:border-primary/50 transition-colors">
              <div className="flex flex-col md:flex-row">
                <div className="flex-1 p-6 md:p-8">
                  <div className="flex items-center gap-3 mb-4">
                    <Badge variant={exp.status === "published" ? "default" : "secondary"}>
                      {exp.status.charAt(0).toUpperCase() + exp.status.slice(1)}
                    </Badge>
                    <span className="text-xs font-mono text-muted-foreground">ID: {exp.id}</span>
                  </div>
                  
                  <h3 className="text-2xl font-bold font-serif text-foreground mb-3">
                    {exp.title}
                  </h3>
                  
                  <p className="text-muted-foreground mb-6">
                    {exp.summary}
                  </p>
                  
                  <div className="flex flex-wrap gap-4 text-sm">
                    <div className="flex flex-col">
                      <span className="text-muted-foreground text-xs uppercase tracking-wider font-semibold mb-1">Models</span>
                      <span className="font-medium">{exp.models.join(", ")}</span>
                    </div>
                    <div className="w-px h-8 bg-border hidden md:block"></div>
                    <div className="flex flex-col">
                      <span className="text-muted-foreground text-xs uppercase tracking-wider font-semibold mb-1">Variants</span>
                      <span className="font-mono">{exp.variantCount} conditions</span>
                    </div>
                    <div className="w-px h-8 bg-border hidden md:block"></div>
                    <div className="flex flex-col">
                      <span className="text-muted-foreground text-xs uppercase tracking-wider font-semibold mb-1">Scale</span>
                      <span className="font-mono">n = {exp.trialsPerCell * exp.variantCount * exp.models.length}</span>
                    </div>
                    <div className="w-px h-8 bg-border hidden md:block"></div>
                    <div className="flex flex-col">
                      <span className="text-muted-foreground text-xs uppercase tracking-wider font-semibold mb-1">Last Run</span>
                      <span className="font-mono">{exp.lastRunAt ? format(new Date(exp.lastRunAt), "MMM d, yyyy") : "Pending"}</span>
                    </div>
                  </div>
                </div>
                
                {exp.postSlug && (
                  <div className="bg-muted/50 p-6 md:p-8 md:w-64 flex flex-col justify-center border-t md:border-t-0 md:border-l border-border group-hover:bg-primary/5 transition-colors">
                    <Link 
                      href={`/posts/${exp.postSlug}`}
                      className="inline-flex items-center justify-center gap-2 text-primary font-medium hover:underline"
                    >
                      Read Findings
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                    </Link>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
