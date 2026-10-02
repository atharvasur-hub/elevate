"use client";

import React, { useState } from "react";
import { Sparkles, Brain, Lightbulb, ChevronDown, ChevronUp, Database, ArrowUpRight, Zap, Target } from "lucide-react";
import { SqlViewer } from "./SqlViewer";

interface AiRecommendationsProps {
  summary?: string | null;
  sqlQuery?: string;
  question?: string;
  isLoading: boolean;
  rowCount: number;
}

export function AiRecommendations({
  summary,
  sqlQuery,
  question,
  isLoading,
  rowCount,
}: AiRecommendationsProps) {
  const [showSql, setShowSql] = useState(false);

  // Generate automated smart takeaways/recommendations from the summary or response context
  const getDerivedInsights = () => {
    if (!summary) return [];
    
    // Split bullet points or sentences
    const lines = summary
      .split(/(?:\r\n|\r|\n|\. )/)
      .map((s) => s.trim().replace(/^[-*•]\s*/, ""))
      .filter((s) => s.length > 25);

    return lines.slice(0, 3);
  };

  const insights = getDerivedInsights();

  return (
    <div className="w-full bg-slate-900/80 border border-slate-800/90 rounded-2xl p-5 shadow-2xl backdrop-blur-xl transition-all duration-300">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-purple-600/30 to-sky-600/30 border border-purple-500/30 text-purple-400 shadow-inner">
            <Brain className="w-5 h-5 text-purple-300" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              AI Intelligence & Recommendations
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-purple-950 text-purple-300 border border-purple-800/60">
                Gemini 2.5 Flash
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              Synthesized natural language insights & policy intelligence
            </p>
          </div>
        </div>

        {sqlQuery && (
          <button
            onClick={() => setShowSql(!showSql)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-xs text-slate-300 hover:text-white transition-colors cursor-pointer"
          >
            <Database className="w-3.5 h-3.5 text-sky-400" />
            <span>{showSql ? "Hide SQL" : "View SQL"}</span>
            {showSql ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        )}
      </div>

      {/* SQL Drawer */}
      {showSql && sqlQuery && (
        <div className="mt-4 transition-all">
          <SqlViewer sql={sqlQuery} />
        </div>
      )}

      {/* Content Area */}
      <div className="mt-4 space-y-4">
        {isLoading ? (
          <div className="space-y-3 py-3 animate-pulse">
            <div className="h-4 bg-slate-800 rounded-md w-3/4" />
            <div className="h-4 bg-slate-800/60 rounded-md w-full" />
            <div className="h-4 bg-slate-800/40 rounded-md w-5/6" />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
              <div className="h-20 bg-slate-800/40 rounded-xl" />
              <div className="h-20 bg-slate-800/40 rounded-xl" />
            </div>
          </div>
        ) : summary ? (
          <>
            {/* Main AI Summary Box */}
            <div className="p-4 rounded-xl bg-gradient-to-r from-purple-950/20 via-slate-900 to-sky-950/20 border border-purple-500/20 text-slate-200 text-sm leading-relaxed">
              <div className="flex items-start gap-3">
                <Sparkles className="w-4 h-4 text-purple-400 mt-0.5 shrink-0" />
                <div className="space-y-2">
                  <p className="text-slate-200 font-normal">{summary}</p>
                </div>
              </div>
            </div>

            {/* Structured Recommendations / Key Observations */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
              <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-sky-400 text-xs font-semibold">
                  <Target className="w-4 h-4" />
                  <span>Strategic Focus</span>
                </div>
                <p className="text-xs text-slate-300 mt-2 line-clamp-3">
                  {insights[0] || "Target high-budget schemes with accelerated disbursement to optimize district-level capital absorption."}
                </p>
                <div className="mt-2 text-[10px] text-slate-500 flex items-center gap-1">
                  <Zap className="w-3 h-3 text-amber-400" /> High Priority
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-emerald-400 text-xs font-semibold">
                  <Lightbulb className="w-4 h-4" />
                  <span>Policy Takeaway</span>
                </div>
                <p className="text-xs text-slate-300 mt-2 line-clamp-3">
                  {insights[1] || "Ensure scheme implementation reports are updated in real-time across urban and rural sub-districts."}
                </p>
                <div className="mt-2 text-[10px] text-slate-500 flex items-center gap-1">
                  <Zap className="w-3 h-3 text-emerald-400" /> Monitored
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex flex-col justify-between">
                <div className="flex items-center gap-2 text-purple-400 text-xs font-semibold">
                  <ArrowUpRight className="w-4 h-4" />
                  <span>Data Coverage</span>
                </div>
                <p className="text-xs text-slate-300 mt-2 line-clamp-3">
                  {`Analysis synthesized across ${rowCount} records returned from the live database query.`}
                </p>
                <div className="mt-2 text-[10px] text-slate-500 flex items-center gap-1">
                  <Zap className="w-3 h-3 text-purple-400" /> Live Query
                </div>
              </div>
            </div>
          </>
        ) : (
          /* Empty / Initial State */
          <div className="py-6 px-4 text-center rounded-xl bg-slate-950/40 border border-dashed border-slate-800">
            <Sparkles className="w-8 h-8 text-slate-600 mx-auto mb-2" />
            <p className="text-sm text-slate-300 font-medium">
              Submit any question above to generate live AI recommendations
            </p>
            <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
              Gemini translates your question into optimized SQL, queries Supabase, and returns deep analytical takeaways and policy recommendations.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
