import { useMemo, useState } from "react";
import { Figure, Missing, Slider, Stat, fmt, isCountChoice, type WidgetProps } from "./shared";

/** A confidence-gated sieve over this run's own items. Illustrative, not a benchmark. */
export function DecisionSieve({ data }: WidgetProps) {
  const [threshold, setThreshold] = useState(60);
  const items = useMemo(() => {
    const v = data?.variants ?? {};
    return Object.values(v)
      .filter((s) => s.questionType === "choice" && isCountChoice(s.options) && s.experiment !== "E0" && s.probabilities)
      .map((s) => ({
        id: s.variantId,
        label: s.label.replace(/^E\d · /, ""),
        experiment: s.experiment ?? "",
        choice: s.choice ?? "",
        confidence: s.confidence ?? 0,
      }))
      .sort((a, b) => b.confidence - a.confidence);
  }, [data]);

  if (!items.length) {
    return (
      <Figure eyebrow="Widget 9 · Decision sieve" title="Sieve" hint="—">
        <Missing what="Choice items" />
      </Figure>
    );
  }
  const t = threshold / 100;
  const accepted = items.filter((i) => i.confidence >= t);
  const review = items.filter((i) => i.confidence < t);

  return (
    <Figure
      eyebrow="Widget 9 · Decision sieve"
      title={`Route the ${items.length} count questions in this run by confidence: at or above the threshold is auto-accepted, below goes to a person.`}
      hint="Raising the threshold trades coverage for reliability, but only against the kind of error confidence can see. “Typical human being → one” and the planted-note answer both pass a 0.6 gate. The sieve is a real tool; it filters indecision, not confident mistakes. This is illustrative: the items are this experiment's own questions, not a workload."
    >
      <Slider id="sieve-threshold" label="Confidence threshold" value={threshold} min={0} max={100} step={5} onChange={setThreshold} display={fmt(t)} />
      <div className="mt-3 grid grid-cols-2 gap-2">
        <Stat label="Auto-accepted" value={`${accepted.length} / ${items.length}`} sub={`${Math.round((accepted.length / items.length) * 100)}% coverage`} />
        <Stat label="Sent to a person" value={`${review.length} / ${items.length}`} />
      </div>
      <div className="mt-3 flex h-3 w-full gap-0.5" aria-hidden>
        {items.map((i) => (
          <span key={i.id} className="flex-1" style={{ background: i.confidence >= t ? "hsl(var(--foreground))" : "hsl(var(--muted))" }} title={`${i.label}: ${fmt(i.confidence)}`} />
        ))}
      </div>
      <div className="mt-3 overflow-x-auto">
      <table className="w-full min-w-[24rem] text-xs">
        <thead>
          <tr className="border-b border-border text-left text-muted-foreground">
            <th className="py-1 pr-2 font-medium">Item</th>
            <th className="py-1 pr-2 font-medium">choice</th>
            <th className="py-1 pr-2 text-right font-medium">confidence</th>
            <th className="py-1 font-medium">route</th>
          </tr>
        </thead>
        <tbody>
          {items.map((i) => (
            <tr key={i.id} className="border-b border-border/60">
              <td className="py-1 pr-2">
                <span className="font-mono text-[10px] text-muted-foreground">{i.experiment}</span> {i.label}
              </td>
              <td className="py-1 pr-2">{i.choice}</td>
              <td className="py-1 pr-2 text-right font-mono tabular-nums">{fmt(i.confidence)}</td>
              <td className="py-1">{i.confidence >= t ? "accept" : <span className="text-destructive">review</span>}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </Figure>
  );
}
