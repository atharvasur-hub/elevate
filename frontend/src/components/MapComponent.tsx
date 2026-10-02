"use client";

import React, { useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import { MapMarkerData } from "@/types";
import { MapPin, IndianRupee, Layers, Navigation, Info } from "lucide-react";

interface MapComponentProps {
  markers: MapMarkerData[];
  selectedMarkerId?: string | number | null;
  onMarkerSelect?: (marker: MapMarkerData) => void;
}

// Custom icon creator using Leaflet DivIcon
function createCustomPin(isActive: boolean = false) {
  const bgClass = isActive ? "bg-amber-400 border-amber-200" : "bg-sky-500 border-sky-200";
  const pulseClass = isActive ? "bg-amber-400/50" : "bg-sky-400/40";

  return L.divIcon({
    className: "custom-leaflet-marker",
    html: `
      <div class="custom-pin-container" style="cursor: pointer;">
        <div class="pulse-ring ${pulseClass}"></div>
        <div class="pulse-pin ${bgClass}"></div>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16],
  });
}

// Helper component to auto-recenter and fit bounds when markers update
function AutoRecenter({ markers }: { markers: MapMarkerData[] }) {
  const map = useMap();

  useEffect(() => {
    if (!markers || markers.length === 0) return;

    if (markers.length === 1) {
      map.flyTo([markers[0].lat, markers[0].lng], 8, { duration: 1.2 });
    } else {
      const bounds = L.latLngBounds(markers.map((m) => [m.lat, m.lng]));
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 8, duration: 1.2 });
    }
  }, [markers, map]);

  return null;
}

export default function MapComponent({
  markers,
  selectedMarkerId,
  onMarkerSelect,
}: MapComponentProps) {
  // Center of India as default
  const defaultCenter: [number, number] = [22.5937, 78.9629];
  const defaultZoom = 4.8;

  const defaultIcon = useMemo(() => createCustomPin(false), []);
  const activeIcon = useMemo(() => createCustomPin(true), []);

  return (
    <div className="relative w-full h-[420px] lg:h-[480px] rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 shadow-2xl">
      {/* Top Map Overlay Bar */}
      <div className="absolute top-3 left-3 z-[1000] flex items-center gap-2 bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-700/70 text-xs text-slate-200 shadow-lg">
        <MapPin className="w-3.5 h-3.5 text-sky-400" />
        <span className="font-semibold">{markers.length} Locations Active</span>
        <span className="text-slate-500">•</span>
        <span className="text-slate-400 text-[11px]">Click pin to inspect details</span>
      </div>

      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        scrollWheelZoom={true}
        className="w-full h-full z-10"
      >
        {/* Standard OpenStreetMap TileLayer */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          maxZoom={19}
        />

        <AutoRecenter markers={markers} />

        {markers.map((marker) => {
          const isSelected = selectedMarkerId === marker.id;
          return (
            <Marker
              key={marker.id}
              position={[marker.lat, marker.lng]}
              icon={isSelected ? activeIcon : defaultIcon}
              eventHandlers={{
                click: () => {
                  if (onMarkerSelect) onMarkerSelect(marker);
                },
              }}
            >
              <Popup className="custom-dark-popup">
                <div className="p-1 space-y-2 text-slate-100 min-w-[210px]">
                  {/* Header */}
                  <div className="border-b border-slate-700/60 pb-1.5">
                    <span className="text-[10px] font-semibold tracking-wider text-sky-400 uppercase">
                      {marker.state || "Location"}
                    </span>
                    <h4 className="text-sm font-bold text-white leading-snug">
                      {marker.district ? `${marker.district}` : marker.title}
                      {marker.sub_district ? ` (${marker.sub_district})` : ""}
                    </h4>
                  </div>

                  {/* Scheme tag if available */}
                  {marker.scheme_name && (
                    <div className="text-xs bg-slate-800/90 rounded-md p-1.5 border border-slate-700/50">
                      <span className="text-slate-400 text-[10px] block">Scheme / Program:</span>
                      <span className="font-medium text-slate-200">{marker.scheme_name}</span>
                    </div>
                  )}

                  {/* Financial Breakdown if available */}
                  {(marker.allocated_amount || marker.utilized_amount) ? (
                    <div className="grid grid-cols-2 gap-1.5 text-[11px] pt-0.5">
                      <div className="bg-slate-800/60 rounded p-1">
                        <span className="text-slate-400 text-[9px] block">Allocated:</span>
                        <span className="font-semibold text-sky-300">
                          ₹{marker.allocated_amount?.toFixed(1)} Cr
                        </span>
                      </div>
                      <div className="bg-slate-800/60 rounded p-1">
                        <span className="text-slate-400 text-[9px] block">Utilized:</span>
                        <span className="font-semibold text-emerald-400">
                          ₹{marker.utilized_amount?.toFixed(1)} Cr
                        </span>
                      </div>
                    </div>
                  ) : null}

                  {/* Status Badge */}
                  {marker.status && (
                    <div className="flex items-center justify-between pt-1">
                      <span className="text-[10px] text-slate-400">Status:</span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded font-medium ${
                          marker.status.toLowerCase().includes("fully") ||
                          marker.status.toLowerCase().includes("complete")
                            ? "bg-emerald-950 text-emerald-400 border border-emerald-500/30"
                            : marker.status.toLowerCase().includes("disbursed")
                            ? "bg-sky-950 text-sky-400 border border-sky-500/30"
                            : "bg-amber-950 text-amber-400 border border-amber-500/30"
                        }`}
                      >
                        {marker.status}
                      </span>
                    </div>
                  )}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
