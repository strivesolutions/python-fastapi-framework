import asyncio
from typing import Any, Coroutine, List

from asyncer import asyncify
from fastapi import Response

from fastapiframework.health.config import get_health_config
from fastapiframework.health.health_check_result import HealthCheckResult
from fastapiframework.health.health_checker import HealthChecker
from fastapiframework.health.service_health import ServiceHealth


async def run_checks(
    service_health: ServiceHealth,
    checks: List[HealthChecker],
) -> None:

    tasks: List[Any] = []
    for check in checks:
        if check.timeout_seconds == 0:
            tasks.append(asyncify(check.run)())
        else:
            task: Coroutine = asyncio.wait(
                [asyncio.create_task(asyncify(check.run)())],  # type: ignore
                timeout=check.timeout_seconds,
            )

            tasks.append(task)

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        if type(result) is tuple:
            check = checks[i]
            service_health.add_result(
                HealthCheckResult.unhealthy(
                    check.name, f"did not respond after {check.timeout_seconds} seconds"
                )
            )
        elif type(result) is HealthCheckResult:
            service_health.add_result(result)
        else:
            check = checks[i]
            service_health.add_result(
                HealthCheckResult.unhealthy(
                    check.name,
                    "did not return a HealthCheckResult",
                )
            )


async def health_handler(response: Response) -> ServiceHealth:
    config = get_health_config()

    service_health = ServiceHealth(service_name=config.service_name)

    await run_checks(service_health, config.checks)

    response.status_code = 500 if service_health.unhealthy else 200
    return service_health
