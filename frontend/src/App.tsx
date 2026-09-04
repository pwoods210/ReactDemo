import './App.css'
import Header from './Components/Header.tsx'
import TradePanel from './Components/TradePanel.tsx'
import DiscoveryFeed from './Components/DiscoveryFeed.tsx'

function App() {
  return (
    <>
      <Header />
      <main className="container py-4">
        <div id="discovery_feed">
          <DiscoveryFeed />
        </div>
        <div id="trade_panel">
          <TradePanel />
        </div>
      </main>
    </>
  );
}

export default App
