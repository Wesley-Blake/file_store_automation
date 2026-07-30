"""pyautogui logic to navigate File explorer or file storage software."""

import datetime
import shutil
import time
from pathlib import Path

import pyautogui as pag
import pyperclip
from pyautogui import ImageNotFoundException


def start(import_start_img: str, import_check_img: str, root: str) -> None:
    """Starter for file storage software"""
    size_x, size_y = pag.size()
    try:
        center = pag.locateCenterOnScreen(
            str(import_start_img),
            confidence=0.7,
            region=(int(size_x * 0.2), 0, int(size_x * 0.4), int(size_y * 0.3)),
        )
        pag.click(center, duration=1)
    except ImageNotFoundException:
        pass
    except Exception as e:
        raise RuntimeError("Something happend, please see error.") from e
    time.sleep(2)
    try:
        x, y = pag.size()
        pag.locateCenterOnScreen(
            import_check_img,
            confidence=0.7,
            region=(0, int(y * 0.8), int(x * 0.25), y),
        )
    except Exception as e:
        raise ImageNotFoundException(
            f"Could not locate import button check image: {import_check_img}"
        ) from e

    pag.click((size_x * 0.75, size_y * 0.75))
    pag.press("home")
    pag.press("PgUp")
    pag.press("f4")
    pag.write(root)
    pag.press("enter")
    pag.click((size_x * 0.75, size_y * 0.75))
    pag.press("home")
    pag.press("PgUp")


class FileExplorer:
    """Actions to navigate File Explorer."""

    def __init__(self, root: str, drop_box_path: str, file_drag: str):
        """Locate the file-drag anchor image and open File Explorer at ``root``."""
        self.root = root
        self.drop_box_path = Path(drop_box_path)
        size_x, size_y = pag.size()
        self._focus_explorer = (size_x * 0.75, size_y * 0.75)
        self._file_drop = (size_x * 0.35, size_y * 0.5)
        temp = pag.locateOnScreen(
            file_drag,
            confidence=0.7,
            region=(int(size_x * 0.5), 0, size_x, int(size_y * 0.3)),
        )
        self._file_drag_region = (int(temp.left * 1.25), int(temp.top * 1.9))

    def focus_explorer_file(self) -> None:
        """Click into File Explorer and move focus to the first item in the list."""
        pag.click(self._focus_explorer)
        pag.press("home")
        # Becuase home doesn't always set the focus.
        pag.press("PgUp")

    def copy_item_name(self) -> str:
        """Copy the name of the first file/dir in file explorer."""
        pag.press("f2")
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
        date_time = datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d%H%M%S")
        extention = file_name[file_name.rfind(".") :]
        return root + date_time + extention

    def _mover(self, doc_type_name: str, file_name: str) -> None:
        """Move a file that doesn't match the expected naming pattern to the drop box."""
        src = Path(self.root) / doc_type_name / file_name
        if not src.exists():
            raise FileNotFoundError(f"Source Doesn't Exist: {src}")
        shutil.move(
            src,
            self.drop_box_path / self._insert_day_time(file_name),
        )
        # Refresh file explorer to reflect the moved file.
        pag.press("f5")

    def file_dragger(self, doc_type_name: str) -> list | None:
        """Drag first file into file storage app, or move it to the drop box if misnamed."""
        # Brings focus to first file in explorer
        file_name = self.copy_item_name()
        if not file_name.endswith(".pdf"):
            return self._mover(doc_type_name, file_name)
        result = file_name.split("-")
        if not result or len(result) < 2:
            return self._mover(doc_type_name, file_name)
        if not result[0].isdigit():
            return self._mover(doc_type_name, file_name)
        try:
            datetime.datetime.fromisoformat(result[1])
        except ValueError:
            return self._mover(doc_type_name, file_name)
        # Move mouse to first file.
        pag.moveTo(self._file_drag_region)
        pag.dragTo(self._file_drop, duration=0.3)
        # NOTE: Lazy for now.
        count = 5
        while not pag.pixelMatchesColor(440, 180, (59, 59, 59)):
            time.sleep(0.1)
            count -= 0.1
            if count == 0:
                raise SystemExit("Something went wrong at file import.")
        # count = 0
        # interval = 0.1
        # save_to = Path.home() / "Downloads"
        # while count < 2:
        #    pag.screenshot(f"{save_to / f'file_drag{count:.2f}.png'}")
        #    time.sleep(interval)
        #    count += interval
        return result[:2]  # I only care about first two elements


class FileStore:
    """Actions to navigate File Storage software."""

    def __init__(
        self,
        primary_id_img: str,
        cancel_box_img: str,
        doc_type_img: str,
        date_box_img: str,
    ):
        """Open the import dialog and locate on-screen fields via image recognition."""
        # Region for fields entry.
        self.size = pag.size()
        self.info: list = []
        self._primary_id_img = primary_id_img
        self._doc_type = pag.locateCenterOnScreen(
            doc_type_img,
            confidence=0.9,
            region=(0, 0, int(self.size.width * 0.25), int(self.size.height * 0.25)),
        )
        self.cancel_box = pag.locateCenterOnScreen(
            cancel_box_img,
            confidence=0.9,
            region=(0, 0, int(self.size.width * 0.25), int(self.size.height * 0.3)),
        )
        self._date_field = pag.locateCenterOnScreen(
            date_box_img,
            confidence=0.9,
            region=(0, 0, int(self.size.width * 0.25), int(self.size.height * 0.4)),
        )
        # NOTE: Lazy for now.
        self._complete = (int(self.size.width * 0.05), int(self.size.height * 0.92))
        # End lazy approach for locating complete button.

    def _cancel(self) -> None:
        """Click the cancel/close control and pause briefly for the UI to catch up."""
        pag.click(self.cancel_box, duration=0.5)
        # Give the program a moment to catch up.
        time.sleep(0.5)

    def import_doc_box(self, document_type_name: str) -> None:
        """
        Set document type box based on folder name from FileExplorer.copy_item_name().
        """
        self._cancel()
        pag.click(self._doc_type)
        pag.write(document_type_name)
        pag.press("enter")

    def _date_box(self) -> None:
        """Clear the date field and write the date parsed from the file name."""
        pag.click(self._date_field)
        pag.hotkey("ctrl", "a")
        time.sleep(0.1)
        pag.write(self.info[1])
        pag.press("tab")
        pag.press("tab")

    def keyword_boxes(self) -> None:
        """Insert info from file name to field boxes."""
        self._date_box()
        pag.hotkey("ctrl", "a")
        pag.hotkey("ctrl", "c")
        if pyperclip.paste() == "    -  -  ":
            pag.write(self.info[1])
            pag.press("tab")
        try:
            primary_id = pag.locateCenterOnScreen(
                self._primary_id_img,
                confidence=0.7,
                region=(0, 0, int(self.size.width * 0.2), int(self.size.height * 0.5)),
            )
        except Exception as e:
            raise ImageNotFoundException("Couldn't find primary ID field.") from e
        pag.click(primary_id)
        pag.write(self.info[0])
        pag.press("tab")

    def complete(self) -> None:
        """Click the complete/submit button to finish importing the current file."""
        pag.click(self._complete, duration=0.1)
        count = 5
        while not pag.pixelMatchesColor(440, 180, (255, 255, 255)):
            time.sleep(0.1)
            count -= 0.1
            if count == 0:
                raise SystemExit("Something went wrong at complete.")
        # count = 0
        # interval = 0.1
        # save_to = Path.home() / "Downloads"
        # while count < 2:
        #    pag.screenshot(f"{save_to / f'complete_button{count}.png'}")
        #    time.sleep(interval)
        #    count += interval
