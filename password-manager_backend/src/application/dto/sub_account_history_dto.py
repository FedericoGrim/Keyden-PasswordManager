from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class SubAccountHistoryDTO(BaseModel):
    id: UUID4
    sub_account_id: UUID4
    username_encrypted: Optional[str]
    email_encrypted: Optional[str]
    password_encrypted: str
    site_link_encrypted: Optional[str]
    dek_wrapped: Optional[str]
    changed_by: Optional[UUID4]
    changed_at: datetime
