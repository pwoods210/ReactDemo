import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { DiscoveredToken } from "../Common/types";
import TokenCard from "./TokenCard";

const token: DiscoveredToken = {
  id: 1,
  name: "Example Token",
  symbol: "EXAMPLE",
  tokenAddress: "1234567890abcdefghijklmnopqrstuvwxyz",
  source: "DexScreener",
  discoveredAt: "2026-08-31T12:34:00Z",
  status: "watching",
};

describe("TokenCard", () => {
  it("renders token identity, address, source, time, and status", () => {
    render(<TokenCard token={token} />);

    expect(screen.getByText("Example Token")).toBeInTheDocument();
    expect(screen.getByText("$EXAMPLE")).toBeInTheDocument();
    expect(screen.getByTitle(token.tokenAddress)).toHaveTextContent(
      "1234567...tuvwxyz",
    );
    expect(screen.getByText("DexScreener")).toBeInTheDocument();
    expect(screen.getAllByText("watching")).toHaveLength(2);
  });

  it("uses the first symbol letter as the token emblem", () => {
    render(<TokenCard token={token} />);

    const emblem = document.querySelector(".token-icon");

    expect(emblem).toHaveTextContent("E");
  });
});
