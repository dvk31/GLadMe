import pytest

from common.services import (
    BaseGateway,
    ChatGateway,
    create_provider,
    get_provider,
    register_provider,
)
from common.services.base import ProviderNotRegistered


@register_provider("dummy-test-provider")
class DummyGateway(BaseGateway):
    def __init__(self, *, configured: bool = True) -> None:
        self.configured = configured

    def chat(self, prompt: str, **kwargs) -> str:
        return prompt.upper()

    def chat_messages(self, messages, **kwargs) -> str:
        return messages[-1]["content"]

    def is_configured(self) -> bool:
        return self.configured


def test_registry_returns_registered_provider() -> None:
    provider_class = get_provider("dummy-test-provider")
    provider = create_provider("dummy-test-provider")

    assert provider_class is DummyGateway
    assert isinstance(provider, DummyGateway)
    assert isinstance(provider, ChatGateway)
    assert provider.chat("hello") == "HELLO"


def test_registry_raises_for_missing_provider() -> None:
    with pytest.raises(ProviderNotRegistered):
        get_provider("missing-provider")
