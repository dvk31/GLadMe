import uuid

import pytest
from django.contrib.auth import get_user_model

from web.models import Project


@pytest.mark.django_db
def test_project_inherits_base_model_fields() -> None:
    user = get_user_model().objects.create_user(
        username="owner",
        email="owner@example.com",
        password="password123",
    )

    project = Project.objects.create(
        name="Starter Project",
        description="Uses the shared base model.",
        created_by=user,
        updated_by=user,
    )

    assert isinstance(project.id, uuid.UUID)
    assert project.created_at is not None
    assert project.updated_at is not None
    assert project.created_by == user
    assert project.updated_by == user


@pytest.mark.django_db
def test_soft_delete_and_restore_update_model_state() -> None:
    user = get_user_model().objects.create_user(
        username="editor",
        email="editor@example.com",
        password="password123",
    )
    project = Project.objects.create(name="Soft Delete Demo")

    project.soft_delete(user=user)
    project.refresh_from_db()

    assert project.is_deleted is True
    assert project.deleted_at is not None
    assert project.updated_by == user

    project.restore(user=user)
    project.refresh_from_db()

    assert project.is_deleted is False
    assert project.deleted_at is None
