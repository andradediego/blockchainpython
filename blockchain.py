blockchain = []

# retrieve the last value of the blockchain
def get_last_blockchain_value():
	return blockchain[-1]

# add value on the blockchain
def add_value(transaction_amount, last_transaction=[1]):
	blockchain.append([last_transaction, transaction_amount])

# get the amount of transaction from the user
def get_user_input():
	return float(input('Your transaction amount please: '))

#get the first transaction
tx_amount = get_user_input()
add_value(tx_amount)

# get the second transaction
# keyword arguments, switching the positions
tx_amount = get_user_input()
add_value(last_transaction=get_last_blockchain_value(), transaction_amount=tx_amount)

#get the third transaction
tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

# out the value on the console
print(blockchain)