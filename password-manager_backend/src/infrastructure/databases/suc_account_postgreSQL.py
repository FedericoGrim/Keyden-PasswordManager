from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.sub_account_postgreSQL_exceptions import *

from domain.interfaces.sub_account_service_interface import ISubAccountService
from domain.entities.sub_account import SubAccount
from infrastructure.databases.models.sub_account_model import SubAccountModel


def _to_domain(model: SubAccountModel) -> SubAccount:
    return SubAccount(
        id=model.id,
        team_id=model.team_id,
        username_encrypted=model.username_encrypted,
        email_encrypted=model.email_encrypted,
        password_encrypted=model.password_encrypted,
        site_link_encrypted=model.site_link_encrypted,
        required_perm_level_id=model.required_perm_level_id,
        dek_wrapped=model.dek_wrapped,
    )


class SubAccountService(ISubAccountService):
    def __init__(self, db: Session):
        self.db = db

    def CreateSubAccount(self, sub_account: SubAccount) -> SubAccount:
        try:
            subaccount_model = SubAccountModel(
                team_id = sub_account.team_id,
                username_encrypted = sub_account.username_encrypted,
                password_encrypted = sub_account.password_encrypted,
                email_encrypted = sub_account.email_encrypted,
                site_link_encrypted = sub_account.site_link_encrypted,
                required_perm_level_id = sub_account.required_perm_level_id,
                dek_wrapped = sub_account.dek_wrapped
            )

            self.db.add(subaccount_model)
            self.db.flush()
            self.db.refresh(subaccount_model)
            return _to_domain(subaccount_model)

        except IntegrityError:
            raise SubAccountAlreadyExistsException("SubAccount with the same name already exists.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCreationFailedException("Failed to create sub_account.")

    def GetSubAccountById(self, sub_account_id: uuid.UUID) -> SubAccount:
        try:
            subaccount_model = self.db.query(SubAccountModel).filter(SubAccountModel.id == sub_account_id).first()
            if not subaccount_model:
                raise SubAccountNotFoundException("SubAccount not found.")
            return _to_domain(subaccount_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve sub_account by ID.")

    def GetAllSubAccountsByTeamId(self, team_id: uuid.UUID) -> list[SubAccount]:
        try:
            subaccount_models = self.db.query(SubAccountModel).filter(SubAccountModel.team_id == team_id).all()
            return [_to_domain(model) for model in subaccount_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve subaccounts.")

    def UpdateSubAccountById(self, new_subaccount: SubAccount) -> SubAccount:
        try:
            subaccount_model = self.db.query(SubAccountModel).filter(SubAccountModel.id == new_subaccount.id).first()
            if not subaccount_model:
                raise SubAccountNotFoundException("SubAccount not found.")

            subaccount_model.username_encrypted = new_subaccount.username_encrypted
            subaccount_model.email_encrypted = new_subaccount.email_encrypted
            subaccount_model.password_encrypted = new_subaccount.password_encrypted
            subaccount_model.site_link_encrypted = new_subaccount.site_link_encrypted
            subaccount_model.required_perm_level_id = new_subaccount.required_perm_level_id
            self.db.flush()
            self.db.refresh(subaccount_model)
            return _to_domain(subaccount_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountUpdateException("Failed to update sub_account.")

    def DeleteSubAccountById(self, sub_account_id: uuid.UUID) -> dict[str, str]:
        try:
            subaccount_model = self.db.query(SubAccountModel).filter(SubAccountModel.id == sub_account_id).first()
            if not subaccount_model:
                raise SubAccountNotFoundException("SubAccount not found.")

            self.db.delete(subaccount_model)
            return {"message": "SubAccount deleted successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountDeletionException("Failed to delete sub_account.")

    def UpdateSubAccountDek(self, sub_account_id: uuid.UUID, dek_wrapped: str) -> SubAccount:
        try:
            subaccount_model = self.db.query(SubAccountModel).filter(SubAccountModel.id == sub_account_id).first()
            if not subaccount_model:
                raise SubAccountNotFoundException("SubAccount not found.")

            subaccount_model.dek_wrapped = dek_wrapped
            self.db.flush()
            self.db.refresh(subaccount_model)
            return _to_domain(subaccount_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountUpdateException("Failed to update sub_account data key.")
