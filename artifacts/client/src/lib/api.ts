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
  total: number;
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

export interface ChiSquareResult {
  statistic: number;
  pValue: number;
  dof: number;
  significant: boolean;
  cramersV: number;
  testable: boolean;
}

export interface PerModelResult {
  model: string;
  chiSquare: ChiSquareResult;
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
