from http import HTTPStatus

from fastapi import APIRouter
from starlette.testclient import TestClient


def test_health(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("health")
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.text == "OK"
