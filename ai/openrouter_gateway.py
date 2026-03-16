"""Minimal OpenRouter gateway for commands and app services."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import httpx
from django.conf import settings

from common.services.base import BaseGateway, ConfigurationError, ServiceError
from common.services.contracts import ChatMessage
from common.services.registry import register_provider

logger = logging.getLogger(__name__)


@dataclass
class GatewayUsage:
    """Small usage snapshot copied from the OpenRouter response."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class OpenRouterError(ServiceError):
    """Raised when the OpenRouter API returns an error."""


@register_provider("openrouter")
class OpenRouterGateway(BaseGateway):
    """Small sync gateway adapted from the existing command client pattern."""

    base_url = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        site_url: str | None = None,
        site_name: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.OPENROUTER_API_KEY
        self.site_url = site_url if site_url is not None else settings.SITE_URL
        self.site_name = site_name if site_name is not None else settings.SITE_NAME
        self.default_model = settings.OPENROUTER_DEFAULT_MODEL
        self.fallback_model = settings.OPENROUTER_FALLBACK_MODEL
        self.default_temperature = settings.OPENROUTER_DEFAULT_TEMPERATURE
        self.timeout = timeout
        self.last_usage: GatewayUsage | None = None

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
            "Content-Type": "application/json",
        }

    def chat(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4000,
    ) -> str:
        messages: list[ChatMessage] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return self.chat_messages(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def chat_messages(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4000,
    ) -> str:
        if not self.is_configured():
            raise ConfigurationError("OPENROUTER_API_KEY is not configured.")

        payload = {
            "model": model or self.default_model or self.fallback_model,
            "messages": list(messages),
            "temperature": (
                self.default_temperature if temperature is None else temperature
            ),
            "max_tokens": max_tokens,
        }

        data = self._post_chat(payload)
        content = self._extract_content(data)
        self.last_usage = self._extract_usage(data)
        return content

    def _post_chat(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise OpenRouterError(f"OpenRouter request failed: {exc}") from exc

        if response.status_code == 401:
            raise OpenRouterError("Invalid OpenRouter API key.")
        if response.status_code == 429:
            raise OpenRouterError("OpenRouter rate limit exceeded.")
        if response.status_code >= 400:
            raise OpenRouterError(self._build_error_message(response))

        return response.json()

    def _extract_content(self, data: dict[str, Any]) -> str:
        message = data.get("choices", [{}])[0].get("message", {})
        content = message.get("content", "")

        if isinstance(content, str) and content.strip():
            return content

        if isinstance(content, list):
            text_parts = [
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            joined = "\n".join(part for part in text_parts if part).strip()
            if joined:
                return joined

        raise OpenRouterError("OpenRouter returned an empty response.")

    def _extract_usage(self, data: dict[str, Any]) -> GatewayUsage:
        usage = data.get("usage", {})
        return GatewayUsage(
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
        )

    def _build_error_message(self, response: httpx.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return f"OpenRouter error ({response.status_code}): {response.text[:200]}"

        error = payload.get("error", {})
        message = error.get("message") or payload.get("detail") or "Unknown OpenRouter error."
        return f"OpenRouter error ({response.status_code}): {message}"
