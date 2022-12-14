from decimal import Decimal
from typing import Any

from humps import camelize
from pydantic import BaseModel


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        response_model_by_alias = True
        json_encoders = {Decimal: str}

    def json(self, *args: Any, **kwargs: Any) -> str:
        kwargs["by_alias"] = True
        kwargs["exclude_none"] = True
        return super().json(*args, **kwargs)
