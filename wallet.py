from Transaction import Transaction
from fastecdsa import keys, curve, ecdsa
import hashlib
class Wallet():
    def __init__(self):
        self.privateKey = keys.gen_private_key(curve.P256)
        self.publicKey = keys.get_public_key(self.privateKey, curve.P256)
        self.address = self.address_gen()
        self.vote = 1
    
    def address_gen(self):
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256( str(self.publicKey).encode()).digest())
        return h.hexdigest()
    
    def createTransaction(self, receiver, amount ):
        transaction =Transaction(self.address, receiver, amount)
        self.vote +=amount
        transaction.sign_tx(self.privateKey)
        return transaction
    
    def calculateVote(self, chain):
        vote = 0
        for block in chain:
            for tx in block.transaction:
                if(tx.to_address=='00f23132c7bc626122a6878bbb0b916e5a2bbc26'):
                    vote+=1
        return vote


# wallet =Wallet()
# wallet1 = Wallet()
# tx= wallet.createTransaction(wallet1.address, 12)
# tx1 = wallet1.createTransaction(wallet.address, 13)
# tx2 =wallet1.createTransaction(wallet.address, 44)
# print(tx.is_valid())
# print(tx.is_valid())
# print(wallet1.vote, wallet.vote)