import time
import shutil
from pathlib import Path
from datetime import datetime
import pyperclip
import pyautogui as pag


def starter(base_dir_path: Path) -> None:
    first_dir = (1253, 208)
    explor_search_bar = (1677, 63)
    pag.moveTo(explor_search_bar, duration=0.1)
    pag.click()
    pag.write(str(base_dir_path), interval=0.03)
    pag.press('enter')
    pag.press('esc')
    pag.moveTo(first_dir, duration=0.1)
    pag.leftClick()


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
    document_type = (227, 232)
    cancel_box()
    pag.moveTo(document_type, duration=0.1)
    pag.click()
    pag.write(document_type_name, interval=0.05)
    pag.press('enter')
    time.sleep(1)


def file_dragger(onbase_path: Path,
                 doc_type_name: str,
                 input_path: Path) -> list | None:
    first_file = (1192, 175)
    file_drop = (610, 525)
    pag.moveTo(first_file, duration=0.1)
    pag.leftClick()
    file_name = copy_file_name()
    result = file_name.split(' - ')
    try:
        datetime.fromisoformat(result[1])
    except ValueError:
        return _mover(onbase_path, doc_type_name, input_path, file_name)
    if len(result) < 2:
        return _mover(onbase_path, doc_type_name, input_path, file_name)
    if not result[0].isdigit():
        return _mover(onbase_path, doc_type_name, input_path, file_name)
    pag.dragTo(file_drop, duration=0.2)
    time.sleep(3)
    return result


def _mover(onbase_path: Path,
           doc_type_name: str,
           input_path: Path,
           file_name: str) -> None:
    dst = input_path / file_name
    src = onbase_path / doc_type_name / file_name
    if not src.exists():
        raise FileExistsError(
            f"Source Doesn't Exist: {src}"
        )
    elif dst.exists():
        raise FileExistsError(
            f"Destination Already Exists: {dst}"
        )
        _mover(
            onbase_path,
            doc_type_name,
            input_path,
            file_name + datetime.now().strftime("-%Y%m%d%H%M%S"),
        )
    else:
        shutil.move(src, dst)
    time.sleep(1)


def import_boxes(info: list) -> None:
    document_date = (174, 311)
    pag.moveTo(document_date, duration=0.1)
    pag.click()
    time.sleep(0.2)
    pag.hotkey('ctrl','a')
    time.sleep(0.2)
    pag.press('backspace')
    pag.write(info[1], interval=0.03)
    pag.press('enter')


def keyword_boxes(id_img_path: str,
                  event_img_path: str,
                  info: list) -> None:
    try:
        left, top, *_ = pag.locateOnScreen(event_img_path, confidence=0.9)
        pag.moveTo((left + 32, top + 32), duration=0.2)
        pag.click()
        pag.write(info[1], interval=0.03)
        pag.press('tab')
    except:
        pass
    left, top, *_ = pag.locateOnScreen(id_img_path, confidence=0.9)
    pag.moveTo((left + 30, top + 27), duration=0.2)
    pag.click()
    pag.write(info[0], interval=0.03)
    pag.press('tab')


def complete() -> None:
    import_button = (88, 994)
    pag.moveTo(import_button, duration=0.1)
    pag.click()
    time.sleep(4)
