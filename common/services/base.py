"""Base classes and exceptions for small service gateways."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from .contracts import ChatMessage


class ServiceError(Exception):
    """Base exception for service-layer failures."""


class ConfigurationError(ServiceError):
    """Raised when a required integration setting is missing."""


class ProviderNotRegistered(ServiceError):
    """Raised when a requested provider is not present in the registry."""


class BaseGateway(ABC):
    """Small ABC used by provider implementations."""

    provider_name = "base"

    @abstractmethod
    def chat(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4000,
    ) -> str:
        """Generate a response from a single prompt."""

    @abstractmethod
    def chat_messages(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4000,
    ) -> str:
        """Generate a response from a chat history."""

    @abstractmethod
    def is_configured(self) -> bool:
        """Return whether the gateway has enough configuration to run."""
