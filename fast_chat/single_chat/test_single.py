from fastapi.testclient import TestClient

from .single_chat import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "WebSocket Chat" in response.content.decode("utf-8")


def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello WebSocket")
        data = websocket.receive_text()
        assert data == "Received message: Hello WebSocket"
