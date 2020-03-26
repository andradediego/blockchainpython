import hashlib as hl
import json

def has_string_256(string):
	return hl.sha256(string).hexdigest()

# create a block hash
def hash_block(block):
	return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()