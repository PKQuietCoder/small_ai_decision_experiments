// Methodology page: rendered SVG block diagrams of the experiment pipeline,
// with the most detail on the agentic tool-use path. All diagrams are built from
// the design-system tokens (sharp corners, flat, Wong palette, serif/sans/mono),
// and are theme-aware via hsl(var(--...)) so they adapt to light/dark.

const INK = "hsl(var(--foreground))";
const CARD = "hsl(var(--card))";
const RULE = "hsl(var(--border))";
const MUTED = "hsl(var(--muted-foreground))";
const BLUE = "hsl(var(--chart-1))"; // Wong blue — the measured decision / outcome
const VERM = "hsl(var(--chart-2))"; // Wong vermilion — the agentic path / manipulation
const SANS = "var(--app-font-sans)";
const MONO = "var(--app-font-mono)";

type Row = { t: string; mono?: boolean; size?: number; fill?: string; weight?: number };

function ArrowDefs() {
  return (
    <defs>
      <marker
        id="mk-arrow"
        markerWidth="9"
        markerHeight="9"
        refX="7.5"
        refY="3"
        orient="auto"
        markerUnits="userSpaceOnUse"
      >
        <path d="M0,0 L7.5,3 L0,6 Z" fill={INK} />
      </marker>
    </defs>
  );
}

function Block({
  x,
  y,
  w,
  h,
  rows,
  accent,
  dashed,
  fill = CARD,
}: {
  x: number;
  y: number;
  w: number;
  h: number;
  rows: Row[];
  accent?: string;
  dashed?: boolean;
  fill?: string;
}) {
  const stroke = accent ?? RULE;
  const lineH = 15;
  const firstBaseline = y + h / 2 - ((rows.length - 1) * lineH) / 2 + 4;
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={w}
        height={h}
        fill={fill}
        stroke={stroke}
        strokeWidth={accent ? 1.6 : 1}
        strokeDasharray={dashed ? "4 3" : undefined}
      />
      {rows.map((r, i) => (
        <text
          key={i}
          x={x + w / 2}
          y={firstBaseline + i * lineH}
          textAnchor="middle"
          fontFamily={r.mono ? MONO : SANS}
          fontSize={r.size ?? 11.5}
          fontWeight={r.weight ?? (i === 0 ? 600 : 400)}
          fill={r.fill ?? (i === 0 ? INK : MUTED)}
        >
          {r.t}
        </text>
      ))}
    </g>
  );
}

function Arrow({
  x1,
  y1,
  x2,
  y2,
  dashed,
  label,
  lx,
  ly,
}: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  dashed?: boolean;
  label?: string;
  lx?: number;
  ly?: number;
}) {
  return (
    <g>
      <line
        x1={x1}
        y1={y1}
        x2={x2}
        y2={y2}
        stroke={INK}
        strokeWidth={1.3}
        markerEnd="url(#mk-arrow)"
        strokeDasharray={dashed ? "4 3" : undefined}
      />
      {label && (
        <text
          x={lx ?? (x1 + x2) / 2}
          y={ly ?? (y1 + y2) / 2 - 4}
          textAnchor="middle"
          fontFamily={SANS}
          fontSize={9.5}
          fill={MUTED}
        >
          {label}
        </text>
      )}
    </g>
  );
}

function ColHeader({ x, y, label }: { x: number; y: number; label: string }) {
  return (
    <text
      x={x}
      y={y}
      textAnchor="middle"
      fontFamily={SANS}
      fontSize={10}
      fontWeight={600}
      letterSpacing="0.08em"
      fill={MUTED}
      style={{ textTransform: "uppercase" } as React.CSSProperties}
    >
      {label}
    </text>
  );
}

function Figure({
  n,
  title,
  vb,
  minW = 560,
  children,
}: {
  n: number;
  title: string;
  vb: string;
  minW?: number;
  children: React.ReactNode;
}) {
  return (
    <figure className="my-10">
      <div className="border border-border bg-background p-4 md:p-6 overflow-x-auto">
        <svg
          viewBox={vb}
          width="100%"
          role="img"
          aria-label={`Figure ${n}. ${title}`}
          className="block"
          style={{ minWidth: minW }}
        >
          <ArrowDefs />
          {children}
        </svg>
      </div>
      <figcaption className="mt-3 text-sm text-muted-foreground font-sans">
        <span className="font-semibold text-foreground">Figure {n} |</span> {title}
      </figcaption>
    </figure>
  );
}

/* ---------------------------------------------------------------- Figure 1 */
function PipelineDiagram() {
  const cx = 360;
  return (
    <>
      <Block x={180} y={14} w={360} h={54} accent={INK} rows={[{ t: "content/experiments/<id>.yaml", mono: true, size: 11 }, { t: "the one file authored by hand" }]} />
      <Arrow x1={cx} y1={68} x2={cx} y2={100} />
      <Block x={180} y={100} w={360} h={54} rows={[{ t: "engine.run_experiment()", mono: true, size: 11 }, { t: "fan out: models × variants × trials" }]} />
      <Arrow x1={cx} y1={154} x2={cx} y2={186} />
      <Block x={180} y={186} w={360} h={54} rows={[{ t: "content/runs/<id>/<runId>.json", mono: true, size: 11 }, { t: "raw per-trial records" }]} />
      <Arrow x1={cx} y1={240} x2={cx} y2={272} />
      <Block x={180} y={272} w={360} h={54} rows={[{ t: "content_store.build_analysis()", mono: true, size: 11 }, { t: "counts · χ² · Cramér's V · baseline overlay" }]} />
      <Arrow x1={cx} y1={326} x2={cx} y2={358} />
      <Block x={180} y={358} w={360} h={54} accent={BLUE} rows={[{ t: "content/analysis/<id>/<runId>.json", mono: true, size: 11 }, { t: "the shape the charts consume" }]} />
      <Arrow x1={cx} y1={412} x2={200} y2={446} />
      <Arrow x1={cx} y1={412} x2={520} y2={446} />
      <Block x={60} y={446} w={280} h={54} rows={[{ t: "FastAPI /api → React + Recharts" }, { t: "live charts" }]} />
      <Block x={380} y={446} w={280} h={54} rows={[{ t: "posts/<slug>.md", mono: true, size: 11 }, { t: "editable draft, then curated" }]} />
    </>
  );
}

/* ---------------------------------------------------------------- Figure 2 */
function FanoutDiagram() {
  return (
    <>
      <ColHeader x={129} y={28} label="one run" />
      <Block x={24} y={56} w={210} h={90} rows={[{ t: "models × variants" }, { t: "× trials_per_cell" }, { t: "→ flat task list", fill: MUTED }]} />
      <Arrow x1={234} y1={101} x2={276} y2={101} />
      <Block x={276} y={71} w={170} h={60} rows={[{ t: "ThreadPoolExecutor" }, { t: "MAX_WORKERS = 8", mono: true, size: 10 }]} />
      <Arrow x1={446} y1={101} x2={496} y2={101} />
      <Block x={496} y={71} w={200} h={60} rows={[{ t: "run JSON", mono: true, size: 11 }, { t: "written back by index" }]} />
    </>
  );
}

/* ---------------------------------------------------------------- Figure 3 */
function TypesDiagram() {
  return (
    <>
      <Block x={210} y={14} w={300} h={46} rows={[{ t: "run_task(trial)", mono: true, size: 11 }, { t: "branch on experiment type", size: 10 }]} />
      <Arrow x1={360} y1={60} x2={126} y2={116} />
      <Arrow x1={360} y1={60} x2={360} y2={116} />
      <Arrow x1={360} y1={60} x2={594} y2={116} />
      <Block x={20} y={116} w={212} h={92} rows={[{ t: "fill_in_blank_decision", mono: true, size: 10.5 }, { t: "decide()", mono: true, size: 10, fill: INK }, { t: "one forced choice", size: 10 }, { t: "from an enum", size: 10 }]} />
      <Block x={254} y={116} w={212} h={92} rows={[{ t: "open_response", mono: true, size: 10.5 }, { t: "respond() → free text", mono: true, size: 10, fill: INK }, { t: "then a judge model", size: 10 }, { t: "codes it", size: 10 }]} />
      <Block x={488} y={116} w={212} h={92} accent={VERM} rows={[{ t: "agentic_budget", mono: true, size: 10.5 }, { t: "run_tool_sequence()", mono: true, size: 10, fill: INK }, { t: "multi-step tool use", size: 10 }, { t: "(see Figure 4)", size: 10 }]} />
      <Arrow x1={126} y1={208} x2={126} y2={244} />
      <Arrow x1={360} y1={208} x2={360} y2={244} />
      <Arrow x1={594} y1={208} x2={594} y2={244} />
      <Block x={20} y={244} w={680} h={40} dashed rows={[{ t: "the decision is always read from a constrained enum — never regex-parsed", size: 11 }]} />
    </>
  );
}

/* ---------------------------------------------------------------- Figure 4 */
function AgenticDiagram() {
  return (
    <>
      <Block x={60} y={12} w={600} h={56} rows={[{ t: "scenario prompt (shared, brace-free)  +  tool definitions" }, { t: "strict schemas · exactly one terminal tool · decision field = closed enum", size: 10 }]} />
      <Arrow x1={360} y1={68} x2={360} y2={86} />
      <line x1={360} y1={86} x2={360} y2={392} stroke={RULE} strokeWidth={1} strokeDasharray="3 3" />
      <ColHeader x={182} y={104} label="forced sequence — controlled" />
      <ColHeader x={538} y={104} label="autonomous — observational" />

      {/* left: forced chain */}
      <Block x={44} y={116} w={276} h={42} rows={[{ t: "force  set_budget", mono: true, size: 11 }]} />
      <Arrow x1={182} y1={158} x2={182} y2={170} />
      <Block x={44} y={170} w={276} h={42} rows={[{ t: "force  inspect_options", mono: true, size: 11 }]} />
      <Arrow x1={182} y1={212} x2={182} y2={224} />
      <Block x={44} y={224} w={276} h={42} rows={[{ t: "force  choose_product  (terminal)", mono: true, size: 10.5 }]} />
      <Arrow x1={182} y1={266} x2={182} y2={278} />
      <Block x={44} y={278} w={276} h={44} accent={BLUE} rows={[{ t: "read decision from enum" }]} />
      <Block x={44} y={336} w={276} h={44} dashed rows={[{ t: "intermediate tools return a synthetic ack —", size: 10 }, { t: "only the partition count varies", size: 10 }]} />

      {/* right: autonomous loop */}
      <Block x={400} y={116} w={276} h={62} rows={[{ t: "force SOME tool — model picks which", size: 10.5 }, { t: "record args + synthetic ack", size: 10 }, { t: "repeat until it calls the terminal tool", size: 9.5, fill: MUTED }]} />
      <path d="M676 134 H690 V160 H677" fill="none" stroke={INK} strokeWidth={1.3} markerEnd="url(#mk-arrow)" />
      <Arrow x1={500} y1={180} x2={466} y2={300} label="terminal" lx={452} ly={250} />
      <Arrow x1={576} y1={180} x2={610} y2={300} dashed label="cap hit" lx={628} ly={250} />
      <Block x={400} y={300} w={130} h={56} accent={BLUE} rows={[{ t: "terminal called →", size: 10 }, { t: "read decision", size: 10, fill: INK }]} />
      <Block x={546} y={300} w={130} h={56} dashed rows={[{ t: "cap → force one", size: 10 }, { t: "terminal (capped)", size: 10 }]} />
    </>
  );
}

/* ---------------------------------------------------------------- Figure 5 */
function ProviderDiagram() {
  const code = (t: string, size = 10) => ({ t, mono: true, size, fill: INK, weight: 400 });
  return (
    <>
      <ColHeader x={190} y={28} label="Anthropic — messages API" />
      <ColHeader x={530} y={28} label="OpenAI — Responses API" />
      <Block
        x={40}
        y={44}
        w={300}
        h={190}
        rows={[
          code("messages.create(...)", 10.5),
          code("tool_choice = {type: tool | any}"),
          code("disable_parallel_tool_use"),
          code("append assistant + tool_result"),
          code("read block.input[decision_key]"),
        ]}
      />
      <Block
        x={380}
        y={44}
        w={300}
        h={190}
        rows={[
          code("responses.create(...)", 10.5),
          code("tool_choice = {type: function} | required", 9.5),
          code("parallel_tool_calls = false · reasoning", 9.5),
          code("chain: previous_response_id +", 10),
          code("function_call_output", 10),
          code("read function_call.arguments[...]", 9.5),
        ]}
      />
      <Arrow x1={190} y1={234} x2={190} y2={250} />
      <Arrow x1={530} y1={234} x2={530} y2={250} />
      <Block x={40} y={250} w={640} h={38} accent={INK} rows={[{ t: "same return contract  →  (decision, transcript)", mono: true, size: 11, fill: INK }]} />
    </>
  );
}

function Prose({ children }: { children: React.ReactNode }) {
  return <p className="font-serif text-lg leading-relaxed text-muted-foreground mb-6">{children}</p>;
}

function H2({ children }: { children: React.ReactNode }) {
  return <h2 className="font-serif text-2xl md:text-3xl font-semibold tracking-tight text-foreground mt-16 mb-5">{children}</h2>;
}

export default function Methodology() {
  return (
    <div className="container mx-auto px-4 md:px-6 py-12 md:py-20 max-w-3xl">
      <header className="mb-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <p className="eyebrow mb-3">Methodology</p>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground font-serif mb-6">
          How the experiments run
        </h1>
        <p className="text-xl text-foreground font-medium">
          Every study is one configuration file run through a fixed pipeline. Nothing is hand-picked:
          each result is aggregated from hundreds of live API calls, and the model's choice is read from
          a constrained field, never parsed from prose. The diagrams below trace that pipeline, with the
          most detail on the agentic path — where the model takes a sequence of tool-calling steps rather
          than answering in one shot.
        </p>
      </header>

      <H2>The pipeline</H2>
      <Prose>
        An experiment is a single YAML config; everything downstream is derived and stored as a file.
        The engine expands the config into trials and writes raw per-trial records; an aggregation step
        turns those into the analysis JSON that the charts and posts read. Because each stage is a file on
        disk, any run can be re-derived, recoded, or checked independently.
      </Prose>
      <Figure n={1} title="One configuration file is expanded into runs, aggregated into analysis, and rendered as a post with live charts." vb="0 0 720 520" minW={520}>
        <PipelineDiagram />
      </Figure>

      <H2>One run</H2>
      <Prose>
        A run executes one model across the full grid of variants (the conditions) and trials per cell.
        The work fans out across a small thread pool; results are written back into a pre-sized array by
        index, so the recorded order is deterministic regardless of which trial finishes first.
      </Prose>
      <Figure n={2} title="A run expands models × variants × trials into a task list, executes it concurrently, and records results in a stable order." vb="0 0 720 170" minW={520}>
        <FanoutDiagram />
      </Figure>

      <H2>Three trial types</H2>
      <Prose>
        The <span className="font-mono text-base">type</span> field selects how a single trial is run. A
        forced single choice uses provider-enforced structured output; a free-text study has the model
        answer in prose, then a fixed judge model codes that answer into categories; an agentic study has
        the model take a sequence of tool-calling steps. In every case the final decision is read from a
        closed enum, not extracted heuristically.
      </Prose>
      <Figure n={3} title="The experiment type routes each trial to one of three mechanics; all three resolve to a decision read from a constrained enum." vb="0 0 720 300" minW={560}>
        <TypesDiagram />
      </Figure>

      <H2>The agentic trial</H2>
      <Prose>
        This is the part most LLM-bias work omits: rather than a single survey answer, the model acts as
        an agent that takes steps. The variant defines the manipulation, and that manipulation is
        expressed as the <em>structure of the tool calls</em> — how many steps the decision is broken
        into, or which options are on the menu — never as a change to the underlying question. Two modes
        share one engine.
      </Prose>
      <Prose>
        In the <strong className="text-foreground font-semibold">forced sequence</strong>, exactly one
        tool is pinned per turn; intermediate tools return only a synthetic acknowledgement, so the model
        never receives new information and the only thing that varies across conditions is the partition.
        In the <strong className="text-foreground font-semibold">autonomous</strong> condition the model
        is forced to call some tool each turn but chooses which, looping until it calls the terminal tool
        on its own (or a step cap forces one final terminal turn).
      </Prose>
      <Figure n={4} title="The agentic engine in both modes. Forced conditions isolate the partition; the autonomous condition records the model's own trajectory. Blue marks where the measured decision is read." vb="0 0 720 400" minW={640}>
        <AgenticDiagram />
      </Figure>

      <H2>Per-turn mechanics, by provider</H2>
      <Prose>
        Both providers implement the same forced and autonomous semantics, but through different APIs.
        Anthropic uses the messages API with forced tool use and synthetic tool results. OpenAI's
        reasoning models reject function tools on chat completions, so that path uses the Responses API,
        chaining turns by reference so the reasoning context carries across calls. Either way the engine
        returns the same pair: the decision plus a transcript of the steps taken.
      </Prose>
      <Figure n={5} title="The Anthropic and OpenAI tool-use paths differ in API surface but return an identical decision-plus-transcript contract." vb="0 0 720 300" minW={560}>
        <ProviderDiagram />
      </Figure>

      <H2>What the numbers are</H2>
      <Prose>
        Aggregation computes each condition's choice share with Wilson intervals, a chi-square test of
        independence with Cramér's V across conditions, and — for agentic studies — mean spend and a
        step-trajectory summary the categorical chart cannot express. Where a human baseline exists, it is
        overlaid for comparison. Each published study also carries a recognition control, so a flat result
        cannot be dismissed as the model merely recognizing a famous paradigm. The exact prompts, every
        trial, and the analysis behind each chart are linked from the study itself.
      </Prose>
    </div>
  );
}
