import pytest

from fastapiframework.models.camel_case_model import CamelCaseModel
from fastapiframework.pubsub.publish import DaprPublisher, create_cloud_event
from fastapiframework.server.exceptions import PubSubConfigurationException


def test_dapr_publisher_requires_pubsub_name():
    publisher = DaprPublisher(pubsub_name=None)

    with pytest.raises(PubSubConfigurationException):
        publisher.publish_event("foo", "bar")


def test_create_cloud_event():
    class TestModel(CamelCaseModel):
        foo: str

    data = TestModel(foo="bar")
    create_cloud_event("pytest", data)
