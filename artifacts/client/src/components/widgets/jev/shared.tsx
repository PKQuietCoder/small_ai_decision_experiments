// Shared pieces for the Jev "average human" widgets. Everything here follows the
// site's design system: flat, sharp corners, hairline rules, Wong palette for
// categorical identity only, sans for UI text, numbers in mono/tabular.
import type { ReactNode } from "react";
import type { SystemOneAnalysis } from "@/lib/api";
import { cn } from "@/lib/utils";

export interface WidgetProps {
  data: SystemOneAnalysis | null;
}

// Color follows the entity (an option keeps its hue in every widget), never its
// rank. `other` and `three or more` are the "none of the counts" buckets and take
// the de-emphasis gray so the three counts carry the only color.
const CHART = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];
const GRAY = "hsl(var(--muted-foreground))";

export const OPTION_COLOR: Record<string, string> = {
  zero: CHART[0],
  one: CHART[1],
  two: CHART[2],
  other: GRAY,
  "three or more": GRAY,
  under_one: CHART[0],
  over_one: CHART[3],
  one_testicle: CHART[1],
  one_breast: CHART[3],
  two_breasts: CHART[2],
  two_testicles: CHART[0],
};

export function colorFor(key: string, index = 0): string {
  return OPTION_COLOR[key] ?? CHART[index % CHART.length];
}

export const OPTION_LABEL: Record<string, string> = {
  zero: "zero",
  one: "one",
  two: "two",
  other: "other / no single count",
  "three or more": "three or more",
  under_one: "under one",
  over_one: "over one, under two",
  one_testicle: "one testicle",
  one_breast: "one breast",
  two_breasts: "two breasts",
  two_testicles: "two testicles",
};

export function labelFor(key: string): string {
  return OPTION_LABEL[key] ?? key.replace(/_/g, " ");
}

export function fmt(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toFixed(digits);
}

export const COUNT_OPTIONS = ["zero", "one", "two", "other"];

export function isCountChoice(options?: string[]): boolean {
  if (!options || options.length !== COUNT_OPTIONS.length) return false;
  const set = new Set(options);
  return COUNT_OPTIONS.every((o) => set.has(o));
}

// TypeSafe's published formulas (docs.typesafe.ai/confidence).
export function choiceConfidence(probs: number[]): number {
  const n = probs.length;
  if (n < 2) return 0;
  const pMax = Math.max(...probs);
  return (pMax - 1 / n) / (1 - 1 / n);
}

export function scoreExpectation(probs: number[]): number {
  return probs.reduce((acc, p, i) => acc + i * p, 0);
}

export function scoreConfidence(probs: number[]): number {
  const n = probs.length;
  if (n < 2) return 0;
  let m = 0;
  probs.forEach((p, i) => {
    if (p > probs[m]) m = i;
  });
  const weighted = probs.reduce((acc, p, i) => acc + p * Math.abs(i - m), 0);
  const centre = (n - 1) / 2;
  const madUnif = probs.reduce((acc, _p, i) => acc + Math.abs(i - centre), 0) / n;
  return madUnif ? Math.max(0, 1 - weighted / madUnif) : 0;
}

export function normalize(weights: number[]): number[] {
  const total = weights.reduce((a, b) => a + b, 0);
  if (total <= 0) return weights.map(() => 1 / weights.length);
  return weights.map((w) => w / total);
}

// ---- chrome -----------------------------------------------------------------

export function Figure({
  eyebrow,
  title,
  hint,
  children,
}: {
  eyebrow: string;
  title: string;
  hint: string;
  children: ReactNode;
}) {
  return (
    <figure className="my-8 border border-border bg-card p-4 font-sans text-sm text-foreground sm:p-5">
      <p className="eyebrow mb-1">{eyebrow}</p>
      <p className="mb-4 font-medium leading-snug">{title}</p>
      {children}
      <figcaption className="mt-4 border-t border-border pt-3 text-xs leading-relaxed text-muted-foreground">
        <span className="font-semibold text-foreground">What to look for.</span> {hint}
      </figcaption>
    </figure>
  );
}

export function Missing({ what }: { what: string }) {
  return (
    <p className="border border-dashed border-border p-4 font-sans text-xs text-muted-foreground">
      {what} is not available for this run.
    </p>
  );
}

export function Segmented<T extends string>({
  options,
  value,
  onChange,
  label,
}: {
  options: { value: T; label: string }[];
  value: T;
  onChange: (value: T) => void;
  label: string;
}) {
  return (
    <div role="radiogroup" aria-label={label} className="inline-flex border border-border">
      {options.map((opt) => {
        const active = opt.value === value;
        return (
          <button
            key={opt.value}
            type="button"
            role="radio"
            aria-checked={active}
            onClick={() => onChange(opt.value)}
            className={cn(
              "px-3 py-1.5 text-xs transition-colors duration-150 [transition-timing-function:cubic-bezier(0.2,0,0,1)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
              active
                ? "bg-primary text-primary-foreground"
                : "bg-background text-foreground hover:bg-muted",
            )}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}

export function Slider({
  id,
  label,
  value,
  min = 0,
  max = 100,
  step = 1,
  onChange,
  display,
  swatch,
}: {
  id: string;
  label: string;
  value: number;
  min?: number;
  max?: number;
  step?: number;
  onChange: (value: number) => void;
  display: string;
  swatch?: string;
}) {
  return (
    <label htmlFor={id} className="grid grid-cols-[minmax(6rem,9rem)_1fr_3.5rem] items-center gap-3 text-xs">
      <span className="flex items-center gap-2 truncate text-muted-foreground">
        {swatch && <span aria-hidden className="inline-block h-2.5 w-2.5 shrink-0" style={{ background: swatch }} />}
        {label}
      </span>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="h-1 w-full cursor-pointer appearance-none bg-border accent-[hsl(var(--foreground))] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      />
      <span className="text-right font-mono tabular-nums">{display}</span>
    </label>
  );
}

export function ProbBars({
  probabilities,
  order,
  highlight,
  compact = false,
}: {
  probabilities: Record<string, number>;
  order?: string[];
  highlight?: string;
  compact?: boolean;
}) {
  const keys = order ?? Object.keys(probabilities);
  return (
    <ul className={cn("space-y-1.5", compact && "space-y-1")}>
      {keys.map((k, i) => {
        const p = probabilities[k] ?? 0;
        return (
          <li
            key={k}
            className="grid grid-cols-[minmax(6rem,9rem)_1fr_3rem] items-center gap-3"
            title={`${labelFor(k)}: ${p.toFixed(3)}`}
          >
            <span
              className={cn(
                "truncate text-xs",
                k === highlight ? "font-semibold text-foreground" : "text-muted-foreground",
              )}
            >
              {labelFor(k)}
            </span>
            <span className={cn("relative block bg-muted", compact ? "h-2" : "h-3")}>
              <span
                className="absolute inset-y-0 left-0 transition-[width] duration-200 [transition-timing-function:cubic-bezier(0.2,0,0,1)]"
                style={{ width: `${Math.max(0, Math.min(1, p)) * 100}%`, background: colorFor(k, i) }}
              />
            </span>
            <span className="text-right font-mono text-xs tabular-nums">{fmt(p)}</span>
          </li>
        );
      })}
    </ul>
  );
}

export function Meter({ label, value, note }: { label: string; value: number | null | undefined; note?: string }) {
  const v = value ?? 0;
  return (
    <div className="grid grid-cols-[minmax(6rem,9rem)_1fr_3rem] items-center gap-3 text-xs">
      <span className="text-muted-foreground">{label}</span>
      <span className="relative block h-3 bg-muted">
        <span
          className="absolute inset-y-0 left-0 bg-foreground transition-[width] duration-200 [transition-timing-function:cubic-bezier(0.2,0,0,1)]"
          style={{ width: `${Math.max(0, Math.min(1, v)) * 100}%` }}
        />
      </span>
      <span className="text-right font-mono tabular-nums">{fmt(value)}</span>
      {note && <span className="col-span-3 text-muted-foreground">{note}</span>}
    </div>
  );
}

export function Stat({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="border border-border bg-background px-3 py-2">
      <p className="text-[11px] text-muted-foreground">{label}</p>
      <p className="text-xl font-semibold leading-tight">{value}</p>
      {sub && <p className="text-[11px] text-muted-foreground">{sub}</p>}
    </div>
  );
}

export function Legend({ items }: { items: { key: string; label?: string }[] }) {
  return (
    <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
      {items.map((it, i) => (
        <li key={it.key} className="flex items-center gap-1.5">
          <span aria-hidden className="inline-block h-2.5 w-2.5" style={{ background: colorFor(it.key, i) }} />
          {it.label ?? labelFor(it.key)}
        </li>
      ))}
    </ul>
  );
}
