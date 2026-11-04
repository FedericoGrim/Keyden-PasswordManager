from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.team_postgreSQL_exceptions import *

from domain.interfaces.team_service_interface import ITeamService
from domain.entities.team import Team
from infrastructure.databases.models.team_model import TeamModel
from infrastructure.databases.models.team_member_model import TeamMemberModel


def _to_domain(model: TeamModel) -> Team:
    return Team(
        id=model.id,
        name=model.name,
        is_personal=model.is_personal,
    )


class TeamService(ITeamService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateTeam(self, new_team: Team) -> Team:
        try:
            team_model = TeamModel(
                name=new_team.name,
                is_personal=new_team.is_personal,
            )

            self.Db.add(team_model)
            self.Db.flush()
            self.Db.refresh(team_model)

            return _to_domain(team_model)

        except IntegrityError:
            raise TeamAlreadyExistsException()

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamCreationFailedException()

    def GetTeamById(self, team_id: uuid.UUID):
        try:
            team_model = (
                self.Db.query(TeamModel).filter(TeamModel.id == team_id).first()
            )
            if not team_model:
                raise GetTeamByIdNotFoundException(
                    "No Team found for the given Team Id."
                )

            return _to_domain(team_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetTeamByIdRetrivalException()

    def GetTeamsByUserId(self, user_id: uuid.UUID):
        try:
            team_models: list[TeamModel] = (
                self.Db.query(TeamModel)
                .join(TeamMemberModel, TeamModel.id == TeamMemberModel.team_id)
                .filter(TeamMemberModel.user_id == user_id)
                .all()
            )
            if not team_models:
                raise GetTeamsByUserIdNotFoundException(
                    "No Teams found for the given User Id."
                )
            return [_to_domain(team_model) for team_model in team_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamRetrievalException("Failed to retrieve teams.")

    def UpdateTeamById(self, new_team: Team) -> Team:
        try:
            team_model = (
                self.Db.query(TeamModel).filter(TeamModel.id == new_team.id).first()
            )
            if not team_model:
                raise TeamNotFoundException("Team not found.")

            team_model.name = new_team.name
            self.Db.flush()
            self.Db.refresh(team_model)

            return _to_domain(team_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamUpdateException()

    def DeleteTeamById(self, team_id: uuid.UUID) -> dict[str, str]:
        try:
            team_model = (
                self.Db.query(TeamModel).filter(TeamModel.id == team_id).first()
            )
            if not team_model:
                raise TeamNotFoundException("Team not found.")

            self.Db.delete(team_model)

            return {"message": "Team deleted successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamDeleteException()
