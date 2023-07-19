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
    data: str

    @staticmethod
    def create(correlation_id: str, data: CamelCaseModel) -> DataRequestPayload:
        return DataRequestPayload(
            correlation_id=correlation_id,
            data=str(base64.b64encode(data.json().encode("utf-8"))),
        )


class DataRequestEvent(CloudEvent):
    data: DataRequestPayload

    def unwrap_as(self, cls: Type[T]) -> T:
        assert issubclass(cls, BaseModel), "cls must be of type BaseModel"

        data = base64.b64decode(self.data.data)
        data = json.loads(data)

        return cls.model_validate(data)
