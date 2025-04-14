import React from 'react'

export default function Transaction({ transaction }) {
    const { input, output } = transaction
    const recipients = Object.keys(output)
    return (
        <div className="Transaction">
            <div>From: {input.address} </div>
            {
                recipients.map((recipient, i) => (
                    <div key={i}>
                        TO : {recipient} | Sent : {output[recipient]}
                    </div>
                ))
            }
        </div>
    )
}
