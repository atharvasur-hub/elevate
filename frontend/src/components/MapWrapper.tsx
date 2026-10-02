"use client";

import React from "react";
import dynamic from "next/dynamic";
import { MapMarkerData } from "@/types";
import { Loader2, MapPin } from "lucide-react";

// Dynamically import MapComponent with SSR disabled to prevent Leaflet window errors
const DynamicMap = dynamic(() => import("./MapComponent"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[420px] lg:h-[480px] rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col items-center justify-center gap-3 text-slate-400">
      <div className="relative flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-2 border-sky-500/20 border-t-sky-400 animate-spin" />
        <MapPin className="w-5 h-5 text-sky-400 absolute" />
      </div>
      <p className="text-xs font-medium text-slate-300">Rendering Geographic Canvas...</p>
    </div>
  ),
});

interface MapWrapperProps {
  markers: MapMarkerData[];
  selectedMarkerId?: string | number | null;
  onMarkerSelect?: (marker: MapMarkerData) => void;
}

export function MapWrapper(props: MapWrapperProps) {
  return <DynamicMap {...props} />;
}
