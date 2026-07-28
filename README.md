# File Store Automation

GUI automation that walks a folder tree in Windows File Explorer and imports each
file into a file storage application, using [PyAutoGUI](https://pyautogui.readthedocs.io/)
image recognition to drive both applications.

## How it works

For each document-type directory under a configured root folder, the script:

1. Opens the directory in File Explorer and opens the "import" dialog in the file
   storage application, setting the document type field from the directory name.
2. For every file in the directory, drags the file into the file storage
   application (or moves it to a drop box if its name doesn't match the expected
   `<id>-<iso-date>...` pattern), fills in the primary ID and date fields parsed
   from the file name, and submits the import.
3. Appends a line to `log.log` for every file imported.
4. Moves to the next directory, stopping once it reaches a directory named `zkill`.

Because it relies on image recognition (`pag.locateOnScreen`) and simulated
mouse/keyboard input, both applications must be visible on screen, at the expected
screen positions/resolution, and not obstructed while the script runs.

## Project layout

```
src/
  __main__.py        Entry point / main loop (run as `python -m src`)
  onbaser.py          FileExplorer and FileStore automation classes
  remaining_files.py  Utility to report files left unprocessed in a directory tree
.env                   Config file (see below)
log.log                Append-only log of imported files
```

## Configuration

Settings are read from an `.env` file (INI format, parsed with `configparser`) in
the project root:

```ini
[file_store]
root = <path to the top-level directory to walk in File Explorer>
drop_box = <path files are moved to when their name doesn't match the expected pattern>
file_drag = <reference image used to locate the drag handle for the first file>
import_start_img = <reference image for the button that opens the import dialog>
import_check_img = <reference image confirming the import dialog opened>
primary_id_img = <reference image for the primary ID field label>
cancel_box_img = <reference image for the cancel/close control>
doc_type_img = <reference image for the document type field>
date_box_img = <reference image for the date field>
```

Reference images are screenshots of UI elements used by PyAutoGUI to locate
fields/buttons on screen; they must be captured at the resolution/scale the
script will run at.

## Requirements

- Windows, with File Explorer and the target file storage application installed.
- Python 3 with:
  - [`pyautogui`](https://pypi.org/project/PyAutoGUI/)
  - [`pyperclip`](https://pypi.org/project/pyperclip/)

## Usage

1. Fill in `.env` with the paths and reference images described above.
2. Arrange the File Explorer window and file storage application on screen as
   expected by the reference images.
3. Run the automation from the project root:

   ```
   python -m src
   ```

Avoid moving the mouse or keyboard focus while the script is running, since it
relies on simulated input and on-screen image matching.

## Notes

- `remaining_files.py` provides a standalone helper, `remaining_files(input_path)`,
  that walks a directory tree and appends a per-directory file count summary to
  `remaining_files.txt`. It isn't currently wired into the main loop.
