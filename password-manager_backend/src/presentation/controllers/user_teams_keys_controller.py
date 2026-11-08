import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from config import Container
from application.security.access_policy import AccessDenied, AccessPolicy
from presentation.security.dependencies import (
    CurrentUser,
    forbidden,
    get_access_policy,
    get_current_user,
)

from infrastructure.databases.database import get_db

from application.dto.user_teams_keys_dto import (
    UserTeamKeyDTO,
    CreateUserTeamKeyDTO,
    UpdateUserTeamKeyDTO,
    RemoveUserTeamKeyDTO,
)

router = APIRouter()


@router.post("/{team_id}/keys")
async def api_add_user_teams_key(
    team_id: uuid.UUID,
    CreateUserTeamKeyDTO: CreateUserTeamKeyDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | UserTeamKeyDTO]:
    interactor_id = current_user.id
    try:
        if CreateUserTeamKeyDTO.team_id != team_id:
            raise AccessDenied()
        policy.require_owner(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    add_key_use_case = container.user_teams_keys().AddUserTeamKeyProvider(
        UserTeamKeyRepository__db=db,
    )

    try:
        user_teams_key = add_key_use_case.execute(interactor_id, CreateUserTeamKeyDTO)
        return {"message": "Key added successfully", "user_teams_key": user_teams_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/keys/{key_id}")
async def api_get_user_teams_key_by_id(
    key_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | UserTeamKeyDTO]:
    try:
        policy.require_own_key(current_user.id, key_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_key_use_case = container.user_teams_keys().GetUserTeamKeyByIdProvider(
        UserTeamKeyRepository__db=db
    )

    try:
        user_teams_key = get_key_use_case.execute(key_id)
        return {
            "message": "Key retrieved successfully",
            "user_teams_key": user_teams_key,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{team_id}/keys")
async def api_get_user_teams_keys_by_team_id(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | list[UserTeamKeyDTO]]:
    try:
        policy.require_member(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_keys_use_case = container.user_teams_keys().GetUserTeamKeysByTeamIdProvider(
        UserTeamKeyRepository__db=db
    )

    try:
        user_teams_keys = get_keys_use_case.execute(team_id)
        return {
            "message": "Keys retrieved successfully",
            "user_teams_keys": user_teams_keys,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}/keys")
async def api_get_user_teams_keys_by_user_id(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | list[UserTeamKeyDTO]]:
    try:
        policy.require_self(current_user.id, user_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_keys_use_case = container.user_teams_keys().GetUserTeamKeysByUserIdProvider(
        UserTeamKeyRepository__db=db
    )

    try:
        user_teams_keys = get_keys_use_case.execute(user_id)
        return {
            "message": "Keys retrieved successfully",
            "user_teams_keys": user_teams_keys,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{team_id}/keys/{user_id}")
async def api_update_user_teams_key(
    user_id: uuid.UUID,
    team_id: uuid.UUID,
    new_key_data: UpdateUserTeamKeyDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | UserTeamKeyDTO]:
    interactor_id = current_user.id
    try:
        if new_key_data.team_id != team_id or new_key_data.user_id != user_id:
            raise AccessDenied()
        policy.require_owner(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    update_key_use_case = container.user_teams_keys().UpdateUserTeamKeyProvider(
        UserTeamKeyRepository__db=db,
    )

    try:
        updated_key = update_key_use_case.execute(interactor_id, new_key_data)
        return {"message": "Key updated successfully", "updated_key": updated_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{team_id}/keys/{user_id}")
async def api_remove_user_teams_key(
    user_id: uuid.UUID,
    team_id: uuid.UUID,
    key_to_delete: RemoveUserTeamKeyDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str]:
    interactor_id = current_user.id
    try:
        if key_to_delete.team_id != team_id or key_to_delete.user_id != user_id:
            raise AccessDenied()
        if user_id != current_user.id:
            policy.require_owner(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    remove_key_use_case = container.user_teams_keys().RemoveUserTeamKeyProvider(
        UserTeamKeyRepository__db=db,
    )

    try:
        remove_key_use_case.execute(interactor_id, key_to_delete)
        return {"message": "Key removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
