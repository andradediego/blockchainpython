from uuid import uuid4
from blockchain import Blockchain
from verification import Verification

class Node:

	def __init__(self):
		# self.id = str(uuid4())
		self.id = 'Diego'
		self.blockchain = Blockchain(self.id)

	def get_user_choice(self):
		user_input = input('Your choice: ')
		return user_input

	def print_blockchain(self):
		# out the value on the console
		for block in self.blockchain.chain:
			print('Outputting Block')
			print(block)
		else:
			print('-' * 20)

	def listen_for_input(self):

		waiting_for_input = True

		# Options to interact
		while waiting_for_input:
			print('Please choose')
			print('1: Add a new transaction value')
			print('2: Mine a new block')
			print('3: Output the blockchain blocks')	
			print('4: Check transaction validity')
			print('q: Quit')

			user_choice = self.get_user_choice()			

			if user_choice == '1':
				# get the transaction
				tx_data = self.get_transaction_value()
				recipient, amount = tx_data
				if self.blockchain.add_transaction(recipient=recipient, sender=self.id, amount=amount):
					print('Added transaction!')
				else:
					print('Transaction failed!')
			elif user_choice == '2':
				# print the blockchain
				self.blockchain.mine_block()
					
			elif user_choice == '3':
				# print the blockchain
				self.print_blockchain()	
			elif user_choice == '4':
				
				if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
					print('All transactions are valid')
				else:
					print('There are invalid transactions')
			elif user_choice == 'q':
				waiting_for_input = False
			else:
				print('Input is invalid, please pick a value from the list!')
			
			print('-' * 20)
			
			if not Verification.verify_chain(self.blockchain.chain):
				print('Invalid blockain!')
				waiting_for_input = False

			print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))
		else:
			print('User left!')

		print('Done!')

	# get the amount of transaction from the user
	def get_transaction_value(self):
		tx_recipient = input('Enter the recipient of the transaction: ')
		tx_amount = float(input('Your transaction amount please: '))
		return tx_recipient, tx_amount


node = Node()
node.listen_for_input()