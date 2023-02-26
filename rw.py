import json 
from data_structures import serde

filename = "wallet.txt"

def write(wallets, ledger):
    with open(filename, 'w') as f:
        f.write(json.dumps(wallets))
        f.write('\n')
        f.write(json.dumps([transcation.deserde() for transcation in ledger]))

def read():
    # f = open(filename, 'r')
    # lines = f.readlines()
    # print(lines)
    # f.close()
    # wallets = json.loads(lines[0])
    # ledger = json.loads(lines[1])
    # return wallets, ledger
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        wallets = json.loads(lines[0])
        ledger = json.loads(lines[1])
        return wallets, [serde(i) for i in ledger]
    except Exception as e:
        print(e)
        return [], []


        