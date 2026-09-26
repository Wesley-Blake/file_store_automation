"""pyautogui logic to navigate File explorer or file storage software."""

import datetime
import shutil
import time
from collections.abc import Callable
from pathlib import Path

import pyautogui as pag
import pyperclip
from pyautogui import ImageNotFoundException

RETRIES = 30
EMPTY_DATE_MASK = "    -  -  "


def _focus_point() -> tuple[float, float]:
    """Point inside File Explorer's file list used to give it focus."""
    size_x, size_y = pag.size()
    return (size_x * 0.75, size_y * 0.75)


def _focus_first_item() -> None:
    """Click into File Explorer and move focus to the first item in the list."""
    pag.click(_focus_point())
    pag.press("home")
    # Becuase home doesn't always set the focus.
    pag.press("PgUp")


def _move_and_click(point, err_msg: str, click: bool = True, **click_kwargs) -> None:
    """Move the mouse to ``point`` until it arrives, then optionally click it."""
    for _ in range(RETRIES):
        if tuple(pag.position()) == tuple(point):
            break
        pag.moveTo(point)
        time.sleep(0.5)
    else:
        raise SystemExit(err_msg)
    if click:
        pag.click(point, **click_kwargs)


def _wait_for_pixel(
    rgb: tuple[int, int, int],
    err_msg: str,
    interval: float,
    on_retry: Callable[[], None] | None = None,
) -> None:
    """Wait until the status pixel matches ``rgb``, calling ``on_retry`` between checks."""
    for _ in range(RETRIES):
        # NOTE: Lazy for now.
        if pag.pixelMatchesColor(440, 180, rgb):
            return
        time.sleep(interval)
        if on_retry is not None:
            on_retry()
    raise SystemExit(err_msg)


def start(import_start_img: str, import_check_img: str, root: str) -> None:
    """Starter for file storage software"""
    size_x, size_y = pag.size()
    try:
        center = pag.locateCenterOnScreen(
            import_start_img,
            confidence=0.7,
            region=(int(size_x * 0.2), 0, int(size_x * 0.4), int(size_y * 0.3)),
        )
        pag.click(center, duration=1)
    except Exception as e:
        raise RuntimeError("Something happend, please see error.") from e
    # pyautogui is faster then the program, it needs a few seconds.
    time.sleep(2)
    try:
        pag.locateCenterOnScreen(
            import_check_img,
            confidence=0.7,
            region=(0, int(size_y * 0.8), int(size_x * 0.25), size_y),
        )
    except Exception as e:
        raise ImageNotFoundException(
            f"Could not locate import button check image: {import_check_img}"
        ) from e

    _focus_first_item()
    pag.press("f4")
    pag.write(root)
    pag.press("enter")
    _focus_first_item()


def _is_valid_name(file_name: str) -> bool:
    """True if ``file_name`` looks like ``<digits>-<iso date>...pdf``."""
    if not file_name.endswith(".pdf"):
        return False
    parts = file_name.split("-")
    if len(parts) < 2 or not parts[0].isdigit():
        return False
    try:
        datetime.datetime.fromisoformat(parts[1])
    except ValueError:
        return False
    return True


class FileExplorer:
    """Actions to navigate File Explorer."""

    def __init__(self, root: str, drop_box_path: str, file_drag: str):
        """Locate the file-drag anchor image and open File Explorer at ``root``."""
        self.root = root
        self.drop_box_path = Path(drop_box_path)
        self.last_file_name = ""
        size_x, size_y = pag.size()
        self._file_drop = (size_x * 0.35, size_y * 0.5)
        temp = pag.locateOnScreen(
            file_drag,
            confidence=0.7,
            region=(int(size_x * 0.5), 0, size_x, int(size_y * 0.3)),
        )
        self._file_drag_region = (int(temp.left * 1.25), int(temp.top * 1.9))

    def focus_explorer_file(self) -> None:
        """Click into File Explorer, focus the first item, and refresh."""
        _focus_first_item()
        pag.press("f5")

    def copy_item_name(self) -> str:
        """Copy the name of the first file/dir in file explorer."""
        pag.press("f2")
        # We want to the fix extention just incase it isn't valid.
        pag.hotkey("ctrl", "a")
        pag.hotkey("ctrl", "c")
        result = pyperclip.paste()
        pag.press("esc")
        return result

    @staticmethod
    def _insert_day_time(file_name: str) -> str:
        """
        If file doesn't match expected result and the file already exists in dropbox,
        this will add date&time stamp to the end of the file name before the extention.
        """
        path = Path(file_name)
        date_time = datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d%H%M%S")
        return path.stem + date_time + path.suffix

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
        file_name = self.copy_item_name()
        self.last_file_name = file_name
        if not _is_valid_name(file_name):
            return self._mover(doc_type_name, file_name)
        _move_and_click(
            self._file_drag_region,
            "Couldn't go to file drag location in explorer.",
            click=False,
        )
        pag.dragTo(self._file_drop, duration=0.3)
        _wait_for_pixel((59, 59, 59), "Something went wrong at file import.", 0.5)
        return file_name.split("-")[:2]  # I only care about first two elements


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
        """Click the cancel/close control."""
        _move_and_click(self.cancel_box, "Failed to find cancel button.")

    def import_doc_box(self, document_type_name: str) -> None:
        """
        Set document type box based on folder name from FileExplorer.copy_item_name().
        """
        self._cancel()
        _move_and_click(self._doc_type, "Failed to find doc type in file store.")
        pag.write(document_type_name)
        pag.press("enter")

    def _date_box(self) -> None:
        """Clear the date field and write the date parsed from the file name."""
        _move_and_click(self._date_field, "Failed to find date field in file store.")
        pag.hotkey("ctrl", "a")
        pag.write(self.info[1])
        # Retry once if the field didn't take the date.
        pag.hotkey("ctrl", "a")
        pag.hotkey("ctrl", "c")
        if pyperclip.paste() == EMPTY_DATE_MASK:
            pag.write(self.info[1])
            pag.press("tab")

    def keyword_boxes(self) -> None:
        """Insert info from file name to field boxes."""
        self._date_box()
        try:
            primary_id = pag.locateCenterOnScreen(
                self._primary_id_img,
                confidence=0.7,
                region=(0, 0, int(self.size.width * 0.2), int(self.size.height * 0.5)),
            )
        except Exception as e:
            raise ImageNotFoundException("Couldn't find primary ID field.") from e
        _move_and_click(primary_id, "Failed to find primary_id field.")
        pag.write(self.info[0])
        pag.press("tab")

    def complete(self) -> None:
        """Click the complete/submit button to finish importing the current file."""
        _move_and_click(self._complete, "Failed to find complete button.")
        _wait_for_pixel(
            (255, 255, 255),
            "Something went wrong at complete.",
            0.1,
            on_retry=lambda: pag.click(self._complete, duration=0.1),
        )
