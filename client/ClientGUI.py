# /usr/bin/python

from tkinter import *
from tkinter import ttk

from wallet import Wallet

root = Tk()
amount = IntVar()
address = StringVar()
ans = StringVar()
wallet = Wallet()


# config = {
#     'apiKey': "AIzaSyBQd1bnNrEpuXbbPH_c15M6kYwv79jU6Ew",
#     'authDomain': "e-votingastu.firebaseapp.com",
#     'databaseURL': "https://e-votingastu.firebaseio.com",
#     'projectId': "e-votingastu",
#     'storageBucket': "e-votingastu.appspot.com",
#     'messagingSenderId': "98525044697",
#     'appId': "1:98525044697:web:90bd1ab962dcecad"
# }
#
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# db = firebase.database()
#
#
#
# try:
#     user = auth.sign_in_with_email_and_password('test1@gmail.com', 'password')
#     data = {
#         "name": "Mortimer 'Morty' Smith"
#     }
#     # print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
#     # print(list(db.child('users').get(user['idToken']).val().values())[0]['name'])
#     print(list(db.child('users').child('123456').get(user['idToken']).val().values())[0])
#     # db.child('users').child('123456').set(data, user['idToken'])
# except Exception as e:
#     print(e.args[1])
#     print(jsonpickle.loads(e.args[1])['error']['message'])


def sent():
    status = wallet.create_transaction(address.get(), amount.get())
    if status == 200:
        ans.set("successfully sent")
    else:
        ans.set("unsuccessfully sent")


mainframe = ttk.Frame(root)
label = Label(mainframe, text="Cast Your Vote")
label.pack()

amount_entry = Entry(mainframe, textvariable=amount)
amount_entry.insert(1, "")
amount_entry.pack()

address_entry = Entry(mainframe, textvariable=address)
address_entry.insert(0, "address")
address_entry.pack()

cand_select = IntVar()
cand_select.set(1)
list_candidate = [
    ("abebe", 1),
    ("ayele", 2),
    ("kebede", 3)
]


def ShowChoice():
    print(cand_select.get())


for cand, value in enumerate(list_candidate):
    Radiobutton(root,
                text=value[0],
                padx=20,
                variable=cand_select,
                command=ShowChoice,
                value=cand).pack(anchor=W)

sentm_btn = Button(mainframe, text="send", command=sent)
sentm_btn.pack()

answer = Label(mainframe, textvariable=ans)
answer.pack()

mainframe.configure(width=700, height=200)
mainframe.pack()
root.mainloop()
