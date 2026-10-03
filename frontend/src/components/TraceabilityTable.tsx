"use client";

import React, { useState } from "react";
import { TraceabilityRow } from "@/types";
import { ChevronDown, ChevronUp, Database } from "lucide-react";

interface TraceabilityTableProps {
  rows: TraceabilityRow[];
}

export function TraceabilityTable({ rows }: TraceabilityTableProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (!rows || rows.length === 0) return null;

  return (
    <div className="w-full bg-slate-900/80 border border-slate-800 rounded-xl overflow-hidden mt-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 flex items-center justify-between bg-slate-950/50 hover:bg-slate-800/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-semibold text-slate-200">
            Traceability Data (Deliverable 4)
          </span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300">
            {rows.length} rows
          </span>
        </div>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-slate-400" />
        ) : (
          <ChevronDown className="w-4 h-4 text-slate-400" />
        )}
      </button>

      {isOpen && (
        <div className="p-4 border-t border-slate-800 max-h-[300px] overflow-y-auto scrollbar-thin">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-slate-950/90 text-slate-300 uppercase tracking-wider font-semibold sticky top-0">
              <tr>
                <th className="py-2 px-3">DB Row ID</th>
                <th className="py-2 px-3">Beneficiary</th>
                <th className="py-2 px-3">Source Dataset</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {rows.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-2 px-3 text-slate-400 font-mono">{row.db_row_id}</td>
                  <td className="py-2 px-3 text-slate-300 font-mono">{row.beneficiary}</td>
                  <td className="py-2 px-3 text-slate-400">{row.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
