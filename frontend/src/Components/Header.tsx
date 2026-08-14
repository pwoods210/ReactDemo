import { useQuery } from "@tanstack/react-query";
import { getServicesHealth } from "../api/health";
import { ServiceBadge } from "./ServiceBadge";
import appLogo from "../assets/turmemeal_icon.svg";

function Header() {
  const {
    data: serviceHealth,
    isError,
  } = useQuery({
    queryKey: ["service-health"],
    queryFn: getServicesHealth,
    refetchInterval: 5000,
  });

  return (
    <header className="app-header">
      <div className="container-fluid px-3 px-md-4 py-3">
        <div className="d-flex flex-wrap align-items-center justify-content-between gap-3">
          <div className="d-flex align-items-center gap-3">
            <div className="app-brand-mark">
              <img
                src={appLogo}
                alt=""
                aria-hidden="true"
                className="app-brand-logo"
              />
            </div>
            <div>
              <div className="app-title">TerMEMEal</div>
              <div className="app-subtitle fst-italic">
                Solana meme-pair trading dashboard
              </div>
            </div>
          </div>
          <div className="header-status d-flex align-items-center gap-3">
            <ServiceBadge
              name="Discovery Service"
              status={
                isError
                  ? "unknown"
                  : serviceHealth?.discovery.status ?? "unknown"
              }
            />
            <ServiceBadge
              name="Trade Service"
              status={
                isError
                  ? "unknown"
                  : serviceHealth?.trade.status ?? "unknown"
              }
            />
            <ServiceBadge
              name="Database Service"
              status={
                isError
                  ? "unknown"
                  : serviceHealth?.database.status ?? "unknown"
              }
            />
            <div className="wallet-status">
              <span className="status-dot" aria-hidden="true"></span>
              <span>Wallet disconnected</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;