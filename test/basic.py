import requests

outer_nodes = ["127.0.0.1:5000"]

for node in outer_nodes:
    try:
        print("Trying node " + node)
        # Do work
        data = {"sender":"alice", "recipients": {"bob": 100}, "source": "127.0.0.1:5002"}
        requests.post("http://"+node+"/transact", json=data)
        print("Sucess!")
        break
    except Exception as e:
        print(e)
        print("Trying next node")

