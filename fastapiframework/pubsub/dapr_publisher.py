from fastapiframework.models.camel_case_model import CamelCaseModel
from fastapiframework.pubsub.data_request_payload import DataRequestPayload
from fastapiframework.server.exceptions import PubSubConfigurationException

from .publisher import Publisher


class DaprPublisher(Publisher):
    def __init__(self, pubsub_name: str, service_name: str):
        self.pubsub_name = pubsub_name
        self.service_name = service_name

    def publish_event(
        self,
        topic: str,
        event: CamelCaseModel,
    ) -> None:
        if not self.pubsub_name:
            raise PubSubConfigurationException(
                "pubsub_name is not initialized, unable to publish event"
            )

        from dapr.clients import DaprClient

        with DaprClient() as client:
            client.publish_event(
                self.pubsub_name,
                topic,
                event.json(),
                data_content_type="application/json",
            )

    def publish_data_payload(
        self,
        topic: str,
        correlation_id: str,
        data: CamelCaseModel,
    ) -> None:
        payload = DataRequestPayload.create(correlation_id, data)

        return self.publish_event(topic, payload)
