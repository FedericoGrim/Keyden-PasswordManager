import uuid

from application.dto.sub_account_dto import SubAccountDTO, CreateSubAccountDTO, UpdateSubAccountDTO, DeleteSubAccountDTO, RotateSubAccountDeksDTO
from application.exceptions.sub_account_use_case_exceptions import *
from application.exceptions.sub_account_history_use_case_exceptions import RotateSubAccountDeksException

from domain.interfaces.sub_account_service_interface import ISubAccountService
from domain.interfaces.sub_account_history_service_interface import ISubAccountHistoryService
from domain.entities.sub_account_history import SubAccountHistory

class CreateSubAccountUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, interactor_id: uuid.UUID, subaccount_create: CreateSubAccountDTO):
        try:
            subaccount_entity = subaccount_create.to_entity()
            result = self.SubAccountRepository.CreateSubAccount(subaccount_entity)

            return result
        except Exception as e:
            raise CreateSubAccountException(str(e)) from e

class GetSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, subaccountId: uuid.UUID):
        try:
            return self.SubAccountRepository.GetSubAccountById(subaccountId)
        except Exception as e:
            raise SubAccountRetrievalException(str(e)) from e

class GetAllSubAccountsByTeamIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, teamId: uuid.UUID):
        try:
            result = self.SubAccountRepository.GetAllSubAccountsByTeamId(teamId)
            return [SubAccountDTO(
                            id=uuid.UUID(str(sub_account.id)),
                            team_id=uuid.UUID(str(sub_account.team_id)),
                            username_encrypted=str(sub_account.username_encrypted),
                            email_encrypted=str(sub_account.email_encrypted),
                            password_encrypted=str(sub_account.password_encrypted),
                            site_link_encrypted=str(sub_account.site_link_encrypted),
                            required_perm_level_id=uuid.UUID(str(sub_account.required_perm_level_id)),
                            dek_wrapped=sub_account.dek_wrapped
                            )
                        for sub_account in result]
        except Exception as e:
            raise SubAccountRetrievalException(str(e)) from e

class UpdateSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService, SubAccountHistoryRepository: ISubAccountHistoryService):
        self.SubAccountRepository = SubAccountRepository
        self.SubAccountHistoryRepository = SubAccountHistoryRepository

    def execute(self, interactor_id: uuid.UUID, new_subaccount: UpdateSubAccountDTO) -> SubAccountDTO:
        try:
            existing_subaccount = self.SubAccountRepository.GetSubAccountById(new_subaccount.id)

            # Snapshot the value being overwritten before it's gone — same
            # dek_wrapped as the live row, so it rotates together with it.
            self.SubAccountHistoryRepository.CreateHistoryEntry(SubAccountHistory(
                sub_account_id=existing_subaccount.id,
                username_encrypted=existing_subaccount.username_encrypted,
                email_encrypted=existing_subaccount.email_encrypted,
                password_encrypted=existing_subaccount.password_encrypted,
                site_link_encrypted=existing_subaccount.site_link_encrypted,
                dek_wrapped=existing_subaccount.dek_wrapped,
                changed_by=interactor_id,
            ))

            result = self.SubAccountRepository.UpdateSubAccountById(new_subaccount.to_entity(existing_subaccount))

            return SubAccountDTO(
                id=uuid.UUID(str(result.id)),
                team_id=uuid.UUID(str(result.team_id)),
                username_encrypted=str(result.username_encrypted),
                email_encrypted=str(result.email_encrypted),
                password_encrypted=str(result.password_encrypted),
                site_link_encrypted=str(result.site_link_encrypted),
                required_perm_level_id=uuid.UUID(str(result.required_perm_level_id)),
                dek_wrapped=result.dek_wrapped
            )

        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e

class DeleteSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, interactor_id: uuid.UUID, subaccount_to_delete: DeleteSubAccountDTO):
        try:
            result = self.SubAccountRepository.DeleteSubAccountById(subaccount_to_delete.id)

            return result
        except Exception as e:
            raise SubAccountDeletionException(str(e)) from e

class RotateSubAccountDeksUseCase():
    """Re-wraps data keys after a team-key rotation. Never touches the
    encrypted payload — only the small dek_wrapped blob per row, for both
    live sub_accounts and their history, so content ciphertext never moves."""
    def __init__(self, SubAccountRepository: ISubAccountService, SubAccountHistoryRepository: ISubAccountHistoryService):
        self.SubAccountRepository = SubAccountRepository
        self.SubAccountHistoryRepository = SubAccountHistoryRepository

    def execute(self, interactor_id: uuid.UUID, rotation: RotateSubAccountDeksDTO) -> dict[str, str]:
        try:
            for item in rotation.sub_accounts:
                self.SubAccountRepository.UpdateSubAccountDek(item.id, item.dek_wrapped)
            for item in rotation.history:
                self.SubAccountHistoryRepository.UpdateHistoryDek(item.id, item.dek_wrapped)

            return {"message": "Data keys rotated successfully."}
        except Exception as e:
            raise RotateSubAccountDeksException(str(e)) from e
