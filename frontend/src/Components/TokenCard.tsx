export type DiscoveryStatus = "new" | "watching" | "graduated";

export interface DiscoveredToken {
  name: string;
  symbol: string;
  tokenAddress: string;
  source: string;
  discoveredAt: string;
  status: DiscoveryStatus;
}

interface TokenCardProps {
  token: DiscoveredToken;
}

const statusClasses: Record<DiscoveryStatus, string> = {
  new: "text-bg-success",
  watching: "text-bg-warning",
  graduated: "text-bg-primary",
};

function shortenAddress(address: string) {
  return `${address.slice(0, 7)}...${address.slice(-7)}`;
}

function TokenCard({ token }: TokenCardProps) {
  const discoveredTime = new Date(token.discoveredAt).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });

  return (
    <article className="discovery-card">
      <div className="discovery-card-header">
        <div className="token-identity">
          <div className="token-icon" aria-hidden="true">
            {token.symbol.slice(0, 1)}
          </div>
          <div>
            <div className="token-name">{token.name}</div>
            <div className="token-symbol">${token.symbol}</div>
          </div>
        </div>
        <span
          className={`badge rounded-pill ${statusClasses[token.status]}`}
        >
          {token.status}
        </span>
      </div>
      <div className="token-address-row">
        <span className="token-detail-label">Token address</span>
        <code title={token.tokenAddress}>
          {shortenAddress(token.tokenAddress)}
        </code>
      </div>
      <div className="discovery-card-details">
        <div>
          <span className="token-detail-label">Source</span>
          <span>{token.source}</span>
        </div>
        <div>
          <span className="token-detail-label">Discovered</span>
          <span>{discoveredTime}</span>
        </div>
        <div>
          <span className="token-detail-label">Status</span>
          <span>{token.status}</span>
        </div>
      </div>
    </article>
  );
}

export default TokenCard;