import time
from backend.utils.cryptohash import crypto_hash
from backend.config import MINRATE
from backend.utils.hex_to_binary import hex_to_binary


GENESIS_DATA = {
    'timestamp' : 1,
    'last_hash' : 'genesis_last_hash',
    'hash' : 'genesis_hash',
    'data' : [],
    'difficulty' : 3,
    'nonce' : 0
}

class Block:
    def __init__(self,timestamp,last_hash,hash,data,difficulty,nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
    

    def __repr__(self):
        return (
            'Block('
            f' timestamp: {self.timestamp}, '
            f' last_hash: {self.last_hash}, '
            f' data: {self.data},  '
            f' hash: {self.hash},  '
            f' difficulty : {self.difficulty}, '
            f' nonce : {self.nonce} '
            )
    
    def __eq__(self, value):
        return self.__dict__ == value.__dict__

    def to_json(self):
        return self.__dict__
    
    @staticmethod
    def min_block(last_block,data):
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block,timestamp)
        nonce = 0
        hash = crypto_hash(timestamp,last_hash,data,difficulty,nonce)

        while hex_to_binary(hash)[0:difficulty] != '0'*difficulty:
            nonce+=1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp,last_hash,data,difficulty,nonce)
        
        
        return Block(timestamp,last_hash,hash,data,difficulty,nonce)

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)   

    @staticmethod
    def from_json(block_json):
        return Block(**block_json) 

    @staticmethod
    def adjust_difficulty(last_block,new_timestamp):
        if (new_timestamp - last_block.timestamp) < MINRATE:
            return last_block.difficulty + 1
        if (last_block.difficulty - 1) > 0 :
            return last_block.difficulty - 1
        return 1
    
    @staticmethod
    def is_valid_block(last_block,block):
        
        if  block.last_hash != last_block.hash:
            raise Exception('The Block last_hash does not match')
        if hex_to_binary(block.hash)[0:block.difficulty] != '0'*block.difficulty:
            raise Exception('The proof of works is not met')
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must be adjusted by only 1')
        
        reconstructes_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
            )
        
        if reconstructes_hash != block.hash:
            raise Exception('The Block Does not Macth')

def main():
    genesis_block = Block.genesis()
    block = Block.min_block(genesis_block,'foo')
    # block.data = "changed your data haha"
    try:
        Block.is_valid_block(genesis_block,block)
    except Exception as e:
        print(f'Error {e}')

if __name__ == '__main__':
    main()