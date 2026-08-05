import { useState } from 'react'
import './App.css'
import ListGroup from './Components/ListGroup.tsx'
import Alert from './Components/Alert.tsx'
import Button from './Components/Button.tsx'
import Header from './Components/Header.tsx'
import TradePanel from './Components/TradePanel.tsx'

function App() {
  const [showAlert, setAlertState] = useState(false)
  let items = ["New York", "San Francisco", "Tokyo", "London", "Paris"]
  const handleSelectItem = (item: string) => {
    console.log(item);
  }
  const handleButtonClick = () => {
    console.log("Button has been clicked.")
  }

  return (
    <>
      <Header />
      <main className="container py-4">
        <div id="trade_panel">
          <TradePanel />
        </div>
      </main>
    </>
  );
}

export default App