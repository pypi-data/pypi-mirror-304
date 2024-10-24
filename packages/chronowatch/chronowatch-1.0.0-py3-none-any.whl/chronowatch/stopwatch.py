import time
from typing import Optional
from dataclasses import dataclass


@dataclass
class TaskInfo:
    task_name: str
    time_nanos: int

    def get_time_seconds(self) -> float:
        return self.time_nanos / 1e9

    def get_time_millis(self) -> float:
        return self.time_nanos / 1e6

    def get_time(self, time_unit: str) -> float:
        if time_unit == 'SECONDS':
            return self.get_time_seconds()
        elif time_unit == 'MILLISECONDS':
            return self.get_time_millis()
        else:
            raise ValueError("Unsupported time unit")


class Stopwatch:
    def __init__(self, id_watch: str = ''):
        self.id = id_watch
        self.task_list: Optional[list[TaskInfo]] = []
        self.start_time_nanos = 0
        self.current_task_name: Optional[str] = None
        self._last_task_info: Optional[TaskInfo] = None
        self.task_count = 0
        self.total_time_nanos = 0

    def set_keep_task_list(self, keep_task_list: bool):
        self.task_list = [] if keep_task_list else None

    def start(self, task_name: str = ''):
        if self.current_task_name is not None:
            raise RuntimeError("Can't start StopWatch: it's already running")
        else:
            self.current_task_name = task_name
            self.start_time_nanos = time.time_ns()

    def stop(self):
        if self.current_task_name is None:
            raise RuntimeError("Can't stop StopWatch: it's not running")
        else:
            last_time = time.time_ns() - self.start_time_nanos
            self.total_time_nanos += last_time
            self._last_task_info = TaskInfo(self.current_task_name, last_time)
            if self.task_list is not None:
                self.task_list.append(self._last_task_info)
            self.task_count += 1
            self.current_task_name = None

    def is_running(self) -> bool:
        return self.current_task_name is not None

    def current_task_name(self) -> Optional[str]:
        return self.current_task_name

    def last_task_info(self) -> TaskInfo:
        if self._last_task_info is None:
            raise RuntimeError("No tasks run")
        return self._last_task_info

    def get_task_info(self) -> list[TaskInfo]:
        if self.task_list is None:
            raise RuntimeError("Task info is not being kept!")
        return self.task_list

    def get_task_count(self) -> int:
        return self.task_count

    def get_total_time_nanos(self) -> int:
        return self.total_time_nanos

    def get_total_time_millis(self) -> float:
        return self.total_time_nanos / 1e6

    def get_total_time_seconds(self) -> float:
        return self.total_time_nanos / 1e9

    def get_total_time(self, time_unit: str) -> float:
        if time_unit == 'SECONDS':
            return self.get_total_time_seconds()
        elif time_unit == 'MILLISECONDS':
            return self.get_total_time_millis()
        else:
            raise ValueError("Unsupported time unit")

    def pretty_print(self, time_unit: str = 'SECONDS') -> str:
        nf = "{:.9f}"
        pf = "{:.0%}"
        sb = []
        sb.append(f"StopWatch '{self.id}': ")
        total = self.get_total_time(time_unit)
        sb.append(nf.format(total))
        sb.append(f" {time_unit.lower()}\n")
        width = max(len(''.join(sb)), 40)
        sb.append("-" * width + "\n")
        sb.append("{:<14}  {:<8}  Task name\n".format("Seconds", "%"))
        sb.append("-" * width + "\n")
        if self.task_list:
            for task in self.task_list:
                time_val = task.get_time(time_unit)
                percentage = task.get_time_seconds() / self.get_total_time_seconds()
                sb.append("{:<14}  {:<8}  {}\n".format(nf.format(time_val), pf.format(percentage), task.task_name))
        else:
            sb.append("No task info kept")
        return ''.join(sb)


    def short_summary(self) -> str:
        return f"StopWatch '{self.id}': {self.get_total_time_seconds()} seconds"

    def __str__(self) -> str:
        task_info_str = '; '.join(
            f"[{task.task_name}] took {task.get_time_seconds()} seconds" for task in self.task_list)
        return f"{self.short_summary()}; {task_info_str}"