import { useState } from "react";
import { Figure, Meter, Missing, ProbBars, Segmented, Stat, fmt, type WidgetProps } from "./shared";

/** E5: a planted, authoritative, false sentence in the state. */
export function PlantedStatement({ data }: WidgetProps) {
  const [condition, setCondition] = useState<"clean" | "planted">("clean");
  const e5 = data?.e5;
  if (!e5?.clean?.probabilities || !e5?.planted?.probabilities) {
    return (
      <Figure eyebrow="Widget 7 · Planted statement" title="E5" hint="—">
        <Missing what="The E5 comparison" />
      </Figure>
    );
  }
  const current = condition === "clean" ? e5.clean : e5.planted;
  const order = current.options ?? Object.keys(current.probabilities ?? {});

  return (
    <Figure
      eyebrow="Widget 7 · Planted statement (E5)"
      title="Flip the state between clean and planted and watch P(one) and confidence move together."
      hint="The planted note asserted the mean as a fact about every individual. It did not make Jev more confident; it made it less. P(one) and confidence fell together, and mass leaked to “other”. Confidence tracked the coherence of the state, not the truth of the planted claim."
    >
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <Segmented
          label="State"
          value={condition}
          onChange={(v) => setCondition(v as "clean" | "planted")}
          options={[
            { value: "clean", label: "Clean state" },
            { value: "planted", label: "With planted note" },
          ]}
        />
        <span className="text-xs text-muted-foreground">
          {condition === "planted" && e5.plantedNote ? (
            <span className="font-serif italic">“{e5.plantedNote}”</span>
          ) : (
            "Only the three facts about the room."
          )}
        </span>
      </div>
      <div className="grid gap-4 md:grid-cols-[1fr_16rem]">
        <div className="space-y-3">
          <ProbBars probabilities={current.probabilities ?? {}} order={order} highlight={current.choice} />
          <Meter label="confidence" value={current.confidence} />
        </div>
        <div className="grid grid-cols-2 gap-2 md:grid-cols-1">
          <Stat label="Δ P(one), planted − clean" value={fmt(e5.deltaPOne)} />
          <Stat label="Δ confidence" value={fmt(e5.deltaConfidence)} />
          <Stat label="argmax" value={e5.choiceChanged ? "changed" : "unchanged"} sub={`${e5.clean.choice} → ${e5.planted.choice}`} />
        </div>
      </div>
    </Figure>
  );
}
