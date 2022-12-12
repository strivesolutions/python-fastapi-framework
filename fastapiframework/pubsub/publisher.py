# from fastapiframework.dapr.cloud_event import CloudEvent


from fastapiframework.models.camel_case_model import CamelCaseModel


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
