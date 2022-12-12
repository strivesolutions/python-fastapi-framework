from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional

from dapr.ext.fastapi import DaprApp
from fastapi import Depends, FastAPI
from fastapi.types import DecoratedCallable

from fastapiframework.health.config import HealthConfig
from fastapiframework.middleware.auth_middleware import check_token
from fastapiframework.middleware.trust_fund_middleware import check_trust_fund_id
from fastapiframework.server.exceptions import PubSubConfigurationException


@dataclass
class Options:
    health: HealthConfig
    pubsub_name: Optional[str] = None
    enable_trust_fund_middleware: bool = False


class Server:
    def __init__(self, options: Options, app: FastAPI):
        self.options = options
        self.app = app
        self.dapr = DaprApp(app)
        self._pubsub_configured = options.pubsub_name is not None

    def add_middleware(self, middleware: type, **options: Any) -> None:
        self.app.add_middleware(middleware, **options)

    def add_route(
        self,
        path: str,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        *,
        anonymous: bool = False,
        check_trust_id: bool = True,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        dependencies = []

        if not anonymous:
            dependencies.append(Depends(check_token))

        if self.options.enable_trust_fund_middleware and check_trust_id:
            dependencies.append(Depends(check_trust_fund_id))

        return self.app.api_route(path, methods=[method], dependencies=dependencies)

    def get(
        self,
        path: str,
        *,
        anonymous: bool = False,
        check_trust_id: bool = True,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.add_route(
            path, "GET", anonymous=anonymous, check_trust_id=check_trust_id
        )

    def post(
        self,
        path: str,
        *,
        anonymous: bool = False,
        check_trust_id: bool = True,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.add_route(
            path, "POST", anonymous=anonymous, check_trust_id=check_trust_id
        )

    def put(
        self,
        path: str,
        *,
        anonymous: bool = False,
        check_trust_id: bool = True,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.add_route(
            path, "PUT", anonymous=anonymous, check_trust_id=check_trust_id
        )

    def delete(
        self,
        path: str,
        *,
        anonymous: bool = False,
        check_trust_id: bool = True,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.add_route(
            path, "DELETE", anonymous=anonymous, check_trust_id=check_trust_id
        )

    def event(self, path: str, topic: str) -> Callable:
        if not self.options.pubsub_name:
            raise PubSubConfigurationException(
                "pubsub_name was not provided on create server options, event handlers may not be used"
            )
        return self.dapr.subscribe(
            pubsub=self.options.pubsub_name,
            topic=topic,
            route=path,
        )
