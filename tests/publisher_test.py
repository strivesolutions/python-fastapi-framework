import pytest

from fastapiframework.pubsub import DaprPublisher
from fastapiframework.server.exceptions import PubSubConfigurationException


def test_dapr_publisher_requires_pubsub_name():
    publisher = DaprPublisher(pubsub_name=None, service_name="pytest")

    with pytest.raises(PubSubConfigurationException):
        publisher.publish_event("foo", "bar")
