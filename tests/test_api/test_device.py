from http import HTTPStatus

import pytest
from fastapi import APIRouter
from starlette.testclient import TestClient

from app.db.repository.device import DeviceRepository
from app.db.repository.protection_system import ProtectionSystemRepository

pytestmark = pytest.mark.anyio

TEST_PROTECTION_SYSTEM = {
    "id": 1,
    "name": "Protection system 1",
    "encryption_mode": "AES_CBC",
}

TEST_DEVICE = {
    "protection_system_id": TEST_PROTECTION_SYSTEM["id"],
    "name": "Device 1",
}
TEST_DEVICE_JSON = {"id": 1, **TEST_DEVICE}


@pytest.fixture
def protection_system_repo(db_session):
    return ProtectionSystemRepository(db_session=db_session)


@pytest.fixture
async def protection_system(db_session, protection_system_repo):
    await protection_system_repo.create(**TEST_PROTECTION_SYSTEM)


async def test_create(protection_system, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("create-device")
    response = client.post(url, json=TEST_DEVICE)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == TEST_DEVICE_JSON


@pytest.fixture
def device_repo(db_session):
    return DeviceRepository(db_session=db_session)


@pytest.fixture
async def device(protection_system, db_session, device_repo):
    await device_repo.create(**TEST_DEVICE)


async def test_read(device, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("read-device", id=1)
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == TEST_DEVICE_JSON


async def test_read_not_found(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("read-device", id=1)
    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Device not found"


async def test_list(device, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("list-device")
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [TEST_DEVICE_JSON]


async def test_update(device, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("update-device", id=1)
    response = client.patch(url, json={"name": "Device 2"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {**TEST_DEVICE_JSON, "name": "Device 2"}


async def test_delete(device, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("delete-device", id=1)
    response = client.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_delete_not_found(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("delete-device", id=1)
    response = client.delete(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Device not found"
