from application.dto.team_perm_levels_dto import *
from application.exceptions.team_perm_levels_use_case_exceptions import *

from domain.interfaces.team_perm_level_service_interface import ITeamPermLevelService

import uuid


class CreateTeamPermLevelUseCase:
    def __init__(self, TeamPermLevelRepository: ITeamPermLevelService):
        self.TeamPermLevelRepository = TeamPermLevelRepository

    def execute(
        self, perm_level: CreateTeamPermLevelDTO, user_interactor_id: uuid.UUID
    ) -> TeamPermLevelDTO:
        try:
            perm_level_entity = perm_level.to_entity()
            result = self.TeamPermLevelRepository.CreateTeamPermLevel(perm_level_entity)

            return result

        except Exception as e:
            raise CreateTeamPermLevelException(str(e)) from e


class GetTeamPermLevelByIdUseCase:
    def __init__(self, TeamPermLevelRepository: ITeamPermLevelService):
        self.TeamPermLevelRepository = TeamPermLevelRepository

    def execute(self, perm_level_id: uuid.UUID) -> TeamPermLevelDTO:
        try:
            perm_level = self.TeamPermLevelRepository.GetTeamPermLevelById(
                perm_level_id
            )
            return TeamPermLevelDTO(
                id=uuid.UUID(str(perm_level.id)),
                team_id=uuid.UUID(str(perm_level.team_id)),
                name=str(perm_level.name),
                rank=int(perm_level.rank),
            )

        except Exception as e:
            raise TeamPermLevelRetrievalException(str(e)) from e


class GetAllTeamPermLevelsByTeamIdUseCase:
    def __init__(self, TeamPermLevelRepository: ITeamPermLevelService):
        self.TeamPermLevelRepository = TeamPermLevelRepository

    def execute(self, teamId: uuid.UUID) -> list[TeamPermLevelDTO]:
        try:
            perm_levels = self.TeamPermLevelRepository.GetAllTeamPermLevelsByTeamId(
                teamId
            )
            return [
                TeamPermLevelDTO(
                    id=uuid.UUID(str(perm_level.id)),
                    team_id=uuid.UUID(str(perm_level.team_id)),
                    name=str(perm_level.name),
                    rank=int(perm_level.rank),
                )
                for perm_level in perm_levels
            ]
        except Exception as e:
            raise TeamPermLevelRetrievalException(str(e)) from e


class UpdateTeamPermLevelByIdUseCase:
    def __init__(self, TeamPermLevelRepository: ITeamPermLevelService):
        self.TeamPermLevelRepository = TeamPermLevelRepository

    def execute(
        self,
        perm_level_id: uuid.UUID,
        new_perm_level: UpdateTeamPermLevelDTO,
        user_interactor_id: uuid.UUID,
    ) -> TeamPermLevelDTO:
        try:
            existing_perm_level = self.TeamPermLevelRepository.GetTeamPermLevelById(
                perm_level_id
            )
            result = self.TeamPermLevelRepository.UpdateTeamPermLevelById(
                perm_level_id, new_perm_level.to_entity(existing_perm_level)
            )

            return TeamPermLevelDTO(
                id=uuid.UUID(str(result.id)),
                team_id=uuid.UUID(str(result.team_id)),
                name=str(result.name),
                rank=int(result.rank),
            )

        except Exception as e:
            raise TeamPermLevelUpdateException(str(e)) from e


class DeleteTeamPermLevelByIdUseCase:
    def __init__(self, TeamPermLevelRepository: ITeamPermLevelService):
        self.TeamPermLevelRepository = TeamPermLevelRepository

    def execute(self, perm_level_id: uuid.UUID, user_interactor_id: uuid.UUID) -> bool:
        try:
            result = self.TeamPermLevelRepository.DeleteTeamPermLevelById(perm_level_id)

            return result
        except Exception as e:
            raise TeamPermLevelDeletionException(str(e)) from e
