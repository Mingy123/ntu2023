from flask import Flask, request
import json, pickle, datetime

Transaction("mingy", ["someone": 10])
class Transaction:
    def __init__(self, sender, recipients):
        self.sender = sender
        self.amount = 0
        for value in recipients.values():
            self.amount += value
        self.recipients = recipients
        self.timestamp = datetime.datetime.now()
        m = hashlib.sha256()
        m.update(pickle.dumps(self))
        self.hash = m.hexdigest()

wallets = { "mingy": 69 }
ledger = []
app = Flask(__name__)

@app.route("/transact", methods=["POST"])
def transact():
    data = request.json
    recipients = data['recipients']
    ledger.append(Transaction(data['sender'], data['recipients']))
    return "Success"
