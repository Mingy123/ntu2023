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
