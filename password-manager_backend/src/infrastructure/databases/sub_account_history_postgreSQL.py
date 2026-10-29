from sqlalchemy.orm import Session
import uuid
import logging

from infrastructure.exceptions.sub_account_history_postgreSQL_exceptions import *

from domain.interfaces.sub_account_history_service_interface import ISubAccountHistoryService
from domain.entities.sub_account_history import SubAccountHistory
from infrastructure.databases.models.sub_account_history_model import SubAccountHistoryModel
from infrastructure.databases.models.sub_account_model import SubAccountModel


def _to_domain(model: SubAccountHistoryModel) -> SubAccountHistory:
    return SubAccountHistory(
        id=model.id,
        sub_account_id=model.sub_account_id,
        username_encrypted=model.username_encrypted,
        email_encrypted=model.email_encrypted,
        password_encrypted=model.password_encrypted,
        site_link_encrypted=model.site_link_encrypted,
        dek_wrapped=model.dek_wrapped,
        changed_by=model.changed_by,
        changed_at=model.changed_at,
    )


class SubAccountHistoryService(ISubAccountHistoryService):
    def __init__(self, db: Session):
        self.db = db

    def CreateHistoryEntry(self, entry: SubAccountHistory) -> SubAccountHistory:
        try:
            history_model = SubAccountHistoryModel(
                sub_account_id=entry.sub_account_id,
                username_encrypted=entry.username_encrypted,
                email_encrypted=entry.email_encrypted,
                password_encrypted=entry.password_encrypted,
                site_link_encrypted=entry.site_link_encrypted,
                dek_wrapped=entry.dek_wrapped,
                changed_by=entry.changed_by,
            )
            self.db.add(history_model)
            self.db.flush()
            self.db.refresh(history_model)
            return _to_domain(history_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountHistoryCreationFailedException("Failed to create sub_account history entry.")

    def GetHistoryBySubAccountId(self, sub_account_id: uuid.UUID) -> list[SubAccountHistory]:
        try:
            history_models = (
                self.db.query(SubAccountHistoryModel)
                .filter(SubAccountHistoryModel.sub_account_id == sub_account_id)
                .order_by(SubAccountHistoryModel.changed_at.desc())
                .all()
            )
            return [_to_domain(model) for model in history_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountHistoryRetrievalException("Failed to retrieve sub_account history.")

    def GetHistoryByTeamId(self, team_id: uuid.UUID) -> list[SubAccountHistory]:
        try:
            history_models = (
                self.db.query(SubAccountHistoryModel)
                .join(SubAccountModel, SubAccountModel.id == SubAccountHistoryModel.sub_account_id)
                .filter(SubAccountModel.team_id == team_id)
                .all()
            )
            return [_to_domain(model) for model in history_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountHistoryRetrievalException("Failed to retrieve sub_account history for team.")

    def UpdateHistoryDek(self, history_id: uuid.UUID, dek_wrapped: str) -> SubAccountHistory:
        try:
            history_model = self.db.query(SubAccountHistoryModel).filter(SubAccountHistoryModel.id == history_id).first()
            if not history_model:
                raise SubAccountHistoryNotFoundException("SubAccount history entry not found.")

            history_model.dek_wrapped = dek_wrapped
            self.db.flush()
            self.db.refresh(history_model)
            return _to_domain(history_model)

        except SubAccountHistoryNotFoundException:
            raise

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountHistoryDekUpdateException("Failed to update sub_account history data key.")
