export interface NaturalLanguageQueryRequest {
  question: string;
  include_summary?: boolean;
}

export interface NaturalLanguageQueryResponse {
  question: string;
  sql_query: string;
  results: Record<string, any>[];
  row_count: number;
  summary?: string | null;
  execution_time_ms: number;
}

export interface LocationCoordinate {
  name: string;
  lat: number;
  lng: number;
  state?: string;
  district?: string;
}

export interface MapMarkerData {
  id: string | number;
  title: string;
  lat: number;
  lng: number;
  state?: string;
  district?: string;
  sub_district?: string;
  scheme_name?: string;
  allocated_amount?: number;
  disbursed_amount?: number;
  utilized_amount?: number;
  status?: string;
  rawDetails?: Record<string, any>;
}
