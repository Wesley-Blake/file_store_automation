from pathlib import Path
from datetime import datetime


def remaining_files(input_path: Path):
    dir_counter = {}
    counter = 0
    #input_path = Path(input("Enter the path to the directory: "))
    if not input_path.is_dir():
        print("The provided path is not a directory.")
        exit(1)
    for root, dirs, files in input_path.walk():
        dir_counter[root] = len(files)
        counter += len(files)

    with open("remaining_files.txt", "a+") as f:
        f.write(f"Generated on: {datetime.now()}\n")
        for dir_path, file_count in dir_counter.items():
            if file_count > 0:
                f.write(f"{file_count=:04d}: {dir_path}\n")
        f.write(f"Total files: {counter}\n\n")
