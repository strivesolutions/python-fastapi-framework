from fastapi import Depends, FastAPI, Response
from strivehealthchecks import run_checks

from .config import HealthConfig, get_health_config, set_health_config


def add_health_handler(app: FastAPI, config: HealthConfig) -> None:
    set_health_config(config)
    app.add_api_route("/healthz", health_handler)  # type:ignore


async def health_handler(
    response: Response,
    config: HealthConfig = Depends(get_health_config),
) -> dict:
    result = await run_checks(config.service_name, config.checks)

    response.status_code = 200 if result.healthy else 500
    return result.to_dict()
