export type DiscoveryStatus =
  | "new"
  | "watching"
  | "graduated";


export interface DiscoveredToken {
  id: number;
  name: string;
  symbol: string;
  tokenAddress: string;
  source: string;
  discoveredAt: string;
  status: DiscoveryStatus;
}


export type ServiceStatus =
  | "up"
  | "down"
  | "unknown"
  | "degraded"
  | "inactive";


export type GroupStatus =
  | "healthy"
  | "degraded"
  | "critical"
  | "checking";


export interface ServiceHealth {
  status: ServiceStatus;
}


export interface ServicesHealthResponse {
  discovery: ServiceHealth;
  trade: ServiceHealth;
  database: ServiceHealth;
  api: ServiceHealth;
}


export interface ServiceHealthItem {
  label: string;
  status: ServiceStatus;
  detail?: string;
}


export interface ServiceHealthMap {
  discovery: ServiceHealthItem;
  trade: ServiceHealthItem;
  database: ServiceHealthItem;
  api: ServiceHealthItem;
}