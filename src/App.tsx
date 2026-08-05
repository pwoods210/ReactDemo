import { useState } from 'react'
import './App.css'
import ListGroup from './Components/ListGroup.tsx'
import Alert from './Components/Alert.tsx'
import Button from './Components/Button.tsx'

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
      <div className="ticks"></div>
      <section id="spacer"></section>
      <div id="tester">
        <ListGroup items={items} heading="Cities" onSelectItem={handleSelectItem}/>
      </div>
      <div className="ticks"></div>
      <section id="spacer"></section>
      <div id="Buy/Sell/Alert">
        {showAlert && <Alert onClose={() => setAlertState(false)}><span> ALERT </span></Alert>}
        <Button message="Alert" onClick={() => setAlertState(true)}/>
        <Button message="BUY" color="green" onClick={handleButtonClick}/>
        <Button message="SELL" color="red" onClick={handleButtonClick}/>
      </div>
    </>
  )
}

export default App