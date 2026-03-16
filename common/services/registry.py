"""Simple provider registry for gateway implementations."""

from typing import TypeVar

from .base import BaseGateway, ProviderNotRegistered

GatewayType = TypeVar("GatewayType", bound=BaseGateway)

_PROVIDER_REGISTRY: dict[str, type[BaseGateway]] = {}


def register_provider(name: str):
    """Register a provider class under a stable name."""

    def decorator(cls: type[GatewayType]) -> type[GatewayType]:
        cls.provider_name = name
        _PROVIDER_REGISTRY[name] = cls
        return cls

    return decorator


def get_provider(name: str) -> type[BaseGateway]:
    """Return the provider class registered for a name."""
    try:
        return _PROVIDER_REGISTRY[name]
    except KeyError as exc:
        raise ProviderNotRegistered(f"No provider registered for '{name}'.") from exc


def create_provider(name: str, *args, **kwargs) -> BaseGateway:
    """Instantiate a provider by name."""
    provider_cls = get_provider(name)
    return provider_cls(*args, **kwargs)


def get_registered_providers() -> list[str]:
    """Return provider names in stable order."""
    return sorted(_PROVIDER_REGISTRY)
