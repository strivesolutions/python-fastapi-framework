from typing import Any, Dict, Optional

from pydantic import BaseModel


class CloudEvent(BaseModel):
    id: str
    source: str
    specversion: str
    type: str
    data: Dict[str, Any]
    datacontenttype: Optional[str]
    pubsubname: Optional[str]
    topic: Optional[str]
    traceid: Optional[str]
    traceparent: Optional[str]
    tracestate: Optional[str]