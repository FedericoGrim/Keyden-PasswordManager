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

from domain.entities.team_perm_level import TeamPermLevel
from application.dto.team_perm_levels_dto import (
    CreateTeamPermLevelDTO,
    UpdateTeamPermLevelDTO,
)
from application.dto.team_perm_levels_dto import TeamPermLevelDTO

router = APIRouter()


@router.post("/{team_id}")
async def CreateTeamPermLevel(
    team_id: uuid.UUID,
    new_perm_level: CreateTeamPermLevelDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, TeamPermLevel]:
    user_interactor_id = current_user.id
    try:
        if new_perm_level.team_id != team_id:
            raise AccessDenied()
        policy.require_owner_or_empty_team(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    create_perm_level_use_case = (
        container.team_perm_levels().CreateTeamPermLevelProvider(
            TeamPermLevelRepository__db=db,
        )
    )

    try:
        result = create_perm_level_use_case.execute(
            perm_level=new_perm_level, user_interactor_id=user_interactor_id
        )
        return "Team perm level created successfully", result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{perm_level_id}")
async def GetTeamPermLevelById(
    perm_level_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, TeamPermLevelDTO]:
    try:
        policy.require_member_of_perm_level(current_user.id, perm_level_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_perm_level_use_case = container.team_perm_levels().GetTeamPermLevelByIdProvider(
        TeamPermLevelRepository__db=db,
    )

    try:
        result = get_perm_level_use_case.execute(perm_level_id)
        return "Team perm level retrieved successfully", result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/team/{team_id}")
async def GetAllTeamPermLevelsByTeamId(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, list[TeamPermLevelDTO]]:
    try:
        policy.require_member(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_perm_levels_use_case = (
        container.team_perm_levels().GetAllTeamPermLevelsByTeamIdProvider(
            TeamPermLevelRepository__db=db,
        )
    )

    try:
        perm_levels = get_perm_levels_use_case.execute(team_id)
        return "Team perm levels retrieved successfully", perm_levels
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{perm_level_id}")
async def UpdateTeamPermLevelById(
    perm_level_id: uuid.UUID,
    updated_data: UpdateTeamPermLevelDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, TeamPermLevelDTO]:
    interactor_id = current_user.id
    try:
        policy.require_owner_of_perm_level(current_user.id, perm_level_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    update_perm_level_use_case = (
        container.team_perm_levels().UpdateTeamPermLevelByIdProvider(
            TeamPermLevelRepository__db=db,
        )
    )

    try:
        result = update_perm_level_use_case.execute(
            perm_level_id=perm_level_id,
            new_perm_level=updated_data,
            user_interactor_id=interactor_id,
        )
        return "Team perm level updated successfully", result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{perm_level_id}")
async def DeleteTeamPermLevel(
    perm_level_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str] | None:
    user_interactor_id = current_user.id
    try:
        policy.require_owner_of_perm_level(current_user.id, perm_level_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    delete_perm_level_use_case = (
        container.team_perm_levels().DeleteTeamPermLevelByIdProvider(
            TeamPermLevelRepository__db=db,
        )
    )

    try:
        if delete_perm_level_use_case.execute(perm_level_id, user_interactor_id):
            return {"message": "Team perm level deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
