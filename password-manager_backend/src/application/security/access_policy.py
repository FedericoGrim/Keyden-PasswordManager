import uuid

from domain.interfaces.access_reader_interface import IAccessReader

OWNER_RANK = 0


class AccessDenied(Exception):
    pass


class AccessPolicy:
    """Deny-by-default authorization rules. Unknown resources are denied the same
    way as forbidden ones so callers cannot probe which ids exist."""

    def __init__(self, reader: IAccessReader) -> None:
        self.reader = reader

    def require_self(self, caller_id: uuid.UUID, target_id: uuid.UUID) -> None:
        if caller_id != target_id:
            raise AccessDenied()

    def require_member(self, user_id: uuid.UUID, team_id: uuid.UUID) -> None:
        if self.reader.rank_in_team(user_id, team_id) is None:
            raise AccessDenied()

    def require_owner(self, user_id: uuid.UUID, team_id: uuid.UUID) -> None:
        if self.reader.rank_in_team(user_id, team_id) != OWNER_RANK:
            raise AccessDenied()

    def require_owner_or_empty_team(
        self, user_id: uuid.UUID, team_id: uuid.UUID
    ) -> None:
        """Team creation is a multi-request bootstrap (team, owner level, member,
        key): while the team has no members, the first caller may set it up."""
        if not self.reader.team_has_members(team_id):
            return
        self.require_owner(user_id, team_id)

    def require_member_of_sub_account(
        self, user_id: uuid.UUID, sub_account_id: uuid.UUID
    ) -> uuid.UUID:
        team_id = self.reader.team_of_sub_account(sub_account_id)
        if team_id is None:
            raise AccessDenied()
        self.require_member(user_id, team_id)
        return team_id

    def require_member_of_category(
        self, user_id: uuid.UUID, category_id: uuid.UUID
    ) -> uuid.UUID:
        team_id = self.reader.team_of_category(category_id)
        if team_id is None:
            raise AccessDenied()
        self.require_member(user_id, team_id)
        return team_id

    def require_member_of_perm_level(
        self, user_id: uuid.UUID, perm_level_id: uuid.UUID
    ) -> uuid.UUID:
        team_id = self.reader.team_of_perm_level(perm_level_id)
        if team_id is None:
            raise AccessDenied()
        self.require_member(user_id, team_id)
        return team_id

    def require_owner_of_perm_level(
        self, user_id: uuid.UUID, perm_level_id: uuid.UUID
    ) -> uuid.UUID:
        team_id = self.reader.team_of_perm_level(perm_level_id)
        if team_id is None:
            raise AccessDenied()
        self.require_owner(user_id, team_id)
        return team_id

    def require_member_of_member_row(
        self, user_id: uuid.UUID, member_id: uuid.UUID
    ) -> uuid.UUID:
        row = self.reader.member_row(member_id)
        if row is None:
            raise AccessDenied()
        team_id, _ = row
        self.require_member(user_id, team_id)
        return team_id

    def require_own_key(self, user_id: uuid.UUID, key_id: uuid.UUID) -> None:
        row = self.reader.key_row(key_id)
        if row is None or row[1] != user_id:
            raise AccessDenied()

    def require_perm_level_in_team(
        self, perm_level_id: uuid.UUID, team_id: uuid.UUID
    ) -> None:
        if self.reader.team_of_perm_level(perm_level_id) != team_id:
            raise AccessDenied()

    def require_can_add_member(
        self, caller_id: uuid.UUID, team_id: uuid.UUID, new_user_id: uuid.UUID
    ) -> None:
        if not self.reader.team_has_members(team_id):
            self.require_self(caller_id, new_user_id)
            return
        self.require_owner(caller_id, team_id)

    def require_owner_or_self(
        self, caller_id: uuid.UUID, team_id: uuid.UUID, target_user_id: uuid.UUID
    ) -> None:
        if target_user_id == caller_id:
            self.require_member(caller_id, team_id)
        else:
            self.require_owner(caller_id, team_id)
