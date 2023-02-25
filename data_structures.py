import json, datetime, pickle, hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1
CURVE = SECP256k1

class Transaction:
    def __init__(self, sender, recipients):
        print(sender)
        self.sender = sender
        self.amount = 0
        for value in recipients.values():
            self.amount += value
        self.recipients = recipients
        self.timestamp = datetime.datetime.now().timestamp()
        m = hashlib.sha256()
        m.update(json.dumps({
            "sender": sender,
            "recipients": recipients,
            "timestamp": self.timestamp
        }).encode('utf-8'))
        self.hash = m.hexdigest()

    def verify_ecdsa(self, public_key: VerifyingKey, signature):
        m = hashlib.sha256()
        m.update(json.dumps({
            "pubkey": public_key.to_pem()[27:-26].decode(),
            "recipients": self.recipients
        }).encode('utf-8'))
        client_hash = m.digest()
        return public_key.verify(signature, b'mingy')

    def verify(self, wallets):
        # Return False if you try to transact a negative amount
        for amt in self.recipients.values():
            if amt < 0: return False
        # Return False if sender/recipient does not exist
        print(wallets)
        print(self.sender not in wallets)
        if self.sender not in wallets:
            print("not instance\n", self.sender, wallets)
            return False
        print(self.recipients)
        for recipient in self.recipients:
            print(recipient)
            print(recipient in wallets)
            if recipient not in wallets: return False
        print(self.amount)
        print(wallets[self.sender])
        # Return False if sender does not have enough money
        if wallets[self.sender] < self.amount: return False
        return True

    def process(self, wallets):
        
        wallets[self.sender] -= self.amount
        for recipient, credit in self.recipients.items():
            wallets[recipient] += credit

        return wallets
    
    def deserde(self):
        return json.dumps({
            "sender": self.sender,
            "recipients": self.recipients,
        })

def serde(string):
    data = json.loads(string)
    return Transaction(data['sender'], data['recipients'])
