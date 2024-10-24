import pickle
import socket


class UDP_Client:
    def __init__(self, server_ip: str = "localhost", port: int = 8080):
        self.server_address = (server_ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        """
        Send data to the server.

        Args:
            data (dict): The data to be sent, must be a dictionary.
        """

        message = pickle.dumps(data)
        self.sock.sendto(message, self.server_address)

    def close(self):
        self.sock.close()
