from typing import Mapping

import pytest
from fastapi.testclient import TestClient
from health.config import HealthConfig
from health.health_check_result import HealthCheckResult
from health.health_checker import create_health_check

from fastapiframework import Options, create_server


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
                # this is a valid JWT from JWT.io, not from our service. It's just testing the token parsing.
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
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
