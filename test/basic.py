import requests

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
    name = input("who r u: ").strip()

    while(True):
        print("""
i love boys
1) give monie
2) check monie
3) NEW name!!!!!!
""")

        option = input("> ")
        if option == "1":
            receipient = input("2 who: ")
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
                    # Do work
                    data = {"sender":name, "recipients": {receipient.strip(): amount}}
                    response = requests.post(f"http://{node}/transact", json=data)
                    if response.text == "Success":
                        print("yipee!!!!")
                        break

                    else:
                        print(f"u r stupid,,, {response.text}")
                except Exception as e:
                    print(e)
                    print("Trying next node")

        elif option == "2":
            user = input("who: ")
            print(requests.get(f"http://{outer_nodes[0]}/query", {"user":user.strip()}).text)
        elif option == "3":
            name = input("who r u NOW: ").strip()
        else:
            print("u r stupid")


main()