from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import (
    get_content_repository,
    get_protection_system_repository,
)
from app.api.models.content import Content, ContentCreate, DecryptedContent
from app.db.repository.content import ContentRepository
from app.db.repository.protection_system import ProtectionSystemRepository
from app.services import Encryptor

router = APIRouter(prefix="/content", tags=["Content"])


@router.post("", name="create-content", description="Create content")
async def create_content(
    create_data: ContentCreate,
    repo: ContentRepository = Depends(get_content_repository),
    protection_system_repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> Content:
    protection_system = await protection_system_repo.get(create_data.protection_system_id)
    if not protection_system:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Protection system not found")

    encryptor = Encryptor.from_plaintext_key(create_data.encryption_key)
    iv, ciphertext = encryptor.encrypt(create_data.payload)

    content = await repo.create(
        protection_system_id=protection_system.id,
        encryption_key=encryptor.get_encryption_key(iv),
        encrypted_payload=ciphertext,
    )
    return Content.model_validate(content)


@router.get("/{id}", name="read-content", description="Read content")
async def read_content(
    id: int,
    repo: ContentRepository = Depends(get_content_repository),
) -> Content:
    content = await repo.get(id)
    if not content:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Content not found")

    return Content.model_validate(content)


@router.get("/{id}/decrypt", name="decrypt-content", description="Decrypt content")
async def decrypt_content(
    id: int,
    repo: ContentRepository = Depends(get_content_repository),
) -> DecryptedContent:
    content = await repo.get(id)
    if not content:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Content not found")

    encryptor, iv = Encryptor.from_encryption_key(content.encryption_key)
    plaintext = encryptor.decrypt(content.encrypted_payload, iv)

    return DecryptedContent(payload=plaintext)
