import json 
from data_structures import serde

filename = "wallet.txt"

def write(wallets, ledger):
    f = open(filename, 'w')
    f.write(json.dumps(wallets))
    f.write('\n')
    f.write(json.dumps([transcation.deserde() for transcation in ledger]))
    f.close()

def read():
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        wallets = json.loads(lines[0])
        ledger = json.loads(lines[1])
        return wallets, [serde(i) for i in ledger]
    except Exception as e:
        print(e)
        return [], []


        