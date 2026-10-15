// In-article widgets. A post places `<div data-widget="<name>" markdown="1">…</div>`
// in its Markdown with a static fallback inside; pages/post.tsx portals the matching
// component into that slot after render. Names are stable public identifiers —
// renaming one breaks the posts that reference it.
import type { ComponentType } from "react";
import type { WidgetProps } from "./jev/shared";
import { TalebsRoom } from "./jev/talebs-room";
import { ScoreExplorer } from "./jev/score-explorer";
import { ChoiceExplorer } from "./jev/choice-explorer";
import { ArgmaxCollapse } from "./jev/argmax-collapse";
import { ParaphraseSpread } from "./jev/paraphrase-spread";
import { OrderShuffle } from "./jev/order-shuffle";
import { PlantedStatement } from "./jev/planted-statement";
import { NoulBattery } from "./jev/noul-battery";
import { DecisionSieve } from "./jev/decision-sieve";

export const WIDGETS: Record<string, ComponentType<WidgetProps>> = {
  "talebs-room": TalebsRoom,
  "score-explorer": ScoreExplorer,
  "choice-explorer": ChoiceExplorer,
  "argmax-collapse": ArgmaxCollapse,
  "paraphrase-spread": ParaphraseSpread,
  "order-shuffle": OrderShuffle,
  "planted-statement": PlantedStatement,
  "noul-battery": NoulBattery,
  "decision-sieve": DecisionSieve,
};
