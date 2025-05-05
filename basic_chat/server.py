import socket
import sys
import threading

from cli import main_cli


class Server:
    """
    Attributes
    ----------
    host : str
        The host to use to connect the server.
    port : int
        The port to use to connect the server.
    """

    def __init__(self, host, port):
        # keep track of all clients
        self.clients = []
        # server config - use IPv4 and TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # try to bind to host and port
        try:
            self.server_socket.bind((host, port))
        except socket.gaierror:
            print("Please provide a valid host.")
            sys.exit(1)
        except PermissionError:
            print("You do not have permission to use this port.")
            sys.exit(1)
        except OSError:
            print("The provided address is already in use.")
            sys.exit(1)
        except OverflowError:
            print("The port must be in range 0-65535.")
            sys.exit(1)
        except Exception as e:
            print(f"Could not connect to given host/port: {e}")
            sys.exit(1)

        self.server_socket.listen(5)
        print(f"Listening for new connections on {host}:{port}")


    def handle_client(self, client_socket: socket.socket):
        """
        Continuously receive data from clients
        Display incoming messages.
        We assume to have a disconnect when the received data is empty.
        With disconnect, remove client from list and close connection.

        Parameters
        ----------
        client_socket : socket.socket
            data sent from client, containing the message
        """
        while True:
            data = client_socket.recv(1024)
            if not data:
                # empty data == client disconnected
                break
            # read data
            message = data.decode('utf-8')
            # output message
            print(message)

        # close socket and remove client with disconnect
        client_socket.close()
        self.clients.remove(client_socket)


    def run(self):
        """
        Wait for incoming connections and add them to a client list.
        Make a new thread for each client and pass on the data to handle_client().
        """
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                # save new client to client list
                self.clients.append(client_socket)
                print(f"New established connection from {client_address}")
                # new thread for new client
                client_handler = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_handler.start()
        finally:
            # close the connection
            self.server_socket.close()


if __name__ == "__main__":
    host, port = main_cli()
    try:
        server = Server(host, port)
        server.run()
    except KeyboardInterrupt:
        # catch KeyboardInterrupt to shut down
        print("Shutting down")
        sys.exit(0)
