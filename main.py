import os
from pathlib import Path
import time
import configparser
import pyautogui as pag
from onbaser import *
from remaining_files import remaining_files


cfg = configparser.ConfigParser()
cfg.read('.env')
if cfg:
    primary_id_img = cfg['file_store']['p_id_img']
    event_date_img = cfg['file_store']['event_date_img']
    onbase_path = Path(cfg['file_store']['onbase_path'])
    input_path = Path(cfg['file_store']['drop_box_path'])
else:
    raise FileNotFoundError("Config file not found: .env")

if not onbase_path.is_dir() or not input_path.is_dir():
    raise FileNotFoundError(f"OnBase path not found: {onbase_path}")
if not os.path.isfile(primary_id_img) and not os.path.isfile(event_date_img):
    raise FileNotFoundError(f"Image file not found: {primary_id_img} or {event_date_img}")

starter(onbase_path)
for i in range(len(os.listdir(str(onbase_path)))):
    doc_type_name = copy_file_name()
    if doc_type_name.startswith("1."):
        pag.press('down')
        continue
    length = len(os.listdir(str(onbase_path / doc_type_name)))
    if length == 0:
        pag.press('down')
        if doc_type_name == "zkill":
            break
    else:
        pag.press('enter')
        import_doc_box(doc_type_name)
        for file in range(length):
            info = file_dragger(onbase_path, doc_type_name, input_path)
            if info is None:
                continue
            import_boxes(info)
            keyword_boxes(primary_id_img, event_date_img, info)
            complete()
        # return ..\\
        go_to_parent = (1084, 63)
        time.sleep(0.5)
        pag.moveTo(go_to_parent, duration=0.3)
        pag.click()
        pag.press('down')

remaining_files(input_path)
