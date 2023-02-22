from datetime import datetime
from decimal import Decimal
from typing import Any

from humps import camelize
from pydantic import BaseModel


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        response_model_by_alias = True
        json_encoders = {
            Decimal: str,
            datetime: convert_datetime_to_iso_8601_with_z_suffix,
        }

    def json(self, *args: Any, **kwargs: Any) -> str:
        kwargs["by_alias"] = True
        kwargs["exclude_none"] = True
        return super().json(*args, **kwargs)
