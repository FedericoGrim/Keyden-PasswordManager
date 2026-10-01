import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SubAccountHistory:
    """Pure business object: a snapshot of a SubAccount's fields taken right
    before an update overwrote them."""

    sub_account_id: uuid.UUID
    password_encrypted: str
    username_encrypted: Optional[str] = None
    email_encrypted: Optional[str] = None
    site_link_encrypted: Optional[str] = None
    dek_wrapped: Optional[str] = None
    changed_by: Optional[uuid.UUID] = None
    changed_at: Optional[datetime] = None
    id: Optional[uuid.UUID] = None
