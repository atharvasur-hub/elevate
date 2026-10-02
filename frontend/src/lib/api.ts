import { NaturalLanguageQueryRequest, NaturalLanguageQueryResponse } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function askNaturalLanguageQuery(
  request: NaturalLanguageQueryRequest
): Promise<NaturalLanguageQueryResponse> {
  const url = `${API_BASE_URL}/api/v1/query/ask`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      question: request.question,
      include_summary: request.include_summary ?? true,
    }),
  });

  if (!response.ok) {
    let errorDetail = "Failed to fetch response from FastAPI backend";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorData.message || JSON.stringify(errorData);
    } catch {
      errorDetail = `HTTP ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export async function checkBackendHealth(): Promise<{ status: "online" | "offline"; message?: string }> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);
    const res = await fetch(`${API_BASE_URL}/api/v1/health`, {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    if (res.ok) {
      return { status: "online" };
    }
    return { status: "offline", message: `Status code ${res.status}` };
  } catch (err: any) {
    return { status: "offline", message: err?.message || "Connection refused" };
  }
}
