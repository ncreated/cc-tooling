# Makefile Template

Generate a `Makefile` with these targets. Use **tabs** for indentation (required by Make).

## Base Makefile (always included)

```makefile
VENV := venv

help:
	@$(VENV)/bin/python main.py --help

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

run:
	@$(VENV)/bin/python main.py $(ARGS)

clean:
	@rm -rf __pycache__ .pytest_cache
```

## Optional: test target

Add only if the user opted for tests during interview:

```makefile
test:
	@$(VENV)/bin/python -m pytest tests/ -v
```

## Notes

- `help` must be the **first target** so it runs on bare `make`
- `run` passes arguments via `ARGS`, e.g. `make run ARGS="fetch --force"`
- `clean` targets can be extended based on the tool's output directories (e.g. `workspace/`, `output/`)
