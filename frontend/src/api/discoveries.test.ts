import { afterEach, describe, expect, it, vi } from "vitest";

import { fetchDiscoveries } from "./discoveries";

const token = {
  id: 1,
  name: "Example Token",
  symbol: "EXAMPLE",
  tokenAddress: "token-123",
  source: "DexScreener",
  discoveredAt: "2026-08-31T00:00:00Z",
  status: "new" as const,
};

describe("fetchDiscoveries", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns discoveries from a successful response", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [token],
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(fetchDiscoveries()).resolves.toEqual([token]);
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/discoveries",
      { signal: undefined },
    );
  });

  it("throws when the discovery response is not successful", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 503,
      }),
    );

    await expect(fetchDiscoveries()).rejects.toThrow(
      "Discovery request failed with status 503",
    );
  });
});
