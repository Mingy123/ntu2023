import json, datetime

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

    def verify(self, wallets):
        # Return False if sender/recipient does not exist
        if self.sender not in wallets: return False
        for recipient in self.recipients:
            if recipient not in wallets: return False

        # Return False if sender does not have enough money
        if wallets[self.sender] < self.amount: return False
        return True
    
    def deserde(self):
        return json.dumps({
            "sender": self.sender,
            "recipients": self.recipients,
        })

def serde(string):
    data = json.loads(string)
    return Transaction(data['sender'], data['recipients'])
