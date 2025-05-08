from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from .manager import ConnectionManager
from .settings import APP_NAME

# Simple html template for the chat
# In production build a frontend with a framework like React or others
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


# Set up app and manager
app = FastAPI(title=APP_NAME)
manager = ConnectionManager()


@app.get("/")
async def get() -> HTMLResponse:
    # use the root as main url for the chat and return the html from above
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int) -> None:
    # create a websocket for each client
    await manager.connect(websocket)
    await manager.broadcast(f"#{client_id} joined the Chat.")

    try:
        while True:
            # handle incoming messages and broadcast them
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        # disconnect the socket when a connection is closed
        manager.disconnect(websocket)
        await manager.broadcast(f"#{client_id} left the chat")
