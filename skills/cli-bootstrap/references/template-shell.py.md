# Shell Utility Template

Generate `lib/utils/shell.py` — a subprocess wrapper for running external commands.

```python
"""Shell command runner."""

import subprocess


class ShellError(Exception):
    """Shell command failed."""

    def __init__(self, command: list[str], returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        cmd_str = " ".join(command)
        super().__init__(f"command failed (exit {returncode}): {cmd_str}\n{stderr}")


def run(args: list[str], cwd: str | None = None, timeout: int = 30) -> str:
    """Run a shell command and return its stdout.

    Args:
        args: Command and arguments as a list (e.g. ["git", "status"]).
        cwd: Working directory. None uses the current directory.
        timeout: Timeout in seconds.

    Returns:
        Captured stdout as a string (stripped).

    Raises:
        ShellError: If the command exits with a non-zero code.
    """
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
    except subprocess.TimeoutExpired:
        raise ShellError(args, -1, f"timed out after {timeout}s")

    if result.returncode != 0:
        raise ShellError(args, result.returncode, result.stderr.strip())

    return result.stdout.strip()
```

## Usage examples (for CLAUDE.md reference)

```python
import json
from lib.utils.shell import run, ShellError

# Simple command
output = run(["git", "status"])

# With working directory and timeout
diff = run(["git", "diff", "HEAD~1"], cwd="/path/to/repo", timeout=60)

# Parse JSON output (composable — no mixed-responsibility run_json)
data = json.loads(run(["gh", "pr", "view", "123", "--json", "title,body"]))

# Error handling
try:
    run(["gh", "api", "repos/org/repo"])
except ShellError as e:
    print(f"Failed: {e}")
```
