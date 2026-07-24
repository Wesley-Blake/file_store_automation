"""pyautogui logic to navigate File explorer or file storage software."""

import shutil
import time
from datetime import datetime
from pathlib import Path

import pyautogui as pag
import pyperclip
from pyautogui import ImageNotFoundException


class FileExplorer:
    """Actions to navigate File Explorer."""

    def __init__(
        self, file_store_path: Path, drop_box_path: Path, first_file_img: Path
    ):
        self._file_store_path = file_store_path
        self._drop_box_path = drop_box_path
        size_x, size_y = pag.size()
        self._focus_first_file = (size_x * 0.75, size_y * 0.75)
        self._file_drop = (size_x * 0.35, size_y * 0.5)
        self._start()

    def _focus_first_file(self) -> None:
        pag.click(self._focus_first_file)
        pag.press("home")
        # Becuase home doesn't always set the focus.
        pag.press("PgUp")

    def _start(self) -> None:
        """File explorer function, starter"""
        self._focus_first_file()
        pag.hotkey("ctrl", "l")
        pag.write(str(self._file_store_path))
        pag.press("enter")
        self._focus_first_file()

    def _copy_item_name(self) -> str:
        """Copy the name of the first file/dir in file explorer."""
        self._focus_first_file()
        pag.press("f2")
        # File Explorer is slow, gives it a moment to do the thing.
        time.sleep(0.3)
        # We want to the fix extention just incase it isn't valid.
        pag.hotkey("ctrl", "a")
        pag.hotkey("ctrl", "c")
        result = pyperclip.paste()
        pag.press("esc")
        return result

    def _insert_day_time(self, file_name: str) -> str:
        """
        If file doesn't match expected result and the file already exists in dropbox,
        this will add date&time stamp to the end of the file name before the extention.
        """
        root = file_name[: file_name.rfind(".")]
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        extention = file_name[file_name.rfind(".") :]
        return root + date_time + extention

    def _mover(self, doc_type_name: str, file_name: str) -> None:
        src = self._file_store_path / doc_type_name / file_name
        if not src.exists():
            raise FileExistsError(f"Source Doesn't Exist: {src}")
        shutil.move(
            src,
            self._drop_box_path / self._insert_day_time(file_name),
        )
        # Refresh file explorer to reflect the moved file.
        pag.press("f5")

    def file_dragger(self, doc_type_name: str) -> list | None:
        """Move first file to files storage application."""
        # TODO: log the action
        # Brings focus to first file in explorer
        file_name = self._copy_item_name()
        result = file_name.split("-")
        if not result or len(result) < 2:
            return self._mover(doc_type_name, file_name)
        if not result[0].isdigit():
            return self._mover(doc_type_name, file_name)
        try:
            datetime.fromisoformat(result[1])
        except ValueError:
            return self._mover(doc_type_name, file_name)
        # Move mouse to first file.
        pag.moveTo(self._focus_first_file)
        pag.dragTo(self._file_drop, duration=0.3)
        # I want this image to catch the loading bar
        count = 0
        interval = 0.5
        save_to = Path.home() / "Downloads"
        while count < 5:
            pag.screenshot(f"{save_to / f'file_drag{count}.png'}")
            time.sleep(interval)
            count += interval
        return result[:2]  # I only care about first two elements


class FileStore:
    """Actions to navigate File Storage software."""

    def __init__(
        self,
        primary_id_img: Path,
        import_button_img: Path,
        import_button_check_img: Path,
        cancel_box_img: Path,
        doc_type_img: Path,
        date_box_img: Path,
    ):
        size_x, size_y = pag.size()
        # Region for fields entry.
        self.info: list | None = None
        self._region = (0, 0, size_x * 0.5, size_y)
        self._primary_id = pag.locateCenterOnScreen(
            primary_id_img, confidence=0.9, region=self._region
        )
        # TODO: future marker for each doc type.
        self._cancel_box = pag.locateCenterOnScreen(
            cancel_box_img, confidence=0.9, region=(0, 0, size_x * 0.25, size_y * 0.3)
        )
        self._doc_type = pag.locateCenterOnScreen(
            doc_type_img, confidence=0.9, region=(0, 0, size_x * 0.25, size_y * 0.25)
        )
        self._date_box = pag.locateCenterOnScreen(
            date_box_img, confidence=0.9, region=(0, 0, size_x * 0.25, size_y * 0.4)
        )
        # Lazy for now.
        self._complete = (size_x * 0.05, size_y * 0.92)
        # End lazy approach for locating complete button.
        self._start(import_button_img, import_button_check_img)

    def _start(self, import_loader_img: Path, import_check_img: Path) -> None:
        """Starter for file storage software"""
        size_x, size_y = pag.size()
        try:
            center = pag.locateCenterOnScreen(
                str(import_loader_img),
                confidence=0.7,
                region=(0, 0, size_x * 0.5, size_y * 0.3),
            )
            pag.click(center)
        except ImageNotFoundException:
            raise ImageNotFoundException(
                f"Could not locate import button image: {import_loader_img}"
            )
        try:
            pag.locateCenterOnScreen(
                str(import_check_img),
                confidence=0.7,
                region=self._region,
            )
        except ImageNotFoundException:
            raise ImageNotFoundException(
                f"Could not locate import button check image: {import_check_img}"
            )

    def _cancel_box(self) -> None:
        pag.click(self._cancel_box, duration=0.1)
        # Give the program a moment to catch up.
        time.sleep(1)

    def import_doc_box(self, document_type_name: str) -> None:
        """
        Set document type box based on folder name from FileExplorer.copy_item_name().
        """
        self._cancel_box()
        pag.click(self._doc_type, duration=0.1)
        pag.write(document_type_name, interval=0.05)
        pag.press("enter")

    def _date_box(self) -> None:
        pag.click(self._date_box, duration=0.1)
        pag.hotkey("ctrl", "a")
        time.sleep(0.1)
        pag.write(self.info[1], interval=0.03)
        pag.press("tab")
        pag.press("tab")

    def _complete(self) -> None:
        pag.click(self._complete, duration=0.1)
        count = 0
        interval = 0.5
        save_to = Path.home() / "Downloads"
        while count < 5:
            pag.screenshot(f"{save_to / f'complete_button{count}.png'}")
            time.sleep(interval)
            count += interval

    def keyword_boxes(self) -> None:
        """Insert info from file name to field boxes."""
        self._date_box()
        pag.hotkey("ctrl", "a")
        pyperclip.copy()
        if pyperclip.paste() == "    -  -  ":
            pag.write(self.info[1], interval=0.03)
            pag.press("tab")
        pag.click(self._primary_id, duration=0.2)
        pag.write(self.info[0], interval=0.03)
        pag.press("tab")
        # TODO: copy employee name field and check if len>0
        self._complete()
