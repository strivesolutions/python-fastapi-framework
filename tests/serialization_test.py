import json
from decimal import Decimal

from fastapiframework.models.camel_case_model import CamelCaseModel


def test_decimals_serialize_as_strings():
    class Model(CamelCaseModel):
        value: Decimal

    j = Model(value=1.5).json()
    d = json.loads(j)

    assert d["value"] == "1.5"
