import { Link, useLocation } from "wouter";
import { useSite } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import logo from "@assets/logo.png";

export function AppLayout({ children }: { children: React.ReactNode }) {
  const { data: site, isLoading } = useSite();
  const [location] = useLocation();

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/about", label: "About" },
  ];

  return (
    <div className="min-h-[100dvh] flex flex-col font-sans">
      <header className="sticky top-0 z-40 w-full bg-background border-b border-border">
        <div className="container mx-auto px-4 md:px-6 h-16 flex items-center justify-between">
          <Link href="/" className="font-serif font-semibold tracking-tight text-foreground text-lg flex items-center gap-2.5">
            <img src={logo} alt="Borrowed Instincts logo" className="h-8 w-8 rounded-none object-contain" />
            {isLoading ? <Skeleton className="h-5 w-32" /> : site?.title || "Borrowed Instincts"}
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
            <p className="font-serif font-semibold text-foreground">{site?.title || "Borrowed Instincts"}</p>
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
