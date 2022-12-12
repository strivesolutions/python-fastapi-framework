from __future__ import annotations

import base64
import json
from typing import Type, TypeVar

from cloudevents.pydantic import CloudEvent
from pydantic import BaseModel

from fastapiframework.models.camel_case_model import CamelCaseModel

T = TypeVar("T", bound=CamelCaseModel)


class DataRequestPayload(CamelCaseModel):
    correlation_id: str
    data: dict


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
