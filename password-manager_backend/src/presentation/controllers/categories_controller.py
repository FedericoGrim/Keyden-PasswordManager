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

from domain.entities.categories import Category
from application.dto.categories_dto import (
    CreateCategoryDTO,
    UpdateCategoryDTO,
    CategoryDTO,
)

router = APIRouter()


@router.post("/{team_id}")
async def CreateCategory(
    team_id: uuid.UUID,
    new_category: CreateCategoryDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, Category]:
    user_interactor_id = current_user.id
    try:
        if new_category.team_id != team_id:
            raise AccessDenied()
        policy.require_member(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    create_category_use_case = container.categories().CreateCategoriesProvider(
        CategoriesRepository__db=db,
    )

    try:
        result = create_category_use_case.execute(
            category=new_category, user_interactor_id=user_interactor_id
        )
        return "Category created successfully", result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}")
async def GetAllCategoriesByTeamId(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, list[CategoryDTO]]:
    try:
        policy.require_member(current_user.id, team_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_categories_use_case = container.categories().GetAllCategoriesByTeamIdProvider(
        CategoriesRepository__db=db,
    )

    try:
        categories = get_categories_use_case.execute(team_id)
        return "Categories retrieved successfully", categories
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{category_id}")
async def UpdateCategoryById(
    category_id: uuid.UUID,
    updated_data: UpdateCategoryDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, CategoryDTO]:
    interactor_id = current_user.id
    try:
        policy.require_member_of_category(current_user.id, category_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    update_category_use_case = container.categories().UpdateCategoryByIdProvider(
        CategoriesRepository__db=db,
    )

    try:
        result = update_category_use_case.execute(
            categoryId=category_id,
            new_category=updated_data,
            user_interactor_id=interactor_id,
        )
        return "Category updated successfully", result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}")
async def DeleteCategory(
    category_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> dict[str, str] | None:
    user_interactor_id = current_user.id
    try:
        policy.require_member_of_category(current_user.id, category_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    delete_category_use_case = container.categories().DeleteCategoryByIdProvider(
        CategoriesRepository__db=db,
    )

    try:
        if delete_category_use_case.execute(category_id, user_interactor_id):
            return {"message": "Category deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
