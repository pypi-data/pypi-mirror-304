import time

from pyudp import MulticastServer

multicast_server = MulticastServer()

try:
    while True:
        time.sleep(1)

        t = time.time()
        message = {"time": t}
        print(f"Sending: {message}")

        multicast_server.send(message)

except KeyboardInterrupt:
    multicast_server.close()
    print("Server closed")
