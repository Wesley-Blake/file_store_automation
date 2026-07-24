"""Main loop to take files from file explorer to file storage software."""

import configparser
from pathlib import Path

import pyautogui as pag

from onbaser import FileExplorer, FileStore

# TODO: logger
# Date&time: Doc name: filename

cfg = configparser.ConfigParser()
# NOTE: if this fails, the program should fail.
if not cfg.read(".env"):
    raise FileNotFoundError("Either the file is empty or doesn't exist.")
# NOTE: FileStore should go first because self._start() needs to locate the import button before interacting with the file explorer.
store_ob = FileStore(
    cfg["file_store"]["import_start_img"],
    cfg["file_store"]["import_check_img"],
    cfg["file_store"]["primary_id_img"],
    cfg["file_store"]["cancel_box_img"],
    cfg["file_store"]["doc_type_img"],
    cfg["file_store"]["date_box_img"],
)
explor_ob = FileExplorer(
    cfg["file_store"]["root"],
    cfg["file_store"]["drop_box"],
    cfg["file_store"]["file_drag"],
)
# NOTE: I wish I had a do while.
root = Path(explor_ob._root)
current_dir = root
while current_dir.name != "zkill":
    current_dir = root / explor_ob._copy_item_name()
    if current_dir.name == explor_ob._drop_box_path.name:
        pag.press("down")
        continue
    if next(current_dir.iterdir(), None) is not None:
        # Do something with the directory contents.
        pag.press("enter")
        store_ob.import_doc_box(current_dir.name)
        for item in current_dir.iterdir():
            explor_ob.focus_explorer_file()
            store_ob.info = explor_ob.file_dragger(current_dir.name)
            if store_ob.info is None:
                continue
            with open("log.log", "a+") as log_file:
                log_file.write(f"{current_dir.name}: {store_ob.info}\n")
            store_ob.keyword_boxes()
            store_ob.complete()
        explor_ob.focus_explorer_file()
        pag.hotkey("alt", "up")
    pag.press("down")
