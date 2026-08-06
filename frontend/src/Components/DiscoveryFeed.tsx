import { useEffect, useState } from "react";
import TokenCard from "./TokenCard";
import type { DiscoveredToken } from "./TokenCard";

const DISCOVERIES_URL = "http://localhost:8000/api/discoveries";

function DiscoveryFeed() {
  const [tokens, setTokens] = useState<DiscoveredToken[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadDiscoveries() {
      try {
        const response = await fetch(DISCOVERIES_URL, {
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(
            `Discovery request failed with status ${response.status}`,
          );
        }
        const discoveredTokens =
          (await response.json()) as DiscoveredToken[];

        setTokens(discoveredTokens);
      } catch (requestError) {
        if (
          requestError instanceof DOMException &&
          requestError.name === "AbortError"
        ) {
          return;
        }
        const message =
          requestError instanceof Error
            ? requestError.message
            : "An unknown error occurred.";

        setError(message);
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    }

    void loadDiscoveries();

    return () => {
      controller.abort();
    };
  }, []);

  const tokenCountLabel =
    tokens.length === 1
      ? "1 token"
      : `${tokens.length} tokens`;

  return (
    <section className="discovery-feed">
      <header className="discovery-feed-header">
        <div>
          <div className="discovery-feed-label live-pulse">
            Live discovery
          </div>
          <h2 className="discovery-feed-title">
            Recently discovered tokens
          </h2>
        </div>
        <span className="badge rounded-pill text-bg-secondary">
          {tokenCountLabel}
        </span>
      </header>
      <div className="discovery-feed-content">
        {isLoading && (
          <p className="text-secondary mb-0">
            Loading discovered tokens...
          </p>
        )}
        {!isLoading && error && (
          <div className="alert alert-danger mb-0" role="alert">
            Unable to load discoveries: {error}
          </div>
        )}
        {!isLoading && !error && tokens.length === 0 && (
          <p className="text-secondary mb-0">
            Listening for new token discoveries...
          </p>
        )}
        {!isLoading &&
          !error &&
          tokens.map((token) => (
            <TokenCard
              key={token.tokenAddress}
              token={token}
            />
          ))}
      </div>
    </section>
  );
}

export default DiscoveryFeed;