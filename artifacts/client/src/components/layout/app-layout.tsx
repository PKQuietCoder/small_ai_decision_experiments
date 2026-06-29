import { useState } from "react";
import { Link, useLocation } from "wouter";
import { useSite } from "@/hooks/use-api";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetTitle,
} from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import banner from "@assets/banner-wordmark.png";

export function AppLayout({ children }: { children: React.ReactNode }) {
  const { data: site } = useSite();
  const [location] = useLocation();
  const [open, setOpen] = useState(false);

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/methodology", label: "Methodology" },
    { href: "/about", label: "About" },
  ];

  return (
    <div className="min-h-[100dvh] flex flex-col font-sans">
      <header className="sticky top-0 z-40 w-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 border-b border-border">
        <div className="container mx-auto px-4 md:px-6 h-16 flex items-center justify-between gap-3">
          <Link
            href="/"
            aria-label={site?.title || "Borrowed Intuitions"}
            className="flex items-center min-w-0"
          >
            <img
              src={banner}
              alt={site?.title || "Borrowed Intuitions"}
              className="h-8 sm:h-9 w-auto shrink-0 rounded-none object-contain"
            />
          </Link>

          <nav className="hidden sm:flex items-center gap-6 text-sm font-medium text-muted-foreground">
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

          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger asChild>
              <button
                type="button"
                aria-label="Open navigation menu"
                className="sm:hidden -mr-2 inline-flex h-10 w-10 items-center justify-center rounded-md text-foreground transition-colors hover:bg-muted"
              >
                <Menu size={22} />
              </button>
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <SheetTitle className="mb-6 font-serif text-lg">Menu</SheetTitle>
              <nav className="flex flex-col gap-1">
                {navLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    onClick={() => setOpen(false)}
                    className={`rounded-md px-3 py-2.5 text-base transition-colors ${
                      location === link.href
                        ? "bg-muted font-semibold text-foreground"
                        : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
                    }`}
                  >
                    {link.label}
                  </Link>
                ))}
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      <main className="flex-1">
        {children}
      </main>

      <footer className="border-t border-border/50 py-12 mt-20">
        <div className="container mx-auto px-4 md:px-6 flex flex-col md:flex-row items-center justify-between gap-6 text-sm text-muted-foreground">
          <div className="flex items-center gap-6">
            <p>
              © {new Date().getFullYear()}{" "}
              {site?.authorUrl ? (
                <a
                  href={site.authorUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-foreground transition-colors"
                >
                  {site?.author}
                </a>
              ) : (
                site?.author
              )}
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
