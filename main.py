import os
from pathlib import Path
import time
import pyautogui as pag
import pyperclip
from onbaser import *
from ramaing_files import ramaing_files



with open("file_store_automation\\secrets.txt", "r") as f:
    primary_id_img = f.readline().strip()
    event_date_img = f.readline().strip()
    onbase_path = Path(f.readline().strip())
    if not onbase_path.exists():
        raise FileNotFoundError(f"OnBase path not found: {onbase_path}")

os.chdir(str(onbase_path))

starter(str(onbase_path))
for i in range(len(os.listdir())):
    doc_type_name = copy_file_name()
    if doc_type_name.startswith("1."):
        pag.press('down')
        continue
    length = len(os.listdir(str(onbase_path / doc_type_name)))
    if length == 0:
        pag.press('down')
        continue
    else:
        pag.press('enter')
        import_doc_box(doc_type_name)
        for file in range(length):
            info = file_dragger()
            import_boxes(info)
            keyword_boxes(primary_id_img, event_date_img, info)
            complete()
        # return ..\\
        go_to_parent = (1084, 63)
        time.sleep(0.5)
        pag.moveTo(go_to_parent, duration=0.3)
        pag.click()
        pag.press('down')

raming_files()
