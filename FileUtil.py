import json
import jsonpickle
import os

class FileUtil():
    def __init__(self, fname):
        self.name = fname
    
    def read(self):
        with open(self.name, 'r') as f :
            chain = f.read()
        print("block is read successfully")
        return jsonpickle.decode(chain)      
    
    def write(self, obj):
        with open(self.name, 'a+') as f:
            f.seek(0, 2)
            f.truncate()
            f.seek(f.tell()-1, os.SEEK_SET )
            f.truncate()
            f.write(',')
            f.write(jsonpickle.encode(obj))
            f.write(']')
        print("block is stored successfully")
    def storeGenesisBlock(self, obj):
        if(os.path.isfile(self.name)):
            return
        with open(self.name, 'w+') as f:
            f.write('[')
            f.write(jsonpickle.encode(obj))
            f.write(']') 
        print("genesis block is stored successfully")
    def replace(self, bestChain):
        with open(self.name, 'w') as f:
            f.write(jsonpickle.encode(bestChain))
