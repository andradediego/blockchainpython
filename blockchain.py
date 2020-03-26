MINING_REWARD = 10
GENESIS_BLOCK = {
		'previous_hash': '',
		'index': 0,
		'transactions': []
	}

blockchain = [GENESIS_BLOCK]
open_transactions = []
owner = 'Diego'
participants = {
	owner
}

waiting_for_input = True

# verify if the user have sufficient coins
def verify_transaction(transaction):
	sender_balance = get_balance(transaction['sender'])
	return sender_balance >= transaction['amount']


# retrieve the last value of the blockchain
def get_last_blockchain_value():
	if len(blockchain) < 1:
		return None
	return blockchain[-1]


# add transaction on the blockchain
def add_transaction(recipient, sender=owner, amount=1.0):
	transaction = {
		'sender': sender, 
		'recipient': recipient,
		'amount': amount
	}
	
	if verify_transaction(transaction):
		open_transactions.append(transaction)
		participants.add(recipient)
		participants.add(sender)
		return True

	return False

# mine block and get rewarded
def mine_block():	
	last_block = blockchain[-1]
	hashed_block = hash_block(last_block)
	reward_transaction = {
		'sender': 'MINING', 
		'recipient': owner,
		'amount': MINING_REWARD
	}
	copied_transactions = open_transactions[:]
	copied_transactions.append(reward_transaction)
	block = {
		'previous_hash': hashed_block,
		'index': len(blockchain),
		'transactions': copied_transactions
	}
	blockchain.append(block)
	return True

# get the amount of transaction from the user
def get_transaction_value():
	tx_recipient = input('Enter the recipient of the transaction: ')
	tx_amount = float(input('Your transaction amount please: '))
	return tx_recipient, tx_amount


def get_user_choice():
	user_input = input('Your choice: ')
	return user_input


def print_blockchain():
	# out the value on the console
	for block in blockchain:
		print('Outputting Block')
		print(block)
	else:
		print('-' * 20)

# create a block hash
def hash_block(block):
	return '-'.join([str(block[key]) for key in block])


# return the actual balance
def get_balance(participant):
	# get the values that a participant sent
	tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
	# get the values that a participant sent which is open
	open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
	tx_sender.append(open_tx_sender)
	
	# get the total of the amount sent
	amount_sent = 0
	for tx in tx_sender:
		if len(tx) > 0:
			amount_sent += tx[0]

	# get the total of the amount a participant receive
	tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
	amount_received = 0
	for tx in tx_recipient:
		if len(tx) > 0:
			amount_received += tx[0]
	
	# return the balance
	return amount_received - amount_sent


# verify if all the hashs are equal
def verify_chain():
	for (index, block) in enumerate(blockchain):
		if index == 0:
			continue
		elif block['previous_hash'] != hash_block(blockchain[index - 1]):
			return False
	
	return True


def verify_transactions():	
	return all([verify_transaction(tx) for tx in open_transactions])

# Options to interact
while waiting_for_input:
	print('Please choose')
	print('1: Add a new transaction value')
	print('2: Mine a new block')
	print('3: Output the blockchain blocks')
	print('4: Output participants')
	print('5: Check transaction validity')
	print('h: Manipulate the chain')
	print('q: Quit')
	
	user_choice = get_user_choice()

	if user_choice == '1':
		# get the transaction
		tx_data = get_transaction_value()
		recipient, amount = tx_data
		if add_transaction(recipient=recipient, amount=amount):
			print('Added transaction!')
		else:
			print('Transaction failed!')
	elif user_choice == '2':
		# print the blockchain
		if mine_block():
			open_transactions = []
	elif user_choice == '3':
		# print the blockchain
		print_blockchain()	
	elif user_choice == '4':
		print(participants)
	elif user_choice == '5':
		if verify_transactions():
			print('All transactions are valid')
		else:
			print('There are invalid transactions')
	elif user_choice == 'h':
		if len(blockchain) >= 1:
			blockchain[0] = {
					'previous_hash': '',
					'index': 0,
					'transactions': [{
						'sender': 'Max',
						'recipient': 'Diego',
						'amount': 100.0
					}]
				}
	elif user_choice == 'q':
		waiting_for_input = False
	else:
		print('Input is invalid, please pick a value from the list!')
	
	print('-' * 20)
	
	if not verify_chain():
		print('Invalid blockain!')
		waiting_for_input = False

	print(get_balance(owner))
else:
	print('User left!')

print('Done!')