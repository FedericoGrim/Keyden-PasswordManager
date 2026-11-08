import uuid

from application.dto.sub_account_dto import UpdateSubAccountDTO
from domain.entities.sub_account import SubAccount


def test_update_keeps_the_id_of_the_existing_sub_account() -> None:
    existing = SubAccount(
        id=uuid.uuid4(),
        team_id=uuid.uuid4(),
        username_encrypted="u",
        email_encrypted="e",
        password_encrypted="p",
        site_link_encrypted="s",
        required_perm_level_id=uuid.uuid4(),
        dek_wrapped="d",
    )
    dto = UpdateSubAccountDTO(
        id=uuid.uuid4(),
        username_encrypted=None,
        email_encrypted=None,
        password_encrypted="new",
        site_link_encrypted=None,
        required_perm_level_id=None,
    )

    updated = dto.to_entity(existing)

    assert updated.id == existing.id
    assert updated.password_encrypted == "new"
    assert updated.username_encrypted == "u"
