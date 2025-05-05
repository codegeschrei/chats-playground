- [Overview](#overview)
- [Set up](#set-up)
- [basic\_chat](#basic_chat)
- [fast\_chat](#fast_chat)
  - [single\_chat](#single_chat)
  - [multi\_chat](#multi_chat)
- [flet\_chat](#flet_chat)
- [Additional tools used](#additional-tools-used)
  - [Testing](#testing)
  - [Ruff](#ruff)
  - [Makefile](#makefile)
  - [Docs](#docs)


# Overview
This is a collection of various approaches of simple chat applications.

# Set up

You need [uv](https://docs.astral.sh/uv/) to set up the environment

```bash
# using curl
curl -LsSf https://astral.sh/uv/install.sh | sh
# using wget
wget -qO- https://astral.sh/uv/install.sh | sh
# using brew
brew install uv
# using pip
pip install uv
```

After installing you can, but don't have to, activate a virtual environment.  
To activate the local environment run the following in the terminal (linux/mac):  
`uv venv && source .venv/bin/activate`


# basic_chat
This example is for a simple chat usable in the terminal.  
The chat itself is one-sided, i.e. no messages are broadcast, the client is communicating with the server only.  

To run it use the following commands, each in a new tab.  

Start the server
`uv run basic_chat/server.py` or `make basicChatServer`  
Optionally the host and port can be set  
`uv run basic_chat/server.py --host 127.0.0.1 --port 12345`  

Run the server  
`uv run basic_chat/client.py` or `make basicChatClient`  
Optionally a host, port and username can be set  
`uv run basic_chat/client.py --host 127.0.0.1 --port 12345 --name username`  

The scripts can be terminated with a keyboard interrupt.  

A broadcasting version will be added later.  

# fast_chat
Here are two examples for very simple chat apps built with [fastAPI](https://fastapi.tiangolo.com/)  

One is for a single user chat and the other for multiple users, where messages are broadcast.  

## single_chat
With the single chat a user can send messages to the system,   
which are then prompted back as a confirmation.  

The chat can be run with  
`uv run fastapi dev fast_chat/single_chat/single_chat.py` or `make fastSingleChat`  
Note that we run fastAPI in development mode.  
Then navigate to the following [URL](http://127.0.0.1:8000) to access the chat.  
This URL is displayed in the terminal under 'server' as well.  


## multi_chat
With the multi chat, users can connect to the chat and message each other.  
The chat provides additional messages to let the users know who joined or left the chat.  

The chat can be run with  
`uv run fastapi dev fast_chat/multi_chat/multi_chat.py` or `make fastMultiChat`    
Note that we run fastAPI in development mode.  

Then navigate to the following [URL](http://127.0.0.1:8000) to access the chat.  
This URL is displayed in the terminal under 'server' as well.  
For multiple users open a new tab/window/browser and navigate to the same url.  


# flet_chat

A small chat app built with [flet](https://flet.dev/)  
_flet_ is a framework based on flutter which provides a way to easily built apps without frontend knowledge.  

The app can be run with:  
`uv run flet run --web flet_chat/chat.py`  or `make fletChat`  

A browser window with the chat will open. If more users are wanted, use the same URL in a new tab/window/browser.  

Side Note: I pinned the _websockets_ library down to 13.1 to remove some `DeprecationWarning`, it didn't remove all but since this is just for playing around it's fine.  

# Additional tools used

## Testing

Tests can be run by simply calling  
`uv run pytest` or `make test`  

## Ruff

For linting and code formatting [Ruff](https://docs.astral.sh/ruff/) was used.  

It can be run using the following commands:  
`uv run ruff check` or `make ruff`  
or to fix   
`uv run ruff check --fix` or `make ruff-fix`  

## Makefile

The `Makefile` can be used to run all scripts.  
Currently any optional command line arguments need to be added manually.  

## Docs
To have some basic documentation [mkdocs](https://www.mkdocs.org/) was used.  
The documentation can be run with `make docs`  