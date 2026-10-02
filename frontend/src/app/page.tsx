"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Navbar } from "@/components/Navbar";
import { SearchBar } from "@/components/SearchBar";
import { StatsOverview } from "@/components/StatsOverview";
import { DynamicOutput } from "@/components/DynamicOutput";
import { askNaturalLanguageQuery } from "@/lib/api";
import { DEFAULT_MAP_MARKERS, extractMarkersFromResults } from "@/lib/geoData";
import { MapMarkerData, NaturalLanguageQueryResponse } from "@/types";
import { AlertCircle } from "lucide-react";

export default function DashboardPage() {
  const [question, setQuestion] = useState("Which schemes have allocated funds in Maharashtra?");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Query response state
  const [response, setResponse] = useState<NaturalLanguageQueryResponse | null>(null);
  const [markers, setMarkers] = useState<MapMarkerData[]>(DEFAULT_MAP_MARKERS);
  const [selectedMarkerId, setSelectedMarkerId] = useState<string | number | null>(null);

  const executeQuery = useCallback(async (queryText: string, includeSummary: boolean = true) => {
    setIsLoading(true);
    setError(null);
    setQuestion(queryText);

    try {
      const data = await askNaturalLanguageQuery({
        question: queryText,
        include_summary: includeSummary,
      });

      setResponse(data);

      // Extract coordinates from returned traceability_rows or results
      const activeRows = data.traceability_rows?.length ? data.traceability_rows : data.results || [];
      const extracted = extractMarkersFromResults(activeRows);
      if (extracted.length > 0) {
        setMarkers(extracted);
      } else {
        // If results don't have location fields, keep representative markers
        setMarkers(DEFAULT_MAP_MARKERS);
      }
    } catch (err: any) {
      console.error("Query failed:", err);
      setError(
        err?.message ||
          "Could not reach FastAPI endpoint at http://localhost:8000/api/v1/query/ask. Make sure the backend server is running."
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Run initial query on page mount
  useEffect(() => {
    executeQuery("Which schemes have allocated funds in Maharashtra?", true);
  }, [executeQuery]);

  const activeRows = response?.traceability_rows?.length
    ? response.traceability_rows
    : response?.results || [];

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col selection:bg-sky-500/30 selection:text-sky-200">
      {/* Top Navbar */}
      <Navbar onRefresh={() => executeQuery(question, true)} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-6">
        {/* Search Bar Section */}
        <section className="w-full">
          <SearchBar
            onSearch={(q, incSum) => executeQuery(q, incSum)}
            isLoading={isLoading}
            currentQuestion={question}
          />
        </section>

        {/* Error Alert if any */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-200 flex items-start gap-3 text-sm backdrop-blur">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <span className="font-semibold block">Backend Connection Notice:</span>
              <p className="text-xs text-rose-300/90 mt-0.5">{error}</p>
              <p className="text-[11px] text-rose-400/80 mt-1">
                Tip: Start your backend with <code className="bg-rose-900/60 px-1.5 py-0.5 rounded font-mono">uvicorn app.main:app --reload --port 8000</code>
              </p>
            </div>
            <button
              onClick={() => executeQuery(question, true)}
              className="px-3 py-1 bg-rose-900/60 hover:bg-rose-800/80 rounded-lg text-xs font-medium text-rose-100 transition-colors cursor-pointer"
            >
              Retry
            </button>
          </div>
        )}

        {/* Stats Overview KPIs */}
        <section className="w-full">
          <StatsOverview
            rowCount={response ? response.row_count : markers.length}
            executionTimeMs={response ? response.execution_time_ms : 0}
            markers={markers}
            rawResults={activeRows}
          />
        </section>

        {/* Dynamic Output Component (AI Summary + Map / Bar Chart / Table / Text Visualizer) */}
        <section className="w-full">
          <DynamicOutput
            response={response}
            isLoading={isLoading}
            markers={markers}
            selectedMarkerId={selectedMarkerId}
            onMarkerSelect={(m) => setSelectedMarkerId(m.id)}
          />
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/60 py-5 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p>© 2026 ELEVATE GeoAI Intelligence Platform. Powered by FastAPI & Gemini.</p>
          <div className="flex items-center gap-4 text-slate-400">
            <span>FastAPI: <code className="text-sky-400">/api/v1/query/ask</code></span>
            <span>Database: <code className="text-indigo-400">PostgreSQL</code></span>
          </div>
        </div>
      </footer>
    </div>
  );
}
