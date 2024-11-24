from http import HTTPStatus

import pytest
from fastapi import APIRouter
from starlette.testclient import TestClient

from app.db.repository.protection_system import ProtectionSystemRepository

pytestmark = pytest.mark.anyio

TEST_PROTECTION_SYSTEM = {"name": "Test-1", "encryption_mode": "AES_CBC"}

TEST_CREATE_PROTECTION_SYSTEM = {"id": 2, "name": "Test-2", "encryption_mode": "AES_ECB"}
TEST_CREATE_PROTECTION_SYSTEM_2 = {"id": 3, "name": "Test-3", "encryption_mode": "AES_ECB"}

UNSUPPORTED_ENCRYPTION_MODE = {"name": "Test-1", "encryption_mode": "TEST"}


@pytest.fixture
def repo(db_session):
    return ProtectionSystemRepository(db_session=db_session)


@pytest.fixture
async def protection_system(db_session, repo):
    await repo.create(**TEST_CREATE_PROTECTION_SYSTEM)


@pytest.fixture
async def protection_systems(db_session, repo):
    await repo.create(**TEST_CREATE_PROTECTION_SYSTEM)
    await repo.create(**TEST_CREATE_PROTECTION_SYSTEM_2)


async def test_create(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("create-protection-system")
    response = client.post(url, json=TEST_PROTECTION_SYSTEM)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, **TEST_PROTECTION_SYSTEM}


async def test_create_unprocessable_entity(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("create-protection-system")
    response = client.post(url, json=UNSUPPORTED_ENCRYPTION_MODE)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Input should be 'AES_ECB' or 'AES_CBC'"


async def test_read(protection_system, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("read-protection-system", id=TEST_CREATE_PROTECTION_SYSTEM["id"])
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == TEST_CREATE_PROTECTION_SYSTEM


async def test_read_not_found(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("read-protection-system", id=1)
    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Protection system not found"


async def test_list(protection_systems, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("list-protection-systems")
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [TEST_CREATE_PROTECTION_SYSTEM, TEST_CREATE_PROTECTION_SYSTEM_2]


async def test_update(protection_system, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("update-protection-system", id=TEST_CREATE_PROTECTION_SYSTEM["id"])
    response = client.patch(url, json={"name": "Test-2-Updated"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {**TEST_CREATE_PROTECTION_SYSTEM, "name": "Test-2-Updated"}


async def test_delete(protection_system, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("delete-protection-system", id=TEST_CREATE_PROTECTION_SYSTEM["id"])
    response = client.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
