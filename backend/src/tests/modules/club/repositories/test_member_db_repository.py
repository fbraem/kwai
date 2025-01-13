"""Module for testing the member database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.domain.file_upload import FileUploadEntity, FileUploadIdentifier
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository
from kwai.modules.club.repositories.member_repository import (
    MemberNotFoundException,
    MemberRepository,
)


pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


async def test_create_member(make_member_in_db):
    """Test create member."""
    member = await make_member_in_db()
    assert not member.id.is_empty(), "There should be a member created."


async def test_update_member(
    member_repo: MemberRepository, database: Database, make_member_in_db
):
    """Test update member."""
    member = await make_member_in_db()
    member = Entity.replace(member, remark="This is an update.")
    async with UnitOfWork(database):
        await member_repo.update(member)
    member = await member_repo.get(member_repo.create_query().filter_by_id(member.id))
    assert member.remark == "This is an update.", "The member should be updated."


async def test_get_all(member_repo: MemberRepository, make_member_in_db):
    """Test get all."""
    await make_member_in_db()
    try:
        it = member_repo.get_all()
        await anext(it)
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_delete(
    member_repo: MemberRepository, database: Database, make_member_in_db
):
    """Test deleting a member."""
    member = await make_member_in_db()
    async with UnitOfWork(database):
        await member_repo.delete(member)
    with pytest.raises(MemberNotFoundException):
        await member_repo.get(member_repo.create_query().filter_by_id(member.id))


async def test_activate_members(
    member_repo: MemberRepository, database: Database, owner: Owner
):
    """Test activate members."""
    async with UnitOfWork(database):
        upload_entity = FileUploadEntity(
            id_=FileUploadIdentifier(1),
            filename="test.txt",
            owner=owner,
        )
        await member_repo.activate_members(upload_entity)


async def test_deactivate_members(
    member_repo: MemberRepository, database: Database, owner: Owner
):
    """Test activate members."""
    async with UnitOfWork(database):
        upload_entity = FileUploadEntity(
            id_=FileUploadIdentifier(1),
            filename="test.txt",
            owner=owner,
        )
        await member_repo.deactivate_members(upload_entity)
