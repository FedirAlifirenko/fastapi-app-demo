from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.dependencies import get_protection_system_repository
from app.api.models.protection_system import (
    ProtectionSystem,
    ProtectionSystemCreate,
    ProtectionSystemUpdate,
)
from app.db.repository.protection_system import ProtectionSystemRepository

router = APIRouter(prefix="/protection-system", tags=["Protection System"])


@router.post("", name="create-protection-system", description="Create a new protection system")
async def create_protection_system(
    create_data: ProtectionSystemCreate,
    repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> ProtectionSystem:
    protection_system = await repo.create(
        name=create_data.name,
        encryption_mode=create_data.encryption_mode,
    )
    return ProtectionSystem.model_validate(protection_system)


@router.get("", name="list-protection-systems", description="List protection systems")
async def list_protection_systems(
    repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> list[ProtectionSystem]:
    protection_systems = await repo.list()
    return [ProtectionSystem.model_validate(protection_system) for protection_system in protection_systems]


@router.get("/{id}", name="read-protection-system", description="Get a protection system")
async def get_protection_system(
    id: int,
    repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> ProtectionSystem:
    protection_system = await repo.get(id)
    if not protection_system:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Protection system not found")

    return ProtectionSystem.model_validate(protection_system)


@router.patch("/{id}", name="update-protection-system", description="Update a protection system")
async def update_protection_system(
    id: int,
    update_data: ProtectionSystemUpdate,
    repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> ProtectionSystem:
    protection_system = await repo.get(id)
    if not protection_system:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Protection system not found")

    fields_to_update = update_data.model_dump(exclude_unset=True)
    if not fields_to_update:
        return ProtectionSystem.model_validate(protection_system)

    updated_protection_system = await repo.update(
        protection_system,
        **fields_to_update,
    )
    return ProtectionSystem.model_validate(updated_protection_system)


@router.delete(
    "/{id}",
    name="delete-protection-system",
    description="Delete a protection system. "
    "⚠️ This will also delete all associated Content and Device objects (cascade).",
)
async def delete_protection_system(
    id: int,
    repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> Response:
    protection_system = await repo.get(id)
    if not protection_system:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Protection system not found")

    await repo.delete(protection_system)
    return Response(status_code=HTTPStatus.NO_CONTENT)
