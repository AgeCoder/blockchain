import React, { useEffect, useState } from 'react'
import { FormGroup, FormControl, Button } from "react-bootstrap";
import { APP_BASE_URL } from '../config'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';

export default function ConductTransaction() {
    const [amount, setAmount] = useState(0)
    const [recipient, setRecipient] = useState('')
    const [knownAddresses, setKnownAddresses] = useState([])
    const navigate = useNavigate();

    useEffect(() => {
        fetch(`${APP_BASE_URL}/known-addresses`)
            .then(res => res.json())
            .then(json => setKnownAddresses(json))
    }, [])

    const onSubmit = (e) => {
        e.preventDefault();
        fetch(`${APP_BASE_URL}/wallet/transact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipient, amount })
        })
            .then(rep => rep.json())
            .then(rep => {
                console.log('submitTransaction json');
                alert('SUCCESS!');
                navigate('/transactionPool');
            })
            .catch(err => {
                console.error('Transaction error:', err);
                alert('Request was not able to complete');
            });
    }
    return (
        <div className='ConductTransaction'>
            <Link to='/' >Home</Link>
            <h3>Make a Transaction</h3>
            <FormGroup>
                <FormControl
                    input='text'
                    placeholder='recipient'
                    value={recipient}
                    onChange={(e) => { setRecipient(e.target.value) }}
                />
            </FormGroup>
            <FormGroup>
                <FormControl
                    input='number'
                    placeholder='Amount'
                    value={amount}
                    onChange={(e) => { setAmount(Number(e.target.value)) }}

                />
            </FormGroup>
            <div>
                <Button
                    variant='danger'
                    onClick={onSubmit}
                >
                    Submit
                </Button>
            </div>
            <hr />
            <br />
            <h4>Known Addresses</h4>
            <div>
                {knownAddresses.map((address, i) => (
                    <span key={address}>
                        <u>{address}</u> {i !== address.length - 1 ? ', ' : ' '}
                    </span>
                ))}
            </div>
        </div>
    )
}
