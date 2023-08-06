import time


def get_system_time() -> float:
    return time.perf_counter() * 1e3


def time_from(_time: float) -> float:
    return get_system_time() - _time


def time_to(_time: float) -> float:
    return _time - get_system_time()


def time_between(_time: float, time2: float) -> float:
    return abs(_time - time2)
