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
    while True:
        username = input("Please enter your username to log in (empty to create an account): ")
        if (username.strip() == ''):
            private = SigningKey.generate(curve=SECP256k1)
            public = private.verifying_key
            username = input("Enter username: ")
            response = requests.post(f"http://{random.choice(outer_nodes)}/create", json={"username": username})
            if (response.text == "Success"):
                try:
                    outfile = open(username, 'w')
                    outfile.write(private.to_pem().decode())
                    outfile.close()
                    outfile = open(username+".pub", 'w')
                    outfile.write(public.to_pem().decode())
                    outfile.close()
                    print(f"Account {username} created successfully!")
                except:
                    print("bruh what did you do???")
            else:
                print(f"ok what?? {response.text}")
        else:
            infile = open(username+".pub", 'r')
            pub = infile.read()
            infile.close()
            infile = open(username, 'r')
            priv = infile.read()
            infile.close()
            private = SigningKey.from_pem(priv)
            test_sign = b'among us'
            sign = private.sign(test_sign)
            public = VerifyingKey.from_pem(pub)
            if not public.verify(sign, test_sign):
                print(f"ERROR: {username} and {username}.pub are not a valid key pair.")
                return


        while(True):
            print("""
Welcome to T Pay!
1) Transfer someone money
2) Check someone's money
3) Exit
    """)

            option = input("> ")
            if option == "1":
                recipients = {}
                who = input("To who? (empty to finish) ").strip()
                if who == '':
                    print("that's literally nobody")
                    continue
                while who != '':
                    try:
                        amt = int(input("How much: "))
                        recipients[who] = amt
                    except:
                        print("not a number bruh")
                    who = input("To who? (empty to finish) ").strip()

                try:
                    node = random.choice(outer_nodes)
                    # print("Trying node " + node)
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
                        print("Transaction success!")
                        continue
                    else:
                        print(f"something stupid happened: {response.text}")
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    print("something happened, trying next node")

            elif option == "2":
                user = input("Who's account would you like to check: ")
                print(requests.get(f"http://{random.choice(outer_nodes)}/query", {"user":user.strip()}).text)
            elif option == "3":
                print("Thank you for using T Pay!")
                break
            else:
                print("u r stupid please enter an actually valid option please thank you!!!")


main()