export type DiscoveryStatus =
  | "new"
  | "watching"
  | "graduated";

export interface DiscoveredToken {
  id: number,
  name: string;
  symbol: string;
  tokenAddress: string;
  source: string;
  discoveredAt: string;
  status: DiscoveryStatus;
}

export type ServiceStatus = "up" | "down";

export interface ServiceHealth {
  status: ServiceStatus;
}

export interface ServicesHealthResponse {
  discovery: ServiceHealth;
  trade: ServiceHealth;
  database: ServiceHealth;
}