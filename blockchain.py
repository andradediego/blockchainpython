from functools import reduce
import hashlib as hl
import json
import pickle

#import files 
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10

class Blockchain:
	def __init__(self, hosting_node_id):
		genesis_block = Block(0, '', [], 0)
		self.chain = [genesis_block]
		self.__open_transactions = []
		self.load_data()
		self.hosting_node = hosting_node_id

	@property
	def chain(self):
		return self.__chain[:]

	@chain.setter
	def chain(self, val):
		self.__chain = val

	
	def get_open_transactions(self):
		return self.__open_transactions[:]

	def load_data(self):
		try:
			with open('blockchain.txt', mode='r') as f:
				file_content = f.readlines()
							
				blockchain = json.loads(file_content[0][:-1])
				self.chain = [
					Block(
						block['index'],
						block['previous_hash'],
						[Transaction(tx['sender'], tx['recipient'], tx['amount'])
							for tx in block['transactions']],
						block['proof'],
						block['timestamp']
					) for block in blockchain]

							
				open_transactions = json.loads(file_content[1])
				self.__open_transactions = [
					Transaction(tx['sender'], tx['recipient'], tx['amount'])
					for tx in open_transactions
				]
		except (IOError, IndexError):
			print('Handled excepetion...')
		finally:
			print('Cleanup')


	def save_data(self):
		try:
			with open('blockchain.txt', mode='w') as f:
				saveable_chain = [
					block.__dict__ for block in [
						Block(block_el.index, block_el.previous_hash, [
							tx.__dict__ for tx in block_el.transactions
						], block_el.proof, block_el.timestamp) for block_el in self.chain
					]
				]
				
				f.write(json.dumps(saveable_chain))
				f.write('\n')
				saveable_transactions = [tx.__dict__ for tx in self.__open_transactions]
				f.write(json.dumps(saveable_transactions))			
		except IOError:
			print('Saving failed!')


	def proof_of_work(self):
		last_block = self.chain[-1]
		last_hash = hash_block(last_block)
		proof = 0		
		while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
			proof += 1

		return proof

	# return the actual balance
	def get_balance(self):
		# get the values that a participant sent
		tx_sender = [[tx.amount for tx in block.transactions if tx.sender == self.hosting_node] for block in self.chain]
		# get the values that a participant sent which is open
		open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == self.hosting_node]
		tx_sender.append(open_tx_sender)
		
		# get the total of the amount sent
		amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) 
															if len(tx_amount) > 0 
															else tx_sum + 0, tx_sender, 0)

		# get the total of the amount a participant receive
		tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == self.hosting_node] for block in self.chain]
		amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) 
															if len(tx_amount) > 0 
															else tx_sum + 0, tx_recipient, 0)	
		
		# return the balance
		return amount_received - amount_sent

	# retrieve the last value of the blockchain
	def get_last_blockchain_value(self):
		if len(self.chain) < 1:
			return None
		return self.chain[-1]


	# add transaction on the blockchain
	def add_transaction(self, recipient, sender, amount=1.0):
		transaction = Transaction(sender, recipient, amount)			
		if Verification.verify_transaction(transaction, self.get_balance):
			self.__open_transactions.append(transaction)
			self.save_data()
			return True

		return False

	# mine block and get rewarded
	def mine_block(self):	
		last_block = self.chain[-1]
		hashed_block = hash_block(last_block)
		proof = self.proof_of_work()
		reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
		
		copied_transactions = self.__open_transactions[:]
		copied_transactions.append(reward_transaction)
		block = Block(len(self.chain), hashed_block, copied_transactions, proof)	
		self.chain.append(block)
		self.__open_transactions = []
		self.save_data()
		return True