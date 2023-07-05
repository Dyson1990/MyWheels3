# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 17:17:00 2023

@author: Dyson
"""

from loguru import logger
from pathlib import Path
py_dir = Path(__file__).parent

import os
import subprocess
import time
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Reloader(FileSystemEventHandler):
    def __init__(self, cmd):
        self.cmd = cmd
        self.proc = None

    def on_any_event(self, event):
        if not event.is_directory:
            print("File modified: ", event.src_path)
            # The file has been modified, reload script
            if self.proc is not None and self.proc.poll() is None:
                self.proc.kill()
            self.proc = subprocess.run(["python", self.cmd])
            
if __name__ == '__main__':
    path = r'C:\Users\Weave\MyWheels3'
    cmd = r'C:\Users\Weave\MyWheels3\data_service.py'
    observer = Observer()
    reloader_obj = Reloader(cmd)
    observer.schedule(reloader_obj, path=path, recursive=True)
    observer.start()

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Watching for changes...")
            
            if reloader_obj.proc is not None:
                p = psutil.Process(reloader_obj.proc.pid)
                while True:
                    try:
                        cpu_percent = p.cpu_percent(interval=1)
                        mem_info = p.memory_info()
                    except psutil.NoSuchProcess:
                        break
                    print(f"Process pid={p.pid} CPU usage={cpu_percent:.2f}% Memory usage={mem_info.rss / 1024 / 1024:.2f}MB")
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()