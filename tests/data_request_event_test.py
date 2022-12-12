import json

from fastapiframework.models.camel_case_model import CamelCaseModel
from fastapiframework.pubsub.data_request_payload import DataRequestEvent


def test_data_request_payload_from_event_data():
    event_body = json.loads(
        '{"data": {"correlationId": "96ab7b8e-88b6-4d8a-86d4-0ab120ec6444", "data": "eyJpZCI6Ijk2YWI3YjhlLTg4YjYtNGQ4YS04NmQ0LTBhYjEyMGVjNjQ0NCIsInN0YXR1cyI6ImZldGNoaW5nX2RhdGEiLCJmYWlsdXJlUmVhc29uIjoiIiwidHJ1c3RGdW5kSWQiOjQ2MCwiY29udGFjdFJlY29yZElkIjoxMjI0OTYsInJldGlyZW1lbnRBZ2UiOjU1LCJyZXRpcmVtZW50RGF0ZSI6bnVsbCwid2l0aFNwb3VzZSI6ZmFsc2UsInNwb3VzZURhdGVPZkJpcnRoIjpudWxsLCJwZW5zaW9uRGF0YSI6bnVsbCwiY3BwTGltaXQiOm51bGwsIm9hc0xpbWl0IjpudWxsLCJyZXN1bHQiOm51bGx9"}, "datacontenttype": "application/json", "id": "8a1cb966-599c-4a65-a0cd-4743bf856e94", "pubsubname": "rabbitmq-pubsub", "source": "pension-estimate", "specversion": "1.0", "time": "2022-12-12T16:47:28Z", "topic": "estimate_needs_data", "traceid": "00-00000000000000000000000000000000-0000000000000000-00", "traceparent": "00-00000000000000000000000000000000-0000000000000000-00", "tracestate": "", "type": "com.dapr.event.sent"}'
    )  # noqa
    DataRequestEvent(**event_body)


def test_data_request_payload_as():
    event_body = json.loads(
        '{"data": {"correlationId": "96ab7b8e-88b6-4d8a-86d4-0ab120ec6444", "data": "eyJmb28iOiJiYXIiLCJiYXoiOjk5fQ=="}, "datacontenttype": "application/json", "id": "8a1cb966-599c-4a65-a0cd-4743bf856e94", "pubsubname": "rabbitmq-pubsub", "source": "pension-estimate", "specversion": "1.0", "time": "2022-12-12T16:47:28Z", "topic": "estimate_needs_data", "traceid": "00-00000000000000000000000000000000-0000000000000000-00", "traceparent": "00-00000000000000000000000000000000-0000000000000000-00", "tracestate": "", "type": "com.dapr.event.sent"}'
    )  # noqa
    event = DataRequestEvent(**event_body)

    class TestData(CamelCaseModel):
        foo: str
        baz: int

    data = event.unwrap_as(TestData)
    assert data.foo == "bar"
