import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session


from config import Container
from presentation.security.dependencies import (
    CurrentUser,
    forbidden,
    get_current_user,
    get_token_subject,
)

from application.dto.user_dto import (
    CreateUserDTO,
    UpdateUserDTO,
    UserDTO,
    UserPublicDTO,
)

from infrastructure.databases.database import get_db

router = APIRouter()


# -------------------- CREATE --------------------
@router.post("/")
async def create_user(
    user_data: CreateUserDTO,
    request: Request,
    db: Session = Depends(get_db),
    token_subject: uuid.UUID = Depends(get_token_subject),
) -> dict[str, str | UserDTO]:
    if user_data.keycloak_id != token_subject:
        raise forbidden()
    container: Container = request.app.state.container
    create_user_use_case = container.user().CreateUserProvider(
        UserRepository__db=db,
        TeamRepository__db=db,
        TeamPermLevelRepository__db=db,
        TeamMembersRepository__db=db,
        UserTeamKeyRepository__db=db,
    )
    try:
        created_user: UserDTO = await create_user_use_case.execute(user_data)
        return {"message": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- GET --------------------
@router.get("/{keycloak_user_id}")
async def get_user_by_keycloak_id(
    keycloak_user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    token_subject: uuid.UUID = Depends(get_token_subject),
) -> dict[str, str | UserDTO]:
    if keycloak_user_id != token_subject:
        raise forbidden()
    container: Container = request.app.state.container
    get_user_use_case = container.user().GetUserByKeycloakIdProvider(
        UserRepository__db=db
    )
    try:
        user = get_user_use_case.execute(keycloak_user_id)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------- LOOKUP --------------------
@router.get("/lookup/{username}/{code}")
async def get_user_by_username_and_code(
    username: str,
    code: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> dict[str, str | UserPublicDTO]:
    container: Container = request.app.state.container
    get_user_use_case = container.user().GetUserByUsernameAndCodeProvider(
        UserRepository__db=db
    )
    try:
        user = get_user_use_case.execute(username, code)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/id/{user_id}")
async def get_user_by_id(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> dict[str, str | UserPublicDTO]:
    container: Container = request.app.state.container
    get_user_use_case = container.user().GetUserByIdProvider(UserRepository__db=db)
    try:
        user = get_user_use_case.execute(user_id)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------- UPDATE --------------------
@router.put("/{user_id}")
async def update_user_by_id(
    user_id: uuid.UUID,
    new_user: UpdateUserDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> dict[str, str]:
    if user_id not in (current_user.id, current_user.keycloak_id):
        raise forbidden()
    container: Container = request.app.state.container
    update_user_use_case = container.user().UpdateUserByIdProvider(
        UserRepository__db=db,
    )
    try:
        updated = await update_user_use_case.execute(user_id, new_user)
        if updated:
            return {"message": "User updated successfully"}
        raise HTTPException(status_code=400, detail="User update failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- DELETE --------------------
@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> dict[str, str]:
    if user_id not in (current_user.id, current_user.keycloak_id):
        raise forbidden()
    container: Container = request.app.state.container
    delete_user_use_case = container.user().DeleteUserByIdProvider(
        UserRepository__db=db,
    )
    try:
        deleted = await delete_user_use_case.execute(user_id)
        if deleted:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
