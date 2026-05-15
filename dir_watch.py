import json
import time
from datetime import datetime, timezone
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class JsonLoggingEventHandler(FileSystemEventHandler):
    def __init__(self, log_file: Path):
        self.log_file = log_file

    def _log_event(self, event_type, src_path, dest_path=None, is_directory=False):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "src_path": str(src_path),
            "dest_path": str(dest_path) if dest_path else None,
            "is_directory": is_directory,
        }

        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def on_created(self, event):
        self._log_event(
            event_type="created",
            src_path=event.src_path,
            is_directory=event.is_directory,
        )

    #def on_modified(self, event):
    #    self._log_event(
    #        event_type="modified",
    #        src_path=event.src_path,
    #        is_directory=event.is_directory,
    #    )

    def on_deleted(self, event):
        self._log_event(
            event_type="deleted",
            src_path=event.src_path,
            is_directory=event.is_directory,
        )

    def on_moved(self, event):
        self._log_event(
            event_type="moved",
            src_path=event.src_path,
            dest_path=event.dest_path,
            is_directory=event.is_directory,
        )


def main():
    # Directory to monitor
    with open("onbase\\secret.txt", "r") as f:
        _ = f.readline()
        _ = f.readline()
        path_to_watch = f.readline().strip()
    watch_path = Path(path_to_watch).resolve()

    # JSON log file
    log_file = Path("filesystem_changes.jsonl").resolve()

    event_handler = JsonLoggingEventHandler(log_file)
    observer = Observer()

    observer.schedule(
        event_handler,
        path=str(watch_path),
        recursive=True,
    )

    observer.start()
    print(f"Monitoring {watch_path} (recursive)")
    print(f"Logging to {log_file}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()