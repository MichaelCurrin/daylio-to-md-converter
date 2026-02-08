SHELL = /bin/bash

APP_DIR = daylio2md

OUT_DIR = output
INPUT_PATH = sample/input.csv

all: install app-help demo

h help:
	@grep '^[a-z]' Makefile


install:
	poetry install --no-root

update:
	poetry update

g install-global:
	pipx install . --force


app-help:
	poetry run python -m $(APP_DIR) -h

demo:
	poetry run python -m $(APP_DIR) $(INPUT_PATH) $(OUT_DIR)
