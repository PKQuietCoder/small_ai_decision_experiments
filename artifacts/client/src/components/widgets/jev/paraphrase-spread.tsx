import { useMemo, useState } from "react";
import { Figure, Legend, Missing, Segmented, Slider, colorFor, fmt, labelFor, type WidgetProps } from "./shared";

const PHRASING_LABEL: Record<string, string> = {
  average: "average human being",
  typical: "typical human being",
  arith_mean: "arithmetic mean per person",
  random_person: "one person picked at random",
  most: "most human beings",
};
const LETTERS = ["A", "B", "C", "D", "E"];

/** E3: the same question five ways; the spread across phrasings is the signal. */
export function ParaphraseSpread({ data }: WidgetProps) {
  const organs = useMemo(() => Object.keys(data?.e3 ?? {}), [data]);
  const [organ, setOrgan] = useState(organs[0] ?? "breasts");
  const [threshold, setThreshold] = useState(80);
  const block = data?.e3?.[organ] ?? data?.e3?.[organs[0]];

  if (!block?.phrasings?.length) {
    return (
      <Figure eyebrow="Widget 5 · Paraphrase spread" title="E3" hint="—">
        <Missing what="The E3 paraphrase ensemble" />
      </Figure>
    );
  }
  const rows = block.phrasings;
  const options = block.options;
  const W = 560;
  const H = options.length * 44 + 28;
  const x = (p: number) => 150 + p * (W - 170);

  // Agreement = share of phrasings whose argmax matches the modal argmax.
  const agreement = (b: typeof block) => {
    const choices = (b.phrasings ?? []).map((r) => r.choice ?? "");
    const counts = new Map<string, number>();
    choices.forEach((c) => counts.set(c, (counts.get(c) ?? 0) + 1));
    const modal = Math.max(...counts.values());
    return { modal: [...counts.entries()].find(([, n]) => n === modal)?.[0] ?? "", share: modal / choices.length };
  };

  return (
    <Figure
      eyebrow="Widget 5 · Paraphrase spread (E3)"
      title="P(option) for each of five phrasings of the same question. Bands show min to max; ticks mark the mean."
      hint="Repeating one phrasing gave identical answers (E0). Varying the phrasing moved P(one) across almost the whole scale. “Typical human being” still returned “one”, confidently; no typical person has one. The spread, not any single confidence, is the honest uncertainty."
    >
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <Segmented
          label="Organ"
          value={organ}
          onChange={setOrgan}
          options={organs.map((o) => ({ value: o, label: o }))}
        />
        <Legend items={options.map((o) => ({ key: o }))} />
      </div>
      <div className="overflow-x-auto">
        <svg viewBox={`0 0 ${W} ${H}`} className="min-w-[32rem] w-full font-sans" role="img" aria-label="Dot plot of option probabilities by phrasing">
          {[0, 0.25, 0.5, 0.75, 1].map((t) => (
            <g key={t}>
              <line x1={x(t)} x2={x(t)} y1={8} y2={H - 20} stroke="hsl(var(--border))" strokeWidth="1" />
              <text x={x(t)} y={H - 6} textAnchor="middle" fontSize="10" fill="hsl(var(--muted-foreground))">
                {t.toFixed(2)}
              </text>
            </g>
          ))}
          {options.map((opt, i) => {
            const y = 30 + i * 44;
            const per = block.perOption[opt];
            return (
              <g key={opt}>
                <text x={0} y={y + 4} fontSize="11" fill="hsl(var(--foreground))">
                  {labelFor(opt).replace(" / no single count", "")}
                </text>
                <rect x={x(per.min)} y={y - 7} width={Math.max(1, x(per.max) - x(per.min))} height={14} fill={colorFor(opt, i)} opacity={0.18} />
                <line x1={x(per.mean)} x2={x(per.mean)} y1={y - 11} y2={y + 11} stroke="hsl(var(--foreground))" strokeWidth="1.5" />
                {rows.map((r, j) => {
                  const p = r.probabilities[opt] ?? 0;
                  const jitter = (j - (rows.length - 1) / 2) * 3;
                  return (
                    <g key={r.variantId}>
                      <circle cx={x(p)} cy={y + jitter} r={6} fill="hsl(var(--card))" />
                      <circle cx={x(p)} cy={y + jitter} r={4.5} fill={colorFor(opt, i)}>
                        <title>{`${PHRASING_LABEL[r.phrasing ?? ""] ?? r.phrasing}: P(${opt}) = ${p.toFixed(3)}`}</title>
                      </circle>
                      <text x={x(p)} y={y + jitter - 8} textAnchor="middle" fontSize="8" fill="hsl(var(--muted-foreground))">
                        {LETTERS[j]}
                      </text>
                    </g>
                  );
                })}
              </g>
            );
          })}
        </svg>
      </div>
      <div className="mt-3 overflow-x-auto">
      <table className="w-full min-w-[28rem] text-xs">
        <thead>
          <tr className="border-b border-border text-left text-muted-foreground">
            <th className="py-1 pr-2 font-medium">#</th>
            <th className="py-1 pr-2 font-medium">Phrasing</th>
            <th className="py-1 pr-2 text-right font-medium">P(one)</th>
            <th className="py-1 pr-2 font-medium">choice</th>
            <th className="py-1 text-right font-medium">confidence</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, j) => (
            <tr key={r.variantId} className="border-b border-border/60">
              <td className="py-1 pr-2 font-mono">{LETTERS[j]}</td>
              <td className="py-1 pr-2">{PHRASING_LABEL[r.phrasing ?? ""] ?? r.phrasing}</td>
              <td className="py-1 pr-2 text-right font-mono tabular-nums">{fmt(r.probabilities.one)}</td>
              <td className="py-1 pr-2">{r.choice}</td>
              <td className="py-1 text-right font-mono tabular-nums">{fmt(r.confidence)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
      <div className="mt-4 border-t border-border pt-3">
        <Slider
          id="e3-threshold"
          label="Agreement threshold"
          value={threshold}
          min={20}
          max={100}
          step={20}
          onChange={setThreshold}
          display={`${threshold}%`}
        />
        <ul className="mt-2 grid gap-2 sm:grid-cols-2">
          {organs.map((o) => {
            const b = data?.e3?.[o];
            if (!b) return null;
            const a = agreement(b);
            const accept = a.share * 100 >= threshold;
            return (
              <li key={o} className="flex items-center justify-between border border-border bg-background px-3 py-2 text-xs">
                <span>
                  <span className="font-medium">{o}</span> · {Math.round(a.share * 5)}/5 phrasings agree on “{a.modal}”
                </span>
                <span
                  className="px-1.5 py-0.5 font-medium"
                  style={{
                    background: accept ? "hsl(var(--foreground))" : "transparent",
                    color: accept ? "hsl(var(--background))" : "hsl(var(--destructive))",
                    border: accept ? "none" : "1px solid hsl(var(--destructive))",
                  }}
                >
                  {accept ? "accept" : "send to review"}
                </span>
              </li>
            );
          })}
        </ul>
      </div>
    </Figure>
  );
}
