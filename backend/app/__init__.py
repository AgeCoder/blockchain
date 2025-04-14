import os
import random
import requests as req

from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from flask_cors import CORS

app = Flask(__name__)
CORS(app,resources={r'/*':{'origins': 'http://localhost:3000'}})

ROOT_PORT = 5000
PORT = ROOT_PORT

blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def route_home():
    return 'Welcome to DOP Blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/range')
def route_blockchain_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    return jsonify(blockchain.to_json()[::-1][start:end])

@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    transaction_pool.clear_blockchain_transaction(blockchain)

    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.exisiting_transaction(wallet.address)

    if transaction:
        transaction.update(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )

    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address' : wallet.address , 'balance' : wallet.balance})

@app.route('/known-addresses')
def route_known_addresses():
    known_addresses = set()

    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())
            
    return jsonify(list(known_addresses))



@app.route('/transaction')
def route_transaction():
    return jsonify(transaction_pool.transaction_data())
    
# Optional: expose PORT and other objects if needed
__all__ = ['app', 'blockchain', 'wallet', 'transaction_pool', 'pubsub', 'PORT', 'ROOT_PORT']
