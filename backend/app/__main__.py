import os
import random
import requests as req
from backend.app import app, blockchain, transaction_pool, pubsub, PORT, ROOT_PORT, Wallet, Blockchain , Transaction

# Only run this if started directly via `python -m backend.app`
if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    result = req.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('Successfully synchronized the local chain with others')
    except Exception as e:
        print(f'Error in synchronizing: {e}')
if os.environ.get('SEED_DATA')== 'True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(),Wallet().address,random.randint(2,50)).to_json(),
            Transaction(Wallet(),Wallet().address,random.randint(2,50)).to_json(),

        ])
    for i in range(3):
        transaction_pool.set_transaction(
            Transaction(Wallet(),Wallet().address,random.randint(2,50)),
        )
app.run(port=PORT)

