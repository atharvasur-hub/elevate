"use client";

import React, { useState } from "react";
import { Search, Sparkles, ArrowRight, Loader2, Compass } from "lucide-react";

interface SearchBarProps {
  onSearch: (question: string, includeSummary: boolean) => void;
  isLoading: boolean;
  currentQuestion?: string;
}

const SAMPLE_QUERIES = [
  "Which schemes have allocated funds in Maharashtra?",
  "What are the top 3 schemes with the highest budget allocated?",
  "Show me fund allocation and utilization for PM-KISAN across all districts",
  "Which locations have rural area type with completed or fully utilized funds?",
  "List all schemes in the Agriculture and Healthcare sectors",
];

export function SearchBar({ onSearch, isLoading, currentQuestion = "" }: SearchBarProps) {
  const [query, setQuery] = useState(currentQuestion || "Which schemes have allocated funds in Maharashtra?");
  const [includeSummary, setIncludeSummary] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onSearch(query.trim(), includeSummary);
  };

  const handleSelectSample = (sample: string) => {
    setQuery(sample);
    onSearch(sample, includeSummary);
  };

  return (
    <div className="w-full bg-slate-900/90 border border-slate-800/80 rounded-2xl p-4 sm:p-5 shadow-2xl backdrop-blur-xl transition-all duration-300">
      <form onSubmit={handleSubmit} className="relative flex flex-col gap-3">
        {/* Main Search Input Box */}
        <div className="relative flex items-center">
          <div className="absolute left-4 text-sky-400 pointer-events-none flex items-center">
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin text-sky-400" />
            ) : (
              <Search className="w-5 h-5" />
            )}
          </div>

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            placeholder="Ask anything about government schemes, fund allocations, states, or districts..."
            className="w-full pl-12 pr-28 sm:pr-36 py-3.5 bg-slate-950/80 border border-slate-700/60 rounded-xl text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500 text-sm sm:text-base transition-all"
          />

          <div className="absolute right-2 flex items-center gap-2">
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-lg text-xs sm:text-sm font-semibold shadow-lg shadow-sky-500/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95 cursor-pointer"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="hidden sm:inline">Executing...</span>
                </>
              ) : (
                <>
                  <span>Ask AI</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>
        </div>

        {/* Options & Sample Prompt Chips */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pt-1 text-xs text-slate-400">
          {/* Suggested queries */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 max-w-full scrollbar-none">
            <span className="flex items-center gap-1 text-slate-400 font-medium whitespace-nowrap pl-0.5">
              <Compass className="w-3.5 h-3.5 text-sky-400" />
              Try asking:
            </span>
            <div className="flex items-center gap-1.5 flex-nowrap">
              {SAMPLE_QUERIES.slice(0, 3).map((sample, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelectSample(sample)}
                  disabled={isLoading}
                  className="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700/90 text-slate-300 hover:text-white border border-slate-700/50 whitespace-nowrap transition-colors text-xs text-left cursor-pointer"
                >
                  {sample.length > 38 ? `${sample.slice(0, 38)}...` : sample}
                </button>
              ))}
            </div>
          </div>

          {/* AI Summary Checkbox */}
          <label className="flex items-center gap-2 self-end sm:self-auto cursor-pointer select-none text-slate-300 hover:text-white text-xs">
            <input
              type="checkbox"
              checked={includeSummary}
              onChange={(e) => setIncludeSummary(e.target.checked)}
              className="rounded bg-slate-950 border-slate-700 text-sky-500 focus:ring-sky-500/40 w-3.5 h-3.5"
            />
            <span className="flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-sky-400" /> Include Gemini AI Analysis
            </span>
          </label>
        </div>
      </form>
    </div>
  );
}
