from flask import Flask, request
from data_structures import *
import json, pickle, datetime

wallets = { "mingy": 69 }
ledger = []
app = Flask(__name__)

@app.route("/transact", methods=["POST"])
def transact():
    data = request.json
    recipients = data['recipients']
    ledger.append(Transaction(data['sender'], data['recipients']))
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
            ledger = ledger[:i+1]
            #TODO
    if not found:
        abort(406) # Not Acceptable