import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from config import Container

from infrastructure.databases.database import get_db

from application.dto.team_member_dto import (
    TeamMemberDTO,
    CreateTeamMemberDTO,
    UpdateTeamMemberDTO,
    RemoveTeamMemberDTO,
)

router = APIRouter()


@router.post("/{team_id}/members")
async def api_add_member_to_team(
    interactor_id: uuid.UUID,
    CreateTeamMemberDTO: CreateTeamMemberDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamMemberDTO]:
    container: Container = request.app.state.container
    add_member_use_case = container.team_members().AddMemberToTeamProvider(
        TeamMembersRepository__db=db,
    )

    try:
        team_member = add_member_use_case.execute(interactor_id, CreateTeamMemberDTO)
        return {
            "message": "Member added to team successfully",
            "team_member": team_member,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/members/{member_id}")
async def api_get_team_member_by_id(
    member_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamMemberDTO]:
    container: Container = request.app.state.container
    get_member_use_case = container.team_members().GetTeamMemberByIdProvider(
        TeamMembersRepository__db=db
    )

    try:
        team_member = get_member_use_case.execute(member_id)
        return {
            "message": "Team member retrieved successfully",
            "team_member": team_member,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{team_id}/members")
async def api_get_team_members_by_team_id(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | list[TeamMemberDTO]]:
    container: Container = request.app.state.container
    get_members_use_case = container.team_members().GetTeamMembersByTeamIdProvider(
        TeamMembersRepository__db=db
    )

    try:
        team_members = get_members_use_case.execute(team_id)
        return {
            "message": "Team members retrieved successfully",
            "team_members": team_members,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{team_id}/members/{member_id}/role")
async def api_update_team_member_role(
    interactor_id: uuid.UUID,
    new_user_data: UpdateTeamMemberDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamMemberDTO]:
    container: Container = request.app.state.container
    update_role_use_case = container.team_members().UpdateTeamMemberRoleProvider(
        TeamMembersRepository__db=db,
    )

    try:
        updated_member = update_role_use_case.execute(interactor_id, new_user_data)
        return {
            "message": "Team member role updated successfully",
            "updated_member": updated_member,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{team_id}/members/{member_id}")
async def api_remove_member_from_team(
    interactor_id: uuid.UUID,
    team_member_to_delete: RemoveTeamMemberDTO,
    request: Request,
    db: Session = Depends(get_db),
):
    container: Container = request.app.state.container
    remove_member_use_case = container.team_members().RemoveMemberFromTeamProvider(
        TeamMembersRepository__db=db,
    )

    try:
        remove_member_use_case.execute(interactor_id, team_member_to_delete)
        return {"message": "Member removed from team successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
