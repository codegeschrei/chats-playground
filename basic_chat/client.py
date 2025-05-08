import socket
import sys

from cli import client_cli


class Client:
    """
    Attributes
    ----------
    host : str
        The host to use to connect the server.
    port : int
        The port to use to connect the server.
    username : str
        A username for the client.
    """

    def __init__(self, host: str, port: int, username: str):
        # connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.username = username

    def run(self):
        """
        Wait for new messages and send them.

        """

        while True:
            print("Enter a new message:")
            message = input()
            if self.username:
                message = self.username + ": " + message
            self.client_socket.sendall(message.encode("utf-8"))


if __name__ == "__main__":
    host, port, username = client_cli()
    try:
        Client(host, port, username).run()
    except KeyboardInterrupt:
        # catch KeyboardInterrupt to shut down
        print("Shutting down")
        sys.exit(0)
