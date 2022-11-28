from typing import Dict

from fastapiframework.health.health_check_result import (
    HealthCheckResult,
    HealthCheckStatus,
)
from fastapiframework.models.camel_case_model import CamelCaseModel


class ServiceHealth(CamelCaseModel):
    service_name: str
    checks: Dict[str, HealthCheckResult] = {}
    unhealthy: bool = False

    def add_result(self, result: HealthCheckResult) -> None:
        self.checks[result.check_name] = result

        if result.status == HealthCheckStatus.unhealthy and not self.unhealthy:
            self.unhealthy = True
