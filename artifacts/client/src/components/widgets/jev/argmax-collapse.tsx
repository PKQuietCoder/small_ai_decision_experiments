import { useMemo, useState } from "react";
import { Figure, Missing, ProbBars, fmt, labelFor, type WidgetProps } from "./shared";

const CANDIDATES: { id: string; label: string }[] = [
  { id: "e3_breasts_random_person", label: "E3 · one person picked at random (breasts)" },
  { id: "e3_testicles_random_person", label: "E3 · one person picked at random (testicles)" },
  { id: "e5_planted", label: "E5 · planted statement" },
  { id: "e2_maria_breasts", label: "E2 · Maria, breasts" },
  { id: "e2_tom_testicles", label: "E2 · Tom, testicles" },
  { id: "e7_mixed", label: "E7 · the mixed option set" },
  { id: "e1_breasts_choice", label: "E1 · the naive question" },
];

/** The `choice` field is the argmax: one label standing in for a whole distribution. */
export function ArgmaxCollapse({ data }: WidgetProps) {
  const available = useMemo(
    () => CANDIDATES.filter((c) => data?.variants?.[c.id]?.probabilities),
    [data],
  );
  const [selected, setSelected] = useState(available[0]?.id ?? "");
  const [revealed, setRevealed] = useState(false);
  const answer = data?.variants?.[selected || (available[0]?.id ?? "")];

  if (!answer?.probabilities) {
    return (
      <Figure eyebrow="Widget 4 · Argmax collapse" title="The label and what it hides." hint="—">
        <Missing what="A Choice answer" />
      </Figure>
    );
  }
  const probs = answer.probabilities;
  const order = answer.options ?? Object.keys(probs);
  const top = answer.choice ?? order[0];
  const second = order.filter((o) => o !== top).sort((a, b) => (probs[b] ?? 0) - (probs[a] ?? 0))[0];

  return (
    <Figure
      eyebrow="Widget 4 · Argmax collapse"
      title="What the `choice` field says, and what the distribution behind it says."
      hint="On the “one person at random” question the label reads “other” while almost half the mass sits on “one”. The label is the modal answer; the distribution is the honest answer. Software that stores only the label has thrown the second away."
    >
      <label className="mb-3 block text-xs text-muted-foreground">
        Question
        <select
          value={selected || available[0]?.id}
          onChange={(e) => {
            setSelected(e.target.value);
            setRevealed(false);
          }}
          className="mt-1 block w-full border border-border bg-background px-2 py-1.5 text-xs text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        >
          {available.map((c) => (
            <option key={c.id} value={c.id}>
              {c.label}
            </option>
          ))}
        </select>
      </label>
      {answer.instructions && <p className="mb-4 font-serif text-base italic">“{answer.instructions}”</p>}
      <div className="grid gap-4 md:grid-cols-2">
        <div className="border border-border bg-background p-4">
          <p className="text-[11px] text-muted-foreground">choice</p>
          <p className="text-4xl font-semibold leading-none">{top.replace(/_/g, " ")}</p>
          <p className="mt-2 text-xs text-muted-foreground">confidence {fmt(answer.confidence)}</p>
          <button
            type="button"
            onClick={() => setRevealed((r) => !r)}
            aria-expanded={revealed}
            className="mt-4 border border-border bg-background px-2.5 py-1 text-xs hover:bg-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
          >
            {revealed ? "Hide the distribution" : "Reveal the distribution"}
          </button>
        </div>
        <div className={revealed ? "opacity-100 transition-opacity duration-200" : "opacity-30 transition-opacity duration-200"} aria-hidden={!revealed}>
          <p className="mb-2 text-[11px] text-muted-foreground">probabilities</p>
          <ProbBars probabilities={probs} order={order} highlight={top} />
          {revealed && second && (
            <p className="mt-3 text-xs text-muted-foreground">
              Margin over the runner-up “{labelFor(second)}”: {fmt((probs[top] ?? 0) - (probs[second] ?? 0))}.
            </p>
          )}
        </div>
      </div>
    </Figure>
  );
}
