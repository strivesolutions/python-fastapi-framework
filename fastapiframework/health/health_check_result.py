from __future__ import annotations

from enum import Enum
from typing import Optional

from fastapiframework.models.camel_case_model import CamelCaseModel


class HealthCheckStatus(str, Enum):
    ok = "ok"
    unhealthy = "unhealthy"


class HealthCheckResult(CamelCaseModel):
    check_name: str  # TODO: ignore in json export
    status: HealthCheckStatus
    error_details: Optional[str] = None

    @staticmethod
    def ok(check_name: str) -> HealthCheckResult:
        return HealthCheckResult(check_name=check_name, status=HealthCheckStatus.ok)

    @staticmethod
    def unhealthy(check_name: str, error_details: str) -> HealthCheckResult:
        return HealthCheckResult(
            check_name=check_name,
            status=HealthCheckStatus.unhealthy,
            error_details=error_details,
        )
