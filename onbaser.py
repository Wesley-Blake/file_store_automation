"""pyautogui logic to navigate File explorer or file storage software."""
import time
import shutil
from pathlib import Path
from datetime import datetime
import pyperclip
import pyautogui as pag
from pyautogui import ImageNotFoundException

class FileExplorer():
    """Actions to navigate File Explorer."""
    def __init__(
        self,
        file_store_path: Path,
        drop_box_path: Path,
        first_file_img: Path
    ):
        self.file_store_path = file_store_path
        self.drop_box_path = drop_box_path
        size_x, size_y = pag.size()
        x, y , w, h = pag.locateOnScreen(
            str(first_file_img),
            confidence=0.7,
            # Narrow search to right top screen
            # Requires integers, doesn't accept float.
            region=(int(size_x*0.5),0,size_x,int(size_y*0.5))
        )
        self.first_file = (x + w * 0.5, y + h * 1.25)
        self.file_drop = (size_x * 0.35, size_y * 0.5)
        self.focus_first_file = (size_x * 0.75, size_y * 0.75)
        self._start()


    def _focus_first_file(self) -> None:
        pag.click(self.focus_first_file)
        pag.press('home')
        # Becuase home doesn't always set the focus.
        pag.press('PgUp')

    def _start(self) -> None:
        """File explorer function, starter"""
        self._focus_first_file()
        pag.hotkey('ctrl','l')
        #pag.write(str(self.file_store_path), interval=0.03)
        pag.write(str(self.file_store_path))
        pag.press('enter')
        self._focus_first_file()

    def copy_item_name(self) -> str:
        """Copy the name of the first file/dir in file explorer."""
        self._focus_first_file()
        pag.press('f2')
        # File Explorer is slow, gives it a moment to do the thing.
        time.sleep(0.3)
        # We want to the fix extention just incase it isn't valid.
        pag.hotkey('ctrl','a')
        pag.hotkey('ctrl','c')
        result = pyperclip.paste()
        pag.press('esc')
        return result

    def _insert_day_time(self, file_name: str) -> str:
        """
        If file doesn't match expected result and the file already exists in dropbox,
        this will add date&time stamp to the end of the file name before the extention.
        """
        root = file_name[:file_name.rfind('.')]
        date_time = datetime.now().strftime("-%Y%m%d%H%M%S")
        extention = file_name[file_name.rfind('.'):]
        return root + date_time + extention

    def _mover(self, doc_type_name: str, file_name: str) -> None:
        src = self.file_store_path / doc_type_name / file_name
        dst = self.drop_box_path / file_name
        if not src.exists():
            raise FileExistsError(f"Source Doesn't Exist: {src}")
        if dst.exists():
            shutil.move(
                src,
                self.drop_box_path / self._insert_day_time(file_name),
            )
        else:
            shutil.move(src, dst)
        # Gives file explorer a second to catch up.
        time.sleep(1)

    def file_dragger(self, doc_type_name: str) -> list | None:
        """Move first file to files storage application."""
        # Brings focus to first file in explorer
        file_name = self.copy_item_name()
        result = file_name.split('-')
        if len(result) < 2:
            return self._mover(doc_type_name, file_name)
        if not result[0].isdigit():
            return self._mover(doc_type_name, file_name)
        try:
            datetime.fromisoformat(result[1])
        except ValueError:
            return self._mover(doc_type_name, file_name)
        # Move mouse to first file.
        pag.moveTo(self.first_file)
        pag.dragTo(self.file_drop, duration=0.3)
        # ocr?
        time.sleep(2)
        # end ocr?
        return result


class FileStore():
    """Actions to navigate File Storage software."""
    def __init__(
        self,
        #import_button_img: Path,
        primary_id_img: Path,
        event_date_img: Path
    ):
        size_x, size_y = pag.size()
        # Region for fields entry.
        # TODO: future, not self.region but region.
        self.region = (0,0, size_x*0.5, size_y)
        # first import button and second in complete.
        #self.import_button_img = import_button_img
        #self.import_button_img = import_button_img
        self.primary_id = pag.locateCenterOnScreen(
            primary_id_img,
            confidence=0.9,
            region=self.region
        )
        # TODO: future marker for each doc type.
        self.event_date_img = event_date_img
        #self._start(import_button_img, import_button_check_img)

    def _start(
            self,
            import_button_img: Path,
            import_button_check_img: Path
        ) -> None:
        """Starter for file storage software"""
        #try:
        #    center = locateCenterOnScreen(
        #        str(import_button_img),
        #        confidence=0.7,
        #        region=self.region,
        #    )
        #    pag.click(center)
        #try:
        #    center = locateCenterOnScreen(
        #        str(import_button_check_img),
        #        confidence=0.7,
        #        region=self.region,
        #    )
        pass

    def _cancel_box(self) -> None:
        #time.sleep(1)
        # TODO: ocr
        cancel_button = (175, 80)
        pag.click(cancel_button, duration=0.1)
        # end ocr
        #pag.click()
        # Give the program a moment to catch up.
        time.sleep(1)

    def import_doc_box(self, document_type_name: str) -> None:
        """
        Set document type box based on folder name from FileExplorer.copy_item_name().
        """
        # ocr
        self._cancel_box()
        document_type = (227, 232)
        pag.click(document_type, duration=0.1)
        #pag.click()
        # end ocr
        pag.write(document_type_name, interval=0.05)
        pag.press('enter')
        #time.sleep(1)

    def _date_box(self, info: list) -> None:
        # TODO: ocr
        document_date = (174, 311)
        pag.click(document_date, duration=0.1)
        #pag.click()
        # end ocr
        time.sleep(0.1)
        pag.hotkey('ctrl','a')
        time.sleep(0.1)
        pag.press('backspace')
        pag.write(info[1], interval=0.03)
        pag.press('enter')

    def _complete(self) -> None:
        # ocr
        import_button = (88, 994)
        pag.click(import_button, duration=0.1)
        # end ocr
        #pag.click()
        # ocr wait on uploading
        time.sleep(4)
        # end ocr wait on uploading

    def keyword_boxes(self, info: list) -> None:
        """Insert info from file name to field boxes."""
        self._date_box(info)
        try:
            center = pag.locateCenterOnScreen(
                self.event_date_img,
                confidence=0.9,
                region=self.region
            )
            pag.click(center, duration=0.2)
            pag.write(info[1], interval=0.03)
            pag.press('tab')
        except ImageNotFoundException:
            print("Could not locate event date.")
        pag.click(center, duration=0.2)
        pag.write(info[0], interval=0.03)
        pag.press('tab')
        # TODO: copy employee name field and check if len>0
        self._complete()
