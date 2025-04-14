import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import TransactionPool from './components/TransactionPool';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<App />} />
      <Route path='/blockchain' element={<Blockchain />} />
      <Route path='/transaction' element={<ConductTransaction />} />
      <Route path='/transactionPool' element={<TransactionPool />} />
    </Routes>
  </BrowserRouter>
);
