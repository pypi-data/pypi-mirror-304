import time

from pyudp import MulticastClient

multicast_client = MulticastClient()
multicast_client.start()

try:
    while True:
        time.sleep(0.1)

        while multicast_client.queue.qsize() > 0:
            data = multicast_client.queue.get()
            print(f"Received: {data}")

except KeyboardInterrupt:
    multicast_client.close()
    print("Client closed")
