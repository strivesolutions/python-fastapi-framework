from __future__ import annotations

import base64
import json
from typing import Type, TypeVar

from pydantic import BaseModel

from fastapiframework.dapr.cloud_event import CloudEvent
from fastapiframework.models.camel_case_model import CamelCaseModel

T = TypeVar("T", bound=CamelCaseModel)


class DataRequestPayload(CamelCaseModel):
    correlation_id: str
    data: dict

    @staticmethod
    def from_event_data(source: dict) -> DataRequestPayload:
        e = CloudEvent(**source)
        correlation_id = e.data["correlationId"]
        data = base64.b64decode(e.data["data"])
        data = json.loads(data)

        return DataRequestPayload(
            correlation_id=correlation_id,
            data=data,
        )

    def unwrap_as(self, cls: Type[T]) -> T:
        assert issubclass(cls, BaseModel), "cls must be of type BaseModel"

        return cls.parse_obj(self.data)


class DataRequestEventData(CamelCaseModel):
    correlation_id: str
    data: str


class DataRequestEvent(CloudEvent):
    data: DataRequestEventData  # type: ignore

    def unwrap_as(self, cls: Type[T]) -> T:
        assert issubclass(cls, BaseModel), "cls must be of type BaseModel"

        data = base64.b64decode(self.data.data)
        data = json.loads(data)

        return cls.parse_obj(data)
