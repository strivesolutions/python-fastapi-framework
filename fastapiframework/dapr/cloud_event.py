from typing import Optional

from pydantic import BaseModel


class CloudEvent(BaseModel):
    id: str
    source: str
    specversion: str
    type: str
    data: dict
    datacontenttype: Optional[str]
    pubsubname: Optional[str]
    topic: Optional[str]
    traceid: Optional[str]
    traceparent: Optional[str]
    tracestate: Optional[str]
