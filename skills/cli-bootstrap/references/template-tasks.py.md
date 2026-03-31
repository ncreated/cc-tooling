# Tasks Utility Template

Generate `lib/utils/tasks.py` — a ThreadPoolExecutor wrapper for parallel work with progress tracking.

```python
"""Parallel task runner with progress tracking."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from lib.utils.logger import Logger


def run_parallel(items, fn, max_workers=1, label="task", logger=None):
    """Run fn(item) for each item in parallel with progress tracking.

    Args:
        items: Iterable of items to process.
        fn: Callable that takes one item and returns a result.
        max_workers: Number of parallel workers (1 = sequential).
        label: Label for progress messages (e.g. "review", "fetch").
        logger: Logger instance. If None, creates a default one.

    Returns:
        List of results (one per item, in completion order).

    Raises:
        Exception: Re-raises the first exception from a failed task.
    """
    if logger is None:
        logger = Logger()

    items = list(items)
    total = len(items)
    logger.info(f"[{label}] 🚀 {total} tasks, workers: {max_workers}")

    results = []
    errors = []
    done_count = {"n": 0}

    def _tracked(item):
        result = fn(item)
        done_count["n"] += 1
        logger.info(f"[{label}] {done_count['n']}/{total} done")
        return result

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_tracked, item): item for item in items}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                errors.append(e)

    if errors:
        logger.error(f"[{label}] {len(errors)} task(s) failed")
        raise errors[0]

    logger.info(f"[{label}] 🏁 all {total} tasks done")
    return results
```

## Usage example

```python
from lib.utils.tasks import run_parallel
from lib.utils.logger import Logger

def process_file(path):
    # ... do work ...
    return {"path": path, "status": "ok"}

logger = Logger(verbose=args.verbose)
results = run_parallel(
    items=file_paths,
    fn=process_file,
    max_workers=args.jobs,
    label="process",
    logger=logger,
)
```

## Dependency

This utility imports `Logger` from `lib.utils.logger`. If the user selected tasks but not logger, **include the logger utility as well** — tasks depends on it.
