// Methodology page: a high-level, plain-language description of how every study
// in the series works, written to apply to all experiments (current and future)
// rather than any single one. It closes with the layout of the open replication
// package so readers can reproduce a study themselves. Built from design-system
// tokens (serif prose, mono for the data layout, sentence-case headings, flat,
// sharp corners).

function Lead({ children }: { children: React.ReactNode }) {
  return <p className="text-xl text-foreground font-medium leading-relaxed mb-6">{children}</p>;
}

function Prose({ children }: { children: React.ReactNode }) {
  return <p className="font-serif text-lg leading-relaxed text-muted-foreground mb-6">{children}</p>;
}

function H2({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="font-serif text-2xl md:text-3xl font-semibold tracking-tight text-foreground mt-16 mb-5">
      {children}
    </h2>
  );
}

const STEPS: { title: string; body: string }[] = [
  {
    title: "Anchor on a human baseline",
    body: "We start from a classic, published study of human decision making and take its measured result as the point of comparison. That human number is what every model is held against.",
  },
  {
    title: "Rebuild the same decision",
    body: "We recreate the choice the original participants faced, written as a task a model can complete. Everything is held constant except the one thing under test.",
  },
  {
    title: "Run it across many models, many times",
    body: "Each condition is put to a range of current language models through their live APIs, and repeated over many independent trials rather than a single answer, so the result is a rate and not an anecdote.",
  },
  {
    title: "Change one thing at a time",
    body: "Conditions differ by a single deliberate manipulation: the wording, the framing, or the options on offer. Any shift in behavior can then be traced to that one change.",
  },
];

const VERDICTS: { term: string; body: string }[] = [
  { term: "Copy", body: "the model reproduces the human bias at a comparable size." },
  { term: "Smooth", body: "the model damps the bias toward noise, or removes it entirely." },
  { term: "Amplify", body: "the model shows the bias more strongly than people do." },
];

const PACKAGE_LAYOUT = `experiments/<id>/
├── README.md        design, results, and how to replicate (when present)
├── manifest.json    start here: models, conditions, human baseline, run ids
├── methodology/     the experiment as code: the config, the exact prompts,
│                    the tool definitions or judge rubric, the human baseline
├── raw/             every trial exactly as it was recorded
│   ├── runs/...     full per-trial data (each answer or tool transcript)
│   └── trials.csv   all trials flattened into one table
├── results/         the computed numbers behind the charts
│   ├── analysis/... counts, proportions, intervals, significance, baseline
│   ├── summary_by_condition.csv
│   └── significance.csv
└── followups/       extra controls, when a study has them`;

export default function Methodology() {
  return (
    <div className="container mx-auto px-4 md:px-6 py-12 md:py-20 max-w-3xl">
      <header className="mb-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <p className="eyebrow mb-3">Methodology</p>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground font-serif mb-6">
          How the experiments work
        </h1>
        <Lead>
          Every entry in this series follows the same recipe. We take a classic finding about
          human decision making, one with a measured human baseline, and put the same decision to
          today's language models. The aim is not a single clever example but a fair test, run
          many times across many models, that anyone can check or run again.
        </Lead>
      </header>

      <H2>The question behind every study</H2>
      <Prose>
        Decades of research show that people do not decide by pure reason. We follow predictable
        shortcuts: a number seen first pulls the next one toward it, the framing of a question
        flips the answer, the way a choice is split changes what we pick. As more decisions are
        handed to language models, and to agents that act over several steps, one question turns
        from philosophical to empirical: do these models inherit our biases, dampen them, or
        invent new ones of their own? Each study answers that for one classic effect at a time.
      </Prose>

      <H2>From a human baseline to a model test</H2>
      <Prose>
        The method is deliberately identical for every experiment, so results stay comparable
        across studies and the same approach extends cleanly to new ones.
      </Prose>
      <ol className="my-8 space-y-6">
        {STEPS.map((s, i) => (
          <li key={s.title} className="flex gap-4">
            <span className="font-mono text-sm text-muted-foreground pt-1 tabular-nums">
              {String(i + 1).padStart(2, "0")}
            </span>
            <div>
              <h3 className="font-serif text-lg font-semibold text-foreground mb-1">{s.title}</h3>
              <p className="font-serif text-lg leading-relaxed text-muted-foreground">{s.body}</p>
            </div>
          </li>
        ))}
      </ol>

      <H2>Reading the result: copy, smooth, amplify</H2>
      <Prose>
        Three words carry the verdict of every entry, always measured against the original study's
        human baseline.
      </Prose>
      <dl className="my-8 space-y-4">
        {VERDICTS.map((v) => (
          <div key={v.term} className="border-l-2 border-border pl-4">
            <dt className="inline font-serif text-lg font-semibold text-foreground">{v.term}: </dt>
            <dd className="inline font-serif text-lg leading-relaxed text-muted-foreground">
              {v.body}
            </dd>
          </div>
        ))}
      </dl>
      <Prose>
        Every verdict rests on the numbers, not impressions. We report each condition's choice
        share with confidence intervals, test whether the differences between conditions are
        statistically significant, and overlay the human baseline for direct comparison. Where a
        result could be explained by a model simply recognizing a famous experiment, a control
        re-runs it on unfamiliar material, so neither a flat nor a strong finding can be dismissed
        as mere recall.
      </Prose>

      <H2>Replicate it yourself</H2>
      <Prose>
        Nothing here is a black box. Every experiment ships as a self-contained package in the
        project's GitHub repository, under <span className="font-mono text-base">experiments/&lt;id&gt;/</span>.
        You do not need this codebase to use it: the package is provider-agnostic, so a study can
        be reproduced with any stack.
      </Prose>
      <figure className="my-8">
        <pre className="border border-border bg-card p-4 md:p-5 overflow-x-auto font-mono text-xs md:text-sm leading-relaxed text-foreground">
          {PACKAGE_LAYOUT}
        </pre>
        <figcaption className="mt-3 text-sm text-muted-foreground font-sans">
          <span className="font-semibold text-foreground">Figure 1 |</span> The layout of an
          experiment's replication package. Each folder is regenerated from the recorded runs, so
          the prompts, the raw answers, and the computed results all trace back to the same data.
        </figcaption>
      </figure>
      <Prose>
        Start with <span className="font-mono text-base">manifest.json</span> for the models,
        conditions, and human baseline; read the exact prompts in{" "}
        <span className="font-mono text-base">methodology/</span>; and check the recorded answers
        in <span className="font-mono text-base">raw/</span> against the computed{" "}
        <span className="font-mono text-base">results/</span>. Re-run an entry, recode it, or
        recompute the statistics. If you reach a different answer, that is a result worth reporting.
      </Prose>
    </div>
  );
}
