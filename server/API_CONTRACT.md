# LLM Decision Science — API Contract

The FastAPI backend serves JSON at the `/api` prefix. In the frontend, build URLs
as `` `${import.meta.env.BASE_URL}api/...` `` (BASE_URL is `/`, so this resolves to
`/api/...`). Do **not** use generated client hooks — call `fetch` directly.

In development, draft (unpublished) posts/experiments are included only when the
request carries `?preview=1`. In production they are always hidden.

---

## GET /api/healthz
```json
{ "status": "ok" }
```

## GET /api/site
Site-wide metadata for header/footer/about.
```json
{
  "title": "The Model Notebook",
  "tagline": "Field notes on language models — creativity, experiments, and science.",
  "description": "A file-based notebook of logs and findings on large language models ...",
  "author": "The Model Notebook",
  "categories": ["Creativity", "Experiments", "Science"],  // ordered category list for the feed filter
  "aboutHtml": "<p>...</p>"   // rendered HTML for the About page (from markdown)
}
```
(Additional keys may be present; treat the object as open. `aboutHtml` is server-rendered HTML and may be long.)

## GET /api/posts
Returns an array of post summaries (published only; drafts with `?preview=1`).
Ordered newest-first. Use for the home/feed page.
```json
[
  {
    "slug": "the-metaphor-effect",
    "title": "The Metaphor Effect: ...",
    "excerpt": "We hold a decision scenario perfectly constant ...",
    "category": "Experiment",
    "tags": ["framing", "metaphor", "decision-making", "prompting"],
    "date": "2026-06-18",
    "readingMinutes": 2,
    "featured": true,
    "published": true,
    "experimentId": "metaphor-effect"
  }
]
```

## GET /api/posts/{slug}
Full post. 404 if not found / not visible. Adds `bodyHtml` (rendered markdown,
already sanitized HTML — render with care) and `analysis` (live stats for charts).
```json
{
  "slug": "the-metaphor-effect",
  "title": "...",
  "excerpt": "...",
  "category": "Experiment",
  "tags": ["..."],
  "date": "2026-06-18",
  "readingMinutes": 2,
  "featured": true,
  "published": true,
  "experimentId": "metaphor-effect",
  "bodyHtml": "<h2 id=\"...\">...</h2>...",
  "analysis": { /* see Analysis object below; may be null if no run */ }
}
```

## GET /api/experiments
Array of experiment summaries (for an /experiments index page).
```json
[
  {
    "id": "metaphor-effect",
    "title": "The Metaphor Effect: ...",
    "summary": "We hold a decision scenario perfectly constant ...",
    "status": "published",
    "models": ["GPT-4o mini", "Claude 3.5 Haiku"],
    "variantCount": 6,
    "trialsPerCell": 25,
    "lastRunAt": "2026-06-18T22:48:38.559220+00:00",
    "totalRuns": 1,
    "postSlug": "the-metaphor-effect"
  }
]
```

## GET /api/experiments/{id}
Single experiment with its latest `analysis` object (same shape as in the post),
or analysis `null` if it has never been run. 404 if not found.

---

## Analysis object (drives all charts)
```jsonc
{
  "experimentId": "metaphor-effect",
  "experimentTitle": "The Metaphor Effect: ...",
  "runId": "20260618T224838Z-sample",
  "runDate": "2026-06-18T22:48:38.559220+00:00",
  "prompt": "You are advising the founder ...",   // full prompt text, preserve newlines
  "decisionOptions": [
    { "id": "A", "label": "Restructure leadership" },
    { "id": "B", "label": "Coach and support" },
    { "id": "C", "label": "Diagnose first" },
    { "id": "D", "label": "Push accountability" }
  ],
  "models": ["GPT-4o mini", "Claude 3.5 Haiku"],
  "variants": [
    { "id": "sinking_ship", "label": "Sinking ship", "metaphor": "a sinking ship" }
    // ... 6 total
  ],
  "primaryDecision": "A",
  "primaryDecisionLabel": "Restructure leadership",
  "totalTrials": 300,
  "trialsPerCell": 25,
  "parseFailures": 0,

  // Aggregated across all models, one row per variant. PRIMARY chart source.
  "byVariant": [
    {
      "variantId": "sinking_ship",
      "label": "Sinking ship",
      "metaphor": "a sinking ship",
      "total": 50,
      "counts":      { "A": 29, "B": 7, "C": 5, "D": 9 },
      "proportions": { "A": 0.58, "B": 0.14, "C": 0.10, "D": 0.18 },
      "ci": { "A": [0.4423, 0.7063], "B": [...], "C": [...], "D": [...] } // Wilson 95% CI [low, high]
    }
    // ... one per variant
  ],

  // Per variant AND per model (for grouped/faceted charts). No `ci`.
  "byVariantModel": [
    {
      "variantId": "sinking_ship",
      "label": "Sinking ship",
      "model": "GPT-4o mini",
      "total": 25,
      "counts":      { "A": 15, "B": 3, "C": 3, "D": 4 },
      "proportions": { "A": 0.60, "B": 0.12, "C": 0.12, "D": 0.16 }
    }
    // ... variants x models
  ],

  // Chi-square test of independence (metaphor vs decision), all models pooled.
  "overall": {
    "statistic": 194.2567,
    "pValue": 3.11e-33,
    "dof": 15,
    "significant": true,
    "cramersV": 0.4646,
    "testable": true
  },

  // Same test computed within each model.
  "perModel": [
    {
      "model": "GPT-4o mini",
      "chiSquare": {
        "statistic": 91.3636, "pValue": 5.52e-13, "dof": 15,
        "significant": true, "cramersV": 0.4506, "testable": true
      }
    }
  ]
}
```

### Charting guidance
- **Main chart:** grouped/stacked bars of `byVariant[*].proportions` keyed by
  `decisionOptions`, x-axis = variant `label`. Shows how the metaphor moves the
  decision mix. Optionally overlay Wilson CI from `ci`.
- **Per-model comparison:** use `byVariantModel` to facet by `model` or focus on
  the `primaryDecision` proportion per variant per model.
- **Significance callout:** surface `overall.pValue`, `overall.cramersV`,
  `overall.significant`, plus `perModel`.
- `proportions` already sum to ~1 per row; multiply by 100 for percentages.
- Handle `analysis: null` gracefully (experiment defined but not yet run).
