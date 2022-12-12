# from fastapiframework.dapr.cloud_event import CloudEvent
from typing import Optional

from cloudevents.pydantic import CloudEvent

from fastapiframework.models.camel_case_model import CamelCaseModel
from fastapiframework.pubsub.data_request_payload import DataRequestPayload
from fastapiframework.server.exceptions import PubSubConfigurationException


class Publisher:
    def publish_event(self, topic: str, event: CamelCaseModel) -> None:
        raise NotImplementedError()

    def publish_data_payload(
        self,
        topic: str,
        correlation_id: str,
        event_data: CamelCaseModel,
    ) -> None:
        raise NotImplementedError()


class DaprPublisher(Publisher):
    def __init__(self, pubsub_name: str, service_name: str):
        self.pubsub_name = pubsub_name
        self.service_name = service_name

    def publish_event(
        self,
        topic: str,
        data: CamelCaseModel,
        data_type: Optional[str] = None,
    ) -> None:
        if not self.pubsub_name:
            raise PubSubConfigurationException(
                "pubsub_name is not initialized, unable to publish event"
            )

        data_type = data_type or type(data).__name__
        event = create_cloud_event(self.service_name, data_type, data)

        from dapr.clients import DaprClient

        with DaprClient() as client:
            client.publish_event(
                self.pubsub_name,
                topic,
                event,
            )

    def publish_data_payload(
        self,
        topic: str,
        correlation_id: str,
        data: CamelCaseModel,
    ) -> None:
        payload = DataRequestPayload(
            correlation_id=correlation_id,
            data=data,
        )

        return self.publish_event(topic, payload, type(data).__name__)


def create_cloud_event(source: str, data_type: str, data: CamelCaseModel) -> CloudEvent:
    return CloudEvent(
        {
            "datacontenttype": "application/json",
            "type": data_type,
            "source": source,
        },
        data.json(),
    )
