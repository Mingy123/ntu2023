import json, datetime, pickle, hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1
CURVE = SECP256k1

class Transaction:
    def __init__(self, sender, recipients, amount=0, timestamp=-1, hash=''):
        self.sender = sender
        self.amount = amount
        for value in recipients.values():
            self.amount += value
        self.recipients = recipients
        if (timestamp == -1):
            self.timestamp = datetime.datetime.now().timestamp()
        else:
            self.timestamp = timestamp
        if (hash == ''):
            m = hashlib.sha256()
            m.update(json.dumps({
                "sender": sender,
                "recipients": recipients,
                "timestamp": self.timestamp
            }).encode('utf-8'))
            self.hash = m.hexdigest()
        else:
            self.hash = hash


    def verify_ecdsa(self, public_key: VerifyingKey, signature):
        m = hashlib.sha256()
        m.update(json.dumps({
            "pubkey": public_key.to_pem()[27:-26].decode(),
            "recipients": self.recipients
        }).encode('utf-8'))
        client_hash = m.digest()
        return public_key.verify(signature, client_hash)

    def verify(self, wallets):
        # transact a negative amount
        for amt in self.recipients.values():
            if amt < 0: return False
        # sender/recipient does not exist
        if self.sender not in wallets:
            return False
        for recipient in self.recipients:
            if recipient not in wallets: return False
        # sender does not have enough money
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
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.hash
        })

def serde(string):
    data = json.loads(string)
    return Transaction(data['sender'], data['recipients'], data['amount'], data['timestamp'], data['hash'])