import { Link, useLocation } from "wouter";
import { useSite } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";

export function AppLayout({ children }: { children: React.ReactNode }) {
  const { data: site, isLoading } = useSite();
  const [location] = useLocation();

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/experiments", label: "Experiments" },
    { href: "/about", label: "About" },
  ];

  return (
    <div className="min-h-[100dvh] flex flex-col font-sans">
      <header className="sticky top-0 z-40 w-full backdrop-blur-md bg-background/80 border-b border-border/50">
        <div className="container mx-auto px-4 md:px-6 h-16 flex items-center justify-between">
          <Link href="/" className="font-bold tracking-tight text-primary text-lg flex items-center gap-2">
            <div className="w-6 h-6 rounded-sm bg-primary text-primary-foreground flex items-center justify-center text-xs">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5H5a2 2 0 0 0 0 4"/></svg>
            </div>
            {isLoading ? <Skeleton className="h-5 w-32" /> : site?.title || "LLM Decision Science"}
          </Link>
          
          <nav className="flex items-center gap-6 text-sm font-medium text-muted-foreground">
            {navLinks.map((link) => (
              <Link 
                key={link.href} 
                href={link.href}
                className={`transition-colors hover:text-foreground ${location === link.href ? "text-foreground font-semibold" : ""}`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {children}
      </main>

      <footer className="border-t border-border/50 py-12 mt-20">
        <div className="container mx-auto px-4 md:px-6 flex flex-col md:flex-row items-center justify-between gap-6 text-sm text-muted-foreground">
          <div>
            <p className="font-medium text-foreground">{site?.title || "LLM Decision Science"}</p>
            <p className="mt-1">{site?.tagline}</p>
          </div>
          <div className="flex items-center gap-6">
            <p>© {new Date().getFullYear()} {site?.author}</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
