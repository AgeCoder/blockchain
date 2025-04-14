import React, { useEffect, useState } from 'react';
import { APP_BASE_URL } from '../config';
import Block from './Block';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom'

const PAGE_RANGE = 3;

export default function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0);

    const fetchBlockchainPage = ({ start, end }) => {
        fetch(`${APP_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
            .then(res => res.json())
            .then(data => setBlockchain(data))
            .catch(err => console.error('Error fetching blockchain page:', err));
    };

    useEffect(() => {
        fetchBlockchainPage({ start: 0, end: PAGE_RANGE });
        fetch(`${APP_BASE_URL}/blockchain/length`)
            .then(res => res.json())
            .then(data => setBlockchainLength(data))
            .catch(err => console.error('Error fetching blockchain length:', err));
    }, []);

    const totalPages = Math.ceil(blockchainLength / PAGE_RANGE);

    return (
        <div className="Blockchain">
            <Link to='/' >Home</Link>
            <hr />
            <h1>Blockchain</h1>

            <div>
                {blockchain.map((block, i) => (
                    <div key={block.hash || i}>
                        <Block block={block} />
                    </div>
                ))}
            </div>

            <div className="pagination">
                {Array.from({ length: totalPages }, (_, index) => {
                    const start = index * PAGE_RANGE;
                    const end = (index + 1) * PAGE_RANGE;

                    return (
                        <span key={index} onClick={() => fetchBlockchainPage({ start, end })}>
                            <Button size="sm" variant="danger" className="m-1">
                                {index + 1}
                            </Button>
                        </span>
                    );
                })}
            </div>
        </div>
    );
}
