blockchain = []
waiting_for_input = True

# retrieve the last value of the blockchain
def get_last_blockchain_value():
	if len(blockchain) < 1:
		return None
	return blockchain[-1]

# add transaction on the blockchain
def add_transaction(transaction_amount, last_transaction):
	if last_transaction == None:
		last_transaction = [1]
	blockchain.append([last_transaction, transaction_amount])

# get the amount of transaction from the user
def get_transaction_value():
	user_input = float(input('Your transaction amount please: '))
	return user_input


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

	
def verify_chain():
	block_index = 0
	is_valid = True

	for block in blockchain:
		if block_index == 0:
			block_index += 1
			continue
		elif block[0] != blockchain[block_index - 1]:
			is_valid = False		
			break
		block_index += 1
	return is_valid


while waiting_for_input:
	print('Please choose')
	print('1: Add a new transaction value')
	print('2: Output the blockchain blocks')
	print('h: Manipulate the chain')
	print('q: Quit')
	
	user_choice = get_user_choice()

	if user_choice == '1':
		# get the transaction
		tx_amount = get_transaction_value()
		add_transaction(last_transaction=get_last_blockchain_value(), transaction_amount=tx_amount)
	elif user_choice == '2':
		# print the blockchain
		print_blockchain()	
	elif user_choice == 'h':
		if len(blockchain) >= 1:
			blockchain[0] = [2]
	elif user_choice == 'q':
		waiting_for_input = False
	else:
		print('Input is invalid, please pick a value from the list!')
	
	print('Choice registered')
	
	if not verify_chain():
		print('Invalid blockain!')
		waiting_for_input = False
else:
	print('User left!')

print('Done!')