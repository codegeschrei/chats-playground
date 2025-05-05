.PHONY: help basicChatServer basicChatClient fastSingleChat fastMultiChat fletChat test ruff ruff-fix build-docs docs clean clean-all

default: help

help:
	@echo "Usage: make [target] ...\n"
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

basicChatServer: ## run the server of the basic Chat
	uv run basic_chat/server.py

basicChatClient: ## run the client of the basic Chat
	uv run basic_chat/client.py

fastSingleChat: ## run the the fastAPI Chat for a single user
	uv run fastapi dev fast_chat/single_chat/single_chat.py

fastMultiChat: ## run the the fastAPI Chat for a multiple user
	uv run fastapi dev fast_chat/multi_chat/multi_chat.py

fletChat: ## run the flet chat
	uv run flet run --web flet_chat/chat.py

test: ## run tests
	uv run pytest

ruff: ## run ruff
	uv run ruff check

ruff-fix: ## run ruff and fix issues
	uv run ruff check --fix

build-docs: ## build the docs
	uv run mkdocs build

docs: ## run the docs
	uv run mkdocs serve

clean: ## clean up cached files
	find . | grep -E "(__pycache__)" | xargs rm -rf
	find . | grep -E "(.pytest_cache)" | xargs rm -rf

clean-all: ## clean up all additional files
	find . | grep -E "(__pycache__)" | xargs rm -rf
	find . | grep -E "(.pytest_cache)" | xargs rm -rf
	find . | grep -E "(storage)" | xargs rm -rf
	rm -rf .venv
	rm -rf .ruff_cache