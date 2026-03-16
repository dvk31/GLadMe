"""Example models that demonstrate the shared base classes."""

from django.db import models

from common.models import BaseModel, SoftDeleteMixin


class Project(SoftDeleteMixin, BaseModel):
    """Small example model that teams can replace with their own domain objects."""

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name
