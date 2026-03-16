"""Reusable model mixins for the template."""

from django.db import models
from django.utils import timezone


class SoftDeleteMixin(models.Model):
    """Opt-in soft delete behavior with explicit restore support."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self, user=None) -> None:
        """Mark the record as deleted without removing the row."""
        self.deleted_at = timezone.now()
        update_fields = ["deleted_at"]

        if hasattr(self, "updated_by"):
            self.updated_by = user
            update_fields.append("updated_by")

        if hasattr(self, "updated_at"):
            self.updated_at = timezone.now()
            update_fields.append("updated_at")

        self.save(update_fields=update_fields)

    def restore(self, user=None) -> None:
        """Restore a previously soft-deleted record."""
        self.deleted_at = None
        update_fields = ["deleted_at"]

        if hasattr(self, "updated_by"):
            self.updated_by = user
            update_fields.append("updated_by")

        if hasattr(self, "updated_at"):
            self.updated_at = timezone.now()
            update_fields.append("updated_at")

        self.save(update_fields=update_fields)
