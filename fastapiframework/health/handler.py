from fastapi import FastAPI, Response

from fastapiframework.health.config import get_health_config
from fastapiframework.health.service_health import ServiceHealth

health_app = FastAPI()


@health_app.get("/")
async def health_handler(response: Response) -> ServiceHealth:
    config = get_health_config()

    service_health = ServiceHealth(service_name=config.service_name)

    for check in config.checks:
        result = check.run()
        service_health.add_result(result)

    response.status_code = 500 if service_health.unhealthy else 200
    return service_health
