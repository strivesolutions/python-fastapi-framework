from typing import Callable

from .health_check_result import HealthCheckResult

HealthCheckFunc = Callable[[str], HealthCheckResult]


class HealthChecker:
    def __init__(self, name: str, run: HealthCheckFunc, timeout_seconds: int = 0):
        self.name = name
        self.__run = run
        self.timeout_seconds = timeout_seconds

    def run(self) -> HealthCheckResult:
        return self.__run(self.name)


def create_health_check(name: str, run: HealthCheckFunc) -> HealthChecker:
    return HealthChecker(name=name, run=run)


def create_health_check_with_timeout(
    name: str, timeout_seconds: int, run: HealthCheckFunc
) -> HealthChecker:
    return HealthChecker(name=name, run=run, timeout_seconds=timeout_seconds)
