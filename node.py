from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

#local files
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

CORS(app)


def convert_block_json(block_chain_snapshot):
	dict_chain = [block.__dict__.copy() for block in block_chain_snapshot]
	for dict_block in dict_chain:
		dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
	
	return dict_chain

@app.route('/', methods=['GET'])
def get_ui():
	return send_from_directory('ui', 'index.html')

@app.route('/mine', methods=['POST'])
def mine_block():
	# response = {
	# 	'message': 'Saving the keys Failed'
	# }
	# return jsonify(response), 200
	block = blockchain.mine_block()	
	# block = 2
	if block != None:
		dict_block = block.__dict__.copy()		
		dict_block['transactions'] = [
    	tx.__dict__ for tx in dict_block['transactions']]
		response = {
			'message': 'Block added successfully.',
			'block': dict_block,
			'funds': blockchain.get_balance()
		}
		return jsonify(response), 201
	else:
		response = {
			'message': 'Adding a block failed.',
			'wallet_set_up': wallet.public_key != None
		}
		return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
	dict_chain = convert_block_json(blockchain.chain)	
	return jsonify(dict_chain), 200

@app.route('/wallet', methods=['POST'])
def create_key():
	wallet.create_keys()
	if wallet.save_keys():
		global blockchain
		blockchain = Blockchain(wallet.public_key)
		response = {
			'public_key': wallet.public_key,
			'private_key': wallet.private_key,
			'funds': blockchain.get_balance()
		}
		return jsonify(response), 201
	else:
		response = {
			'message': 'Saving the keys Failed'
		}
		return jsonify(response), 500

@app.route('/wallet', methods=['GET'])
def load_keys():
	if wallet.load_keys():		
		global blockchain
		blockchain = Blockchain(wallet.public_key)
		response = {
			'public_key': wallet.public_key,
			'private_key': wallet.private_key,
			'funds': blockchain.get_balance()
		}
		return jsonify(response), 201
	else:
		response = {
			'message': 'Loading the keys Failed'
		}
		return jsonify(response), 500

@app.route('/balance', methods=['GET'])
def get_balance():
	balance = blockchain.get_balance()
	if balance != None:
		response = {
			'message': 'Fetch balance successfully',
			'wallet_set_up': balance
		}
		return jsonify(response), 201
	else:
		response = {
			'message': 'Loading the balance Failed',
			'wallet_set_up': wallet.public_key != None
		}
		return jsonify(response), 500


@app.route('/transaction', methods=['POST'])
def add_transactions():
	if wallet.public_key == None:
		response = {
			'message': 'No wallet setup'			
		}
		return jsonify(response), 400

	values = request.get_json()	
	if not values:
		response = {
			'message': 'No data found'			
		}
		return jsonify(response), 400
	
	required_fields = ['recipient', 'amount']

	if not all(field in values for field in required_fields):
		response = {
			'message': 'Required data is missing'
		}
		return jsonify(response), 400

	recipient = values['recipient']
	amount = values['amount']
	signature = wallet.sign_transactions(wallet.public_key, recipient, amount)	
	success = blockchain.add_transaction(recipient=recipient, sender=wallet.public_key, signature=signature, amount=amount)
	if success:
		response = {
			'message': 'Succesfully added transaction',
			'transaction': {
				'sender': wallet.public_key,
				'recipient': recipient,
				'amount': amount,
				'signature': signature
			},
			'funds': blockchain.get_balance()
		}
		return jsonify(response), 201
	else:
		response = {
			'message': 'Create a transaction Failed'
		}
		return jsonify(response), 500

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
	transactions = blockchain.get_open_transactions()
	dict_transactions = [tx.__dict__ for tx in transactions]
	
	return jsonify(dict_transactions), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)