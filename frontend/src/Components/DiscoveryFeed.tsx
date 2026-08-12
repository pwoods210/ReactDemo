import { useQuery } from "@tanstack/react-query";

import TokenCard from "./TokenCard";
import type { DiscoveredToken } from "./TokenCard";


const DISCOVERIES_URL = "http://localhost:8000/api/discoveries";


async function fetchDiscoveries(
  signal: AbortSignal,
): Promise<DiscoveredToken[]> {
  const response = await fetch(DISCOVERIES_URL, {
    signal,
  });

  if (!response.ok) {
    throw new Error(
      `Discovery request failed with status ${response.status}`,
    );
  }

  return response.json();
}


function DiscoveryFeed() {
  const {
    data: tokens = [],
    isPending,
    isError,
    error,
    isFetching,
  } = useQuery({
    queryKey: ["discoveries"],
    queryFn: ({ signal }) => fetchDiscoveries(signal),

    // Temporary polling until we add the live SSE connection.
    refetchInterval: 5000,
  });

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

        <div className="d-flex align-items-center gap-2">
          {isFetching && !isPending && (
            <span className="text-secondary small">
              Refreshing...
            </span>
          )}

          <span className="badge rounded-pill text-bg-secondary">
            {tokenCountLabel}
          </span>
        </div>
      </header>

      <div className="discovery-feed-content">
        {isPending && (
          <p className="text-secondary mb-0">
            Loading discovered tokens...
          </p>
        )}

        {isError && (
          <div className="alert alert-danger mb-0" role="alert">
            Unable to load discoveries: {error.message}
          </div>
        )}

        {!isPending && !isError && tokens.length === 0 && (
          <p className="text-secondary mb-0">
            Listening for new token discoveries...
          </p>
        )}

        {!isError &&
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