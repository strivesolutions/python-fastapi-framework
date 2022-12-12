# from __future__ import annotations

# import uuid
# from typing import Optional

# from pydantic import BaseModel


# class CloudEvent(BaseModel):
#     id: str
#     source: str
#     specversion: str
#     type: str
#     data: dict | str
#     datacontenttype: Optional[str]
#     pubsubname: Optional[str]
#     topic: Optional[str]
#     traceid: Optional[str]
#     traceparent: Optional[str]
#     tracestate: Optional[str]

#     @staticmethod
#     def new_json(
#         *,
#         data: BaseModel,
#         source: str = "fastapiframework",
#         pubsubname: Optional[str] = None,
#         topic: Optional[str] = None,
#         traceid: Optional[str] = None,
#         traceparent: Optional[str] = None,
#         tracestate: Optional[str] = None,
#     ) -> CloudEvent:
#         return CloudEvent(
#             id=uuid.uuid4().hex,
#             source=source,
#             data=data.json(),
#             topic=topic,
#             datacontenttype="application/json",
#             pubsubname=pubsubname,
#             traceid=traceid,
#             traceparent=traceparent,
#             tracestate=tracestate,
#         )
