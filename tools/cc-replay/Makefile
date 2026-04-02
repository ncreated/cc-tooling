.PHONY: install run watch clean

VENV := .venv
PYTHON := $(VENV)/bin/python

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

run: install
	$(PYTHON) -m ccreplay $(ARGS)

watch: install
	$(PYTHON) -m ccwatch $(ARGS)

clean:
	rm -rf $(VENV)
