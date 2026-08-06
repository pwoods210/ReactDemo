import TokenCard from "./TokenCard";
import type { DiscoveredToken } from "./TokenCard";

const exampleToken: DiscoveredToken = {
  name: "Example Meme Token",
  symbol: "MEME",
  tokenAddress: "7YxExampleTokenAddress123456789ABCDEFG",
  source: "DexScreener",
  discoveredAt: "2026-08-05T21:00:00-04:00",
  status: "new",
};

function DiscoveryFeed() {
  return (
    <section className="discovery-feed">
      <div className="discovery-feed-header">
        <div className="discovery-feed-label">Live discovery</div>
        <span className="badge rounded-pill text-bg-secondary">
          1 token
        </span>
      </div>
      <div className="discovery-feed-content">
        <TokenCard token={exampleToken} />
      </div>
    </section>
  );
}

export default DiscoveryFeed;