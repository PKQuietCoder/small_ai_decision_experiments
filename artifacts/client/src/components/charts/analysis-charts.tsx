import React, { useMemo } from "react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  Cell
} from "recharts";
import { Analysis } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Props {
  analysis: Analysis | null;
}

export function ExperimentAnalysis({ analysis }: Props) {
  if (!analysis) {
    return (
      <div className="my-12 p-8 border border-dashed border-muted-foreground/30 rounded-xl bg-muted/30 text-center">
        <h3 className="text-lg font-medium text-foreground mb-2">Experiment Not Yet Run</h3>
        <p className="text-muted-foreground">The analysis for this experiment is pending data collection.</p>
      </div>
    );
  }

  const {
    overall,
    perModel,
    byVariant,
    decisionOptions,
    primaryDecision,
    primaryDecisionLabel,
    totalTrials
  } = analysis;

  // Colors for the chart options (using our CSS variables implicitly)
  const COLORS = [
    "hsl(var(--chart-1))",
    "hsl(var(--chart-2))",
    "hsl(var(--chart-3))",
    "hsl(var(--chart-4))",
    "hsl(var(--chart-5))",
  ];

  // Format data for the main grouped bar chart
  const mainChartData = useMemo(() => {
    return byVariant.map((v) => {
      const row: any = { name: v.label };
      decisionOptions.forEach(opt => {
        row[opt.label] = (v.proportions[opt.id] || 0) * 100;
      });
      return row;
    });
  }, [byVariant, decisionOptions]);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-background border border-border shadow-md rounded-lg p-3 text-sm">
          <p className="font-semibold mb-2 text-foreground">{label}</p>
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center justify-between gap-4 mb-1">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }} />
                <span className="text-muted-foreground">{entry.name}</span>
              </div>
              <span className="font-mono font-medium">{entry.value.toFixed(1)}%</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="my-16 space-y-12 font-sans" data-testid="experiment-analysis">
      {/* Significance Callout */}
      <div className={`p-5 sm:p-6 rounded-xl border-l-4 ${overall.significant ? 'bg-primary/5 border-primary' : 'bg-muted border-muted-foreground'}`}>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h3 className="text-lg sm:text-xl font-bold tracking-tight text-foreground mb-2">
              {overall.significant ? "Statistically Significant Effect" : "No Significant Effect Detected"}
            </h3>
            <p className="text-muted-foreground max-w-2xl leading-relaxed">
              Based on {totalTrials.toLocaleString()} trials, the framing metaphor 
              {overall.significant ? " had a measurable impact" : " did not meaningfully alter"} on the model's decision distribution.
            </p>
          </div>
          <div className="flex flex-row items-center gap-3 sm:flex-col sm:items-end sm:gap-2 sm:text-right shrink-0">
            <Badge variant={overall.significant ? "default" : "secondary"}>
              p {overall.pValue < 0.001 ? "< 0.001" : `= ${overall.pValue.toFixed(3)}`}
            </Badge>
            <span className="text-xs text-muted-foreground font-mono">
              Cramér's V: {overall.cramersV.toFixed(3)}
            </span>
          </div>
        </div>
      </div>

      {/* Main Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Decision Distribution by Variant</CardTitle>
          <CardDescription>Percentage of models selecting each option based on the provided framing</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] sm:h-[400px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mainChartData} margin={{ top: 20, right: 10, left: -10, bottom: 30 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                <XAxis 
                  dataKey="name" 
                  tick={{ fontSize: 12, fill: "hsl(var(--muted-foreground))" }} 
                  tickLine={false}
                  axisLine={{ stroke: "hsl(var(--border))" }}
                  dy={10}
                />
                <YAxis 
                  tickFormatter={(val) => `${val}%`}
                  tick={{ fontSize: 12, fill: "hsl(var(--muted-foreground))" }}
                  tickLine={false}
                  axisLine={false}
                />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "hsl(var(--muted)/0.5)" }} />
                <Legend wrapperStyle={{ paddingTop: "20px" }} />
                {decisionOptions.map((opt, idx) => (
                  <Bar 
                    key={opt.id} 
                    dataKey={opt.label} 
                    stackId="a" 
                    fill={COLORS[idx % COLORS.length]} 
                    radius={[0, 0, 0, 0]}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Primary Decision Breakdown per Model */}
      {perModel && perModel.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Model Specific Results</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {perModel.map(modelResult => (
              <Card key={modelResult.model} className="bg-muted/30">
                <CardContent className="p-4 flex justify-between items-center">
                  <div className="font-medium">{modelResult.model}</div>
                  <Badge variant={modelResult.chiSquare.significant ? "default" : "secondary"}>
                    {modelResult.chiSquare.significant ? "Significant" : "Null"}
                  </Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Methodology Callout */}
      <div className="text-sm text-muted-foreground bg-muted p-4 rounded-lg">
        <strong>Methodology:</strong> {analysis.models.length} models tested over {analysis.totalTrials} total trials ({analysis.trialsPerCell} per cell). 
        Significance tested via Chi-Square test of independence (α = 0.05). Prompt exact text available via API.
      </div>
    </div>
  );
}
