from fastecdsa import keys, curve, ecdsa
from hashlib import sha256
from uuid import uuid4


class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.id = str(uuid4()).replace('-', '')
        self.signature = None

    def calculate_hash(self):
        return sha256((str(self.from_address) + str(self.to_address) + str(self.amount) + self.id).encode()).hexdigest()

    def sign_tx(self, priv_key):
        hash_tx = self.calculate_hash()
        self.signature = ecdsa.sign(hash_tx, priv_key, hashfunc=sha256)

    def is_valid(self):
        if self.signature is None:
            return True
        if len(self.signature) == 0 and self.to_address is None:
            return False
        hash_tx = self.calculate_hash()
        pubkey = keys.get_public_keys_from_sig(self.signature, hash_tx, curve=curve.P256, hashfunc=sha256)
        valid = ecdsa.verify(self.signature, hash_tx, pubkey[0], hashfunc=sha256)
        return valid

    def serialize(self):
        return {
            'id': self.id,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount
        }

# private_key = keys.gen_private_key(curve.P256)

# public_key  = keys.get_public_key(private_key, curve.P256)
# print(sha256( str(public_key).encode()).digest())
# print('priva_key ', private_key)

# h = hashlib.new('ripemd160')
# h.update(sha256( str(public_key).encode()).digest())
# print('ripemd' ,h.hexdigest())

# Tx1 = Transaction(public_key, 'to add', 1223)
# Tx1.sign_tx(private_key)
# Tx1.is_valid()
