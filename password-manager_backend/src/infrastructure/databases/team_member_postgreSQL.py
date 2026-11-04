from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.team_member_postgreSQL_exceptions import *

from domain.interfaces.team_member_service_interface import ITeamMembersService
from domain.entities.team_member import TeamMember
from infrastructure.databases.models.team_member_model import TeamMemberModel


def _to_domain(model: TeamMemberModel) -> TeamMember:
    return TeamMember(
        id=model.id,
        team_id=model.team_id,
        user_id=model.user_id,
        perm_level_id=model.perm_level_id,
    )


class TeamMembersService(ITeamMembersService):
    def __init__(self, db: Session):
        self.Db = db

    def add_member_to_team(self, new_member: TeamMember) -> TeamMember:
        try:
            member_model = TeamMemberModel(
                team_id=new_member.team_id,
                user_id=new_member.user_id,
                perm_level_id=new_member.perm_level_id,
            )

            self.Db.add(member_model)
            self.Db.flush()
            self.Db.refresh(member_model)

            return _to_domain(member_model)

        except IntegrityError:
            raise Exception("Member already exists in the team.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to add member to team.")

    def get_team_member_by_id(self, member_id: uuid.UUID) -> TeamMember:
        try:
            member_model = (
                self.Db.query(TeamMemberModel).filter_by(id=member_id).first()
            )
            if not member_model:
                raise Exception("Member not found.")
            return _to_domain(member_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve team member by ID.")

    def get_members_by_team_id(self, team_id: uuid.UUID) -> list[TeamMember]:
        try:
            member_models = (
                self.Db.query(TeamMemberModel).filter_by(team_id=team_id).all()
            )
            return [_to_domain(member_model) for member_model in member_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve members for the team.")

    def update_member_role(self, new_user_data: TeamMember) -> TeamMember:
        try:
            member_model = (
                self.Db.query(TeamMemberModel)
                .filter_by(user_id=new_user_data.user_id, team_id=new_user_data.team_id)
                .first()
            )

            if not member_model:
                raise Exception("Member not found in the team.")

            member_model.perm_level_id = new_user_data.perm_level_id
            self.Db.flush()
            self.Db.refresh(member_model)

            return _to_domain(member_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to update member role.")

    def remove_member_from_team(
        self, member_id: uuid.UUID, team_id: uuid.UUID
    ) -> dict[str, str]:
        try:
            member_model = (
                self.Db.query(TeamMemberModel)
                .filter_by(user_id=member_id, team_id=team_id)
                .first()
            )

            if not member_model:
                raise Exception("Member not found in the team.")

            self.Db.delete(member_model)
            self.Db.flush()

            return {"message": "Member removed from team successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to remove member from team.")
