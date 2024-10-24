import time

from pyudp import UDP_Server

server = UDP_Server()
server.start()

try:
    while True:
        time.sleep(1)

        while server.queue.qsize() > 0:
            data = server.queue.get()
            print(f"Received: {data}")

except KeyboardInterrupt:
    server.close()
    print("Server closed")
