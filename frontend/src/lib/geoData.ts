import { MapMarkerData } from "@/types";

// Geographic coordinates lookup for Indian states and prominent districts
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
  "telangana": { lat: 18.1124, lng: 79.0193 },
  "andhra pradesh": { lat: 15.9129, lng: 79.7400 },
  "west bengal": { lat: 22.9868, lng: 87.8550 },
  "kerala": { lat: 10.8505, lng: 76.2711 },
  "punjab": { lat: 31.1471, lng: 75.3412 },
  "haryana": { lat: 29.0588, lng: 76.0856 },
  "delhi": { lat: 28.7041, lng: 77.1025 },

  // Districts & Cities
  "pune": { lat: 18.5204, lng: 73.8567 },
  "varanasi": { lat: 25.3176, lng: 82.9739 },
  "bengaluru rural": { lat: 13.2291, lng: 77.5815 },
  "bengaluru": { lat: 12.9716, lng: 77.5946 },
  "bangalore": { lat: 12.9716, lng: 77.5946 },
  "ahmedabad": { lat: 23.0225, lng: 72.5714 },
  "jaipur": { lat: 26.9124, lng: 75.7873 },
  "indore": { lat: 22.7196, lng: 75.8577 },
  "patna": { lat: 25.5941, lng: 85.1376 },
  "coimbatore": { lat: 11.0168, lng: 76.9558 },
  "khordha": { lat: 20.1800, lng: 85.6200 },
  "bhubaneswar": { lat: 20.2961, lng: 85.8245 },
  "kamrup": { lat: 26.3100, lng: 91.5900 },
  "guwahati": { lat: 26.1445, lng: 91.7362 },
  "haveli": { lat: 18.5000, lng: 73.9100 },
  "sadar": { lat: 25.3300, lng: 82.9900 },
  "hoskote": { lat: 13.0694, lng: 77.7981 },
  "daskroi": { lat: 22.9500, lng: 72.6300 },
  "sanganer": { lat: 26.8167, lng: 75.7833 },
  "sanwer": { lat: 22.9750, lng: 75.8300 },
  "danapur": { lat: 25.6333, lng: 85.0500 },
  "pollachi": { lat: 10.6588, lng: 77.0084 },
  "mumbai": { lat: 19.0760, lng: 72.8777 },
  "lucknow": { lat: 26.8467, lng: 80.9462 },
  "hyderabad": { lat: 17.3850, lng: 78.4867 },
  "chennai": { lat: 13.0827, lng: 80.2707 },
  "kolkata": { lat: 22.5726, lng: 88.3639 },
};

// Default seed markers to show on initial load
export const DEFAULT_MAP_MARKERS: MapMarkerData[] = [
  {
    id: 1,
    title: "Pune (Haveli), Maharashtra",
    lat: 18.5204,
    lng: 73.8567,
    state: "Maharashtra",
    district: "Pune",
    sub_district: "Haveli",
    scheme_name: "PM-KISAN",
    allocated_amount: 450.0,
    disbursed_amount: 420.0,
    utilized_amount: 410.5,
    status: "Fully Utilized",
  },
  {
    id: 2,
    title: "Varanasi (Sadar), Uttar Pradesh",
    lat: 25.3176,
    lng: 82.9739,
    state: "Uttar Pradesh",
    district: "Varanasi",
    sub_district: "Sadar",
    scheme_name: "PMAY-G",
    allocated_amount: 320.0,
    disbursed_amount: 290.0,
    utilized_amount: 275.0,
    status: "Partially Utilized",
  },
  {
    id: 3,
    title: "Bengaluru Rural (Hoskote), Karnataka",
    lat: 13.2291,
    lng: 77.5815,
    state: "Karnataka",
    district: "Bengaluru Rural",
    sub_district: "Hoskote",
    scheme_name: "MGNREGA",
    allocated_amount: 510.0,
    disbursed_amount: 480.0,
    utilized_amount: 470.0,
    status: "Fully Utilized",
  },
  {
    id: 4,
    title: "Ahmedabad (Daskroi), Gujarat",
    lat: 23.0225,
    lng: 72.5714,
    state: "Gujarat",
    district: "Ahmedabad",
    sub_district: "Daskroi",
    scheme_name: "AB-PMJAY",
    allocated_amount: 280.0,
    disbursed_amount: 260.0,
    utilized_amount: 240.0,
    status: "Disbursed",
  },
  {
    id: 5,
    title: "Jaipur (Sanganer), Rajasthan",
    lat: 26.9124,
    lng: 75.7873,
    state: "Rajasthan",
    district: "Jaipur",
    sub_district: "Sanganer",
    scheme_name: "JJM",
    allocated_amount: 620.0,
    disbursed_amount: 550.0,
    utilized_amount: 510.0,
    status: "Under Execution",
  },
  {
    id: 6,
    title: "Indore (Sanwer), Madhya Pradesh",
    lat: 22.7196,
    lng: 75.8577,
    state: "Madhya Pradesh",
    district: "Indore",
    sub_district: "Sanwer",
    scheme_name: "PM-POSHAN",
    allocated_amount: 190.0,
    disbursed_amount: 180.0,
    utilized_amount: 175.0,
    status: "Fully Utilized",
  },
  {
    id: 7,
    title: "Patna (Danapur), Bihar",
    lat: 25.5941,
    lng: 85.1376,
    state: "Bihar",
    district: "Patna",
    sub_district: "Danapur",
    scheme_name: "PM-SVANIDHI",
    allocated_amount: 140.0,
    disbursed_amount: 120.0,
    utilized_amount: 110.0,
    status: "Partially Utilized",
  },
  {
    id: 8,
    title: "Coimbatore (Pollachi), Tamil Nadu",
    lat: 11.0168,
    lng: 76.9558,
    state: "Tamil Nadu",
    district: "Coimbatore",
    sub_district: "Pollachi",
    scheme_name: "PLI-AUTO",
    allocated_amount: 750.0,
    disbursed_amount: 700.0,
    utilized_amount: 680.0,
    status: "Under Execution",
  },
  {
    id: 9,
    title: "Khordha (Bhubaneswar), Odisha",
    lat: 20.2961,
    lng: 85.8245,
    state: "Odisha",
    district: "Khordha",
    sub_district: "Bhubaneswar",
    scheme_name: "SBM-U-2",
    allocated_amount: 230.0,
    disbursed_amount: 210.0,
    utilized_amount: 195.0,
    status: "Partially Utilized",
  },
  {
    id: 10,
    title: "Kamrup (Guwahati), Assam",
    lat: 26.1445,
    lng: 91.7362,
    state: "Assam",
    district: "Kamrup",
    sub_district: "Guwahati",
    scheme_name: "SAMARTH",
    allocated_amount: 95.0,
    disbursed_amount: 90.0,
    utilized_amount: 85.0,
    status: "Completed",
  },
];

export function extractMarkersFromResults(results: Record<string, any>[]): MapMarkerData[] {
  if (!results || results.length === 0) return [];

  const markers: MapMarkerData[] = [];

  results.forEach((row, index) => {
    let lat: number | undefined;
    let lng: number | undefined;
    let title = "";

    // 1. Check direct coordinates if present
    if (typeof row.lat === "number" && typeof row.lng === "number") {
      lat = row.lat;
      lng = row.lng;
    } else if (typeof row.latitude === "number" && typeof row.longitude === "number") {
      lat = row.latitude;
      lng = row.longitude;
    }

    // 2. Lookup by location keys
    const districtKey = (row.district || row.city || row.sub_district || "")
      .toString()
      .toLowerCase()
      .trim();
    const stateKey = (row.state || "").toString().toLowerCase().trim();

    if (!lat || !lng) {
      if (districtKey && INDIA_COORDINATES[districtKey]) {
        lat = INDIA_COORDINATES[districtKey].lat;
        lng = INDIA_COORDINATES[districtKey].lng;
      } else if (stateKey && INDIA_COORDINATES[stateKey]) {
        lat = INDIA_COORDINATES[stateKey].lat;
        lng = INDIA_COORDINATES[stateKey].lng;
      }
    }

    // If coordinates found, create marker
    if (lat !== undefined && lng !== undefined) {
      // Add slight jitter if duplicate exact coordinates exist
      const duplicateCount = markers.filter(
        (m) => Math.abs(m.lat - lat!) < 0.01 && Math.abs(m.lng - lng!) < 0.01
      ).length;
      const jitterLat = lat + (duplicateCount > 0 ? (duplicateCount * 0.04 * (duplicateCount % 2 === 0 ? 1 : -1)) : 0);
      const jitterLng = lng + (duplicateCount > 0 ? (duplicateCount * 0.04 * (duplicateCount % 3 === 0 ? 1 : -1)) : 0);

      title =
        row.name ||
        row.scheme_name ||
        [row.district, row.state].filter(Boolean).join(", ") ||
        `Record #${index + 1}`;

      markers.push({
        id: row.id || `marker-${index}`,
        title,
        lat: jitterLat,
        lng: jitterLng,
        state: row.state,
        district: row.district,
        sub_district: row.sub_district,
        scheme_name: row.scheme_name || row.name || row.scheme_code,
        allocated_amount: Number(row.allocated_amount || row.budget_allocated || 0),
        disbursed_amount: Number(row.disbursed_amount || 0),
        utilized_amount: Number(row.utilized_amount || 0),
        status: row.status,
        rawDetails: row,
      });
    }
  });

  return markers;
}
