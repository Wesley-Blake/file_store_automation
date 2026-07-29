"""Main loop to take files from file explorer to file storage software."""

import configparser
from pathlib import Path

import pyautogui as pag
from onbaser import FileExplorer, FileStore, start
from remaining_files import remaining_files

cfg = configparser.ConfigParser()
# NOTE: if this fails, the program should fail.
if not cfg.read(".env"):
    raise FileNotFoundError("Either the file is empty or doesn't exist.")
start(
    cfg["file_store"]["import_start_img"],
    cfg["file_store"]["import_check_img"],
    cfg["file_store"]["root"],
)
store_o = FileStore(
    cfg["file_store"]["primary_id_img"],
    cfg["file_store"]["cancel_box_img"],
    cfg["file_store"]["doc_type_img"],
    cfg["file_store"]["date_box_img"],
)
explor_o = FileExplorer(
    cfg["file_store"]["root"],
    cfg["file_store"]["drop_box"],
    cfg["file_store"]["file_drag"],
)


def main():
    root = Path(explor_o.root)
    current_dir = root
    while current_dir.name != "zkill":
        current_dir = root / explor_o.copy_item_name()
        if current_dir.name == explor_o.drop_box_path.name:
            pag.press("down")
            continue
        if next(current_dir.iterdir(), None) is not None:
            pag.press("enter")
            store_o.import_doc_box(current_dir.name)
            for item in current_dir.iterdir():
                explor_o.focus_explorer_file()
                store_o.info = explor_o.file_dragger(current_dir.name)
                if store_o.info is None:
                    continue
                store_o.keyword_boxes()
                store_o.complete()
                with open("log.log", "a+", encoding="utf-8") as log_file:
                    log_file.write(f"{current_dir.name}: {item}\n")
            explor_o.focus_explorer_file()
            pag.hotkey("alt", "up")
        pag.press("down")
    remaining_files(explor_o.drop_box_path)


if __name__ == "__main__":
    main()
