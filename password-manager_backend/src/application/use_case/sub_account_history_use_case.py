import uuid

from application.dto.sub_account_history_dto import SubAccountHistoryDTO
from application.exceptions.sub_account_history_use_case_exceptions import *

from domain.interfaces.sub_account_history_service_interface import ISubAccountHistoryService

class GetSubAccountHistoryBySubAccountIdUseCase():
    def __init__(self, SubAccountHistoryRepository: ISubAccountHistoryService):
        self.SubAccountHistoryRepository = SubAccountHistoryRepository

    def execute(self, sub_account_id: uuid.UUID) -> list[SubAccountHistoryDTO]:
        try:
            result = self.SubAccountHistoryRepository.GetHistoryBySubAccountId(sub_account_id)
            return [SubAccountHistoryDTO(
                            id=uuid.UUID(str(entry.id)),
                            sub_account_id=uuid.UUID(str(entry.sub_account_id)),
                            username_encrypted=entry.username_encrypted,
                            email_encrypted=entry.email_encrypted,
                            password_encrypted=str(entry.password_encrypted),
                            site_link_encrypted=entry.site_link_encrypted,
                            dek_wrapped=entry.dek_wrapped,
                            changed_by=uuid.UUID(str(entry.changed_by)) if entry.changed_by else None,
                            changed_at=entry.changed_at,
                            )
                        for entry in result]
        except Exception as e:
            raise SubAccountHistoryRetrievalException(str(e)) from e

class GetSubAccountHistoryByTeamIdUseCase():
    """Feeds rotateTeamKey: every history row that needs its dek_wrapped re-wrapped."""
    def __init__(self, SubAccountHistoryRepository: ISubAccountHistoryService):
        self.SubAccountHistoryRepository = SubAccountHistoryRepository

    def execute(self, team_id: uuid.UUID) -> list[SubAccountHistoryDTO]:
        try:
            result = self.SubAccountHistoryRepository.GetHistoryByTeamId(team_id)
            return [SubAccountHistoryDTO(
                            id=uuid.UUID(str(entry.id)),
                            sub_account_id=uuid.UUID(str(entry.sub_account_id)),
                            username_encrypted=entry.username_encrypted,
                            email_encrypted=entry.email_encrypted,
                            password_encrypted=str(entry.password_encrypted),
                            site_link_encrypted=entry.site_link_encrypted,
                            dek_wrapped=entry.dek_wrapped,
                            changed_by=uuid.UUID(str(entry.changed_by)) if entry.changed_by else None,
                            changed_at=entry.changed_at,
                            )
                        for entry in result]
        except Exception as e:
            raise SubAccountHistoryRetrievalException(str(e)) from e
