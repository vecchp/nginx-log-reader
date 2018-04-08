import shlex
import time
import threading

from datetime import datetime, timedelta
from queue import Queue
from collections import namedtuple, defaultdict

LogEntry = namedtuple('LogEntry', ['route', 'status_code'])


# Extract route and status code from log entry
# Note: This can also be done with a regex
def parse_log_entry(log_entry: str):
    data = shlex.split(log_entry)
    for i, value in enumerate(data):
        if any(command in value for command in ['HEAD', 'GET', 'PUT', 'POST', 'PATCH', 'DELETE']):
            _, route, _ = value.split(' ')
            return LogEntry(route=route, status_code=data[i + 1])


def summary_output(metric_summary: dict):
    return (f'{k}:{v}|s\n' for k, v in metric_summary.items())


def build_summary(entry: LogEntry, metric_summary: dict):
    status_code_type = f'{entry.status_code[0]}0x'
    metric_summary[status_code_type] += 1

    if status_code_type == "50x":
        metric_summary[entry.route] += 1


class NginxSummary(threading.Thread):
    def __init__(self, outfile: str, queue: Queue, delay: int = 5):
        threading.Thread.__init__(self)
        self.delay = delay
        self.queue = queue
        self.outfile = outfile

    def run(self):
        next_time = datetime.now() + timedelta(seconds=self.delay)
        metric_summary = defaultdict(int)

        with open(self.outfile, 'a') as f:
            while True:
                cur_time = datetime.now()
                if cur_time >= next_time:
                    f.writelines(summary_output(metric_summary))
                    metric_summary = defaultdict(int)
                    next_time = cur_time + timedelta(seconds=self.delay)
                    f.flush()

                if not self.queue.empty():
                    entry = self.queue.get()
                    parsed_entry = parse_log_entry(entry)
                    build_summary(parsed_entry, metric_summary)
                else:
                    time.sleep(1)
