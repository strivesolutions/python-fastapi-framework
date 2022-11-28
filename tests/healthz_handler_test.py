from time import sleep
from timeit import default_timer

import pytest
from fastapi.testclient import TestClient

from fastapiframework import Options, create_app
from fastapiframework.health.config import HealthConfig
from fastapiframework.health.health_check_result import HealthCheckResult
from fastapiframework.health.health_checker import create_health_check


def test_healthz_handler_pass_gives_200():
    def passing_check(name: str) -> HealthCheckResult:
        return HealthCheckResult.ok(name)

    check = create_health_check("test", passing_check)

    app = create_app(Options(health=HealthConfig("test service", checks=[check])))
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200


def test_healthz_handler_fail_gives_500():
    def failing_check(name: str) -> HealthCheckResult:
        return HealthCheckResult.unhealthy(name, "test failure")

    check = create_health_check("test", failing_check)

    app = create_app(Options(health=HealthConfig("test service", checks=[check])))
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 500


def test_healthz_checks_run_asynchronously():
    def delayed_second_check(name: str) -> HealthCheckResult:
        sleep(1)
        return HealthCheckResult.ok(name)

    check1 = create_health_check("test", delayed_second_check)
    check2 = create_health_check("test", delayed_second_check)

    app = create_app(
        Options(
            health=HealthConfig(
                "test service",
                checks=[
                    check1,
                    check2,
                ],
            )
        )
    )
    client = TestClient(app)

    start = default_timer()
    client.get("/healthz")
    end = default_timer()

    expected = 1
    actual = end - start

    assert actual == pytest.approx(
        expected, 0.1
    ), f"Test took {end - start}s to complete (expected ~{expected}s)"
