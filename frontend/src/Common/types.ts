export type DiscoveryStatus =
  | "new"
  | "watching"
  | "graduated";

export interface DiscoveredToken {
  name: string;
  symbol: string;
  tokenAddress: string;
  source: string;
  discoveredAt: string;
  status: DiscoveryStatus;
}