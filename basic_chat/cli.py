import argparse

from settings import HOST, PORT


def main_cli() -> tuple[str, int]:
    """
    Define and check for arguments to set host and port

    Returns
    ----------
    tuple[str, int]
        A tuple of host and port.
    """
    parser = argparse.ArgumentParser(prog="Chat Server", description="Run a chat server")

    parser.add_argument("--host", type=str, help="specify a host to use")
    parser.add_argument("--port", type=int, help="specify a port to use")
    parsed_args = parser.parse_args()

    host = parsed_args.host if parsed_args.host else HOST
    port = parsed_args.port if parsed_args.port else PORT

    return host, port


def client_cli() -> tuple[str, int, str]:
    """
    Define and check for host, port username argument

    Returns
    ----------
    tuple[str, int, str]
        A tuple of host, port and username.
    """
    parser = argparse.ArgumentParser(prog="Chat Client", description="Run a chat client")

    parser.add_argument("--host", type=str, help="specify a host to use")
    parser.add_argument("--port", type=int, help="specify a port to use")
    parser.add_argument("--name", type=str, help="specify your username")
    parsed_args = parser.parse_args()

    host = parsed_args.host if parsed_args.host else HOST
    port = parsed_args.port if parsed_args.port else PORT
    username = parsed_args.name if parsed_args.name else None

    return host, port, username
