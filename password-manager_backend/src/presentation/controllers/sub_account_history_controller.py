from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid

from config import Container
from application.security.access_policy import AccessDenied, AccessPolicy
from presentation.security.dependencies import (
    CurrentUser,
    forbidden,
    get_access_policy,
    get_current_user,
)

from infrastructure.databases.database import get_db

from application.dto.sub_account_history_dto import SubAccountHistoryDTO

router = APIRouter()


@router.get("/{subaccount_id}")
async def GetSubAccountHistoryBySubAccountId(
    subaccount_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | list[SubAccountHistoryDTO]]:
    try:
        policy.require_member_of_sub_account(current_user.id, subaccount_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_history_use_case = (
        container.sub_account_history().GetSubAccountHistoryBySubAccountIdProvider(
            SubAccountHistoryRepository__db=db,
        )
    )

    try:
        history = get_history_use_case.execute(subaccount_id)
        return {
            "message": "SubAccount history retrieved successfully",
            "history": history,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/team/{team_id}")
async def GetSubAccountHistoryByTeamId(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | list[SubAccountHistoryDTO]]:
    try:
        policy.require_member(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_history_use_case = (
        container.sub_account_history().GetSubAccountHistoryByTeamIdProvider(
            SubAccountHistoryRepository__db=db,
        )
    )

    try:
        history = get_history_use_case.execute(team_id)
        return {
            "message": "SubAccount history retrieved successfully",
            "history": history,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
