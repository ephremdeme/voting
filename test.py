import hashlib
import re
import jsonpickle
import plyvel
from fastecdsa import keys, curve, ecdsa

from util.DBUtil import DBUtil
from util import ExcelUtil

db = DBUtil('db/5000')
# print(db.count())
# for i in range(1, 30):
#     db.blockdb.delete(str(i).encode())
# db.put('key'.encode(), 'value'.encode())

# data = {
#     "name": 1,
#     "g": "p"
# }
# data = jsonpickle.encode(data)
# db.saveblock("test", data)
# data = jsonpickle.decode(db.getblock('test').decode())
# count = 0


data = ["http://localhost:5001",
        "http://localhost:5002",
        "http://localhost:5003",
        "http://localhost:5004",
        "http://localhost:5005"]


def address_gen(pubKey):
    h = hashlib.new('ripemd160')
    h.update(hashlib.sha256(str(pubKey).encode()).digest())
    return h.hexdigest()


array = []
#
# for i in range(1000):
#     privkey, pubKey = keys.gen_keypair(curve.P256)
#     array.append((ExcelUtil.generate_pin_password(), str(privkey)))
# ExcelUtil.write_to_excel(array)
# array =  ExcelUtil.read_excel("gen.xlsx")
# ExcelUtil.write_to_excel(array)
#
#
# db.store_sec_address(array, "sec2")
# array = db.get_sec_address("sec2")
# for key, value in array:
#     print(key.decode())
#     print(value.decode())

array = [1, 2]
print(len(array))

print(db.get_block_index('0000bb5afec47b4c0c2191c300affd80051b6f3f586b2da2776555eb7aa7dafd').decode())

print(db.get_block_by_hash('0000bb5afec47b4c0c2191c300affd80051b6f3f586b2da2776555eb7aa7dafd'))

print(db.get_sec_address('fdcfaededb35a87dc82034837cc5ce2bbd483647b0674ea399a3e4a4158f16ab'))
print(db.get_sec_candidate("989625f28dd8fb28f86a1c755a246479a2feb1e426d8e03d0a48640ab7297033"))



