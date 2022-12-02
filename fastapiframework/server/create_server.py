from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from starlette.middleware import Middleware

from fastapiframework.health.handler import add_health_handler
from fastapiframework.middleware.logging_middleware import LoggingMiddleware

from .server import Options, Server


def create_server(options: Options, app: Optional[FastAPI] = None) -> Server:
    assert options, "Options are required"
    assert options.health.checks, "You must provide at least one health check"

    app = app or create_app()
    server = Server(options, app)

    add_health_handler(app, options.health)

    return server


def create_app() -> FastAPI:
    app = FastAPI(
        middleware=[
            Middleware(LoggingMiddleware),
        ],
    )
    app.router.redirect_slashes = False
    return app
