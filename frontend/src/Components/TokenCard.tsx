import { useState } from "react";

import type {
  DiscoveredToken,
  DiscoveryStatus,
} from "../Common/types";

interface TokenCardProps {
  token: DiscoveredToken;
  onDismiss?: () => void;
  isDismissing?: boolean;
  isEntering?: boolean;
}

const statusClasses: Record<DiscoveryStatus, string> = {
  new: "text-bg-success",
  watching: "text-bg-warning",
  graduated: "text-bg-primary",
};

function shortenAddress(address: string) {
  return `${address.slice(0, 7)}...${address.slice(-7)}`;
}

function getTokenImageUrl(token: DiscoveredToken) {
  const profileIcon = token.tokenProfile.icon?.trim();

  if (profileIcon) {
    return profileIcon;
  }

  return token.pairs.find((pair) => pair.info?.imageUrl)?.info?.imageUrl;
}

function TokenCard({
  token,
  onDismiss,
  isDismissing = false,
  isEntering = false,
}: TokenCardProps) {
  const imageUrl = getTokenImageUrl(token);
  const [failedImageUrl, setFailedImageUrl] = useState<string | null>(null);
  const imageSrc = imageUrl && imageUrl !== failedImageUrl ? imageUrl : null;
  const discoveredTime = new Date(token.discoveredAt).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });

  return (
    <article
      className={`discovery-card${
        isDismissing ? " discovery-card--dismissing" : ""
      }${isEntering ? " discovery-card--entering" : ""}`}
    >
      <div className="discovery-card-header">
        <div className="token-identity">
          <div className="token-icon" aria-hidden={imageSrc ? undefined : true}>
            {imageSrc ? (
              <img
                className="token-icon-image"
                src={imageSrc}
                alt={`${token.name} icon`}
                onError={() => setFailedImageUrl(imageSrc)}
              />
            ) : (
              token.symbol.slice(0, 1)
            )}
          </div>
          <div>
            <div className="token-name">{token.name}</div>
            <div className="token-symbol">${token.symbol}</div>
          </div>
        </div>
        <div className="token-card-actions">
          <span
            className={`badge rounded-pill ${statusClasses[token.status]}`}
          >
            {token.status}
          </span>
          {onDismiss ? (
            <button
              type="button"
              className="token-dismiss-button"
              aria-label={`Dismiss ${token.name}`}
              onClick={onDismiss}
              disabled={isDismissing}
            >
              {isDismissing ? "…" : "×"}
            </button>
          ) : null}
        </div>
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
