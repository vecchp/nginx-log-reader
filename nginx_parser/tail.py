import os
import time
import threading

from queue import Queue


# Follow a file like tail -f.
# https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file
# Handles log rotation
def follow(name, delay):
    current = open(name, "r")
    curino = os.fstat(current.fileno()).st_ino
    while True:
        while True:
            line = current.readline()
            if not line:
                break
            yield line

        try:
            if os.stat(name).st_ino != curino:
                new = open(name, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                continue
        except IOError:
            pass
        time.sleep(delay)


class FileTail(threading.Thread):
    def __init__(self, file_path: str, queue: Queue, delay: float = 0.5):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.delay = delay
        self.queue = queue

    def run(self):
        for l in follow(self.file_path, self.delay):
            self.queue.put(l)
