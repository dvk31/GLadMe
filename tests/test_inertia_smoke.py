import pytest


@pytest.mark.django_db
def test_home_page_renders(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert b"data-page=" in response.content
    assert b"Home/Index" in response.content


@pytest.mark.django_db
def test_home_page_handles_inertia_request(client) -> None:
    response = client.get("/", HTTP_X_INERTIA="true")

    assert response.status_code == 200
    if response.get("X-Inertia"):
        assert response["X-Inertia"] == "true"
