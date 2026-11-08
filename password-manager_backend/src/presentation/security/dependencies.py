import uuid
from dataclasses import dataclass
from typing import Any

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.security.access_policy import AccessDenied, AccessPolicy
from infrastructure.auth.oidc_authentication import jwt_authentication
from infrastructure.databases.access_postgreSQL import AccessReader
from infrastructure.databases.database import get_db
from infrastructure.databases.models.user_model import UserModel


@dataclass(frozen=True)
class CurrentUser:
    id: uuid.UUID
    keycloak_id: uuid.UUID


def _subject(payload: dict[str, Any]) -> uuid.UUID:
    try:
        return uuid.UUID(str(payload["sub"]))
    except ValueError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid token subject"
        ) from e


def get_token_subject(
    payload: dict[str, Any] = Depends(jwt_authentication),
) -> uuid.UUID:
    """Keycloak id of the caller, for endpoints reachable before registration."""
    return _subject(payload)


def get_current_user(
    keycloak_id: uuid.UUID = Depends(get_token_subject),
    db: Session = Depends(get_db),
) -> CurrentUser:
    user_id = (
        db.query(UserModel.id).filter(UserModel.keycloak_id == keycloak_id).scalar()
    )
    if user_id is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User is not registered")
    return CurrentUser(id=user_id, keycloak_id=keycloak_id)


def get_access_policy(db: Session = Depends(get_db)) -> AccessPolicy:
    return AccessPolicy(AccessReader(db))


def forbidden() -> HTTPException:
    return HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")


__all__ = [
    "AccessDenied",
    "CurrentUser",
    "forbidden",
    "get_access_policy",
    "get_current_user",
    "get_token_subject",
]
