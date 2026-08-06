import { useState } from 'react'
import './App.css'
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