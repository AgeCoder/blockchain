import { useEffect, useState } from 'react';
import logo from '../asset/logo.png'
import { APP_BASE_URL } from '../config'
import { Link } from 'react-router-dom'
function App() {
  const [walletInfo, setwalletInfo] = useState({})

  useEffect(() => {
    fetch(`${APP_BASE_URL}/wallet/info`).then(res => res.json()).then(
      json => setwalletInfo(json)
    )
  }, [])

  const { address, balance } = walletInfo

  return (
    <div className="App mb-10">
      <img src={logo} alt="Logo" height={400} width={400} />
      <h1>Welcome To Agechain</h1>
      <br />
      <Link to='/blockchain' >Blockchain</Link>
      <Link to='/transaction' >Conduct aTransaction</Link>
      <Link to='/transactionPool' >TransactionPool</Link>
      <br />
      <div className='WalletInfo'>
        <p>Address: {address}</p>
        <p>Balance: {balance}</p>
      </div>
    </div>
  );
}

export default App;
