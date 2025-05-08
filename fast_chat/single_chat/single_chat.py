from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosed

from .settings import APP_NAME

# Set up app
app = FastAPI(title=APP_NAME)


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
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
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


@app.get("/")
async def get():
    # use the root as main url for the chat and return the html from above
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # create a websocket for the client
    await websocket.accept()
    try:
        while True:
            # handle incoming messages and send a message back to acknowledge it
            data = await websocket.receive_text()
            await websocket.send_text(f"Received message: {data}")
    except(WebSocketDisconnect, ConnectionClosed):
        # catch disconnect errors
        print("Shutting down")
