import time
from inspect import ismethod

all_exec_times = {}


class ExecutionTime:
    def __init__(self):
        self._times = []
        self._avg = 0.0

    def add(self, time: float):
        self._times.append(time)
        self._avg = sum(self._times) / len(self._times)

    @property
    def avg(self) -> float:
        return self._avg

    @property
    def last(self) -> float:
        return self._times[-1]

    @property
    def all(self) -> list:
        return self._times


def timed_exec(func: callable):
    """Decorator for timing execution of a function."""
    global all_exec_times

    # Determine if the function is a method of a class
    if ismethod(func):
        # For methods, include the class name and method name
        # BUG: When using @timed_exec on a method, the qualname does not
        #      include the class name (it only includes the method name).
        key = f"{func.__module__}.{func.__qualname__}"
    else:
        # For standalone functions, just include the module and function name
        key = f"{func.__module__}.{func.__name__}"

    if key not in all_exec_times:
        all_exec_times[key] = ExecutionTime()
    exec_times = all_exec_times[key]

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        runtime = time.time() - start
        exec_times.add(runtime)
        return result

    return wrapper
