import requests, hashlib, json, base64, traceback, random
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
    filename = input("Where key? ")
    infile = open(filename+".pub", 'r')
    pub = infile.read()
    infile.close()
    infile = open(filename, 'r')
    priv = infile.read()
    infile.close()
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
4) exit
""")

        option = input("> ")
        if option == "1":
            recipients = {}
            who = input("to who? (empty to finish) ").strip()
            if who == '':
                print("thats nobody")
                continue
            while who != '':
                try:
                    amt = int(input("how much: "))
                    recipients[who] = amt
                except:
                    print("not a number")
                who = input("to who? (empty to finish) ").strip()

            try:
                node = random.choice(outer_nodes)
                print("Trying node " + node)
                m = hashlib.sha256()
                m.update(json.dumps({
                    "pubkey": public.to_pem()[27:-26].decode(),
                    "recipients": recipients
                }).encode('utf-8'))
                client_hash = m.digest()
                sign = base64.b64encode(private.sign(client_hash)).decode()
                data = {
                    "pubkey": pub,
                    "signature": sign,
                    "recipients": recipients
                }
                response = requests.post(f"http://{node}/transact", json=data)
                if response.text == "Success":
                    print("yipee!!!!")
                    continue
                else:
                    print(f"u r stupid,,, {response.text}")
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                print("Trying next node")

        elif option == "2":
            user = input("who: ")
            print(requests.get(f"http://{random.choice(outer_nodes)}/query", {"user":user.strip()}).text)
        elif option == "3":
            private = SigningKey.generate(curve=SECP256k1)
            public = private.verifying_key
            filename = input("Enter file to write public key to: ")
            outfile = open(filename, 'w')
            outfile.write(private.to_pem().decode())
            outfile.close()
            outfile = open(filename+".pub", 'w')
            outfile.write(public.to_pem().decode())
            outfile.close()
        elif option == "4":
            break
        else:
            print("u r stupid")


main()