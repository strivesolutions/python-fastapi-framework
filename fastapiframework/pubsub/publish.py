# from fastapiframework.dapr.cloud_event import CloudEvent
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

    def publish_event(self, topic: str, data: CamelCaseModel) -> None:
        if not self.pubsub_name:
            raise PubSubConfigurationException(
                "pubsub_name is not initialized, unable to publish event"
            )

        event = create_cloud_event(self.service_name, data)

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

        return self.publish_event(topic, payload)


def create_cloud_event(source: str, data: CamelCaseModel) -> CloudEvent:
    CloudEvent(
        {
            "datacontenttype": "application/json",
            "type": type(data).__name__,
            "source": source,
        },
        data,
    )
