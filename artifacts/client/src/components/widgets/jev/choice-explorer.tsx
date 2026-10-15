import { useMemo, useState } from "react";
import {
  COUNT_OPTIONS,
  Figure,
  Slider,
  Stat,
  choiceConfidence,
  colorFor,
  fmt,
  normalize,
  type WidgetProps,
} from "./shared";

/** The Choice primitive: a distribution over options → argmax and confidence. */
export function ChoiceExplorer({ data }: WidgetProps) {
  const [weights, setWeights] = useState<number[]>([0, 100, 0, 0]);
  const probs = useMemo(() => normalize(weights), [weights]);
  const n = probs.length;
  const sorted = [...probs].sort((a, b) => b - a);
  const confidence = choiceConfidence(probs);
  const topIdx = probs.indexOf(sorted[0]);
  const ratio = sorted[1] > 0 ? sorted[0] / sorted[1] : null;

  const presets = useMemo(() => {
    const out: { label: string; probs: number[]; note: string }[] = [];
    const v = data?.variants ?? {};
    const push = (id: string, label: string) => {
      const s = v[id];
      if (s?.probabilities) {
        out.push({
          label,
          probs: COUNT_OPTIONS.map((o) => s.probabilities?.[o] ?? 0),
          note: `${s.instructions ?? ""} → ${s.choice} (confidence ${fmt(s.confidence)})`,
        });
      }
    };
    push("e1_breasts_choice", "E1 · average human, breasts");
    push("e3_breasts_random_person", "E3 · one person at random");
    push("e3_breasts_most", "E3 · most human beings");
    push("e4_breasts_reversed", "E4 · reversed option order");
    push("e5_planted", "E5 · planted statement");
    push("e2_maria_breasts", "E2 · Maria");
    return out;
  }, [data]);

  return (
    <Figure
      eyebrow="Widget 3 · Choice confidence explorer"
      title="Choice returns a full distribution; `confidence` is one summary of how peaked it is."
      hint="Confidence is computed from the answer itself, so a confidently wrong answer and a confidently right one look identical here. Compare the three summaries on the E3 “one person at random” preset: the argmax wins by a small margin, and all three statistics say so in different units."
    >
      <div className="grid gap-4 md:grid-cols-[1fr_auto]">
        <div className="space-y-2">
          {COUNT_OPTIONS.map((opt, i) => (
            <Slider
              key={opt}
              id={`choice-${opt}`}
              label={opt}
              value={weights[i]}
              onChange={(v) => setWeights((w) => w.map((x, j) => (j === i ? v : x)))}
              display={fmt(probs[i])}
              swatch={colorFor(opt, i)}
            />
          ))}
          <div className="flex flex-wrap gap-2 pt-2">
            {presets.map((p) => (
              <button
                key={p.label}
                type="button"
                title={p.note}
                onClick={() => setWeights(p.probs.map((x) => Math.round(x * 1000) / 10))}
                className="border border-border bg-background px-2.5 py-1 text-xs hover:bg-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2 md:w-64 md:grid-cols-1">
          <Stat label="choice (argmax)" value={COUNT_OPTIONS[topIdx]} sub={`p_max = ${fmt(sorted[0])}`} />
          <Stat label={`confidence = (p_max − 1/${n}) / (1 − 1/${n})`} value={fmt(confidence)} />
          <Stat label="Alternative: top probability" value={fmt(sorted[0])} />
          <Stat label="Alternative: top ÷ second" value={ratio === null ? "∞" : `${ratio.toFixed(1)}×`} />
        </div>
      </div>
    </Figure>
  );
}
