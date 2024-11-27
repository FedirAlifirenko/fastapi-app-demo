import pytest
from sqlalchemy import select

from app.db.models.user_device import user_device
from app.db.repository.device import DeviceRepository
from app.db.repository.protection_system import ProtectionSystemRepository
from app.db.repository.user import UserRepository

pytestmark = pytest.mark.anyio


@pytest.fixture
def repo(db_session):
    return UserRepository(db_session=db_session)


async def test_create(repo):
    user = await repo.create(username="User1")
    assert user.id == 1
    assert user.username == "User1"


@pytest.fixture
def protection_system_repo(db_session):
    return ProtectionSystemRepository(db_session=db_session)


TEST_PROTECTION_SYSTEM = {
    "id": 1,
    "name": "Protection system 1",
    "encryption_mode": "AES_CBC",
}

TEST_DEVICE = {
    "protection_system_id": TEST_PROTECTION_SYSTEM["id"],
    "name": "Device 1",
}
TEST_DEVICE_ID = 1

TEST_DEVICE_2 = {
    "protection_system_id": TEST_PROTECTION_SYSTEM["id"],
    "name": "Device 2",
}


@pytest.fixture
async def protection_system(db_session, protection_system_repo):
    await protection_system_repo.create(**TEST_PROTECTION_SYSTEM)


@pytest.fixture
async def prepare_association_data(repo, db_session, protection_system):
    device_repo = DeviceRepository(db_session=db_session)
    test_device1 = await device_repo.create(commit=False, **TEST_DEVICE)
    test_device2 = await device_repo.create(commit=False, **TEST_DEVICE_2)

    user = await repo.create(commit=False, username="User1")
    user.devices = [test_device1, test_device2]

    user2 = await repo.create(commit=False, username="User2")
    user2.devices = [test_device1]

    await db_session.commit()

    return {user.id, user2.id}


async def test_association(db_session, prepare_association_data):
    exp_user_ids = prepare_association_data

    stmt = select(user_device.c.user_id).filter(user_device.c.device_id == TEST_DEVICE_ID)
    device1_users = (await db_session.execute(stmt)).scalars().all()

    assert set(device1_users) == exp_user_ids
