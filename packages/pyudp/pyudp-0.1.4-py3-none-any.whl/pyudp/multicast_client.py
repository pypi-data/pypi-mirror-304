import pickle
import socket
import struct
from threading import Thread

from pyudp.utils import ReplacingQueue


class MulticastClient(Thread):
    def __init__(
        self,
        multicast_group: str = "224.0.0.1",
        port: int = 5005,
        queue_maxsize: int = -1,
        buffer_size: int = 128,
        logger=None,
    ):
        Thread.__init__(self, daemon=True)

        self.buffer_size = buffer_size
        self.logger = logger
        self.queue = ReplacingQueue(maxsize=queue_maxsize)

        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind(("", port))

        mreq = struct.pack(
            "4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY
        )
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def run(self):
        while True:
            try:
                data, ser_addr = self.sock.recvfrom(self.buffer_size)
                message = {"data": pickle.loads(data), "ser_addr": ser_addr}
                self.queue.put(message)

                if self.logger:
                    self.logger.debug(message)

            except socket.error:
                break

    def close(self):
        self.sock.close()
        self.join()
