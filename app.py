from flask import Flask, request, abort, render_template
from data_structures import *
import json, pickle, datetime, requests, base64
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import rw

infile = open("parents.txt", 'r')
parents = [i for i in infile.read().split('\n') if i != '']
infile.close()

CURVE = SECP256k1
public_keys = {
    b'MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEeg7UEhlt0z4QmxLZlHtC4kmSkzO/QdDv\nF7Srn5qEPc9SxCrZD2XWD1hLeEB5Ds3l9r7eJjJPky6J1edM6Kqx5A==': 'mingy',
    b'MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEAqV1xDFS0MjbZxFtLSVMgMffgP1q+yM0\n3y68Ix2Q+UFK8dsEKbobK2j3lRVISmMMTsoergK38V6tZuvu1XwMEA==': 'alice'
}

wallets, ledger = rw.read()
print(wallets)
if (wallets == [] and ledger == []):
    wallets = { "mingy": 69, "alice": 2000, "bob":5 }
app = Flask(__name__)

@app.route("/transact", methods=["POST"])
def transact():
    data = request.json
    recipients = data['recipients']
    pubkey = data['pubkey']
    public = VerifyingKey.from_pem(pubkey)
    username = public_keys[public.to_pem()[27:-26]]
    transaction = Transaction(username, recipients)
    if not transaction.verify_ecdsa(public, base64.b64decode(data['signature'])):
        print("ecdsa fail")
        return abort(406)
    if transaction.verify(wallets):
        hehehe = transaction.process(wallets)
        ledger.append(transaction)
        for i in parents:
            requests.post(f"http://{i}/transact", json=data)
        # TEMPORARY: Make sure only 0 writes to file or something idk
        rw.write(wallets, ledger)
        return "Success"
    print("hello there. something went wrong. i am the parent")
    if len(ledger) > 10:
        error_ledger = {
            "head": ledger[-11].hash,
            "ledger": ledger[-10:]
        }
    elif len(ledger) == 0:
        print("length of ledger is 0 what now")
        return abort(406)
    else:
        error_ledger = {
            "head": ledger[0].hash,
            "ledger": ledger[1:]
        }

    # DEAD CODE: source is supposed to be manually added into the request??
    #if "source" in data.keys():
    #    error_ledger["ledger"] = list(map(lambda led: led.deserde(), error_ledger["ledger"]))
    #    requests.post("http://"+data["source"]+"/error", json=json.dumps(error_ledger))
    error_ledger["ledger"] = list(map(lambda led: led.deserde(), error_ledger["ledger"]))
    requests.post(f"http://{request.remote_addr}/error", json=json.dumps(error_ledger))
    return abort(406)

@app.route("/error", methods=['POST'])
def error():
    data = request.json
    thash = data['head']
    found = False
    for i in range(len(ledger)):
        if ledger[i].hash == thash:
            newlist = data['ledger']
            ledger = ledger[:i+1] + newlist
    if not found:
        abort(406) # Not Acceptable

# DEBUG
@app.route("/query", methods=["GET"])
def query():
    user = request.args.get('user')
    return f"balance: {wallets[user]}" if user in wallets.keys() else abort(406)