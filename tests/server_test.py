from typing import Mapping

import pytest
from cloudevents.pydantic import CloudEvent
from fastapi import Response
from fastapi.testclient import TestClient

from fastapiframework import Options, create_server
from fastapiframework.health.config import HealthConfig
from fastapiframework.health.health_check_result import HealthCheckResult
from fastapiframework.health.health_checker import create_health_check
from fastapiframework.models.camel_case_model import CamelCaseModel
from fastapiframework.pubsub.data_request_payload import DataRequestEvent
from fastapiframework.pubsub.responses import fatal_event_error, retriable_event_error
from fastapiframework.server.exceptions import PubSubConfigurationException


def passing_check(name: str) -> HealthCheckResult:
    return HealthCheckResult.ok(name)


mock_check = create_health_check("test", passing_check)
mock_health_config = HealthConfig("test service", checks=[mock_check])


def test_add_get_route():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.get("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.get("/")

    assert response.status_code == 200


def test_add_post_route():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.post("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.post("/")

    assert response.status_code == 200


def test_add_put_route():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.put("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.put("/")

    assert response.status_code == 200


def test_add_delete_route():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.delete("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.delete("/")

    assert response.status_code == 200


def test_get_route_only_responds_to_get():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.get("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)

    assert 405 == client.post("/").status_code
    assert 405 == client.put("/").status_code
    assert 405 == client.delete("/").status_code


def test_post_route_only_responds_to_post():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.post("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)

    assert 405 == client.get("/").status_code
    assert 405 == client.put("/").status_code
    assert 405 == client.delete("/").status_code


def test_put_route_only_responds_to_put():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.put("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)

    assert 405 == client.get("/").status_code
    assert 405 == client.post("/").status_code
    assert 405 == client.delete("/").status_code


def test_delete_route_only_responds_to_delete():
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.delete("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)

    assert 405 == client.get("/").status_code
    assert 405 == client.post("/").status_code
    assert 405 == client.put("/").status_code


@pytest.mark.parametrize(
    "headers,expected_code",
    [
        pytest.param({"X-Trust-Fund-Id": "999"}, 200, id="Trust 999 returns 200"),
        pytest.param({"X-Trust-Fund-Id": "abc"}, 400, id="Trust abc returns 400"),
        pytest.param(None, 400, id="Trust missing returns 400"),
    ],
)
def test_trust_fund_check(headers: Mapping[str, str], expected_code: int):
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.get("/", anonymous=True)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.get("/", headers=headers)

    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "header,expected_code",
    [
        pytest.param(
            {"Authorization": "Bearer 1234"}, 200, id="Invalid token returns 200"
        ),
        pytest.param(None, 200, id="No token provided returns 200"),
    ],
)
def test_anonymous_route(header, expected_code):
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.get("/", anonymous=True, check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.get("/", headers=header)

    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "header,expected_code",
    [
        pytest.param(
            {"Authorization": "Bearer 1"}, 401, id="Invalid token returns 401"
        ),
        pytest.param({"Authorization": "Bearer"}, 401, id="Invalid header returns 401"),
        pytest.param(None, 401, id="No token returns 401"),
        pytest.param(
            {
                # this is a valid JWT from JWT.io, not from our service. It's just testing the token parsing. # noqa
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa
            },
            200,
            id="Valid token returns 200",
        ),
    ],
)
def test_secure_route(header, expected_code):
    server = create_server(
        options=Options(health=mock_health_config, enable_trust_fund_middleware=True)
    )

    @server.get("/", check_trust_id=False)
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.get("/", headers=header)

    assert response.status_code == expected_code


def test_add_event_handler():
    server = create_server(
        options=Options(
            pubsub_name="pubsub",
            health=mock_health_config,
            enable_trust_fund_middleware=True,
        )
    )

    @server.event("/", "test_topic")
    def handler():
        return "ok"

    client = TestClient(server.app)
    response = client.post("/")

    assert response.status_code == 200

    response = client.get("/dapr/subscribe")
    assert response.status_code == 200


def test_event_route_handling():
    server = create_server(
        options=Options(
            pubsub_name="pubsub",
            health=mock_health_config,
            enable_trust_fund_middleware=True,
        )
    )

    @server.event("/", "test_topic")
    def handler(event: CloudEvent):
        return event.data.get("foo")

    client = TestClient(server.app)
    body = """
{
    "specversion" : "1.0",
    "type" : "example.com.cloud.event",
    "source" : "https://example.com/cloudevents/pull",
    "subject" : "123",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "data" : { "foo": "bar" }
}
"""
    response = client.post("/", content=body)

    assert response.status_code == 200
    assert response.text == '"bar"'


def test_event_configuration_error_when_pubsub_name_not_set():
    server = create_server(
        options=Options(
            health=mock_health_config,
            enable_trust_fund_middleware=True,
        )
    )

    with pytest.raises(PubSubConfigurationException):

        @server.event("/", "test_topic")
        def handler(event: CloudEvent):
            return event.data.get("foo")


def test_event_handling_data_request_payload():
    server = create_server(
        options=Options(
            pubsub_name="pubsub",
            health=mock_health_config,
            enable_trust_fund_middleware=True,
        )
    )

    class DataModel(CamelCaseModel):
        foo: str

    @server.event("/", "test_topic")
    def handler(event: DataRequestEvent):
        payload = event.unwrap_as(DataModel)
        return payload.foo

    client = TestClient(server.app)
    body = """
{
    "specversion" : "1.0",
    "type" : "example.com.cloud.event",
    "source" : "https://example.com/cloudevents/pull",
    "subject" : "123",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "data" : {"correlationId": "96ab7b8e-88b6-4d8a-86d4-0ab120ec6444", "data": "eyJmb28iOiJiYXIiLCJiYXoiOjk5fQ=="}
}
"""  # noqa
    response = client.post("/", content=body)

    assert response.status_code == 200
    assert response.text == '"bar"'


def test_event_handler_response_retry():
    server = create_server(
        options=Options(
            pubsub_name="pubsub",
            health=mock_health_config,
            enable_trust_fund_middleware=True,
        )
    )

    @server.event("/", "test_topic")
    def handler(response: Response):
        return retriable_event_error(response)

    client = TestClient(server.app)  # noqa
    response = client.post("/", content=None)

    assert response.status_code == 500


def test_event_handler_response_fatal():
    server = create_server(
        options=Options(
            pubsub_name="pubsub",
            health=mock_health_config,
            enable_trust_fund_middleware=True,
        )
    )

    @server.event("/", "test_topic")
    def handler(response: Response):
        return fatal_event_error(response)

    client = TestClient(server.app)  # noqa
    response = client.post("/", content=None)

    assert response.status_code == 404
