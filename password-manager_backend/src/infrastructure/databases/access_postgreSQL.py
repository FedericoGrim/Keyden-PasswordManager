import uuid
from typing import Optional

from sqlalchemy.orm import Session

from domain.interfaces.access_reader_interface import IAccessReader
from infrastructure.databases.models.categories_model import CategoriesModel
from infrastructure.databases.models.sub_account_model import SubAccountModel
from infrastructure.databases.models.team_member_model import TeamMemberModel
from infrastructure.databases.models.team_perm_level_model import TeamPermLevelModel
from infrastructure.databases.models.user_teams_keys_model import UserTeamKeyModel


class AccessReader(IAccessReader):
    def __init__(self, db: Session) -> None:
        self.db = db

    def rank_in_team(self, user_id: uuid.UUID, team_id: uuid.UUID) -> Optional[int]:
        return (
            self.db.query(TeamPermLevelModel.rank)
            .join(
                TeamMemberModel, TeamMemberModel.perm_level_id == TeamPermLevelModel.id
            )
            .filter(
                TeamMemberModel.user_id == user_id, TeamMemberModel.team_id == team_id
            )
            .scalar()
        )

    def team_has_members(self, team_id: uuid.UUID) -> bool:
        return (
            self.db.query(TeamMemberModel.id)
            .filter(TeamMemberModel.team_id == team_id)
            .first()
            is not None
        )

    def team_of_sub_account(self, sub_account_id: uuid.UUID) -> Optional[uuid.UUID]:
        return (
            self.db.query(SubAccountModel.team_id)
            .filter(SubAccountModel.id == sub_account_id)
            .scalar()
        )

    def team_of_category(self, category_id: uuid.UUID) -> Optional[uuid.UUID]:
        return (
            self.db.query(CategoriesModel.team_id)
            .filter(CategoriesModel.id == category_id)
            .scalar()
        )

    def team_of_perm_level(self, perm_level_id: uuid.UUID) -> Optional[uuid.UUID]:
        return (
            self.db.query(TeamPermLevelModel.team_id)
            .filter(TeamPermLevelModel.id == perm_level_id)
            .scalar()
        )

    def member_row(self, member_id: uuid.UUID) -> Optional[tuple[uuid.UUID, uuid.UUID]]:
        row = (
            self.db.query(TeamMemberModel.team_id, TeamMemberModel.user_id)
            .filter(TeamMemberModel.id == member_id)
            .first()
        )
        return (row[0], row[1]) if row else None

    def key_row(self, key_id: uuid.UUID) -> Optional[tuple[uuid.UUID, uuid.UUID]]:
        row = (
            self.db.query(UserTeamKeyModel.team_id, UserTeamKeyModel.user_id)
            .filter(UserTeamKeyModel.id == key_id)
            .first()
        )
        return (row[0], row[1]) if row else None
