import os
from pathlib import Path
import time
import pyautogui as pag
from onbaser import *
from remaining_files import remaining_files



with open("file_store_automation\\secrets.txt", "r") as f:
    primary_id_img = f.readline().strip()
    event_date_img = f.readline().strip()
    onbase_path = Path(f.readline().strip())
    input_path = Path(f.readline().strip())
    if not onbase_path.is_dir() or not input_path.is_dir():
        raise FileNotFoundError(f"OnBase path not found: {onbase_path}")

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
