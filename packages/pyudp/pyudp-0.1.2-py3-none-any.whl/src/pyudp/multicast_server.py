import pickle
import socket


class MulticastServer:
    def __init__(self, multicast_group: str = "224.0.0.1", port: int = 5005):
        self.server_address = (multicast_group, port)

        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def send(self, data):
        message = pickle.dumps(data)
        self.sock.sendto(message, self.server_address)

    def close(self):
        self.sock.close()
