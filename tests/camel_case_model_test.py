import json
from datetime import datetime, timezone
from typing import Optional

from fastapiframework.models.camel_case_model import CamelCaseModel


def test_serializes_to_camel_case():
    class TestModel(CamelCaseModel):
        foo_bar: str = "baz"

    target = TestModel()
    j = target.json()
    d = json.loads(j)

    assert "fooBar" in d


def test_can_initialize_field_with_camel_case():
    class TestModel(CamelCaseModel):
        foo_bar: str

    target = TestModel.parse_obj({"fooBar": "baz"})

    expected = "baz"
    assert target.foo_bar == expected


def test_can_initialize_field_with_field_name():
    class TestModel(CamelCaseModel):
        foo_bar: str

    target = TestModel.parse_obj({"foo_bar": "baz"})

    expected = "baz"
    assert target.foo_bar == expected


def test_json_does_not_include_null_values():
    class TestModel(CamelCaseModel):
        foo_bar: Optional[str] = None

    target = TestModel()
    j = target.json()
    d = json.loads(j)

    assert "fooBar" not in d


def test_utc_serializes_with_z():
    class TestModel(CamelCaseModel):
        date: datetime

    target = TestModel(
        date=datetime(2023, 1, 1).replace(tzinfo=timezone.utc),
    )

    j = target.json()
    d: dict = json.loads(j)

    expected = "2023-01-01T00:00:00Z"
    actual = d.get("date")

    assert expected == actual
