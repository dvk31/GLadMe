"""Base model building blocks for the template."""

from uuid import uuid4

from django.conf import settings
from django.db import models


class UUIDPrimaryKeyModel(models.Model):
    """Abstract base with a UUID primary key."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Abstract base with creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditFieldsMixin(models.Model):
    """Optional audit fields that follow the active auth user model."""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True


class BaseModel(UUIDPrimaryKeyModel, TimeStampedModel, AuditFieldsMixin):
    """
    Neutral default base model for domain records.

    The template keeps this intentionally small so teams can extend it
    without inheriting tenant, ACL, or JSON blob conventions.
    """

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"
