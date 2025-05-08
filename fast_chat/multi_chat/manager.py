from fastapi import WebSocket


class ConnectionManager:
    """
    Handle all connection events of clients

    """

    def __init__(self) -> None:
        # keep track of all active connections
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        expects a websocket to establish a connection

        Parameters
        ----------
        websocket : WebSocket
            The websocket to connect to.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Expects a websocket to disconnect a client by removing them
        from the client list

        Parameters
        ----------
        websocket : WebSocket
            The Websocket to remove.
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        """
        Broadcast incoming messages to all clients

        Parameters
        ----------
        message : str
            The client message to broadcast.
        """
        for connection in self.active_connections:
            await connection.send_text(message)
