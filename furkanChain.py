"""
furkanCoin (FC)
transaction_lists
x1 : Anıl Melih'e 100 FC yollar.
x2 : Burak Melih'e 200 FC yollar.
x3 : Melih Burak'a 30 FC yollar.
x4 : Deniz Anıl'a 500 FC yollar.
x5 : Melih Canan'a 1000 FC yollar.
x6 : Melih Deniz'e 200 FC yollar.

Blokların gösterimi
BLOCK1 ("AAA" , x1, x2, x3) -> fb34cc, BLOCK2("fb34cc", x4, x5, x6)  -> 77ab00, BLOCK3(323dd, x7)

"""

import hashlib
import json
import time


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 2
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
 
    def is_valid_proof(self, block, block_hash):
            return (block_hash.startswith('0' * Blockchain.difficulty) and
                    block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
                self.unconfirmed_transactions.append(transaction)
    
    def mine(self):
            if not self.unconfirmed_transactions:
                return False
    
            last_block = self.last_block
    
            new_block = Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
    
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index

from flask import Flask, request
import requests
 
app =  Flask(__name__)

blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
app.run(debug=True, port=5000)