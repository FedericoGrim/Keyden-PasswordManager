import uuid

from application.exceptions.team_member_use_case_exceptions import (
    TeamMemberAdditionException,
    TeamMemberRemovalException,
    TeamMemberRetrievalByIdException,
    TeamMemberRoleUpdateException,
    TeamMembersRetrievalByTeamIdException,
)
from application.dto.team_member_dto import (
    TeamMemberDTO,
    CreateTeamMemberDTO,
    UpdateTeamMemberDTO,
    RemoveTeamMemberDTO,
)

from domain.interfaces.team_member_service_interface import ITeamMembersService


class AddMemberToTeamUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService) -> None:
        self.team_members_repository = TeamMembersRepository

    def execute(
        self, interactor_id: uuid.UUID, new_member: CreateTeamMemberDTO
    ) -> TeamMemberDTO:
        try:
            team_member = self.team_members_repository.add_member_to_team(
                new_member.to_entity()
            )

            return TeamMemberDTO(
                id=uuid.UUID(str(team_member.id)),
                user_id=uuid.UUID(str(team_member.user_id)),
                team_id=uuid.UUID(str(team_member.team_id)),
                perm_level_id=uuid.UUID(str(team_member.perm_level_id)),
            )

        except Exception as e:
            raise TeamMemberAdditionException(str(e)) from e


class GetTeamMemberByIdUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService) -> None:
        self.team_members_repository = TeamMembersRepository

    def execute(self, member_id: uuid.UUID) -> TeamMemberDTO:
        try:
            member = self.team_members_repository.get_team_member_by_id(member_id)
            return TeamMemberDTO(
                id=uuid.UUID(str(member.id)),
                user_id=uuid.UUID(str(member.user_id)),
                team_id=uuid.UUID(str(member.team_id)),
                perm_level_id=uuid.UUID(str(member.perm_level_id)),
            )

        except Exception as e:
            raise TeamMemberRetrievalByIdException(str(e)) from e


class GetTeamMembersByTeamIdUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService) -> None:
        self.team_members_repository = TeamMembersRepository

    def execute(self, team_id: uuid.UUID) -> list[TeamMemberDTO]:
        try:
            team_members = self.team_members_repository.get_members_by_team_id(team_id)
            return [
                TeamMemberDTO(
                    id=uuid.UUID(str(member.id)),
                    user_id=uuid.UUID(str(member.user_id)),
                    team_id=uuid.UUID(str(member.team_id)),
                    perm_level_id=uuid.UUID(str(member.perm_level_id)),
                )
                for member in team_members
            ]

        except Exception as e:
            raise TeamMembersRetrievalByTeamIdException(str(e)) from e


class UpdateTeamMemberRoleUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService) -> None:
        self.team_members_repository = TeamMembersRepository

    def execute(
        self, interactor_id: uuid.UUID, new_user_data: UpdateTeamMemberDTO
    ) -> TeamMemberDTO:
        try:
            updated_member = self.team_members_repository.update_member_role(
                new_user_data.to_entity(
                    self.team_members_repository.get_team_member_by_id(
                        new_user_data.user_id
                    )
                )
            )

            return TeamMemberDTO(
                id=uuid.UUID(str(updated_member.id)),
                user_id=uuid.UUID(str(updated_member.user_id)),
                team_id=uuid.UUID(str(updated_member.team_id)),
                perm_level_id=uuid.UUID(str(updated_member.perm_level_id)),
            )

        except Exception as e:
            raise TeamMemberRoleUpdateException(str(e)) from e


class RemoveMemberFromTeamUseCase:
    def __init__(self, TeamMembersRepository: ITeamMembersService) -> None:
        self.team_members_repository = TeamMembersRepository

    def execute(
        self, user_interactor: uuid.UUID, user_to_delete: RemoveTeamMemberDTO
    ) -> dict[str, str]:
        try:
            removal_result = self.team_members_repository.remove_member_from_team(
                member_id=user_to_delete.member_id, team_id=user_to_delete.team_id
            )

            return removal_result

        except Exception as e:
            raise TeamMemberRemovalException(str(e)) from e
