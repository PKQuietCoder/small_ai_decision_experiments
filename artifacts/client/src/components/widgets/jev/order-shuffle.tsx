import { useMemo, useState } from "react";
import { Figure, Missing, Segmented, colorFor, fmt, labelFor, type WidgetProps } from "./shared";

const ORDER_SHORT: Record<string, string> = {
  original: "orig",
  reversed: "rev",
  rotated: "rot",
  permuted: "perm",
};

/** E4: the same question with the options in four orders. */
export function OrderShuffle({ data }: WidgetProps) {
  const organs = useMemo(() => Object.keys(data?.e4 ?? {}), [data]);
  const [organ, setOrgan] = useState(organs[0] ?? "breasts");
  const [showArgmax, setShowArgmax] = useState(false);
  const block = data?.e4?.[organ] ?? data?.e4?.[organs[0]];

  if (!block?.orders?.length) {
    return (
      <Figure eyebrow="Widget 6 · Option-order shuffle" title="E4" hint="—">
        <Missing what="The E4 order shuffle" />
      </Figure>
    );
  }
  const orders = block.orders;
  const options = block.options;
  const W = 560;
  const plotH = 160;
  const H = plotH + 60;
  const groupW = (W - 60) / options.length;
  const barW = Math.min(18, (groupW - 24) / orders.length - 2);
  const y = (p: number) => 20 + (1 - p) * plotH;

  return (
    <Figure
      eyebrow="Widget 6 · Option-order shuffle (E4)"
      title="P(option) under four option orders, one bar per order; the dark tick is the mean across orders."
      hint="The documented first-option lean did not show on this item: the four orders agree to within 0.01 and the argmax never moved. Position bias is item-dependent, so the check is cheap insurance rather than a guaranteed finding. Use the mean over orders as the estimate either way."
    >
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <Segmented label="Organ" value={organ} onChange={setOrgan} options={organs.map((o) => ({ value: o, label: o }))} />
        <Segmented
          label="Argmax markers"
          value={showArgmax ? "on" : "off"}
          onChange={(v) => setShowArgmax(v === "on")}
          options={[
            { value: "off", label: "Probabilities" },
            { value: "on", label: "Mark the argmax" },
          ]}
        />
      </div>
      <div className="overflow-x-auto">
        <svg viewBox={`0 0 ${W} ${H}`} className="min-w-[32rem] w-full font-sans" role="img" aria-label="Grouped bars of option probability by option order">
          {[0, 0.5, 1].map((t) => (
            <g key={t}>
              <line x1={40} x2={W} y1={y(t)} y2={y(t)} stroke="hsl(var(--border))" strokeWidth="1" />
              <text x={34} y={y(t) + 3} textAnchor="end" fontSize="10" fill="hsl(var(--muted-foreground))">
                {t.toFixed(1)}
              </text>
            </g>
          ))}
          {options.map((opt, i) => {
            const gx = 50 + i * groupW;
            const mean = block.perOption[opt].mean;
            return (
              <g key={opt}>
                {orders.map((r, j) => {
                  const p = r.probabilities[opt] ?? 0;
                  const bx = gx + 12 + j * (barW + 2);
                  const isTop = r.choice === opt;
                  return (
                    <g key={r.variantId}>
                      <rect x={bx} y={y(p)} width={barW} height={Math.max(0, y(0) - y(p))} fill={colorFor(opt, i)}>
                        <title>{`${r.order} order: P(${opt}) = ${p.toFixed(3)}`}</title>
                      </rect>
                      {showArgmax && isTop && (
                        <circle cx={bx + barW / 2} cy={y(p) - 8} r={3.5} fill="hsl(var(--foreground))" />
                      )}
                      <text x={bx + barW / 2} y={y(0) + 12} textAnchor="middle" fontSize="8" fill="hsl(var(--muted-foreground))">
                        {ORDER_SHORT[r.order ?? ""] ?? r.order}
                      </text>
                    </g>
                  );
                })}
                <line
                  x1={gx + 8}
                  x2={gx + 12 + orders.length * (barW + 2)}
                  y1={y(mean)}
                  y2={y(mean)}
                  stroke="hsl(var(--foreground))"
                  strokeWidth="1.5"
                />
                <text x={gx + 12 + (orders.length * (barW + 2)) / 2} y={y(0) + 28} textAnchor="middle" fontSize="11" fill="hsl(var(--foreground))">
                  {labelFor(opt).replace(" / no single count", "")}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
      <div className="mt-3 overflow-x-auto">
      <table className="w-full min-w-[32rem] text-xs">
        <thead>
          <tr className="border-b border-border text-left text-muted-foreground">
            <th className="py-1 pr-2 font-medium">Order</th>
            <th className="py-1 pr-2 font-medium">Options as sent</th>
            {options.map((o) => (
              <th key={o} className="py-1 pr-2 text-right font-medium">
                {o}
              </th>
            ))}
            <th className="py-1 font-medium">choice</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((r) => (
            <tr key={r.variantId} className="border-b border-border/60">
              <td className="py-1 pr-2">{r.order}</td>
              <td className="py-1 pr-2 font-mono text-[10px]">{(r.criteriaOrder ?? []).join(" › ")}</td>
              {options.map((o) => (
                <td key={o} className="py-1 pr-2 text-right font-mono tabular-nums">
                  {fmt(r.probabilities[o])}
                </td>
              ))}
              <td className="py-1">{r.choice}</td>
            </tr>
          ))}
          <tr className="font-medium">
            <td className="py-1 pr-2">SD across orders</td>
            <td />
            {options.map((o) => (
              <td key={o} className="py-1 pr-2 text-right font-mono tabular-nums">
                {fmt(block.perOption[o].sd, 3)}
              </td>
            ))}
            <td className="py-1">{block.distinctChoices.length === 1 ? "unchanged" : `${block.distinctChoices.length} distinct`}</td>
          </tr>
        </tbody>
      </table>
      </div>
    </Figure>
  );
}
