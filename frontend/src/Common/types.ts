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