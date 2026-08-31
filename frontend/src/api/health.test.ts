import { afterEach, describe, expect, it, vi } from "vitest";

import { getServicesHealth } from "./health";

describe("getServicesHealth", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("combines service health with the API health check", async () => {
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL) => {
      if (String(input).endsWith("/health/services")) {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            discovery: { status: "up" },
            trade: { status: "down" },
            database: { status: "up" },
          }),
        });
      }

      return Promise.resolve({
        ok: true,
        json: async () => true,
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(getServicesHealth()).resolves.toEqual({
      discovery: { status: "up" },
      trade: { status: "down" },
      database: { status: "up" },
      api: { status: "up" },
    });
  });

  it("marks the API down when its health endpoint fails", async () => {
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL) => {
      if (String(input).endsWith("/health/services")) {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            discovery: { status: "up" },
            trade: { status: "down" },
            database: { status: "up" },
          }),
        });
      }

      return Promise.resolve({
        ok: false,
        json: async () => false,
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(getServicesHealth()).resolves.toMatchObject({
      api: { status: "down" },
    });
  });

  it("throws when the services health endpoint fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
      }),
    );

    await expect(getServicesHealth()).rejects.toThrow(
      "Failed to fetch service health",
    );
  });
});
