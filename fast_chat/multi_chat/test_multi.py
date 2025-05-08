from fastapi.testclient import TestClient

from .manager import ConnectionManager
from .multi_chat import app

client = TestClient(app)
manager = ConnectionManager()


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "WebSocket Chat" in response.content.decode("utf-8")


def test_websocket():
    with client.websocket_connect("/ws/123") as websocket:
        data = websocket.receive_text()
        assert data == "#123 joined the Chat."

        websocket.send_text("Hello WebSocket")
        data = websocket.receive_text()
        assert data == "Client #123 says: Hello WebSocket"
