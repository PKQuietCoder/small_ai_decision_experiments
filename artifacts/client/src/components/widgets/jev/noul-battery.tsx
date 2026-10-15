import { Figure, Missing, Stat, fmt, type WidgetProps } from "./shared";

/** E8: one Noul per claim; the model states Taleb's point without a composite. */
export function NoulBattery({ data }: WidgetProps) {
  const e8 = data?.e8;
  if (!e8?.claims?.length) {
    return (
      <Figure eyebrow="Widget 8 · Noul battery" title="E8" hint="—">
        <Missing what="The E8 Noul battery" />
      </Figure>
    );
  }
  const pol = e8.polarity;
  return (
    <Figure
      eyebrow="Widget 8 · Noul battery (E8)"
      title="P(yes) for seven separate claims about the room."
      hint="Asked claim by claim, the model says the mean is one (high), a typical woman has two (high), and that anyone has exactly one (low). That is the statistical point stated by the model itself, with no option set forcing the answers to share one probability mass. The polarity pair should sum to about 1."
    >
      <ul className="space-y-2">
        {e8.claims.map((c) => (
          <li key={c.variantId} className="grid grid-cols-[1fr_8rem_3rem] items-center gap-3 text-xs sm:grid-cols-[1fr_12rem_3rem]" title={c.instructions ?? ""}>
            <span>{c.claim}</span>
            <span className="relative block h-3 bg-muted">
              <span className="absolute inset-y-0 left-0 bg-[hsl(var(--chart-1))]" style={{ width: `${c.p * 100}%` }} />
              <span className="absolute inset-y-0 w-px bg-foreground" style={{ left: "50%" }} aria-hidden />
            </span>
            <span className="text-right font-mono tabular-nums">{fmt(c.p)}</span>
          </li>
        ))}
      </ul>
      <p className="mt-2 text-[11px] text-muted-foreground">Bar = P(yes); the hairline at 0.50 is indifference. A Noul carries no confidence field; |2p − 1| is the docs' suggested sharpness statistic.</p>
      {pol && (
        <div className="mt-4 grid gap-2 sm:grid-cols-3">
          <Stat label="P(exactly two breasts)" value={fmt(pol.exactlyTwo)} />
          <Stat label="P(fewer than two breasts)" value={fmt(pol.fewerThanTwo)} />
          <Stat label="Sum (consistency check)" value={fmt(pol.sum)} sub={`${pol.residual >= 0 ? "−" : "+"}${fmt(Math.abs(pol.residual))} from 1.00`} />
        </div>
      )}
    </Figure>
  );
}
