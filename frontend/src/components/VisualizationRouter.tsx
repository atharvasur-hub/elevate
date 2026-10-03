"use client";

import React from "react";
import { NaturalLanguageQueryResponse } from "@/types";
import { DataResultsTable } from "./DataResultsTable";
import { MapWrapper } from "./MapWrapper";
import { extractMarkersFromResults } from "@/lib/geoData";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { MapPin, BarChart3, Table as TableIcon } from "lucide-react";

interface VisualizationRouterProps {
  response: NaturalLanguageQueryResponse;
}

export function VisualizationRouter({ response }: VisualizationRouterProps) {
  const { visualization_type, chart_data } = response;

  if (!chart_data || chart_data.length === 0) {
    return (
      <div className="p-8 text-center text-slate-400 border border-slate-800 rounded-xl bg-slate-900/50">
        No data available to visualize.
      </div>
    );
  }

  // --- MAP VIEW ---
  if (visualization_type === "map") {
    const markers = extractMarkersFromResults(chart_data);
    return (
      <div className="space-y-3">
        <div className="flex items-center gap-2 px-1">
          <MapPin className="w-5 h-5 text-sky-400" />
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Geographic Scheme Map
          </h2>
        </div>
        <MapWrapper markers={markers} selectedMarkerId={null} onMarkerSelect={() => {}} />
      </div>
    );
  }

  // --- BAR CHART VIEW ---
  if (visualization_type === "bar_chart") {
    // Try to auto-detect x-axis (usually a string like region/name) and y-axis (numbers)
    const keys = Object.keys(chart_data[0]);
    const xKey = keys.find((k) => typeof chart_data[0][k] === "string") || keys[0];
    const yKeys = keys.filter((k) => typeof chart_data[0][k] === "number");

    return (
      <div className="space-y-3">
        <div className="flex items-center gap-2 px-1">
          <BarChart3 className="w-5 h-5 text-emerald-400" />
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Data Chart
          </h2>
        </div>
        <div className="w-full h-[400px] bg-slate-900/80 border border-slate-800 rounded-xl p-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chart_data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={xKey} stroke="#94a3b8" tick={{ fill: "#94a3b8", fontSize: 12 }} />
              <YAxis stroke="#94a3b8" tick={{ fill: "#94a3b8", fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#f8fafc" }}
                itemStyle={{ color: "#38bdf8" }}
              />
              <Legend wrapperStyle={{ paddingTop: "20px" }} />
              {yKeys.map((key, i) => (
                <Bar key={key} dataKey={key} fill={i === 0 ? "#38bdf8" : "#10b981"} radius={[4, 4, 0, 0]} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  // --- DATA GRID VIEW (Fallback) ---
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 px-1">
        <TableIcon className="w-5 h-5 text-indigo-400" />
        <h2 className="text-sm font-bold text-white uppercase tracking-wider">
          Data Grid
        </h2>
      </div>
      <DataResultsTable results={chart_data} question="" />
    </div>
  );
}
