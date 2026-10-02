"use client";

import React from "react";
import { Database, Clock, IndianRupee, MapPin, CheckCircle2, TrendingUp } from "lucide-react";
import { MapMarkerData } from "@/types";

interface StatsOverviewProps {
  rowCount: number;
  executionTimeMs: number;
  markers: MapMarkerData[];
  rawResults: Record<string, any>[];
}

export function StatsOverview({
  rowCount,
  executionTimeMs,
  markers,
  rawResults,
}: StatsOverviewProps) {
  // Compute total funds from markers or raw results
  let totalAllocated = 0;
  let totalDisbursed = 0;
  let totalUtilized = 0;

  rawResults.forEach((row) => {
    if (typeof row.allocated_amount === "number") totalAllocated += row.allocated_amount;
    else if (typeof row.budget_allocated === "number") totalAllocated += row.budget_allocated;

    if (typeof row.disbursed_amount === "number") totalDisbursed += row.disbursed_amount;
    if (typeof row.utilized_amount === "number") totalUtilized += row.utilized_amount;
  });

  const utilizationRate =
    totalAllocated > 0 ? ((totalUtilized / totalAllocated) * 100).toFixed(1) : null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5 w-full">
      {/* 1. Records Fetched */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex flex-col justify-between hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400">
          <span className="text-xs font-medium uppercase tracking-wider">Results</span>
          <Database className="w-4 h-4 text-sky-400" />
        </div>
        <div className="mt-2 flex items-baseline gap-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">{rowCount}</span>
          <span className="text-xs text-slate-400">records</span>
        </div>
        <div className="mt-1 flex items-center gap-1 text-[11px] text-emerald-400">
          <CheckCircle2 className="w-3 h-3" />
          <span>Postgres Live Query</span>
        </div>
      </div>

      {/* 2. Execution Latency */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex flex-col justify-between hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400">
          <span className="text-xs font-medium uppercase tracking-wider">Latency</span>
          <Clock className="w-4 h-4 text-indigo-400" />
        </div>
        <div className="mt-2 flex items-baseline gap-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">
            {executionTimeMs ? executionTimeMs.toFixed(0) : "0"}
          </span>
          <span className="text-xs text-slate-400">ms</span>
        </div>
        <div className="mt-1 flex items-center gap-1 text-[11px] text-indigo-400">
          <span>AI NL-to-SQL + Exec</span>
        </div>
      </div>

      {/* 3. Geo Markers Detected */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex flex-col justify-between hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400">
          <span className="text-xs font-medium uppercase tracking-wider">Geo Points</span>
          <MapPin className="w-4 h-4 text-rose-400" />
        </div>
        <div className="mt-2 flex items-baseline gap-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">{markers.length}</span>
          <span className="text-xs text-slate-400">mapped</span>
        </div>
        <div className="mt-1 flex items-center gap-1 text-[11px] text-rose-400">
          <span>Interactive Leaflet Pins</span>
        </div>
      </div>

      {/* 4. Financial Metric */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 flex flex-col justify-between hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400">
          <span className="text-xs font-medium uppercase tracking-wider">
            {totalAllocated > 0 ? "Total Fund Value" : "Scheme Coverage"}
          </span>
          {totalAllocated > 0 ? (
            <IndianRupee className="w-4 h-4 text-emerald-400" />
          ) : (
            <TrendingUp className="w-4 h-4 text-amber-400" />
          )}
        </div>
        <div className="mt-2 flex items-baseline gap-1.5">
          <span className="text-2xl font-bold text-white tracking-tight">
            {totalAllocated > 0
              ? `₹${totalAllocated.toLocaleString("en-IN")}`
              : `${rowCount} Schemes`}
          </span>
          {totalAllocated > 0 && <span className="text-xs text-slate-400">Cr</span>}
        </div>
        <div className="mt-1 flex items-center gap-1 text-[11px] text-slate-400">
          {utilizationRate ? (
            <span className="text-emerald-400 font-medium">
              {utilizationRate}% Utilized (₹{totalUtilized.toFixed(0)} Cr)
            </span>
          ) : (
            <span>National Welfare Schemes</span>
          )}
        </div>
      </div>
    </div>
  );
}
