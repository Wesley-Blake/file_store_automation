"""Main loop to take files from file explorer to file storage software."""

from pathlib import Path
import configparser
import pyautogui as pag
from onbaser import FileExplorer
from onbaser import FileStore
from remaining_files import remaining_files

# TODO: logger
# Date&time: Doc name: filename

cfg = configparser.ConfigParser()
# NOTE: if this fails, the program should fail.
if not cfg.read(".env"):
    raise FileNotFoundError("Either the file is empty or doesn't exist.")
try:
    # File explorer object
    root = Path(cfg["file_store"]["root"])
    drop_box = Path(cfg["file_store"]["drop_box"])
    first_file_img = Path(cfg["file_store"]["first_file_img"])
    # File storage object
    import_button_img = cfg["file_store"]["import_button_img"]
    primary_id_img = Path(cfg["file_store"]["p_id_img"])
    event_date_img = Path(cfg["file_store"]["event_date_img"])
except Exception as e:
    raise KeyError("It looks like you are missing one or more keys.") from e

store_ob = FileStore(
    primary_id_img,
    event_date_img,
)
# NOTE: focus set on first file.
explor_ob = FileExplorer(
    root,
    drop_box,
    first_file_img,
)
# NOTE: I wish I had a do while.
current_dir = Path()
while current_dir.name != "zkill":
    # NOTE: focus on first file.
    current_dir = root / explor_ob.copy_item_name()
    if current_dir.name == drop_box.name:
        continue
    if not current_dir.is_dir():
        continue
    if next(current_dir.iterdir(), None):
        # NOTE: focus on first file.
        pag.press("enter")
        # TODO: do the import box
        store_ob.import_doc_box(current_dir.name)
        for _ in current_dir.iterdir():
            # TODO: add dragger
            if info := explor_ob.file_dragger(current_dir.name) is None:
                continue
            # TODO: file storage actions.
            import_boxes(info)
            keyword_boxes(info)
        # TODO: go to parrent
        go_to_parent = (1084, 63)
        pag.click(go_to_parent, duration=0.3)
    pag.press("down")

# TODO: update path
remaining_files(input_path)
