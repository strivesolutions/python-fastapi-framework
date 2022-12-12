from fastapiframework.models.camel_case_model import CamelCaseModel
from fastapiframework.pubsub.data_request_payload import DataRequestPayload
from fastapiframework.server.exceptions import PubSubConfigurationException


class Publisher:
    def publish_event(self, topic: str, event: str | CamelCaseModel) -> None:
        raise NotImplementedError()

    def publish_data_payload(
        self,
        topic: str,
        correlation_id: str,
        event_data: CamelCaseModel,
    ) -> None:
        raise NotImplementedError()


class DaprPublisher(Publisher):
    def __init__(self, pubsub_name: str):
        self.pubsub_name = pubsub_name

    def publish_event(self, topic: str, event: str | CamelCaseModel) -> None:
        if not self.pubsub_name:
            raise PubSubConfigurationException(
                "pubsub_name is not initialized, unable to publish event"
            )

        if isinstance(event, CamelCaseModel):
            event = event.json()

        from dapr.clients import DaprClient

        with DaprClient() as client:
            client.publish_event(self.pubsub_name, topic, event)

    def publish_data_payload(
        self,
        topic: str,
        correlation_id: str,
        event_data: CamelCaseModel,
    ) -> None:
        event = DataRequestPayload(
            correlation_id=correlation_id,
            data=event_data,
        )

        return self.publish_event(topic, event)
