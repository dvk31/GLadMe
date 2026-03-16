"""Minimal Inertia views for the template."""

from django.conf import settings
from inertia import render

from ai.openrouter_gateway import OpenRouterGateway

from .models import Project


def home(request):
    """Render the starter page that shows the template seams."""
    gateway = OpenRouterGateway()
    projects = [
        {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat(),
        }
        for project in Project.objects.filter(deleted_at__isnull=True)[:5]
    ]

    return render(
        request,
        "Home/Index",
        {
            "siteName": settings.SITE_NAME,
            "siteUrl": settings.SITE_URL,
            "openrouterConfigured": gateway.is_configured(),
            "defaultModel": settings.OPENROUTER_DEFAULT_MODEL,
            "projects": projects,
        },
        template_data={"meta_title": settings.SITE_NAME},
    )
