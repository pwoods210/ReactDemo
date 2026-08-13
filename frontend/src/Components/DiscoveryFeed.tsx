import { useEffect, useRef } from "react";
import { useQuery } from "@tanstack/react-query";

import { fetchDiscoveries } from "../api/discoveries";
import DiscoveryScrollControl from "./DiscoveryScroll";
import TokenCard from "./TokenCard";


export default function DiscoveryFeed() {
  const feedRef = useRef<HTMLDivElement>(null);

  // Remembers whether the user is currently following the newest discoveries.
  const isAtNewestRef = useRef(true);

  // Lets us distinguish a new token being added from a normal query refetch.
  const previousTokenCountRef = useRef(0);

  const {
    data: tokens = [],
    isPending,
    isError,
    error,
    isFetching,
  } = useQuery({
    queryKey: ["discoveries"],
    queryFn: ({ signal }) => fetchDiscoveries(signal),
    refetchInterval: 5000,
  });


  function handleFeedScroll() {
    const feed = feedRef.current;

    if (!feed) {
      return;
    }

    const distanceFromRight =
      feed.scrollWidth -
      feed.clientWidth -
      feed.scrollLeft;

    // Small tolerance avoids issues caused by fractional pixel positions.
    isAtNewestRef.current = distanceFromRight <= 8;
  }


  useEffect(() => {
    const previousCount = previousTokenCountRef.current;
    const hasNewToken = tokens.length > previousCount;

    if (hasNewToken && isAtNewestRef.current) {
      requestAnimationFrame(() => {
        const feed = feedRef.current;

        if (!feed) {
          return;
        }

        feed.scrollTo({
          left: feed.scrollWidth,
          behavior: "smooth",
        });
      });
    }

    previousTokenCountRef.current = tokens.length;
  }, [tokens.length]);


  return (
    <section className="discovery-feed">
      <div className="discovery-feed-header">
        <div>
          <div className="discovery-feed-label">
            Live Discovery
          </div>

          <h2 className="discovery-feed-title">
          </h2>
        </div>

        {isFetching && !isPending && (
          <span className="text-body-secondary small">
            Updating...
          </span>
        )}
      </div>


      {isPending && (
        <div className="text-body-secondary">
          Loading discoveries...
        </div>
      )}


      {isError && (
        <div className="alert alert-danger mb-0">
          {error instanceof Error
            ? error.message
            : "Failed to load discoveries."}
        </div>
      )}


      {!isPending && !isError && tokens.length === 0 && (
        <div className="text-body-secondary">
          Waiting for token discoveries...
        </div>
      )}


      {!isPending && !isError && tokens.length > 0 && (
        <>
          <div className="discovery-feed-viewport">
            <div
              ref={feedRef}
              className="discovery-feed-content"
              onScroll={handleFeedScroll}
            >
              {[...tokens].reverse().map((token) => (
                <TokenCard
                  key={token.id}
                  token={token}
                />
              ))}
            </div>
          </div>

          {tokens.length > 1 && (
            <DiscoveryScrollControl
              scrollContainerRef={feedRef}
            />
          )}
        </>
      )}
    </section>
  );
}