"""Lightweight service contracts used by gateway implementations."""

from collections.abc import Sequence
from typing import Literal, Protocol, TypedDict, runtime_checkable


class ChatMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


@runtime_checkable
class ChatGateway(Protocol):
    """Minimal chat gateway contract for provider implementations."""

    def chat(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4000,
    ) -> str: ...

    def chat_messages(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4000,
    ) -> str: ...

    def is_configured(self) -> bool: ...
