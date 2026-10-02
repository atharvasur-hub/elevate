import { MapMarkerData } from "@/types";

// Geographic coordinates lookup for Indian states and prominent districts/sub-districts
export const INDIA_COORDINATES: Record<string, { lat: number; lng: number }> = {
  // States & UTs
  "maharashtra": { lat: 19.7515, lng: 75.7139 },
  "uttar pradesh": { lat: 26.8467, lng: 80.9462 },
  "karnataka": { lat: 15.3173, lng: 75.7139 },
  "gujarat": { lat: 22.2587, lng: 71.1924 },
  "rajasthan": { lat: 27.0238, lng: 74.2179 },
  "madhya pradesh": { lat: 22.9734, lng: 78.6569 },
  "bihar": { lat: 25.0961, lng: 85.3131 },
  "tamil nadu": { lat: 11.1271, lng: 78.6569 },
  "odisha": { lat: 20.9517, lng: 85.0985 },
  "assam": { lat: 26.2006, lng: 92.9376 },
  "delhi": { lat: 28.7041, lng: 77.1025 },

  // Districts
  "pune": { lat: 18.5204, lng: 73.8567 },
  "nagpur": { lat: 21.1458, lng: 79.0882 },
  "nashik": { lat: 19.9975, lng: 73.7898 },
  "thane": { lat: 19.2183, lng: 72.9781 },
  "ahmedabad": { lat: 23.0225, lng: 72.5714 },
  "surat": { lat: 21.1702, lng: 72.8311 },
  "vadodara": { lat: 22.3072, lng: 73.1812 },

  // Sub-districts / Tehsils (Gujarat - Ahmedabad)
  "bavla": { lat: 22.8368, lng: 72.3644 },
  "city": { lat: 23.0225, lng: 72.5714 },
  "daskroi": { lat: 22.9500, lng: 72.6300 },
  "dholka": { lat: 22.7200, lng: 72.4400 },
  "sanand": { lat: 22.9868, lng: 72.3815 },

  // Sub-districts / Tehsils (Gujarat - Surat)
  "choryasi": { lat: 21.1702, lng: 72.8311 },
  "kamrej": { lat: 21.2700, lng: 72.9600 },
  "mangrol": { lat: 21.4167, lng: 73.0833 },
  "olpad": { lat: 21.3300, lng: 72.7500 },

  // Sub-districts / Tehsils (Gujarat - Vadodara)
  "karjan": { lat: 22.0500, lng: 73.1700 },
  "padra": { lat: 22.2300, lng: 73.0800 },
  "savli": { lat: 22.5600, lng: 73.2200 },
  "vaghodia": { lat: 22.3000, lng: 73.4200 },

  // Sub-districts / Tehsils (Maharashtra - Nagpur)
  "hingna": { lat: 21.0667, lng: 78.9667 },
  "kamptee": { lat: 21.2333, lng: 79.2000 },
  "nagpur rural": { lat: 21.1458, lng: 79.0882 },
  "ramtek": { lat: 21.4000, lng: 79.3333 },
  "umred": { lat: 20.8500, lng: 79.3333 },

  // Sub-districts / Tehsils (Maharashtra - Nashik)
  "igatpuri": { lat: 19.7000, lng: 73.5500 },
  "malegaon": { lat: 20.5500, lng: 74.5333 },
  "niphad": { lat: 20.0800, lng: 74.1100 },
  "sinnar": { lat: 19.8500, lng: 73.9833 },

  // Sub-districts / Tehsils (Maharashtra - Pune)
  "baramati": { lat: 18.1500, lng: 74.5800 },
  "haveli": { lat: 18.5000, lng: 73.9100 },
  "junnar": { lat: 19.2000, lng: 73.8800 },
  "khed": { lat: 18.8400, lng: 73.9000 },
  "shirur": { lat: 18.8300, lng: 74.3800 },

  // Sub-districts / Tehsils (Maharashtra - Thane)
  "ambernath": { lat: 19.2000, lng: 73.1900 },
  "bhiwandi": { lat: 19.3000, lng: 73.0600 },
  "kalyan": { lat: 19.2403, lng: 73.1305 },
  "ulhasnagar": { lat: 19.2167, lng: 73.1500 },
};

// Default seed markers
export const DEFAULT_MAP_MARKERS: MapMarkerData[] = [
  {
    id: 1,
    title: "Pune (Haveli), Maharashtra",
    lat: 18.5000,
    lng: 73.9100,
    state: "Maharashtra",
    district: "Pune",
    sub_district: "Haveli",
    scheme_name: "Agriculture Subsidy",
    allocated_amount: 6000.0,
    disbursed_amount: 6000.0,
    utilized_amount: 6000.0,
    status: "Active",
  },
  {
    id: 2,
    title: "Nagpur (Hingna), Maharashtra",
    lat: 21.0667,
    lng: 78.9667,
    state: "Maharashtra",
    district: "Nagpur",
    sub_district: "Hingna",
    scheme_name: "Rural Dev Scheme",
    allocated_amount: 16250.0,
    disbursed_amount: 16250.0,
    utilized_amount: 16250.0,
    status: "Tree Plantation",
  },
  {
    id: 3,
    title: "Nashik (Niphad), Maharashtra",
    lat: 20.0800,
    lng: 74.1100,
    state: "Maharashtra",
    district: "Nashik",
    sub_district: "Niphad",
    scheme_name: "Agriculture Subsidy",
    allocated_amount: 6000.0,
    disbursed_amount: 6000.0,
    utilized_amount: 6000.0,
    status: "Active",
  },
  {
    id: 4,
    title: "Ahmedabad (Bavla), Gujarat",
    lat: 22.8368,
    lng: 72.3644,
    state: "Gujarat",
    district: "Ahmedabad",
    sub_district: "Bavla",
    scheme_name: "Water Tap Connection",
    allocated_amount: 19715.91,
    disbursed_amount: 19715.91,
    utilized_amount: 19715.91,
    status: "Non-Functional",
  },
  {
    id: 5,
    title: "Surat (Kamrej), Gujarat",
    lat: 21.2700,
    lng: 72.9600,
    state: "Gujarat",
    district: "Surat",
    sub_district: "Kamrej",
    scheme_name: "Water Tap Connection",
    allocated_amount: 14938.40,
    disbursed_amount: 14938.40,
    utilized_amount: 14938.40,
    status: "Functional",
  },
  {
    id: 6,
    title: "Vadodara (Savli), Gujarat",
    lat: 22.5600,
    lng: 73.2200,
    state: "Gujarat",
    district: "Vadodara",
    sub_district: "Savli",
    scheme_name: "Rural Dev Scheme",
    allocated_amount: 24750.0,
    disbursed_amount: 24750.0,
    utilized_amount: 24750.0,
    status: "Pond Excavation",
  },
];

export function extractMarkersFromResults(results: Record<string, any>[]): MapMarkerData[] {
  if (!results || results.length === 0) return [];

  const markers: MapMarkerData[] = [];

  results.forEach((row, index) => {
    let lat: number | undefined;
    let lng: number | undefined;

    // 1. Check direct coordinates from database row
    if (typeof row.latitude === "number" && typeof row.longitude === "number") {
      lat = row.latitude;
      lng = row.longitude;
    } else if (typeof row.lat === "number" && typeof row.lng === "number") {
      lat = row.lat;
      lng = row.lng;
    }

    // 2. Fallback to dictionary lookup by sub_district / district / state
    const subDistrictKey = (row.sub_district || row.block || row.tehsil || "")
      .toString()
      .toLowerCase()
      .trim();
    const districtKey = (row.district || row.city || "")
      .toString()
      .toLowerCase()
      .trim();
    const stateKey = (row.state || "")
      .toString()
      .toLowerCase()
      .trim();

    if (lat === undefined || lng === undefined) {
      if (subDistrictKey && INDIA_COORDINATES[subDistrictKey]) {
        lat = INDIA_COORDINATES[subDistrictKey].lat;
        lng = INDIA_COORDINATES[subDistrictKey].lng;
      } else if (districtKey && INDIA_COORDINATES[districtKey]) {
        lat = INDIA_COORDINATES[districtKey].lat;
        lng = INDIA_COORDINATES[districtKey].lng;
      } else if (stateKey && INDIA_COORDINATES[stateKey]) {
        lat = INDIA_COORDINATES[stateKey].lat;
        lng = INDIA_COORDINATES[stateKey].lng;
      }
    }

    // If coordinates exist, build marker
    if (lat !== undefined && lng !== undefined) {
      // Jitter for duplicate coordinates so markers don't overlap completely
      const duplicateCount = markers.filter(
        (m) => Math.abs(m.lat - lat!) < 0.005 && Math.abs(m.lng - lng!) < 0.005
      ).length;
      const jitterLat = lat + (duplicateCount > 0 ? duplicateCount * 0.015 * (duplicateCount % 2 === 0 ? 1 : -1) : 0);
      const jitterLng = lng + (duplicateCount > 0 ? duplicateCount * 0.015 * (duplicateCount % 3 === 0 ? 1 : -1) : 0);

      const title =
        [row.sub_district, row.district, row.state].filter(Boolean).join(", ") ||
        row.name ||
        row.beneficiary_code ||
        `Record #${index + 1}`;

      const schemeName =
        row.scheme_name ||
        (row.subsidy_disbursed_inr !== undefined || row.land_holding_hectares !== undefined ? "Agriculture Scheme" : null) ||
        (row.days_worked !== undefined || row.project_type !== undefined ? "Rural Dev Scheme" : null) ||
        (row.tap_connection_status !== undefined || row.cost_incurred !== undefined ? "Water Scheme" : null) ||
        "Government Scheme";

      const amount = Number(
        row.subsidy_disbursed_inr ??
        row.wages_paid_inr ??
        row.cost_incurred ??
        row.allocated_amount ??
        row.disbursed_amount ??
        0
      );

      const status =
        row.tap_connection_status ||
        row.project_type ||
        row.status ||
        (row.subsidy_disbursed_inr ? "Disbursed" : "Registered");

      markers.push({
        id: row.id || `marker-${index}`,
        title,
        lat: jitterLat,
        lng: jitterLng,
        state: row.state,
        district: row.district,
        sub_district: row.sub_district,
        scheme_name: schemeName,
        allocated_amount: amount,
        disbursed_amount: amount,
        utilized_amount: amount,
        status,
        rawDetails: row,
      });
    }
  });

  return markers;
}
