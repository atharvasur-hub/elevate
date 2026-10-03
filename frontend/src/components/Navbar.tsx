"use client";

import React, { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/api";
import { Sparkles, Database, Activity, RefreshCw } from "lucide-react";

interface NavbarProps {
  onRefresh?: () => void;
}

export function Navbar({ onRefresh }: NavbarProps) {
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");

  const verifyHealth = async () => {
    setBackendStatus("checking");
    const res = await checkBackendHealth();
    setBackendStatus(res.status);
  };

  useEffect(() => {
    verifyHealth();
    const interval = setInterval(verifyHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-white/10 bg-slate-950/80 backdrop-blur-md px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Brand & Title */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-sky-500 via-indigo-500 to-purple-500 p-[2px] shadow-lg shadow-sky-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-sky-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                BHARATGEO <span className="text-xs px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-medium">GeoAI Hub</span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Government Scheme & Fund Intelligence Engine
            </p>
          </div>
        </div>

        {/* Status Indicators & Actions */}
        <div className="flex items-center gap-3">
          {/* Backend Status Badge */}
          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              backendStatus === "online"
                ? "bg-emerald-950/40 text-emerald-400 border-emerald-500/30"
                : backendStatus === "offline"
                ? "bg-rose-950/40 text-rose-400 border-rose-500/30"
                : "bg-amber-950/40 text-amber-400 border-amber-500/30"
            }`}
          >
            <span
              className={`h-2 w-2 rounded-full ${
                backendStatus === "online"
                  ? "bg-emerald-400 animate-pulse shadow-sm shadow-emerald-400"
                  : backendStatus === "offline"
                  ? "bg-rose-500"
                  : "bg-amber-400 animate-ping"
              }`}
            />
            <span className="capitalize">
              {backendStatus === "checking"
                ? "Connecting to FastAPI..."
                : backendStatus === "online"
                ? "FastAPI Connected"
                : "FastAPI Offline (8000)"}
            </span>
          </div>

          {/* Database Link indicator */}
          <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300">
            <Database className="w-3.5 h-3.5 text-sky-400" />
            <span>PostgreSQL / Supabase</span>
          </div>

          {/* Refresh Action */}
          {onRefresh && (
            <button
              onClick={() => {
                verifyHealth();
                onRefresh();
              }}
              title="Refresh connection & sample query"
              className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
