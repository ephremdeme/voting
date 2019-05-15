from fastecdsa import keys, curve, ecdsa

from hashlib import sha256
import hashlib
import json
from uuid import uuid4


class Transaction :
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.id = str(uuid4()).replace('-', '')
        self.signature = None
        
    def calculate_hash(self):
        return sha256((str(self.from_address)  + str(self.to_address)  + str(self.amount) +self.id).encode()).hexdigest()

    def sign_tx(self, priv_key):
        pub_key = keys.get_public_key(priv_key, curve.P256)
        if(not self.from_address == pub_key):
            raise Exception('public key not valid')
        hashTx = self.calculate_hash()
        self.signature = ecdsa.sign(hashTx, priv_key, hashfunc=sha256)
        print(hashTx)
        print('signature : ' ,self.signature )
    
    def is_valid(self):
        if(self.signature == None):
            return True
        if(len(self.signature) == 0):
            return False
        hashTx = self.calculate_hash()
        valid = ecdsa.verify(self.signature, hashTx, self.from_address, hashfunc=sha256)
        print(valid)
        return valid
    def serialize(self):
        return {
            'Tx_ID'        : self.id,
            'from_address' : sha256(str(self.from_address).encode()).hexdigest(),
            'to_address'   : sha256(str(self.to_address).encode()).hexdigest(),
            'amount'       : self.amount
        }

private_key = keys.gen_private_key(curve.P256)

public_key  = keys.get_public_key(private_key, curve.P256)
print(sha256( str(public_key).encode()).digest())
print('priva_key ', private_key)

h = hashlib.new('ripemd160')
h.update(sha256( str(public_key).encode()).digest())
print('ripemd' ,h.hexdigest())

Tx1 = Transaction(public_key, 'to add', 1223)
Tx1.sign_tx(private_key)
Tx1.is_valid()



# private_key = keys.gen_private_key(curve.P256)

# public_key  = keys.get_public_key(private_key, curve.P256)
# print('priva_key ', private_key)

# Tx2 = Transaction(public_key, 'to add', 12)
# Tx2.signTx(private_key)
# Tx2.verify()
# print()