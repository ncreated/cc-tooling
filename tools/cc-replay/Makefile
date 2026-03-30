.PHONY: install run clean

VENV := .venv
PYTHON := $(VENV)/bin/python

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

run: install
	$(PYTHON) -m ccreplay $(ARGS)

clean:
	rm -rf $(VENV)
