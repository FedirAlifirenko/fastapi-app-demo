from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.dependencies import get_device_repository, get_protection_system_repository
from app.api.models.device import Device, DeviceCreate, DeviceUpdate
from app.db.repository.device import DeviceRepository
from app.db.repository.protection_system import ProtectionSystemRepository

router = APIRouter(prefix="/device", tags=["Device"])


@router.post("", name="create-device", description="Create a new device")
async def create_device(
    create_data: DeviceCreate,
    repo: DeviceRepository = Depends(get_device_repository),
    protection_system_repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> Device:
    protection_system = await protection_system_repo.get(create_data.protection_system_id)
    if not protection_system:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Protection system not found")

    device = await repo.create(
        name=create_data.name,
        protection_system_id=create_data.protection_system_id,
    )
    return Device.model_validate(device)


@router.get("", name="list-device", description="List devices")
async def list_devices(
    repo: DeviceRepository = Depends(get_device_repository),
) -> list[Device]:
    devices = await repo.list()
    return [Device.model_validate(device) for device in devices]


@router.get("/{id}", name="read-device", description="Get a device")
async def get_device(
    id: int,
    repo: DeviceRepository = Depends(get_device_repository),
) -> Device:
    device = await repo.get(id)
    if not device:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Device not found")

    return Device.model_validate(device)


@router.patch("/{id}", name="update-device", description="Update a device")
async def update_device(
    id: int,
    update_data: DeviceUpdate,
    repo: DeviceRepository = Depends(get_device_repository),
    protection_system_repo: ProtectionSystemRepository = Depends(get_protection_system_repository),
) -> Device:
    device = await repo.get(id)
    if not device:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Device not found")

    if protection_system_id := update_data.protection_system_id:
        protection_system = await protection_system_repo.get(protection_system_id)
        if not protection_system:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Protection system not found"
            )

    fields_to_update = update_data.model_dump(exclude_unset=True)
    if not fields_to_update:
        return Device.model_validate(device)

    updated_device = await repo.update(device, **fields_to_update)
    return Device.model_validate(updated_device)


@router.delete("/{id}", name="delete-device", description="Delete a device")
async def delete_device(
    id: int,
    repo: DeviceRepository = Depends(get_device_repository),
) -> Response:
    device = await repo.get(id)
    if not device:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Device not found")

    await repo.delete(device)
    return Response(status_code=HTTPStatus.NO_CONTENT)
