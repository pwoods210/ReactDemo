import appLogo from "../assets/turmemeal_icon.svg";

function Header() {
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
            <span className="badge rounded-pill text-bg-warning">
              Paper Mode
            </span>
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