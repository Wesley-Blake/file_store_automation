import time
import shutil
from pathlib import Path
from datetime import datetime
import pyperclip
import pyautogui as pag


def starter(base_dir_path: Path) -> None:
    """File explorer function, starter"""
    first_dir = (1253, 208)
    # start new search bar
    # focus file explorer
    # press ctrl + l
    explor_search_bar = (1677, 63)
    pag.moveTo(explor_search_bar, duration=0.1)
    pag.click()
    # end start new search bar
    pag.write(str(base_dir_path), interval=0.03)
    pag.press('enter')
    # remove
    pag.press('esc')
    # end remove
    # focus dir list
    # press home key
    pag.moveTo(first_dir, duration=0.1)
    pag.leftClick()
    # end focus dir list


def cancel_box() -> None:
    time.sleep(1)
    cancel_button = (175, 80)
    pag.moveTo(cancel_button, duration=0.1)
    pag.click()
    time.sleep(1)


def copy_file_name() -> str:
    pag.press('f2')
    time.sleep(0.5)
    pag.hotkey('ctrl','a')
    pag.hotkey('ctrl','c')
    result = pyperclip.paste()
    pag.press('esc')
    return result


def import_doc_box(document_type_name: str) -> None:
    # ocr
    document_type = (227, 232)
    cancel_box()
    # end ocr
    pag.moveTo(document_type, duration=0.1)
    pag.click()
    pag.write(document_type_name, interval=0.05)
    pag.press('enter')
    time.sleep(1)


def file_dragger(
    onbase_path: Path,
    doc_type_name: str,
    input_path: Path
    ) -> list | None:
    # ocr
    first_file = (1192, 175)
    # calc center
    file_drop = (610, 525)
    # calc center
    # end ocr
    pag.moveTo(first_file, duration=0.1)
    pag.leftClick()
    file_name = copy_file_name()
    # make file dates only a number example 20260526
    # make split only '-'
    result = file_name.split(' - ')
    if len(result) < 2:
        return _mover(onbase_path, doc_type_name, input_path, file_name)
    if not result[0].isdigit():
        return _mover(onbase_path, doc_type_name, input_path, file_name)
    try:
        datetime.fromisoformat(result[1])
    except ValueError:
        return _mover(onbase_path, doc_type_name, input_path, file_name)
    # end make file dates
    pag.dragTo(file_drop, duration=0.2)
    # ocr?
    time.sleep(3)
    # end ocr?
    return result


def _mover(
    onbase_path: Path,
    doc_type_name: str,
    input_path: Path,
    file_name: str
    ) -> None:
    src = onbase_path / doc_type_name / file_name
    dst = input_path / file_name
    if not src.exists():
        raise FileExistsError(
            f"Source Doesn't Exist: {src}"
        )
    elif dst.exists():
        shutil.move(
            src,
            input_path / (file_name[:file_name.rfind('.')] + datetime.now().strftime("-%Y%m%d%H%M%S") + file_name[file_name.rfind('.'):]),
        )
    else:
        shutil.move(src, dst)
    time.sleep(1)


def import_boxes(info: list) -> None:
    # ocr
    document_date = (174, 311)
    pag.moveTo(document_date, duration=0.1)
    # end ocr
    pag.click()
    time.sleep(0.2)
    pag.hotkey('ctrl','a')
    time.sleep(0.2)
    pag.press('backspace')
    pag.write(info[1], interval=0.03)
    pag.press('enter')


def keyword_boxes(
    id_img_path: str,
    event_img_path: str,
    info: list
    ) -> None:
    try:
        # ocr
        left, top, *_ = pag.locateOnScreen(event_img_path, confidence=0.9)
        #x, y = pag.locateCenterOnScreen(event_img_path, confidence=0.9)
        pag.moveTo((left + 32, top + 32), duration=0.2)
        # end ocr
        pag.click()
        pag.write(info[1], interval=0.03)
        pag.press('tab')
    except:
        pass
    # ocr
    left, top, *_ = pag.locateOnScreen(id_img_path, confidence=0.9)
    pag.moveTo((left + 30, top + 27), duration=0.2)
    # end ocr
    pag.click()
    pag.write(info[0], interval=0.03)
    pag.press('tab')


def complete() -> None:
    # ocr
    import_button = (88, 994)
    pag.moveTo(import_button, duration=0.1)
    # end ocr
    pag.click()
    # ocr wait on uploading
    time.sleep(4)
    # end ocr wait on uploading
