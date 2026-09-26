"""Report how many files remain unprocessed under a directory tree."""

import datetime
from pathlib import Path

from redact import redact


def _redacted_dir(input_path: Path, root: Path) -> str:
    """Show ``root`` as ``input_path.name`` plus a hash of each sub-directory."""
    parts = root.relative_to(input_path).parts
    return "/".join([input_path.name, *(redact(p) for p in parts)])


def remaining_files(input_path: Path):
    """Count files per subdirectory of ``input_path`` and append a report to remaining_files.txt."""
    if not input_path.is_dir():
        raise SystemExit("The provided path is not a directory.")
    total = 0
    with open("remaining_files.txt", "a", encoding="utf-8") as f:
        f.write(f"Generated on: {datetime.datetime.now(tz=datetime.UTC)}\n")
        for root, _, files in input_path.walk():
            file_count = len(files)
            f.write(f"{file_count=:4d}: {_redacted_dir(input_path, root)}\n")
            total += file_count
        f.write(f"Total files: {total}\n\n")
