from Transaction import Transaction
from fastecdsa import keys, curve
import hashlib
import requests
import pyrebase
import jsonpickle

config = {
    'apiKey': "AIzaSyBQd1bnNrEpuXbbPH_c15M6kYwv79jU6Ew",
    'authDomain': "e-votingastu.firebaseapp.com",
    'databaseURL': "https://e-votingastu.firebaseio.com",
    'projectId': "e-votingastu",
    'storageBucket': "e-votingastu.appspot.com",
    'messagingSenderId': "98525044697",
    'appId': "1:98525044697:web:90bd1ab962dcecad"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


class Wallet:
    def __init__(self):
        self.privateKey = keys.gen_private_key(curve.P256)
        self.publicKey = keys.get_public_key(self.privateKey, curve.P256)
        self.address = self.address_gen()
        self.vote = 1

    def create_user(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            data = {
                "private_key": self.privateKey
            }
            auth.get_account_info(user['idToken'])
            user_id = auth.get_account_info(user['idToken'])['users'][0]['localId']
            db.child('users').child(user_id).push(data, user['idToken'])
            return True
        except Exception as e:
            print(jsonpickle.loads(e.args[1])['error']['message'])
            return jsonpickle.loads(e.args[1])['error']['message']

    def sign_in_user(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            auth.get_account_info(user['idToken'])
            user_id = auth.get_account_info(user['idToken'])['users'][0]['localId']
            private_key = list(db.child('users').child(user_id).get(user['idToken']).val().values())[0]
            self.privateKey = private_key
            self.address = self.address_gen()
            self.publicKey = keys.get_public_key(self.privateKey, curve.P256)
            return True
        except Exception as e:
            print(jsonpickle.loads(e.args[1])['error']['message'])
            return jsonpickle.loads(e.args[1])['error']['message']

    @staticmethod
    def password_reset(email):
        auth.send_password_reset_email(email)

    @staticmethod
    def check_password_reset(rest_code, new_password):
        auth.verify_password_reset_code(rest_code, new_password)

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
