from flask import Flask, request, abort
from data_structures import *
import json, pickle, datetime, requests

wallets = { "mingy": 69, "alice": 200, "bob":5 }
ledger = []
app = Flask(__name__)

@app.route("/transact", methods=["POST"])
def transact():
    data = request.json
    recipients = data['recipients']
    transaction = Transaction(data['sender'], data['recipients'])
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
            return "bruh"
        else:
            error_ledger = {
                "head": ledger[0].hash,
                "ledger": ledger[1:]
            }
        if "source" in data:
            error_ledger["ledger"] = list(map(lambda led: led.deserde(), error_ledger["ledger"]))
            print(str(error_ledger))
            requests.post("http://"+data["source"]+"/error", json=json.dumps(error_ledger))
        abort(406)
    return "Success"

@app.route("/error", methods=['POST'])
def error():
    data = request.json
    hash = data['head']
    found = False
    for i in range(len(ledger)):
        if ledger[i].hash == hash:
            newlist = data['ledger']
            print("\ngetting an error:\n", newlist, '\n\n')
            ledger = ledger[:i+1] + newlist
            print("New Ledger:\n"+ledger)
    if not found:
        abort(406) # Not Acceptable

# DEBUG
@app.route("/query")
def query():
    return json.dumps(wallets)