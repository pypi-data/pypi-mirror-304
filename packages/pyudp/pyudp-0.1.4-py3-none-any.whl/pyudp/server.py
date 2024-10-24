import pickle
import socket
from threading import Thread

from pyudp.utils import ReplacingQueue


class UDP_Server(Thread):
    def __init__(
        self,
        port: int = 8080,
        queue_maxsize: int = -1,
        buffer_size: int = 128,
        logger=None,
    ):
        Thread.__init__(self, daemon=True)

        self.buffer_size = buffer_size
        self.logger = logger
        self.queue = ReplacingQueue(queue_maxsize)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))

    def run(self):
        while True:
            try:
                data, cli_addr = self.sock.recvfrom(self.buffer_size)
                message = {"data": pickle.loads(data), "cli_addr": cli_addr}
                self.queue.put(message)

                if self.logger:
                    self.logger.debug(message)

            except socket.error:
                break

    def close(self):
        self.sock.close()
        self.join()
