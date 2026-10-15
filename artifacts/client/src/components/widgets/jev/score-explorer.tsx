import { useMemo, useState } from "react";
import {
  Figure,
  Slider,
  Stat,
  colorFor,
  fmt,
  normalize,
  scoreConfidence,
  scoreExpectation,
  type WidgetProps,
} from "./shared";

const LEVELS = ["zero", "one", "two", "three or more"];

/** The Score primitive: four level probabilities → one expectation and a confidence. */
export function ScoreExplorer({ data }: WidgetProps) {
  const [weights, setWeights] = useState<number[]>([50, 0, 50, 0]);
  const probs = useMemo(() => normalize(weights), [weights]);
  const expectation = scoreExpectation(probs);
  const confidence = scoreConfidence(probs);
  const between = Math.abs(expectation - Math.round(expectation)) > 0.05;
  const modal = probs.indexOf(Math.max(...probs));

  const presets: { label: string; probs: number[]; note: string }[] = [];
  const e1 = data?.e1;
  (["breasts", "testicles"] as const).forEach((organ) => {
    const s = e1?.[organ]?.score;
    if (s?.probabilities) {
      presets.push({
        label: `Load E1 · ${organ}`,
        probs: LEVELS.map((_, i) => s.probabilities?.[String(i)] ?? 0),
        note: `Jev's actual Score answer (score ${fmt(s.score)}, confidence ${fmt(s.confidence)}).`,
      });
    }
  });
  presets.push({
    label: "Hypothetical half zero, half two",
    probs: [0.5, 0, 0.5, 0],
    note: "Not an observed answer: the split that would also give an expectation of 1.0, at confidence 0.",
  });

  return (
    <Figure
      eyebrow="Widget 2 · Score expectation explorer"
      title="Score returns per-level probabilities, a probability-weighted expectation, and a confidence."
      hint="Two very different distributions can share the expectation 1.0: all mass on “one” (confidence 1) or half on “zero” and half on “two” (confidence 0). The expectation alone cannot tell you which; read the distribution. Jev's E1 answer put the whole mass on “one”."
    >
      <div className="grid gap-4 md:grid-cols-[1fr_auto]">
        <div className="space-y-2">
          {LEVELS.map((level, i) => (
            <Slider
              key={level}
              id={`score-${i}`}
              label={`${i} · ${level}`}
              value={weights[i]}
              onChange={(v) => setWeights((w) => w.map((x, j) => (j === i ? v : x)))}
              display={fmt(probs[i])}
              swatch={colorFor(level, i)}
            />
          ))}
          <div className="flex flex-wrap gap-2 pt-2">
            {presets.map((p) => (
              <button
                key={p.label}
                type="button"
                title={p.note}
                onClick={() => setWeights(p.probs.map((x) => Math.round(x * 100)))}
                className="border border-border bg-background px-2.5 py-1 text-xs hover:bg-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2 md:w-64 md:grid-cols-1">
          <Stat
            label="score = Σ i · pᵢ"
            value={fmt(expectation)}
            sub={between ? `Between levels “${LEVELS[Math.floor(expectation)]}” and “${LEVELS[Math.ceil(expectation)] ?? ""}”.` : `On level “${LEVELS[Math.round(expectation)]}”.`}
          />
          <Stat
            label="confidence = max(0, 1 − Σ pᵢ|i − m| / MAD_unif)"
            value={fmt(confidence)}
            sub={`m = ${modal} (“${LEVELS[modal]}”), MAD_unif = 1.0 for four levels.`}
          />
        </div>
      </div>
      <div
        className="mt-3 border-l-2 pl-3 text-xs"
        style={{ borderColor: between ? "hsl(var(--destructive))" : "hsl(var(--border))" }}
      >
        {between
          ? "The expectation lands between two levels. No level — no person — has this value; it is a summary of the mass on either side."
          : "The expectation sits on a level. Check the confidence: a sharp peak and a symmetric split can both land here."}
      </div>
    </Figure>
  );
}
