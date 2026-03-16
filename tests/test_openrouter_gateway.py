import pytest

from ai.openrouter_gateway import OpenRouterError, OpenRouterGateway
from common.services.base import ConfigurationError


class DummyResponse:
    def __init__(self, status_code: int, payload: dict, text: str = "") -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self) -> dict:
        return self._payload


class DummyClient:
    def __init__(self, response: DummyResponse) -> None:
        self.response = response
        self.last_request: dict | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def post(self, url: str, *, headers: dict, json: dict):
        self.last_request = {
            "url": url,
            "headers": headers,
            "json": json,
        }
        return self.response


def test_gateway_requires_api_key(settings) -> None:
    settings.OPENROUTER_API_KEY = ""
    gateway = OpenRouterGateway()

    assert gateway.is_configured() is False

    with pytest.raises(ConfigurationError):
        gateway.chat("hello")


def test_gateway_returns_response_text(settings, monkeypatch) -> None:
    settings.OPENROUTER_API_KEY = "test-key"
    client = DummyClient(
        DummyResponse(
            200,
            {
                "choices": [{"message": {"content": "Hello from OpenRouter"}}],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 12,
                    "total_tokens": 22,
                },
            },
        )
    )
    monkeypatch.setattr("ai.openrouter_gateway.httpx.Client", lambda *args, **kwargs: client)

    gateway = OpenRouterGateway()
    response = gateway.chat("hello")

    assert response == "Hello from OpenRouter"
    assert gateway.last_usage is not None
    assert gateway.last_usage.total_tokens == 22
    assert client.last_request is not None
    assert client.last_request["headers"]["Authorization"] == "Bearer test-key"
    assert client.last_request["json"]["messages"] == [{"role": "user", "content": "hello"}]


def test_gateway_raises_for_api_error(settings, monkeypatch) -> None:
    settings.OPENROUTER_API_KEY = "bad-key"
    client = DummyClient(
        DummyResponse(
            401,
            {"error": {"message": "invalid key"}},
        )
    )
    monkeypatch.setattr("ai.openrouter_gateway.httpx.Client", lambda *args, **kwargs: client)

    gateway = OpenRouterGateway()

    with pytest.raises(OpenRouterError, match="Invalid OpenRouter API key"):
        gateway.chat("hello")
