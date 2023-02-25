import requests, hashlib, json, base64, traceback
from ecdsa import SigningKey, VerifyingKey, SECP256k1

outer_nodes = ["127.0.0.1:5000"]

# for node in outer_nodes:
#     try:
#         print("Trying node " + node)
#         # Do work
#         data = {"sender":"alice", "recipients": {"bob": 100}, "source": "127.0.0.1:5002"}
#         requests.post(f"http://{node}/transact", json=data)
#         print("NOT Sucess!")
#         break
#     except Exception as e:
#         print(e)
#         print("Trying next node")

def main():
    pub = open("ecdsa.pub", 'r').read()
    priv = open("ecdsa", "r").read()
    private = SigningKey.from_pem(priv)
    sign = private.sign(b'among us')
    public = VerifyingKey.from_pem(pub)
    if not public.verify(sign, b'among us'):
        print("ERROR: ecdsa and ecdsa.pub are not a valid key pair.")
        return


    while(True):
        print("""
i love boys
1) give monie
2) check monie
3) NEW name!!!!!!
""")

        option = input("> ")
        if option == "1":
            recipient = input("2 who: ")
            while True:
                amount = input("hao muhc: ")
                try:
                    amount = int(amount)
                except Exception as e:
                    print("that isnt a numbnr,,,,")
                else:
                    break

            for node in outer_nodes:
                try:
                    print("Trying node " + node)
                    m = hashlib.sha256()
                    m.update(json.dumps({
                        "pubkey": public.to_pem()[27:-26].decode(),
                        "recipients": {recipient: amount}
                    }).encode('utf-8'))
                    client_hash = m.digest()
                    sign = base64.b64encode(private.sign(b'mingy'))
                    data = {
                        "pubkey": pub,
                        "signature": sign,
                        "recipients": {
                            recipient.strip(): amount
                        }
                    }
                    response = requests.post(f"http://{node}/transact", json=data)
                    if response.text == "Success":
                        print("yipee!!!!")
                        break

                    else:
                        print(f"u r stupid,,, {response.text}")
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    print("Trying next node")

        elif option == "2":
            user = input("who: ")
            print(requests.get(f"http://{outer_nodes[0]}/query", {"user":user.strip()}).text)
        elif option == "3":
            pub = input("who r u NOW: ").strip()
        else:
            print("u r stupid")


main()