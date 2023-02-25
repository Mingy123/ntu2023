from flask import Flask, request, abort, render_template
from data_structures import *
import json, pickle, datetime, requests, base64
from ecdsa import SigningKey, VerifyingKey, SECP256k1

CURVE = SECP256k1
public_keys = {
    b'MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEeg7UEhlt0z4QmxLZlHtC4kmSkzO/QdDv\nF7Srn5qEPc9SxCrZD2XWD1hLeEB5Ds3l9r7eJjJPky6J1edM6Kqx5A==': 'mingy'
}
wallets = { "mingy": 69, "alice": 2000, "bob":5 }
ledger = []
app = Flask(__name__)

@app.route("/transact", methods=["POST"])
def transact():
    data = request.json
    recipients = data['recipients']
    pubkey = data['pubkey']
    public = VerifyingKey.from_pem(pubkey)
    print(public, type(public))
    username = public_keys[public.to_pem()[27:-26]]
    transaction = Transaction(username, recipients)
    if not transaction.verify_ecdsa(public, base64.b64decode(data['signature'])):
        print("ecdsa fail")
        return abort(406)
    if transaction.verify(wallets):
        print(json.dumps(wallets))
        hehehe = transaction.process(wallets)
        print(json.dumps(hehehe))
        ledger.append(transaction)
    else:
        if len(ledger) > 10:
            error_ledger = {
                "head": ledger[-11].hash,
                "ledger": ledger[-10:]
            }
        elif len(ledger) == 0:
            # bruh
            return abort(406)
        else:
            error_ledger = {
                "head": ledger[0].hash,
                "ledger": ledger[1:]
            }
        if "source" in data:
            error_ledger["ledger"] = list(map(lambda led: led.deserde(), error_ledger["ledger"]))
            print(error_ledger)
            requests.post("http://"+data["source"]+"/error", json=json.dumps(error_ledger))
        return abort(406)
    return "Success"

@app.route("/error", methods=['POST'])
def error():
    data = request.json
    thash = data['head']
    found = False
    for i in range(len(ledger)):
        if ledger[i].hash == thash:
            newlist = data['ledger']
            print("\ngetting an error:\n", newlist, '\n\n')
            ledger = ledger[:i+1] + newlist
            print("New Ledger:\n"+ledger)
    if not found:
        abort(406) # Not Acceptable

# DEBUG
@app.route("/query", methods=["GET"])
def query():
    user = request.args.get('user')
    return f"balance: {wallets[user]}" if user in wallets.keys() else abort(406)

if __name__ == "__main__":
    app.run(port=5001)