export interface SiteInfo {
  title: string;
  tagline: string;
  intro: string;
  description: string;
  author: string;
  authorUrl?: string;
  categories?: string[];
  types?: string[];
  aboutHtml: string;
  [key: string]: any;
}

export interface PostSummary {
  slug: string;
  title: string;
  excerpt: string;
  type?: string;
  category: string;
  tags: string[];
  date: string;
  readingMinutes: number;
  featured: boolean;
  published: boolean;
  // Listed as a grayed, non-clickable "Coming soon" placeholder; its detail page is
  // withheld by the API (404 in production).
  comingSoon?: boolean;
  experimentId?: string;
  // Headline verdict vs. the human baseline ("copy" | "smooth" | "amplify") and a
  // one-line summary of the recognition/replication controls. Both optional.
  verdict?: string;
  controls?: string;
}

export interface DecisionOption {
  id: string;
  label: string;
}

export interface Variant {
  id: string;
  label: string;
  metaphor?: string;
  [key: string]: any;
}

export interface ByVariantData {
  variantId: string;
  label: string;
  metaphor?: string;
  // null for proportion-only rows (human baselines, probe mean probabilities).
  total: number | null;
  counts: Record<string, number>;
  proportions: Record<string, number>;
  ci?: Record<string, [number, number]>;
}

export interface ByVariantModelData {
  variantId: string;
  label: string;
  model: string;
  total: number;
  counts: Record<string, number>;
  proportions: Record<string, number>;
}

// Statistics are null when the table is degenerate (`testable: false`), e.g. a
// fully saturated table or a systemone_probe run, which has no sampling to test.
export interface ChiSquareResult {
  statistic: number | null;
  pValue: number | null;
  dof: number | null;
  significant: boolean;
  cramersV: number | null;
  testable: boolean;
}

export interface PerModelResult {
  model: string;
  chiSquare: ChiSquareResult;
}

// ---- systemone_probe (TypeSafe Jev) ---------------------------------------
// One typed question per variant, answered with a probability distribution.
// Shapes mirror server/experiments/systemone_analysis.py; see API_CONTRACT.md.
export interface ProbeAnswer {
  variantId: string;
  label: string;
  experiment?: string | null;
  organ?: string | null;
  questionType: "choice" | "score" | "noul";
  instructions?: string | null;
  trials: number;
  latencyMs?: number | null;
  // choice
  options?: string[];
  probabilities?: Record<string, number>;
  choice?: string;
  choices?: string[];
  confidence?: number | null;
  confidenceRecomputed?: number | null;
  topProbability?: number;
  topToSecondRatio?: number | null;
  // score
  levels?: string[];
  probabilitiesByLevel?: Record<string, number>;
  score?: number;
  scoreRecomputed?: number;
  modalLevel?: string;
  betweenLevels?: boolean;
  // noul
  p?: number;
  confidenceAbs?: number;
}

export interface ProbeSpreadRow {
  variantId: string;
  instructions?: string | null;
  probabilities: Record<string, number>;
  choice?: string;
  confidence?: number | null;
  phrasing?: string;
  order?: string;
  criteriaOrder?: string[];
}

export interface ProbeSpreadBlock {
  options: string[];
  perOption: Record<string, { mean: number; min: number; max: number; spread: number; sd?: number }>;
  maxSpread: number;
  maxSd?: number;
  distinctChoices: string[];
  meanOfMeans: Record<string, number>;
  meanChoice: string;
  phrasings?: ProbeSpreadRow[];
  orders?: ProbeSpreadRow[];
}

export interface SystemOneAnalysis {
  state: Record<string, string> | null;
  meta: {
    responseModels: string[];
    requestedModel: string | null;
    runId: string;
    startedAt: string;
    finishedAt: string;
    calls: number;
    okCalls: number;
    failedCalls: number;
    variants: number;
    experiments: string[];
    inputTokens: number;
    outputTokens: number;
    estimatedUsd: number;
    latencyMs: { mean: number | null; min: number | null; max: number | null; total: number | null };
  };
  variants: Record<string, ProbeAnswer>;
  confidenceCheck: {
    rows: { variantId: string; questionType: string; reported: number; recomputed: number; delta: number }[];
    maxAbsDelta: number;
  };
  sieve?: {
    items: { variantId: string; experiment: string | null; label: string; choice: string; confidence: number }[];
    count: number;
    byThreshold: { threshold: number; accepted: number; review: number; coverage: number | null }[];
  };
  e0?: {
    variantId: string;
    instructions?: string;
    n: number;
    options: string[];
    perTrial: { trial: number; probabilities: Record<string, number>; choice: string; confidence: number; latencyMs: number }[];
    mean: Record<string, number>;
    sd: Record<string, number>;
    maxSd: number;
    confidenceSd: number;
    distinctChoices: string[];
    docsReferenceMeanSd: number;
  };
  e1?: Record<string, { choice?: ProbeAnswer; score?: ProbeAnswer }>;
  e2?: {
    persons: { person: string; organ: string; variantId: string; probabilities: Record<string, number>; choice: string; confidence: number | null; integer: number | null }[];
    codeMeans: Record<string, number>;
  };
  e3?: Record<string, ProbeSpreadBlock>;
  e4?: Record<string, ProbeSpreadBlock>;
  e5?: {
    clean: ProbeAnswer;
    planted: ProbeAnswer;
    deltaPOne?: number;
    deltaConfidence?: number;
    choiceChanged?: boolean;
    plantedNote?: string | null;
  };
  e6?: ProbeAnswer & { state?: Record<string, string>; codeValue?: number; codeBucket?: string; agrees?: boolean | null };
  e7?: ProbeAnswer;
  e8?: {
    claims: { variantId: string; claim: string; instructions?: string | null; p: number; confidenceAbs: number }[];
    polarity?: { exactlyTwo: number; fewerThanTwo: number; sum: number; residual: number };
  };
}

export interface Analysis {
  experimentId: string;
  experimentTitle: string;
  runId: string;
  runDate: string;
  prompt: string;
  decisionOptions: DecisionOption[];
  models: string[];
  variants: Variant[];
  primaryDecision: string;
  primaryDecisionLabel: string;
  totalTrials: number;
  trialsPerCell: number;
  parseFailures: number;
  byVariant: ByVariantData[];
  byVariantModel: ByVariantModelData[];
  overall: ChiSquareResult;
  perModel: PerModelResult[];
  // Present only for systemone_probe experiments; when set, the post page renders
  // the in-article widgets instead of the generic chi-square chart.
  systemone?: SystemOneAnalysis;
}

export interface Post extends PostSummary {
  bodyHtml: string;
  analysis: Analysis | null;
}

export interface ExperimentSummary {
  id: string;
  title: string;
  summary: string;
  status: string;
  models: string[];
  variantCount: number;
  trialsPerCell: number;
  lastRunAt: string | null;
  totalRuns: number;
  postSlug?: string;
}

export interface Experiment extends ExperimentSummary {
  analysis: Analysis | null;
}

// Fetchers
const API_BASE = `${import.meta.env.BASE_URL.replace(/\/$/, "")}/api`;

async function fetchJson<T>(url: string): Promise<T> {
  const isDev = import.meta.env.DEV;
  const suffix = isDev ? "?preview=1" : "";
  const separator = url.includes("?") ? "&" : "?";
  const reqUrl = isDev ? `${url}${separator}preview=1` : url;
  
  const response = await fetch(reqUrl);
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Not Found");
    }
    throw new Error(`API Error: ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  getSite: () => fetchJson<SiteInfo>(`${API_BASE}/site`),
  getPosts: () => fetchJson<PostSummary[]>(`${API_BASE}/posts`),
  getPost: (slug: string) => fetchJson<Post>(`${API_BASE}/posts/${slug}`),
  getExperiments: () => fetchJson<ExperimentSummary[]>(`${API_BASE}/experiments`),
  getExperiment: (id: string) => fetchJson<Experiment>(`${API_BASE}/experiments/${id}`),
};
