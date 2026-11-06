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

from application.dto.user_favorite_dto import CreateFavoriteDTO, FavoriteDTO

from infrastructure.databases.database import get_db

router = APIRouter()


# -------------------- CREATE --------------------
@router.post("/")
async def add_favorite(
    new_favorite: CreateFavoriteDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | FavoriteDTO]:
    try:
        policy.require_self(current_user.id, new_favorite.user_id)
        policy.require_member_of_sub_account(
            current_user.id, new_favorite.sub_account_id
        )
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    add_favorite_use_case = container.user_favorites().AddFavoriteProvider(
        UserFavoriteRepository__db=db,
    )
    try:
        favorite = add_favorite_use_case.execute(new_favorite)
        return {"message": "Favorite added successfully", "favorite": favorite}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- GET --------------------
@router.get("/user/{user_id}")
async def get_favorites_by_user_id(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str | list[FavoriteDTO]]:
    try:
        policy.require_self(current_user.id, user_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_favorites_use_case = container.user_favorites().GetFavoritesByUserIdProvider(
        UserFavoriteRepository__db=db,
    )
    try:
        favorites = get_favorites_use_case.execute(user_id)
        return {"message": "Favorites retrieved successfully", "favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------- DELETE --------------------
@router.delete("/{user_id}/{sub_account_id}")
async def remove_favorite(
    user_id: uuid.UUID,
    sub_account_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str]:
    try:
        policy.require_self(current_user.id, user_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    remove_favorite_use_case = container.user_favorites().RemoveFavoriteProvider(
        UserFavoriteRepository__db=db,
    )
    try:
        return remove_favorite_use_case.execute(user_id, sub_account_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
