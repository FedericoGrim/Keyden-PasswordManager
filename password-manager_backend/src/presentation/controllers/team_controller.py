import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from config import Container

from application.dto.team_dto import (
    TeamDTO,
    CreateTeamDTO,
    UpdateTeamDTO,
    DeleteTeamDTO,
)

from infrastructure.databases.database import get_db

router = APIRouter()


# -------------------- CREATE --------------------
@router.post("/")
async def ApiCreateTeam(
    user_interactor_id: uuid.UUID,
    team: CreateTeamDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    container: Container = request.app.state.container
    create_team_use_case = container.team().CreateTeamProvider(
        TeamRepository__db=db,
    )

    try:
        new_team = create_team_use_case.execute(user_interactor_id, team)
        return {"message": "Team created successfully", "team_id": str(new_team.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- GET --------------------
@router.get("/{team_id}")
async def ApiGetTeamById(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamDTO]:
    container: Container = request.app.state.container
    get_team_use_case = container.team().GetTeamByIdProvider(TeamRepository__db=db)

    try:
        team = get_team_use_case.execute(team_id)
        return {"message": "Team retrieved successfully", "team": team}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}")
async def ApiGetTeamsByUserId(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | list[TeamDTO]]:
    container: Container = request.app.state.container
    get_teams_use_case = container.team().GetTeamsByUserIdProvider(
        TeamRepository__db=db
    )

    try:
        teams = get_teams_use_case.execute(user_id)
        return {"message": "Teams retrieved successfully", "teams": teams}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------- UPDATE --------------------
@router.put("/{team_id}")
async def ApiUpdateTeam(
    user_interactor_id: uuid.UUID,
    new_team_data: UpdateTeamDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamDTO]:
    container: Container = request.app.state.container
    update_team_use_case = container.team().UpdateTeamByIdProvider(
        TeamRepository__db=db,
    )

    try:
        updated_team = update_team_use_case.execute(user_interactor_id, new_team_data)
        return {"message": "Team updated successfully", "team": updated_team}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- DELETE --------------------
@router.delete("/{team_id}")
async def ApiDeleteTeam(
    interactor_id: uuid.UUID,
    team_to_delete: DeleteTeamDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    container: Container = request.app.state.container
    delete_team_use_case = container.team().DeleteTeamByIdProvider(
        TeamRepository__db=db,
    )

    try:
        deleted = delete_team_use_case.execute(interactor_id, team_to_delete)
        if deleted:
            return {"message": "Team deleted successfully"}
        raise HTTPException(status_code=400, detail="Team deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
