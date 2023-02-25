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

    def verify(self):
        #check that all recipients and valid
        #check that the user has that much money
        #if that does not check out, tell the previous sender
        #if that checks out, forward the request to the people in parents.txt

        return False

Transaction("mingy", ["someone": 10])
