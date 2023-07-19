from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from strivehealthchecks import HealthChecker

config: Optional[HealthConfig] = None


def set_health_config(c: HealthConfig) -> None:
    global config
    config = c


def get_health_config() -> HealthConfig:
    assert config is not None, "Health config has not been initialized"
    return config


@dataclass
class HealthConfig:
    service_name: str
    checks: List[HealthChecker]
