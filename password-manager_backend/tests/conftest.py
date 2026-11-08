import os
import uuid
from typing import Optional

import pytest

os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test")

from domain.interfaces.access_reader_interface import IAccessReader  # noqa: E402


class FakeAccessReader(IAccessReader):
    def __init__(self) -> None:
        self.ranks: dict[tuple[uuid.UUID, uuid.UUID], int] = {}
        self.sub_account_teams: dict[uuid.UUID, uuid.UUID] = {}
        self.category_teams: dict[uuid.UUID, uuid.UUID] = {}
        self.perm_level_teams: dict[uuid.UUID, uuid.UUID] = {}
        self.member_rows: dict[uuid.UUID, tuple[uuid.UUID, uuid.UUID]] = {}
        self.key_rows: dict[uuid.UUID, tuple[uuid.UUID, uuid.UUID]] = {}
        self.teams_with_members: set[uuid.UUID] = set()

    def rank_in_team(self, user_id: uuid.UUID, team_id: uuid.UUID) -> Optional[int]:
        return self.ranks.get((user_id, team_id))

    def team_has_members(self, team_id: uuid.UUID) -> bool:
        return team_id in self.teams_with_members

    def team_of_sub_account(self, sub_account_id: uuid.UUID) -> Optional[uuid.UUID]:
        return self.sub_account_teams.get(sub_account_id)

    def team_of_category(self, category_id: uuid.UUID) -> Optional[uuid.UUID]:
        return self.category_teams.get(category_id)

    def team_of_perm_level(self, perm_level_id: uuid.UUID) -> Optional[uuid.UUID]:
        return self.perm_level_teams.get(perm_level_id)

    def member_row(self, member_id: uuid.UUID) -> Optional[tuple[uuid.UUID, uuid.UUID]]:
        return self.member_rows.get(member_id)

    def key_row(self, key_id: uuid.UUID) -> Optional[tuple[uuid.UUID, uuid.UUID]]:
        return self.key_rows.get(key_id)


@pytest.fixture
def reader() -> FakeAccessReader:
    return FakeAccessReader()
