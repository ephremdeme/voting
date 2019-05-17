# /usr/bin/python

#    Name                ID
# 1) Amanuel Asfaw       R/0142/08
# 2) Bereket Asfaw       R/0242/08
# 3) Ephrem  Demelash    R/0427/08
# 4) Kidist  Alemayehu   R/0709/08
# 5) Girma   Moges       R/0550/08

from tkinter import StringVar, Label, Entry, Button, Tk, IntVar
from tkinter import ttk

from client.wallet import Wallet

root = Tk()
amount = IntVar()
address = StringVar()
ans = StringVar()
wallet = Wallet()


def stem():
    status = wallet.create_transaction(address.get(), amount.get())
    if status == 200:
        ans.set("successfully sent")
    else:
        ans.set("unsuccessfully sent")


mainframe = ttk.Frame(root)
label = Label(mainframe, text="insert a word")
label.pack()

amount_entry = Entry(mainframe, textvariable=amount)
amount_entry.insert(0, "amount")
amount_entry.pack()

address_entry = Entry(mainframe, textvariable=address)
address_entry.insert(0, "address")
address_entry.pack()

stemm_btn = Button(mainframe, text="send", command=stem)
stemm_btn.pack()

answer = Label(mainframe, textvariable=ans)
answer.pack()

mainframe.configure(width=400, height=200)
mainframe.pack()
root.mainloop()
