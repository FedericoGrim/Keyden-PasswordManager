from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid

from config import Container

from infrastructure.databases.database import get_db

from application.dto.team_perm_levels_dto import (
    CreateTeamPermLevelDTO,
    UpdateTeamPermLevelDTO,
)

router = APIRouter()


@router.post("/{team_id}")
async def CreateTeamPermLevel(
    new_perm_level: CreateTeamPermLevelDTO,
    user_interactor_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
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
):
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
):
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
    interactor_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
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
    user_interactor_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
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
