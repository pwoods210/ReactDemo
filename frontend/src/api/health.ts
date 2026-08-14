import type { ServiceHealth, ServicesHealthResponse } from "../Common/types";

export async function getServicesHealth(): Promise<ServicesHealthResponse> {
  const response = await fetch("http://localhost:8000/health/services");

  if (!response.ok) {
    throw new Error("Failed to fetch service health");
  }

  return response.json();
}