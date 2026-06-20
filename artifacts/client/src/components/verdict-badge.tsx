import type { PostSummary } from "@/lib/api";

// The series' headline vocabulary. Every experiment lands on one of three verdicts,
// measured against the original study's human baseline. Rendered legend-style — a
// small Wong-colored swatch (a true circle, the one curve the design system allows)
// plus a mono label. Color is earned here: the verdict is a categorical fact.
const VERDICTS: Record<string, { label: string; dot: string }> = {
  copy: { label: "Copies the bias", dot: "bg-chart-2" }, //    vermilion
  smooth: { label: "Smooths the bias", dot: "bg-chart-1" }, // blue
  amplify: { label: "Amplifies the bias", dot: "bg-chart-4" }, // orange
  mixed: { label: "Mixed", dot: "bg-muted-foreground" },
};

interface VerdictBadgeProps {
  verdict?: PostSummary["verdict"];
  /** Compact variant for the feed card: swatch + eyebrow label, no border or "Verdict" tag. */
  compact?: boolean;
}

export function VerdictBadge({ verdict, compact = false }: VerdictBadgeProps) {
  const meta = verdict ? VERDICTS[verdict.toLowerCase()] : undefined;
  if (!meta) return null;

  if (compact) {
    return (
      <span className="inline-flex items-center gap-1.5">
        <span
          className={`h-2 w-2 shrink-0 rounded-full ${meta.dot}`}
          aria-hidden="true"
        />
        <span className="eyebrow">{meta.label}</span>
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-2 border border-border px-3 py-1">
      <span className="eyebrow">Verdict</span>
      <span
        className={`h-2.5 w-2.5 shrink-0 rounded-full ${meta.dot}`}
        aria-hidden="true"
      />
      <span className="font-mono text-xs font-semibold uppercase tracking-wider text-foreground">
        {meta.label}
      </span>
    </span>
  );
}
