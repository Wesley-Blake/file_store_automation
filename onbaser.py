import time
import shutil
from pathlib import Path
from datetime import datetime
import pyperclip
import pyautogui as pag

class file_explorer():
    def __init__(self, file_store_path: Path, drop_box_path: Path, first_file_img: Path):
        if not all(
            file_store_path.exists(),
            drop_box_path.exists(),
            first_file_img.exists()
        ):
            raise FileNotFoundError("Args aren't proper paths.")
        self.file_store_path = file_store_path
        self.drop_box_path = drop_box_path
        self.first_file_img = first_file_img
        self.x, self.y = pag.size()
        x, y , w, h= pag.locateOnScreen(str(self.first_file_img), confidence=0.7, region=(int(self.x*0.5),0,self.x,int(self.y*0.5)))
        self.first_tuple = (x + w * 0.5, y + h * 1.25)

    def _firstFile(self):
        pag.click(self.x * 0.75, self.y * 0.75)
        pag.press('home')
        # Becuase home doesn't always set teh focus.
        pag.press('PgUp')

    def starter(self) -> None:
        """File explorer function, starter"""
        self._firstFile()
        pag.hotkey('ctrl','l')
        #pag.write(str(self.file_store_path), interval=0.03)
        pag.write(str(self.file_store_path))
        pag.press('enter')
        self._firstFile()

    def copy_file_name(self) -> str:
        self._firstFile()
        pag.press('f2')
        time.sleep(0.3)
        pag.hotkey('ctrl','a')
        pag.hotkey('ctrl','c')
        result = pyperclip.paste()
        pag.press('esc')
        return result

    def _insert_day_time(file_name):
        #(file_name[:file_name.rfind('.')] + datetime.now().strftime("-%Y%m%d%H%M%S") + file_name[file_name.rfind('.'):])
        root = file_name[:file_name.rfind('.')]
        date_time = datetime.now().strftime("-%Y%m%d%H%M%S")
        extention = file_name[file_name.rfind('.'):]
        return root + date_time + extention

    def _mover(self, doc_type_name: str, file_name: str) -> None:
        src = self.file_store_path / doc_type_name / file_name
        dst = self.drop_box_path / file_name
        if not src.exists():
            raise FileExistsError(f"Source Doesn't Exist: {src}")
        elif dst.exists():
            shutil.move(
                src,
                self.drop_box_path / self._insert_day_time(file_name),
            )
        else:
            shutil.move(src, dst)
        # Gives file explorer a second to catch up.
        time.sleep(1)

    def file_dragger(self, doc_type_name: str) -> list | None:
        # Brings focus to first file in explorer
        file_name = self.copy_file_name()
        # TODO: detect file date format transform to 20260525
        # TODO: split by '-' only not ' - '
        result = file_name.split(' - ')
        if len(result) < 2:
            return self._mover(doc_type_name, file_name)
        if not result[0].isdigit():
            return self._mover(doc_type_name, file_name)
        try:
            datetime.fromisoformat(result[1])
        except ValueError:
            return self._mover(doc_type_name, file_name)
        # Move mouse to first file.
        pag.moveTo(self.first_tuple)
        file_drop = (self.x * 0.35, self.y * 0.5)
        pag.dragTo(file_drop, duration=0.3)
        # ocr?
        time.sleep(2)
        # end ocr?
        return result


class file_store():
    def __init__(import_button_img: Path, primary_id_img: Path, event_date_img: Path):
        if not all(
            import_button_img.exists(),
            primary_id_img.exists(),
            event_date_img.exists()
        ):
            raise FileNotFoundError("Arguments not proper path.")
        self.import_button_img = import_button_img
        self.primary_id_img = primary_id_img
        self.event_date_img = event_date_img
        self.x, self.y = pag.size()
        self.region = (0,0, self.x*0.5, self.y)

    def _cancel_box(self) -> None:
        #time.sleep(1)
        # TODO: ocr
        cancel_button = (175, 80)
        pag.moveTo(cancel_button, duration=0.1)
        # end ocr
        pag.click()
        time.sleep(1)

    def import_doc_box(self, document_type_name: str) -> None:
        # ocr
        self._cancel_box()
        document_type = (227, 232)
        pag.moveTo(document_type, duration=0.1)
        pag.click()
        # end ocr
        pag.write(document_type_name, interval=0.05)
        pag.press('enter')
        #time.sleep(1)

    def date_box(self, info: list) -> None:
        # TODO: ocr
        document_date = (174, 311)
        pag.moveTo(document_date, duration=0.1)
        pag.click()
        # end ocr
        time.sleep(0.1)
        pag.hotkey('ctrl','a')
        time.sleep(0.1)
        pag.press('backspace')
        pag.write(info[1], interval=0.03)
        pag.press('enter')

    def keyword_boxes(self, info: list) -> None:
        try:
            # ocr
            center = pag.locateCenterOnScreen(self.event_date_img, confidence=0.9, region=self.region)
            #x, y = pag.locateCenterOnScreen(event_img_path, confidence=0.9)
            #pag.moveTo(center, duration=0.2)
            # end ocr
            pag.click(center, duration=0.2)
            pag.write(info[1], interval=0.03)
            pag.press('tab')
        except:
            pass
        # ocr
        center = pag.locateCenterOnScreen(id_img_path, confidence=0.9, region=self.region)
        #pag.moveTo(center, duration=0.2)
        # end ocr
        pag.click(center, duration=0.2)
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

if __name__ == '__main__':
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read('.env')
    if cfg:
        primary_id_img = cfg['file_store']['p_id_img']
        event_date_img = cfg['file_store']['event_date_img']
        import_button_img = cfg['file_store']['import_button_img']
        onbase_path = Path(cfg['file_store']['onbase_path'])
        input_path = Path(cfg['file_store']['drop_box_path'])
        first_file_img = Path(cfg['file_store']['first_file_img'])
    else:
        raise FileNotFoundError("Config file not found: .env")
    file_e = file_explorer(onbase_path, input_path, first_file_img)
    file_e.file_dragger("SF Payroll Timesheet")
