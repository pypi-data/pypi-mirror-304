import time

from pyudp import UDP_Client

client = UDP_Client()

try:
    while True:
        time.sleep(0.5)

        t = time.time()
        message = {"time": t}
        print(f"Sending: {message}")

        client.send(message)

except KeyboardInterrupt:
    client.close()
    print("Client closed")
