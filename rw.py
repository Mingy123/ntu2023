import json 

filename = "idonthaveagoodfilename.txt"

def write(wallets, ledger):
    f = open(filename, 'w')
    f.write(json.dumps(wallets))
    f.write('\n')
    f.write(json.dumps([transcation.deserde() for transcation in ledger]))
    f.close()

def read():
    # f = open(filename, 'r')
    # lines = f.readlines()
    # print(lines)
    # f.close()
    # wallets = json.loads(lines[0])
    # ledger = json.loads(lines[1])
    # return wallets, ledger
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        wallets = json.loads(lines[0])
        ledger = json.loads(lines[1])
        return wallets, ledger
    except:
        return [], []


        