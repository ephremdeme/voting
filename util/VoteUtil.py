from . import DBUtil
from api.BlockchainAPINode import votedb
from blockchain.Transaction import Transaction
from fastecdsa import keys, curve
import hashlib
import json
import requests
import jsonpickle


class VoteUtil:
    def __init__(self):
        self.private_key = keys.gen_private_key(curve.P256)
        self.publicKey = keys.get_public_key(self.private_key, curve.P256)
        self.address = self.address_gen()
        self.vote = 1

    def cast_vote(self, vote_hash, voter_pin, cand_address):
        if not votedb.verify_voter(vote_hash, voter_pin):
            return json.dumps({
                "msg": "Already Voted"
            })
        vote = Transaction(self.address, cand_address, self.vote)
        vote.sign_tx(self.private_key)
        transaction = jsonpickle.encode(vote)
        r = requests.post(
            'http://localhost:5000/transaction/broadcast', json=transaction)
        if not r.status_code == 200:
            return json.dumps({
                "msg": "There was an Error!, Please Try Agian"
            })
        votedb.delete_voter(vote_hash, voter_pin)
        return True

    def address_gen(self):
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(str(self.publicKey).encode()).digest())
        return h.hexdigest()
