import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if it's a file and not a directory
        if not event.is_directory:
            print(f"New file created: {event.src_path}")

if __name__ == "__main__":
    # For Linux/macOS, use "/" for root, for Windows use "C:\\"
    path = "/" if os.name != 'nt' else "C:\\"
    
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"Monitoring the entire system from: {path} for new file creations...")

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
