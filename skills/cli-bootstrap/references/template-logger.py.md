# Logger Utility Template

Generate `lib/utils/logger.py` — a thread-safe logger with severity levels that integrates with `-v/--verbose`.

```python
"""Thread-safe logger with severity levels."""

import threading


class Logger:
    """Thread-safe logger with severity-based filtering.

    Usage:
        logger = Logger(verbose=args.verbose)
        logger.info("Processing started")
        logger.debug("Detailed info only shown with -v")
        logger.warn("Something looks off")
        logger.error("Something failed")
    """

    _LEVELS = {
        "debug": ("🔍", 0),
        "info": ("✅", 1),
        "warn": ("⚠️", 2),
        "error": ("❌", 3),
    }

    def __init__(self, verbose: bool = False):
        self._lock = threading.Lock()
        self._min_level = 0 if verbose else 1

    def _log(self, level: str, msg: str) -> None:
        emoji, priority = self._LEVELS[level]
        if priority < self._min_level:
            return
        with self._lock:
            print(f"{emoji} {msg}")

    def debug(self, msg: str) -> None:
        """Log debug message (only shown when verbose=True)."""
        self._log("debug", msg)

    def info(self, msg: str) -> None:
        """Log info message."""
        self._log("info", msg)

    def warn(self, msg: str) -> None:
        """Log warning message."""
        self._log("warn", msg)

    def error(self, msg: str) -> None:
        """Log error message."""
        self._log("error", msg)
```

## Integration with CLI

In `main.py`, create the logger from the parsed `--verbose` flag and pass it to command functions:

```python
from lib.utils.logger import Logger

def cmd_fetch(args) -> int:
    logger = Logger(verbose=getattr(args, "verbose", False))
    logger.info("Starting fetch...")
    # ...
```
