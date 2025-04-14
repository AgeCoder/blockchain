from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT
from backend.wallet.wallet import Wallet
class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self,data):
        self.chain.append(Block.min_block(self.chain[-1],data))
    
    def replace_chain(self,chain):
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace, The incoming chain must be longer')
        
        try:
            Blockchain.is_vaild_chain(chain)
        except Exception as e :
            raise Exception(f'Cannot replace, The incoming chain must be vaild {e}')
        
        self.chain = chain


    def __repr__(self):
        return f'Blockchain: {self.chain}'
    
    def to_json(self):
        return list(map(lambda block : block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block : Block.from_json(block) , chain_json))
        return blockchain

    @staticmethod
    def is_vaild_chain(chain):

        if chain[0] != Block.genesis():
            raise Exception('Genesis Block Must be Vaild')

        for i in range(1,len(chain)):
            Block.is_valid_block(chain[i-1],chain[i])

        Blockchain.is_vaild_transaction_chain(chain)
        
    @staticmethod
    def is_vaild_transaction_chain(chain):
        transaction_id = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transation_json in block.data:
                transaction = Transaction.from_json(transation_json)

                if transaction.id in transaction_id:
                    raise Exception(f'Transaction is not unique')
                
                transaction_id.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There can only be one mining reward per Block. '\
                            f'Check block with hash {block.hash}'
                        )
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]

                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )
                    if historic_balance != transaction.input['amount']:
                        raise Exception('Transaction has an invalid amount')
               
                Transaction.is_vaild(transaction)

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    blockchain.add_block('three')

    print(blockchain)

if __name__ == '__main__':
    main()