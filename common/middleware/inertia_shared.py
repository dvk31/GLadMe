"""Minimal Inertia shared props for auth and flash messages."""

from typing import Any

from django.contrib import messages
from inertia import share


def inertia_share_data(request) -> dict[str, Any]:
    shared: dict[str, Any] = {
        "auth": {"user": None},
        "flash": {
            "success": None,
            "error": None,
            "warning": None,
            "info": None,
        },
    }

    if request.user.is_authenticated:
        shared["auth"]["user"] = {
            "id": str(request.user.pk),
            "email": request.user.email,
            "display_name": request.user.get_full_name() or request.user.get_username(),
        }

    for message in messages.get_messages(request):
        if message.level_tag in shared["flash"]:
            shared["flash"][message.level_tag] = str(message)

    return shared


class InertiaShareMiddleware:
    """Attach the shared props payload to each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        share(request, **inertia_share_data(request))
        return self.get_response(request)
