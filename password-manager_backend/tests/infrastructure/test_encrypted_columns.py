import pytest
from sqlalchemy import Text

from infrastructure.databases.models.sub_account_history_model import (
    SubAccountHistoryModel,
)
from infrastructure.databases.models.sub_account_model import SubAccountModel

ENCRYPTED_FIELDS = ["username_encrypted", "email_encrypted", "site_link_encrypted"]


@pytest.mark.parametrize("model", [SubAccountModel, SubAccountHistoryModel])
@pytest.mark.parametrize("field", ENCRYPTED_FIELDS)
def test_encrypted_columns_have_no_length_limit(
    model: type[SubAccountModel | SubAccountHistoryModel], field: str
) -> None:
    column = model.__table__.c[field]

    assert isinstance(column.type, Text)  # pyright: ignore[reportUnknownMemberType]
