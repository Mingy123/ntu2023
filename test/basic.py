import requests

outer_nodes = ["localhost:5000"]

for node in outer_nodes:
    try:
        print("Trying node " + node)
        # Do work
        data = {
            "sender": 12, # Sent from User ID 12
            "recipients": {25: 100} # User ID 25 gets 100 dollars
        }
        requests.post("http://"+node+"/transact", json=data)
        print("Sucess!")
        break
    except Exception as e:
        print(e)
        print("Trying next node")

