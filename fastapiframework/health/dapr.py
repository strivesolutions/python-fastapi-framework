import requests
from strivehealthchecks import HealthChecker, HealthCheckResult


def create_dapr_health_check(endpoint: str) -> HealthChecker:
    def run(name: str) -> HealthCheckResult:
        url = f"{endpoint}/v1.0/healthz"
        try:
            resp = requests.get(url)

            return (
                HealthCheckResult.ok(name)
                if resp.status_code == 204
                else HealthCheckResult.unhealthy(
                    name, f"Response from Dapr was {resp.status_code}"
                )
            )
        except Exception as e:
            return HealthCheckResult.unhealthy(name, str(e))

    return HealthChecker(name="dapr", run=run)
