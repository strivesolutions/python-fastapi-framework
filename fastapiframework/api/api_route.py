from dataclasses import dataclass
from typing import Any, Coroutine

from fastapiframework.api.method_type import MethodType


@dataclass
class ApiRoute:
    method: MethodType
    path: str
    handler: Coroutine[Any, Any, Any]
    anonymous: bool = False
    skip_trust_check: bool = False
