import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { APP_BASE_URL } from '../config';
import Transaction from './Transaction'
import { Button } from 'react-bootstrap'

export default function TransactionPool() {
    const navigate = useNavigate();
    const [transactionPool, setTransactionPool] = useState([])

    const fetchTransactions = () => {
        fetch(`${APP_BASE_URL}/transaction`)
            .then(res => res.json())
            .then(data => setTransactionPool(data.reverse()))
            .catch(err => console.error('Error fetching blockchain length:', err));
    }

    useEffect(() => {
        fetchTransactions()
        const intervalid = setInterval(fetchTransactions, 10000)
        return () => clearInterval(intervalid)
    }, [])

    const fecthMineBlock = () => {
        fetch(`${APP_BASE_URL}/blockchain/mine`)
            .then(() => {
                alert('Success')
                navigate('/blockchain');
            })
            .catch(err => console.error('Error fetching blockchain length:', err));
    }

    return (
        <div>
            <Link to='/' >Home</Link>
            <br />

            <hr />
            <h1>TransactionPool</h1>
            {transactionPool.map((transaction, i) => (
                <div key={i}>
                    <hr />
                    <Transaction transaction={transaction} />
                </div>
            ))}
            <hr />
            <Button variant='danger' onClick={fecthMineBlock}>Mine Block of these transactionn</Button>
        </div>
    )
}
