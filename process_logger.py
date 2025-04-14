import csv
from datetime import datetime
from time import sleep

import psutil

process_registry = {}


def human_datetime(timestamp: float):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def main(sleep_period: float = 0.5):
    while True:
        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
            except psutil.NoSuchProcess:
                continue
            if process_registry.get(p):
                process_registry[p]["status"] = p.status()
                process_registry[p]["cpu_percent"] = p.cpu_percent()
                process_registry[p]["memory_percent"] = p.memory_percent()

            else:
                process_registry[p] = {
                    "status": p.status(),
                    "name": p.name(),
                    "pid": p.pid,
                    "start_time": human_datetime(p.create_time()),
                    "end_time": "",
                    "cpu_percent": p.cpu_percent(),
                    "memory_percent": p.memory_percent(),
                }

        n = 0
        procs_to_del = []
        for p, data in process_registry.items():
            try:
                p.status()
            except psutil.NoSuchProcess:
                process_registry[p]["end_time"] = human_datetime(
                    datetime.now().timestamp()
                )
                process_registry[p]["status"] = "terminated"
                print(
                    f"DATETIME={human_datetime(datetime.now().timestamp())} PID={p.pid} NAME={data['name']} is no longer exists"
                )
                procs_to_del.append(p)
            n += 1
        for p in procs_to_del:
            del process_registry[p]
        sleep(sleep_period)
