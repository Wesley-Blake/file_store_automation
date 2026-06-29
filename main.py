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
if not cfg.read('.env'):
    raise FileNotFoundError("Either the file is empty or doesn't exist.")
try:
    # File explorer object
    file_explorer_path = Path(cfg['file_store']['file_explorer_path'])
    drop_box_path = Path(cfg['file_store']['drop_box_path'])
    first_file_img = Path(cfg['file_store']['first_file_img'])
    # File storage object
    #import_button_img = cfg['file_store']['import_button_img']
    primary_id_img = Path(cfg['file_store']['p_id_img'])
    event_date_img = Path(cfg['file_store']['event_date_img'])
except KeyError as exc:
    raise KeyError("It looks like you are missing one or more keys.") from exc

# Change for to while loop
# TODO: instantiate both objects.
# TODO: both starters
# We aren't going to use a variable from a for loop.
while True:
    # TODO: Check if first copy is dropbox: continue
    # TODO: get doc_type_name
    current_dir = onbase_path / copy_file_name()
    if next(current_dir.iterdir(), None):
        pag.press('enter')
        # TODO: do the import box
        import_doc_box(current_dir.name)
        for _ in current_dir.iterdir():
            # TODO: add dragger
            if info := file_dragger(current_dir.name) is None:
                continue
            # TODO: file storage actions.
            import_boxes(info)
            keyword_boxes(info)
        # TODO: go to parrent
        go_to_parent = (1084, 63)
        pag.click(go_to_parent, duration=0.3)
    pag.press('down')
    if current_dir.name == "zkill":
        break

# TODO: update path
remaining_files(input_path)
