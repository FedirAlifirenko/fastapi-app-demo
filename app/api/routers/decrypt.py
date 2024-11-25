from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_content_repository, get_device_repository
from app.api.models.decrypt import DecryptRequest, DecryptResponse
from app.db.repository.content import ContentRepository
from app.db.repository.device import DeviceRepository
from app.services import Encryptor

router = APIRouter(prefix="/decrypt", tags=["Decrypt"])


@router.post("", name="decrypt-content", description="Decrypt payload for given device and content")
async def decrypt_content(
    decrypt_request: DecryptRequest,
    device_repo: DeviceRepository = Depends(get_device_repository),
    content_repo: ContentRepository = Depends(get_content_repository),
) -> DecryptResponse:
    device = await device_repo.get(decrypt_request.device_id)
    if not device:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Device not found")

    content = await content_repo.get(decrypt_request.content_id)
    if not content:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Content not found")

    if device.protection_system_id != content.protection_system_id:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Protection system mismatch")

    protection_system = device.protection_system
    if protection_system.encryption_mode != "AES_CBC":
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Encryption mode isn't supported"
        )

    encryptor, iv = Encryptor.from_encryption_key(content.encryption_key)
    plaintext = encryptor.decrypt(content.encrypted_payload, iv)

    return DecryptResponse(payload=plaintext)
