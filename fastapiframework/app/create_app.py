from dataclasses import dataclass
from typing import List, Optional

from fastapi import FastAPI
from starlette.middleware import Middleware

from fastapiframework.health.config import HealthConfig, set_health_config
from fastapiframework.health.handler import health_app


@dataclass
class Options:
    health: HealthConfig


def create_app(
    options: Options,
    middleware: Optional[List[type]] = None,
) -> FastAPI:
    assert options, "Options are required"
    assert options.health.checks, "You must provide at least one health check"

    app = FastAPI(
        middleware=[Middleware(m) for m in middleware] if middleware else None,
    )

    set_health_config(options.health)

    app.mount("/healthz", health_app)

    return app
