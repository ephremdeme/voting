from Transaction import Transaction
from fastecdsa import keys, curve, ecdsa
import hashlib
import requests
import jsonpickle


class Wallet:
    def __init__(self):
        self.privateKey = keys.gen_private_key(curve.P256)
        self.publicKey = keys.get_public_key(self.privateKey, curve.P256)
        self.address = self.address_gen()
        self.vote = 1

    def address_gen(self):
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(str(self.publicKey).encode()).digest())
        return h.hexdigest()

    def create_transaction(self, receiver, amount):
        transaction = Transaction(self.address, receiver, amount)
        transaction.sign_tx(self.privateKey)
        transaction = jsonpickle.encode(transaction)
        r = requests.post('http://localhost:5000/transaction/broadcast', json=transaction)
        return r.status_code

# wallet =Wallet()
# wallet1 = Wallet()
# tx= wallet.create_transaction(wallet1.address, 12)
# tx1 = wallet1.create_transaction(wallet.address, 13)
# tx2 =wallet1.create_transaction(wallet.address, 44)
# # print(tx.is_valid())
# # print(tx.is_valid())
# print(wallet1.vote, wallet.vote)
