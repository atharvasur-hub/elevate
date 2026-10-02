"use client";

import React, { useMemo, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { MapWrapper } from "@/components/MapWrapper";
import { DataResultsTable } from "@/components/DataResultsTable";
import { SqlViewer } from "@/components/SqlViewer";
import { Modal } from "@/components/Modal";
import { extractMarkersFromResults, DEFAULT_MAP_MARKERS } from "@/lib/geoData";
import { MapMarkerData, NaturalLanguageQueryResponse } from "@/types";
import {
  Sparkles,
  MapPin,
  BarChart3,
  Table as TableIcon,
  FileText,
  Code2,
  ChevronDown,
  ChevronUp,
  Layers,
  Database,
  Info,
  FileCode2,
  Copy,
  Check,
  ExternalLink,
} from "lucide-react";

interface DynamicOutputProps {
  response: NaturalLanguageQueryResponse | null;
  isLoading?: boolean;
  markers?: MapMarkerData[];
  selectedMarkerId?: string | number | null;
  onMarkerSelect?: (marker: MapMarkerData) => void;
}

const BAR_COLORS = [
  "#38bdf8", // Sky 400
  "#818cf8", // Indigo 400
  "#34d399", // Emerald 400
  "#f472b6", // Pink 400
  "#fbbf24", // Amber 400
  "#a78bfa", // Purple 400
];

export function DynamicOutput({
  response,
  isLoading = false,
  markers: propMarkers,
  selectedMarkerId,
  onMarkerSelect,
}: DynamicOutputProps) {
  const [showSql, setShowSql] = useState(false);
  const [isEvidenceModalOpen, setIsEvidenceModalOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  // Determine rows safely from traceability_rows or fallback results
  const rows = useMemo(() => {
    if (!response) return [];
    return response.traceability_rows?.length
      ? response.traceability_rows
      : response.results || [];
  }, [response]);

  // Determine markers for map view
  const mapMarkers = useMemo(() => {
    if (propMarkers && propMarkers.length > 0) return propMarkers;
    if (rows.length > 0) {
      const extracted = extractMarkersFromResults(rows);
      if (extracted.length > 0) return extracted;
    }
    return DEFAULT_MAP_MARKERS;
  }, [propMarkers, rows]);

  // Extract chart configuration for bar_chart view
  const chartConfig = useMemo(() => {
    if (!rows || rows.length === 0) return null;

    const sample = rows[0];
    const keys = Object.keys(sample);

    // Identify categorical key for X-axis (preferred names, states, sectors, codes)
    const categoryKey =
      keys.find((k) =>
        ["scheme_name", "name", "state", "district", "sector", "code", "financial_year"].includes(
          k.toLowerCase()
        )
      ) ||
      keys.find((k) => typeof sample[k] === "string") ||
      keys[0];

    // Identify numeric keys for Y-axis bars
    const numericKeys = keys.filter(
      (k) =>
        k !== categoryKey &&
        (typeof sample[k] === "number" ||
          k.toLowerCase().includes("amount") ||
          k.toLowerCase().includes("budget"))
    );

    // Format rows for chart (convert any numeric strings to floats)
    const chartData = rows.slice(0, 15).map((row, idx) => {
      const formatted: Record<string, any> = {
        name: String(row[categoryKey] || `Item ${idx + 1}`),
      };
      numericKeys.forEach((nk) => {
        const val = row[nk];
        formatted[nk] = typeof val === "number" ? val : parseFloat(val) || 0;
      });
      return formatted;
    });

    return {
      categoryKey,
      numericKeys: numericKeys.length > 0 ? numericKeys : ["value"],
      chartData,
    };
  }, [rows]);

  const handleCopyEvidence = () => {
    navigator.clipboard.writeText(JSON.stringify(rows, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isLoading) {
    return (
      <div className="w-full bg-slate-900/60 border border-slate-800/80 rounded-3xl p-8 backdrop-blur-xl shadow-2xl flex flex-col items-center justify-center gap-4 min-h-[380px]">
        <div className="relative flex items-center justify-center">
          <div className="w-16 h-16 rounded-full border-2 border-sky-500/20 border-t-sky-400 animate-spin" />
          <Sparkles className="w-6 h-6 text-sky-400 absolute animate-pulse" />
        </div>
        <div className="text-center space-y-1">
          <p className="text-sm font-semibold text-slate-200">
            Synthesizing Database Analysis...
          </p>
          <p className="text-xs text-slate-400">
            Gemini is evaluating schemas, running PostgreSQL, and selecting optimal visualization
          </p>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="w-full bg-slate-900/40 border border-slate-800/60 rounded-3xl p-8 text-center text-slate-500">
        <Info className="w-8 h-8 mx-auto text-slate-600 mb-2" />
        <p className="text-sm">Submit a query above to view dynamic visualizations and AI insights.</p>
      </div>
    );
  }

  const displayType = response.display_type || "table";
  const aiSummary = response.ai_summary || response.summary || "Analysis executed successfully.";

  // Render visualization depending on display_type via switch statement
  const renderVisualization = () => {
    switch (displayType) {
      case "map":
        return (
          <div className="space-y-3">
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-sky-400" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Geospatial Distribution Map
                </h3>
              </div>
              <span className="text-[11px] text-sky-400 font-mono bg-sky-950/60 border border-sky-800/50 px-2 py-0.5 rounded-full">
                {mapMarkers.length} Locations Mapped
              </span>
            </div>
            <MapWrapper
              markers={mapMarkers}
              selectedMarkerId={selectedMarkerId}
              onMarkerSelect={onMarkerSelect}
            />
          </div>
        );

      case "bar_chart":
        return (
          <div className="space-y-3">
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-indigo-400" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Comparative Analysis Chart
                </h3>
              </div>
              <span className="text-[11px] text-indigo-400 font-mono bg-indigo-950/60 border border-indigo-800/50 px-2 py-0.5 rounded-full">
                {chartConfig?.chartData.length || 0} Data Points
              </span>
            </div>

            <div className="w-full bg-slate-950/70 border border-slate-800/90 rounded-2xl p-4 sm:p-6 backdrop-blur">
              {chartConfig && chartConfig.chartData.length > 0 ? (
                <div className="h-[360px] sm:h-[420px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartConfig.chartData}
                      margin={{ top: 20, right: 30, left: 10, bottom: 60 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                      <XAxis
                        dataKey="name"
                        stroke="#64748b"
                        fontSize={11}
                        interval={0}
                        angle={-30}
                        textAnchor="end"
                        tick={{ fill: "#94a3b8" }}
                      />
                      <YAxis
                        stroke="#64748b"
                        fontSize={11}
                        tick={{ fill: "#94a3b8" }}
                        tickFormatter={(val) => `₹${val}`}
                      />
                      <Tooltip
                        cursor={{ fill: "rgba(56, 189, 248, 0.05)" }}
                        contentStyle={{
                          backgroundColor: "#090d16",
                          borderColor: "#334155",
                          borderRadius: "0.75rem",
                          color: "#f8fafc",
                          fontSize: "12px",
                          boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.5)",
                        }}
                        formatter={(value: any, name: any) => [
                          typeof value === "number" ? `₹${value.toLocaleString("en-IN")} Cr` : value,
                          String(name).replace(/_/g, " "),
                        ]}
                      />
                      <Legend
                        verticalAlign="top"
                        wrapperStyle={{ paddingBottom: "12px", fontSize: "12px" }}
                        formatter={(val) => (
                          <span className="text-slate-300 font-medium">
                            {String(val).replace(/_/g, " ")}
                          </span>
                        )}
                      />
                      {chartConfig.numericKeys.map((k, idx) => (
                        <Bar
                          key={k}
                          dataKey={k}
                          fill={BAR_COLORS[idx % BAR_COLORS.length]}
                          radius={[6, 6, 0, 0]}
                          maxBarSize={48}
                        />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-[200px] flex items-center justify-center text-slate-500 text-xs">
                  No quantitative data available to plot bar chart.
                </div>
              )}
            </div>
          </div>
        );

      case "table":
        return (
          <div className="space-y-3">
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center gap-2">
                <TableIcon className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Tabular Data Records Grid
                </h3>
              </div>
              <span className="text-[11px] text-emerald-400 font-mono bg-emerald-950/60 border border-emerald-800/50 px-2 py-0.5 rounded-full">
                {rows.length} Records Loaded
              </span>
            </div>
            <DataResultsTable results={rows} question={response.question} />
          </div>
        );

      case "text":
        return (
          <div className="space-y-3">
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-purple-400" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Detailed Analysis
                </h3>
              </div>
              <span className="text-[11px] text-purple-400 font-mono bg-purple-950/60 border border-purple-800/50 px-2 py-0.5 rounded-full">
                Narrative Output
              </span>
            </div>

            <div className="w-full bg-slate-950/70 border border-slate-800/90 rounded-2xl p-6 backdrop-blur space-y-4">
              <p className="text-slate-200 text-base sm:text-lg leading-relaxed font-light">
                {aiSummary}
              </p>
              {rows.length > 0 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pt-4 border-t border-slate-800/80">
                  {rows.slice(0, 6).map((item, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs space-y-1"
                    >
                      <div className="text-slate-400 font-mono text-[11px]">Record #{idx + 1}</div>
                      <div className="font-medium text-slate-200 truncate">
                        {item.name || item.scheme_name || item.state || JSON.stringify(item)}
                      </div>
                      {item.status && (
                        <div className="text-sky-400 font-semibold text-[10px]">{item.status}</div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );

      default:
        return <DataResultsTable results={rows} question={response.question} />;
    }
  };

  const getDisplayTypeBadge = () => {
    switch (displayType) {
      case "map":
        return {
          label: "Map View",
          icon: <MapPin className="w-3.5 h-3.5 text-sky-400" />,
          classes: "bg-sky-500/10 text-sky-300 border-sky-500/30",
        };
      case "bar_chart":
        return {
          label: "Bar Chart View",
          icon: <BarChart3 className="w-3.5 h-3.5 text-indigo-400" />,
          classes: "bg-indigo-500/10 text-indigo-300 border-indigo-500/30",
        };
      case "table":
        return {
          label: "Table Grid",
          icon: <TableIcon className="w-3.5 h-3.5 text-emerald-400" />,
          classes: "bg-emerald-500/10 text-emerald-300 border-emerald-500/30",
        };
      case "text":
        return {
          label: "Text Narrative",
          icon: <FileText className="w-3.5 h-3.5 text-purple-400" />,
          classes: "bg-purple-500/10 text-purple-300 border-purple-500/30",
        };
      default:
        return {
          label: displayType,
          icon: <Layers className="w-3.5 h-3.5 text-slate-400" />,
          classes: "bg-slate-800 text-slate-300 border-slate-700",
        };
    }
  };

  const badge = getDisplayTypeBadge();

  return (
    <div className="w-full space-y-6">
      {/* ALWAYS DISPLAY AI SUMMARY ABOVE THE VISUALIZED COMPONENT */}
      <section className="w-full bg-gradient-to-br from-slate-900/90 via-slate-900/70 to-slate-950 border border-slate-800 rounded-3xl p-5 sm:p-6 shadow-2xl backdrop-blur-xl relative overflow-hidden">
        {/* Glow accent */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-sky-500/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl pointer-events-none -ml-20 -mb-20" />

        <div className="relative z-10 space-y-3">
          {/* Header Row */}
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-gradient-to-tr from-sky-500/20 to-purple-500/20 border border-sky-500/30 text-sky-400">
                <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-white tracking-wide flex items-center gap-2">
                  <span>Gemini AI Insights & Synthesis</span>
                </h2>
                <p className="text-[11px] text-slate-400 font-medium">
                  {response.question}
                </p>
              </div>
            </div>

            {/* Visualizer Badge & SQL Toggle */}
            <div className="flex items-center gap-2">
              <div
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${badge.classes}`}
              >
                {badge.icon}
                <span>{badge.label}</span>
              </div>

              {response.sql_query && (
                <button
                  onClick={() => setShowSql(!showSql)}
                  className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-300 hover:text-white text-xs font-medium transition-colors cursor-pointer"
                >
                  <Code2 className="w-3.5 h-3.5 text-sky-400" />
                  <span>SQL</span>
                  {showSql ? (
                    <ChevronUp className="w-3 h-3 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-3 h-3 text-slate-400" />
                  )}
                </button>
              )}
            </div>
          </div>

          {/* AI Summary Text */}
          <div className="pt-1">
            <p className="text-sm sm:text-base text-slate-200 leading-relaxed font-normal">
              {aiSummary}
            </p>
          </div>

          {/* Metrics Pill Footer */}
          <div className="flex flex-wrap items-center gap-3 pt-2 text-[11px] text-slate-400 font-mono">
            <span className="flex items-center gap-1">
              <Database className="w-3 h-3 text-emerald-400" />
              <span>Traceability Rows: <strong className="text-slate-200">{rows.length}</strong></span>
            </span>
            <span>•</span>
            <span>
              Execution Time: <strong className="text-sky-300">{response.execution_time_ms}ms</strong>
            </span>
          </div>

          {/* Expandable SQL Viewer */}
          {showSql && response.sql_query && (
            <div className="pt-2">
              <SqlViewer sql={response.sql_query} />
            </div>
          )}
        </div>
      </section>

      {/* VISUALIZED COMPONENT VIA SWITCH STATEMENT */}
      <section className="w-full">
        {renderVisualization()}
      </section>

      {/* BOTTOM BUTTON: VIEW EVIDENCE (RAW DATA) */}
      <section className="w-full flex items-center justify-between pt-2 pb-1 px-1">
        <div className="text-xs text-slate-500 font-medium">
          Evidence data backed by Supabase PostgreSQL
        </div>
        <button
          onClick={() => setIsEvidenceModalOpen(true)}
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-700/80 hover:border-sky-500/50 text-xs font-medium text-slate-300 hover:text-white transition-all shadow-md hover:shadow-sky-500/10 cursor-pointer group"
        >
          <FileCode2 className="w-4 h-4 text-sky-400 group-hover:scale-110 transition-transform" />
          <span>View Evidence (Raw Data)</span>
          <span className="px-1.5 py-0.2 rounded-md bg-slate-800 text-[10px] text-slate-400 font-mono">
            {rows.length}
          </span>
        </button>
      </section>

      {/* EVIDENCE / RAW DATA MODAL */}
      <Modal
        isOpen={isEvidenceModalOpen}
        onClose={() => setIsEvidenceModalOpen(false)}
        maxWidth="4xl"
        title={
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-sky-500/10 border border-sky-500/30 text-sky-400">
              <Database className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm sm:text-base font-bold text-slate-100">
                Evidence Data (traceability_rows)
              </h3>
              <p className="text-xs text-slate-400">
                Raw JSON output executed against Supabase PostgreSQL database
              </p>
            </div>
          </div>
        }
      >
        <div className="space-y-4">
          {/* Controls Bar */}
          <div className="flex items-center justify-between gap-2 p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs text-slate-300">
            <div className="flex items-center gap-3">
              <span className="font-mono text-emerald-400 font-semibold">
                {rows.length} records in payload
              </span>
              <span className="text-slate-600">|</span>
              <span className="text-slate-400 font-mono text-[11px]">
                Type: Array&lt;Record&lt;string, any&gt;&gt;
              </span>
            </div>

            <button
              onClick={handleCopyEvidence}
              className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-medium text-slate-200 transition-colors cursor-pointer"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-slate-400" />
                  <span>Copy JSON</span>
                </>
              )}
            </button>
          </div>

          {/* Formatted Code Block */}
          <div className="relative rounded-xl border border-slate-800 bg-slate-950 p-4 max-h-[55vh] overflow-auto scrollbar-thin">
            <pre className="text-xs font-mono text-emerald-400/90 leading-relaxed">
              <code>{JSON.stringify(rows, null, 2)}</code>
            </pre>
          </div>
        </div>
      </Modal>
    </div>
  );
}
