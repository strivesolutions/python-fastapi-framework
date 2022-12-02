from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Rule:
    match: str
    path: str


@dataclass
class Route:
    rules: List[Rule]


@dataclass
class Subscription:
    pubsubname: str
    topic: str
    metadata: Dict[str, str]
    routes: List[Route]
