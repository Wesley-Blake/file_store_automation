"""Report how many files remain unprocessed under a directory tree."""

import datetime
from pathlib import Path


def remaining_files(input_path: Path):
    """Count files per subdirectory of ``input_path`` and append a report to remaining_files.txt."""
    # input_path = Path(input("Enter the path to the directory: "))
    if not input_path.is_dir():
        raise SystemExit("The provided path is not a directory.")
    total = 0
    with open("remaining_files.txt", "a+", encoding="utf-8") as f:
        file_count = 0
        f.write(f"Generated on: {datetime.datetime.now(tz=datetime.UTC)}\n")
        for root, _, files in input_path.walk():
            file_count += len(files)
            f.write(f"{file_count=:4d}: {root}\n")
            total += file_count
            file_count = 0
        f.write(f"Total files: {total}\n\n")
