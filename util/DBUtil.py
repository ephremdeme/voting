import jsonpickle
import plyvel
import hashlib
from fastecdsa import keys, curve


class DBUtil:

    def __init__(self, db_name):
        self._db = plyvel.DB(db_name, create_if_missing=True, comparator=self.comparator,
                             comparator_name=b'CaseInsensitiveComparator')
        self._blockdb = self._db.prefixed_db(b'block')
        self._votedb = self._db.prefixed_db(b'vote')
        self._hashdb = self._db.prefixed_db(b'hash')
        self._count = self.block_count()

    def store_sec_address(self, array, section):
        section = str(section).encode()
        secdb = self._db.prefixed_db(section)
        with secdb.write_batch(transaction=True) as write:
            for key, value in array:
                key = str(key).encode()
                value = str(value).encode()
                write.put(key, value)

    def verify_voter(self, section, key, value):
        section = str(section).encode()
        secdb = self._db.prefixed_db(section)
        with secdb.iterator() as it:
            for k, v in it:
                if k.decode() == key and v.decode() == value:
                    return True
        return False

    def get_sec_address(self, section):
        section = str(section).encode()
        secdb = self._db.prefixed_db(section)
        value = []
        with secdb.iterator() as it:
            for kv in it:
                value.append(kv)
        return value

    def store_sec_candidate(self, array, section):
        section = (str(section) + "cand").encode()
        secdb = self._db.prefixed_db(section)
        try:
            with secdb.write_batch(transaction=True) as write:
                for i in range(0, len(array)):
                    write.put(self.address_gen().encode(), array[i].encode())
            return True
        except:
            print("not completed successfully")
            return False

    def get_sec_candidate(self, section):
        section = (str(section) + "cand").encode()
        secdb = self._db.prefixed_db(section)
        value = []
        with secdb.iterator() as it:
            for k, v in it:
                value.append((k.decode(), v.decode()))
        return value

    def store_block(self, index, value):
        key = str(index).encode()
        block_hash = value.hash.encode()
        if self.block_exist(key):
            return False
        value = jsonpickle.encode(value).encode()
        self._blockdb.put(key, value)
        self._count += 1
        self.store_block_hash(block_hash, key)
        return True

    def store_block_hash(self, block_hash, index):
        index = str(index).encode()
        self._hashdb.put(block_hash.encode(), index)
        return True

    def block_count(self):
        count = 0
        with self._blockdb.iterator(include_value=True) as it:
            for key in it:
                count += 1
        return count

    def count(self):
        return self._count

    def store_block_hash_all(self):
        with self._blockdb.iterator() as it:
            for key, value in it:
                block = jsonpickle.decode(value.decode())
                block_hash = block.hash
                self.store_block_hash(block_hash, key.decode())

    def store_genesis_block(self, value):
        self.store_block(1, value)

    def getblock(self, index):
        index = str(index).encode()
        with self._blockdb.snapshot() as sn:
            return jsonpickle.decode(sn.get(index).decode())

    def get_last_block(self):
        with self._blockdb.iterator(reverse=True, include_key=False) as it:
            for value in it:
                return jsonpickle.decode(value.decode())

    def get_block_index(self, block_hash):
        return self._hashdb.get(str(block_hash).encode())

    def get_block_by_hash(self, block_hash):
        index = self.get_block_index(block_hash)
        return self.getblock(index.decode())

    def replace_chain(self, chain):
        with self._blockdb.write_batch(transaction=True) as write:
            for block in chain:
                index = str(block.index).encode()
                block = jsonpickle.encode(block).encode()
                write.put(index, block)
        c = self.count()
        if len(chain) < c:
            for i in range(len(chain), c + 1):
                self._blockdb.delete(str(i).encode())

        self.store_block_hash_all()

    def get_all_block(self):
        chain = []
        with self._blockdb.iterator(include_key=False) as it:
            for value in it:
                chain.append(jsonpickle.decode(value.decode()))
        return chain

    def get_block_range(self, start, end):
        start = str(start).encode()
        end = str(end).encode()
        chain = []
        with self._blockdb.iterator(start=start, stop=end, include_key=False) as it:
            for value in it:
                chain.append(jsonpickle.decode(value.decode()))
        return chain

    def block_exist(self, key):
        if self._blockdb.get(key, default=0) != 0:
            return True
        return False

    def store_network_node(self, nodes):
        self._db.put(b'nodes', jsonpickle.encode(nodes).encode())

    def get_network_node(self):
        node = self._db.get(b'nodes', 0)
        if node == 0:
            return []
        return jsonpickle.decode(node)

    @staticmethod
    def sec_hash(year, school, dept, sec):
        from hashlib import sha256
        sec = str(sec) + str(year) + str(school) + str(dept)
        sec_hash = sha256(sec.encode()).hexdigest()
        return sec_hash

    @staticmethod
    def address_gen():
        priv = keys.gen_private_key(curve=curve.P256)
        pub_key = keys.get_public_key(priv, curve=curve.P256)
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(str(pub_key).encode()).digest())
        return h.hexdigest()

    @staticmethod
    def comparator(key1, key2):
        key1 = key1.decode()
        key2 = key2.decode()
        key1 = key1.lower()
        key2 = key2.lower()
        if (key1.isalnum() and key2.isalnum()) and (key1.startswith("block") and key2.startswith("block")):
            key1 = int(key1.strip("block") if key1.strip("block") is not '' else 0)
            key2 = int(key2.strip("block") if key2.strip("block") is not '' else 0)
            if key1 < key2:
                return -1
            elif key1 > key2:
                return 1
            else:
                return 0
        else:
            if key1 < key2:
                # a sorts before b
                return -1

            if key1 > key2:
                # a sorts after b
                return 1

            # a and b are equal
            return 0
