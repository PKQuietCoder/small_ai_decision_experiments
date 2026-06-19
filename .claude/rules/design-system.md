# Design system — "Nature Points of View" (trust through restraint)

The entire website uses one design language: the editorial, scientific-journal system imported
from the Claude Design project *"Nature Points of View Design System"* (distilled from the
*Nature Methods* "Points of View" column). **Its purpose is to convey trust** — through
restraint, perceptual rigor, and a colorblind-safe palette. Apply it to all pages and feature
work. When unsure, **remove** rather than add.

## Where it lives (don't recreate tokens)
- `artifacts/client/src/index.css` — the single source of truth. All tokens are CSS variables
  wired through Tailwind v4 `@theme`. Build UI from these tokens / Tailwind classes; do not
  introduce parallel color/spacing/radius systems.

## Hard constraints (these are the brand — do not violate)
- **Sharp corners.** Radius is `0`. Never add `rounded-2xl`/`rounded-3xl`/`rounded-[Npx]`. The
  only curves allowed are true circles (chart points, a small monogram) via `rounded-full`.
- **Flat.** No shadows (`--shadow-*` are `none`). Don't add `shadow-*`, `drop-shadow`, or
  hover elevation (`hover:-translate-y`, `hover:shadow-xl`). Hover = a color/border change only.
- **No decorative gradients.** No multi-color/indigo-purple "AI-slop" gradients, no glass, no
  `backdrop-blur`, no background images behind text. The only gradient ever allowed is the
  10–90% gray ramp for *sequential* data.
- **Color is earned.** Default surface is cream paper (`--background`), near-black ink
  (`--foreground`), warm hairline rules (`--border`). Color appears only where a fact needs
  emphasis.
- **Charts use the Wong palette only, for categorical encoding.** `--chart-1..5` are the
  colorblind-safe Wong colors (blue, vermilion, green, orange, purple); also available as
  `--color-wong-*`. Sequential data → gray ramp; never rainbow.
- **Type:** serif (`font-serif` = Spectral) for body/headings and article prose; sans
  (`font-sans` = Inter) for UI, labels, captions, eyebrows; mono (`font-mono` = JetBrains
  Mono) for code/data. Hierarchy via size/weight, **not color**. Headings are **sentence
  case**, never Title Case or ALL-CAPS (except the small-caps `.eyebrow` kicker).
- **Cards = whitespace + an optional hairline border.** A flat `--card` (paper-2) fill with a
  1px `border-border` and `rounded-none`. No shadow, no radius.
- **Spacing:** 8pt grid (Tailwind's 4px scale). Whitespace lives *between* content blocks.
- **Focus:** visible 2px ink outline (`--ring`). Accessibility is non-negotiable.
- **Motion:** ≤200ms, ease-out `cubic-bezier(0.2,0,0,1)`, only to express a state change.

## Voice — the default for ALL site content
Calm, authoritative, second-person, citation-anchored. **No emoji. No exclamation marks in
body copy. No marketing verbs** ("unleash", "supercharge", "delightful"). The work is the
value proposition. Captions use the Nature house style: bold figure number + vertical bar
("**Figure 1 |** …").

This restrained editorial voice is the **default** for everything: blog posts, the site UI,
docs, and READMEs. It is **not** overridden by the `persuasive-writing` skill. That skill's
marketing/persuasive voice is **opt-in** — apply it only when the user **explicitly** asks for
marketing or promotional copy (a landing page, pitch, ad copy, launch announcement). Absent an
explicit request, keep this voice.

## Reusable building blocks
- `.eyebrow` utility (small-caps sans kicker) — use for category/section labels.
- `.prose` is styled for the editorial reading experience (serif body, hairline-rule links
  that turn Wong-blue on hover, double-rule table headers, ink-rule pull quotes). Post bodies
  render inside it — no per-post styling needed.

## Applying it to new work
1. Use existing tokens/Tailwind classes (`bg-background`, `text-foreground`, `border`,
   `bg-card`, `text-muted-foreground`, `font-serif`, `bg-primary`, `text-destructive` for the
   vermilion accent, `chart-1..5`). They already encode the system.
2. Check the new UI against the hard constraints above before finishing — especially radius,
   shadow, gradient, and chart-color rules, which are the easiest to violate by habit.

## Source & IP note
Imported via the `claude_design` MCP from the project at
`claude.ai/design/p/019dee68-280f-7ad2-85dc-8db88243d7f1`. We implement the reusable *design
language* (tokens, type, components, palette, voice). We do **not** apply the third-party
*Nature* / *Nature Methods* journal wordmarks as this site's branding — the site uses its own
"LLM Decision Science" identity rendered in the system's typography.
