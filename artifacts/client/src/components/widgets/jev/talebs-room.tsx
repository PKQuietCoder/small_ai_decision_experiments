import { useMemo, useState } from "react";
import { Figure, Missing, Segmented, Slider, Stat, fmt, type WidgetProps } from "./shared";

const ROOM_SIZE = 20;

interface Person {
  index: number;
  sex: "woman" | "man";
  breasts: number;
  testicles: number;
}

function PersonGlyph({ person, active }: { person: Person; active: boolean }) {
  return (
    <svg viewBox="0 0 24 40" className="h-10 w-6" aria-hidden>
      <circle cx="12" cy="6" r="5" fill="currentColor" />
      <rect x="6" y="13" width="12" height="15" fill="currentColor" />
      <rect x="6" y="29" width="4.5" height="10" fill="currentColor" />
      <rect x="13.5" y="29" width="4.5" height="10" fill="currentColor" />
      {active && <rect x="0.5" y="0.5" width="23" height="39" fill="none" stroke="currentColor" strokeWidth="1" />}
      <title>{`${person.sex === "woman" ? "Woman" : "Man"}: ${person.breasts} breasts, ${person.testicles} testicles`}</title>
    </svg>
  );
}

/** Taleb's room: a population whose mean nobody occupies. */
export function TalebsRoom({ data }: WidgetProps) {
  const [womenPct, setWomenPct] = useState(50);
  const [view, setView] = useState<"people" | "mean">("people");
  const [hovered, setHovered] = useState<number | null>(null);

  const people = useMemo<Person[]>(() => {
    const women = Math.round((ROOM_SIZE * womenPct) / 100);
    return Array.from({ length: ROOM_SIZE }, (_, i) =>
      i < women
        ? { index: i, sex: "woman", breasts: 2, testicles: 0 }
        : { index: i, sex: "man", breasts: 0, testicles: 2 },
    );
  }, [womenPct]);
  const women = people.filter((p) => p.sex === "woman").length;
  const meanBreasts = (2 * women) / ROOM_SIZE;
  const meanTesticles = (2 * (ROOM_SIZE - women)) / ROOM_SIZE;
  const anyoneHasMean =
    people.some((p) => p.breasts === meanBreasts) || people.some((p) => p.testicles === meanTesticles);

  const jevBreasts = data?.e1?.breasts?.choice;
  const jevTesticles = data?.e1?.testicles?.choice;
  const codeMeans = data?.e2?.codeMeans;

  return (
    <Figure
      eyebrow="Widget 1 · Taleb's room"
      title="Twenty adults. Move the slider; switch between the people and their mean."
      hint="At an even split the mean is one breast and one testicle, and no figure in the room has either. Jev's answer to the naive question sits under the composite: it reports the room's mean as if it were a count."
    >
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <Segmented
          label="View"
          value={view}
          onChange={(v) => setView(v as "people" | "mean")}
          options={[
            { value: "people", label: "Show the people" },
            { value: "mean", label: "Show the mean" },
          ]}
        />
        <div className="min-w-[14rem] flex-1">
          <Slider
            id="room-women"
            label="Share of women"
            value={womenPct}
            step={5}
            onChange={setWomenPct}
            display={`${womenPct}%`}
          />
        </div>
      </div>

      {view === "people" ? (
        <div>
          <div className="grid grid-cols-10 gap-1 text-foreground" onMouseLeave={() => setHovered(null)}>
            {people.map((p) => (
              <button
                key={p.index}
                type="button"
                className="flex justify-center py-1 hover:bg-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                onMouseEnter={() => setHovered(p.index)}
                onFocus={() => setHovered(p.index)}
                aria-label={`${p.sex}: ${p.breasts} breasts, ${p.testicles} testicles`}
              >
                <PersonGlyph person={p} active={hovered === p.index} />
              </button>
            ))}
          </div>
          <p className="mt-2 h-5 text-xs text-muted-foreground">
            {hovered === null
              ? "Hover or focus a figure to read their counts."
              : `${people[hovered].sex === "woman" ? "A woman" : "A man"}: ${people[hovered].breasts} breasts, ${people[hovered].testicles} testicles.`}
          </p>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-3 py-2 sm:flex-row sm:justify-center sm:gap-8">
          <svg viewBox="0 0 24 40" className="h-28 w-16 text-foreground" aria-hidden>
            <circle cx="12" cy="6" r="5" fill="currentColor" />
            <rect x="6" y="13" width="12" height="15" fill="currentColor" />
            <rect x="6" y="29" width="4.5" height="10" fill="currentColor" />
            <rect x="13.5" y="29" width="4.5" height="10" fill="currentColor" />
          </svg>
          <div className="grid grid-cols-2 gap-2">
            <Stat label="Mean breasts per person" value={fmt(meanBreasts)} />
            <Stat label="Mean testicles per person" value={fmt(meanTesticles)} />
            <p className="col-span-2 text-xs text-muted-foreground">
              {anyoneHasMean
                ? "At this split the mean coincides with a real person."
                : "Nobody in the room has these counts. The figure above is a summary, not a person."}
            </p>
          </div>
        </div>
      )}

      {jevBreasts && jevTesticles ? (
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          <Stat
            label="Jev, asked for the average human's breasts (E1)"
            value={jevBreasts.choice ?? "—"}
            sub={`P = ${fmt(jevBreasts.probabilities?.[jevBreasts.choice ?? ""])} · confidence ${fmt(jevBreasts.confidence)}`}
          />
          <Stat
            label="Jev, asked for the average human's testicles (E1)"
            value={jevTesticles.choice ?? "—"}
            sub={`P = ${fmt(jevTesticles.probabilities?.[jevTesticles.choice ?? ""])} · confidence ${fmt(jevTesticles.confidence)}`}
          />
          {codeMeans && (
            <p className="text-xs text-muted-foreground sm:col-span-2">
              Built in code from Jev's per-person answers (E2): mean breasts {fmt(codeMeans.breasts, 1)}, mean testicles{" "}
              {fmt(codeMeans.testicles, 1)}.
            </p>
          )}
        </div>
      ) : (
        <div className="mt-4">
          <Missing what="The E1 answer" />
        </div>
      )}
    </Figure>
  );
}
