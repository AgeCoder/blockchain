import React, { useState } from 'react'
import { MILLI_SEC_py } from '../config';
import Transaction from './Transaction';
import { Button } from 'react-bootstrap'

function ToggleTransactionBlock({ block }) {
    const [displayTrnsaction, setdisplayTrnsaction] = useState(false)

    if (displayTrnsaction) {
        return (
            <div>
                {block.map((data, i) => (
                    <div key={i}>
                        <hr />
                        <Transaction transaction={data} />
                    </div>

                ))}
                <br />
                <Button
                    variant='danger'
                    size='sm'
                    onClick={() => { setdisplayTrnsaction(!displayTrnsaction) }}
                >
                    Show Less
                </Button>
            </div>
        )
    }

    return (
        <div>
            <br />

            <Button
                variant='danger'
                size='sm'
                onClick={() => { setdisplayTrnsaction(!displayTrnsaction) }}
            >
                Show More
            </Button>
        </div>
    )
}

export default function Block({ block }) {
    const { timestamp, hash, data } = block
    const hashDisplay = `${hash.substring(0, 15)}...}`
    const timestampDisplay = new Date(timestamp / MILLI_SEC_py).toLocaleString();

    return (
        <div className='Block'>
            <div>Hash: {hashDisplay}</div>
            <div>Timestamp: {timestampDisplay}</div>
            <ToggleTransactionBlock block={data} />
        </div>
    )
}
