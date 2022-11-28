from typing import Callable

from .health_check_result import HealthCheckResult

HealthCheckFunc = Callable[[str], HealthCheckResult]


class HealthChecker:
    def __init__(self, name: str, run: HealthCheckFunc):
        self.name = name
        self.__run = run

    def run(self) -> HealthCheckResult:
        return self.__run(self.name)


def create_health_check(name: str, run: HealthCheckFunc) -> HealthChecker:
    return HealthChecker(name=name, run=run)
