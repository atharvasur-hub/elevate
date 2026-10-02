"use client";

import React, { useState } from "react";
import { Table, Code, Search, Download, Copy, Check, ChevronRight } from "lucide-react";

interface DataResultsTableProps {
  results: Record<string, any>[];
  question: string;
}

export function DataResultsTable({ results, question }: DataResultsTableProps) {
  const [viewMode, setViewMode] = useState<"table" | "json">("table");
  const [filterText, setFilterText] = useState("");
  const [copied, setCopied] = useState(false);

  if (!results || results.length === 0) {
    return (
      <div className="w-full bg-slate-900/80 border border-slate-800 rounded-2xl p-6 text-center text-slate-400">
        <p className="text-sm">No query results to display.</p>
      </div>
    );
  }

  // Extract all distinct keys from returned rows
  const columns = Array.from(
    new Set(results.flatMap((row) => Object.keys(row)))
  );

  // Filter rows based on search
  const filteredResults = results.filter((row) => {
    if (!filterText) return true;
    return Object.values(row).some((val) =>
      String(val).toLowerCase().includes(filterText.toLowerCase())
    );
  });

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(results, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportCsv = () => {
    if (!results.length) return;
    const header = columns.join(",");
    const rows = results.map((row) =>
      columns
        .map((col) => {
          const val = row[col];
          if (val === null || val === undefined) return '""';
          const str = String(val).replace(/"/g, '""');
          return `"${str}"`;
        })
        .join(",")
    );
    const csvContent = "data:text/csv;charset=utf-8," + [header, ...rows].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `query_results_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-2xl backdrop-blur-xl">
      {/* Header Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span>Query Results</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
              {filteredResults.length} / {results.length} rows
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time payload from PostgreSQL database execution
          </p>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {/* Search Filter */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Filter results..."
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-700/80 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
            />
          </div>

          {/* View Toggle */}
          <div className="flex rounded-lg bg-slate-950 p-0.5 border border-slate-800">
            <button
              onClick={() => setViewMode("table")}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium transition-colors cursor-pointer ${
                viewMode === "table"
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/30"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Table className="w-3.5 h-3.5" />
              <span>Table</span>
            </button>
            <button
              onClick={() => setViewMode("json")}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium transition-colors cursor-pointer ${
                viewMode === "json"
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/30"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>JSON</span>
            </button>
          </div>

          {/* Export / Copy buttons */}
          <button
            onClick={handleCopyJson}
            title="Copy JSON to clipboard"
            className="p-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white transition-colors cursor-pointer"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>

          <button
            onClick={handleExportCsv}
            title="Download CSV"
            className="p-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white transition-colors cursor-pointer"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="mt-4">
        {viewMode === "table" ? (
          <div className="overflow-x-auto rounded-xl border border-slate-800 max-h-[420px] scrollbar-thin">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="bg-slate-950/90 text-slate-300 uppercase tracking-wider font-semibold sticky top-0 border-b border-slate-800 z-10 backdrop-blur">
                <tr>
                  <th className="py-2.5 px-3 w-10 text-slate-500">#</th>
                  {columns.map((col) => (
                    <th key={col} className="py-2.5 px-3 whitespace-nowrap">
                      {col.replace(/_/g, " ")}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 bg-slate-900/40">
                {filteredResults.map((row, rIdx) => (
                  <tr
                    key={rIdx}
                    className="hover:bg-slate-800/40 transition-colors group"
                  >
                    <td className="py-2.5 px-3 text-slate-500 font-mono text-[11px]">
                      {rIdx + 1}
                    </td>
                    {columns.map((col) => {
                      const val = row[col];
                      let display = val === null || val === undefined ? "—" : String(val);

                      // Style status or amounts specifically
                      const isAmount =
                        col.includes("amount") || col.includes("budget") || typeof val === "number";
                      const isStatus = col.includes("status");

                      return (
                        <td
                          key={col}
                          className={`py-2.5 px-3 whitespace-nowrap text-slate-300 ${
                            isAmount ? "font-mono font-medium text-sky-300" : ""
                          }`}
                        >
                          {isStatus && typeof val === "string" ? (
                            <span
                              className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${
                                val.toLowerCase().includes("fully") ||
                                val.toLowerCase().includes("completed")
                                  ? "bg-emerald-950 text-emerald-400 border border-emerald-500/30"
                                  : val.toLowerCase().includes("disbursed")
                                  ? "bg-sky-950 text-sky-400 border border-sky-500/30"
                                  : "bg-amber-950 text-amber-400 border border-amber-500/30"
                              }`}
                            >
                              {val}
                            </span>
                          ) : isAmount && typeof val === "number" ? (
                            `₹${val.toLocaleString("en-IN")}`
                          ) : (
                            display
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 max-h-[420px] overflow-auto">
            <pre className="text-xs font-mono text-emerald-400 leading-relaxed">
              <code>{JSON.stringify(filteredResults, null, 2)}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
