from http import HTTPStatus

import pytest
from fastapi import APIRouter
from starlette.testclient import TestClient

from app.db.repository.content import ContentRepository
from app.db.repository.protection_system import ProtectionSystemRepository

pytestmark = pytest.mark.anyio

TEST_PROTECTION_SYSTEM = {
    "id": 1,
    "name": "Protection system 1",
    "encryption_mode": "AES_CBC",
}

TEST_CONTENT = {
    "protection_system_id": TEST_PROTECTION_SYSTEM["id"],
    "encryption_key": "test_key",
    "payload": "Some test payload",
}

TEST_CONTENT_DB = {
    "id": 1,
    "protection_system_id": TEST_PROTECTION_SYSTEM["id"],
    "encryption_key": b"test_key",
    "encrypted_payload": b"encrypted_payload",
}


@pytest.fixture
def protection_system_repo(db_session):
    return ProtectionSystemRepository(db_session=db_session)


@pytest.fixture
async def protection_system(db_session, protection_system_repo):
    await protection_system_repo.create(**TEST_PROTECTION_SYSTEM)


async def test_create(protection_system, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("create-content")
    response = client.post(url, json=TEST_CONTENT)

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["protection_system_id"] == TEST_CONTENT["protection_system_id"]
    assert response_json["encryption_key"]
    assert response_json["encrypted_payload"]


@pytest.fixture
def content_repo(db_session):
    return ContentRepository(db_session=db_session)


@pytest.fixture
async def content(db_session, protection_system, content_repo):
    await content_repo.create(**TEST_CONTENT_DB)


async def test_read(content, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("read-content", id=1)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["protection_system_id"] == TEST_CONTENT["protection_system_id"]
    assert response_json["encryption_key"]
    assert response_json["encrypted_payload"]


async def test_decrypt(protection_system, client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("create-content")
    response = client.post(url, json=TEST_CONTENT)

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["encrypted_payload"] != TEST_CONTENT["payload"]

    url = router.url_path_for("decrypt-content", id=1)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["payload"] == TEST_CONTENT["payload"]
