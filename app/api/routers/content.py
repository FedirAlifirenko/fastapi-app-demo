from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.dependencies import (
    get_content_repository,
    get_protection_system_repository,
)
from app.api.models.content import Content, ContentCreate, DecryptedContent
from app.api.models.protection_system import EncryptionMode
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

    if protection_system.encryption_mode != EncryptionMode.aes_cbc:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Input should be 'AES_CBC'",
        )

    encryptor = Encryptor.from_plaintext_key(create_data.encryption_key)
    iv, ciphertext = encryptor.encrypt(create_data.payload)

    content = await repo.create(
        protection_system_id=protection_system.id,
        encryption_key=encryptor.get_encryption_key(iv),
        encrypted_payload=ciphertext,
    )
    return Content.model_validate(content)


@router.get("", name="list-content", description="List content")
async def list_content(
    repo: ContentRepository = Depends(get_content_repository),
) -> list[Content]:
    contents = await repo.list()
    return [Content.model_validate(content) for content in contents]


@router.get("/{id}", name="read-content", description="Read content")
async def read_content(
    id: int,
    repo: ContentRepository = Depends(get_content_repository),
) -> Content:
    content = await repo.get(id)
    if not content:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Content not found")

    return Content.model_validate(content)


@router.delete("/{id}", name="delete-content", description="Delete content")
async def delete_content(
    id: int,
    repo: ContentRepository = Depends(get_content_repository),
) -> Response:
    content = await repo.get(id)
    if not content:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Content not found")

    await repo.delete(content)
    return Response(status_code=HTTPStatus.NO_CONTENT)


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
