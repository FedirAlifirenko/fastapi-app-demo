from http import HTTPStatus

import pytest
from fastapi import APIRouter
from starlette.testclient import TestClient

pytestmark = pytest.mark.anyio

TEST_PROTECTION_SYSTEM = {
    "name": "Protection system 1",
    "encryption_mode": "AES_CBC",
}
TEST_DEVICE = {
    "name": "Device 1",
}
TEST_CONTENT = {
    "encryption_key": "test_key",
    "payload": "Some test payload",
}


@pytest.fixture
async def prepare_data(client: TestClient, router: APIRouter):
    url = router.url_path_for("create-protection-system")
    response = client.post(url, json=TEST_PROTECTION_SYSTEM)
    assert response.status_code == HTTPStatus.OK
    protection_system_json = response.json()

    url = router.url_path_for("create-device")
    response = client.post(url, json={**TEST_DEVICE, "protection_system_id": protection_system_json["id"]})
    assert response.status_code == HTTPStatus.OK
    device_json = response.json()

    url = router.url_path_for("create-content")
    response = client.post(url, json={**TEST_CONTENT, "protection_system_id": protection_system_json["id"]})
    assert response.status_code == HTTPStatus.OK
    content_json = response.json()

    return device_json["id"], content_json["id"]


async def test_decrypt(prepare_data, client: TestClient, router: APIRouter) -> None:
    device_id, content_id = prepare_data
    url = router.url_path_for("decrypt-content")
    response = client.post(url, json={"device_id": device_id, "content_id": content_id})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["payload"] == TEST_CONTENT["payload"]


@pytest.fixture
async def prepare_data_mismatch(client: TestClient, router: APIRouter):
    url = router.url_path_for("create-protection-system")
    response = client.post(url, json=TEST_PROTECTION_SYSTEM)
    assert response.status_code == HTTPStatus.OK
    protection_system_json_1 = response.json()

    response = client.post(url, json=TEST_PROTECTION_SYSTEM)
    assert response.status_code == HTTPStatus.OK
    protection_system_json_2 = response.json()

    url = router.url_path_for("create-device")
    response = client.post(url, json={**TEST_DEVICE, "protection_system_id": protection_system_json_1["id"]})
    assert response.status_code == HTTPStatus.OK
    device_json = response.json()

    url = router.url_path_for("create-content")
    response = client.post(url, json={**TEST_CONTENT, "protection_system_id": protection_system_json_2["id"]})
    assert response.status_code == HTTPStatus.OK
    content_json = response.json()

    return device_json["id"], content_json["id"]


async def test_decrypt_protection_system_mismatch(
    prepare_data_mismatch, client: TestClient, router: APIRouter
) -> None:
    device_id, content_id = prepare_data_mismatch
    url = router.url_path_for("decrypt-content")
    response = client.post(url, json={"device_id": device_id, "content_id": content_id})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "Protection system mismatch"
