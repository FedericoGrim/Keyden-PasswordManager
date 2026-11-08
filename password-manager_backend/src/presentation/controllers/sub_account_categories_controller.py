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

from application.dto.sub_account_categories_dto import (
    CreateSubAccountCategoryDTO,
    SubAccountCategoriesDTO,
)

from infrastructure.databases.database import get_db
from domain.entities.sub_account_categories import SubAccountCategories

router = APIRouter()


@router.post("/")
async def CreateSubAccauntCategory(
    new_subacc_category: CreateSubAccountCategoryDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, SubAccountCategories]:
    try:
        team_id = policy.require_member_of_sub_account(
            current_user.id, new_subacc_category.sub_account_id
        )
        if policy.reader.team_of_category(new_subacc_category.category_id) != team_id:
            raise AccessDenied()
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    create_subacc_category_use_case = (
        container.sub_account_categories().CreateSubAccountCategoryProvider(
            SubAccountCategoriesRepository__db=db,
        )
    )

    try:
        result = create_subacc_category_use_case.execute(
            new_subacc_category=new_subacc_category
        )
        return "SubAccountCategory created successfully", result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{subaccount_id}")
async def GetAllCategoriesBySubAccountId(
    subaccount_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, list[SubAccountCategoriesDTO]]:
    try:
        policy.require_member_of_sub_account(current_user.id, subaccount_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    get_subacc_categories_use_case = (
        container.sub_account_categories().GetAllCategoriesBySubAccountIdProvider(
            SubAccountCategoriesRepository__db=db,
        )
    )

    try:
        subacc_categories = get_subacc_categories_use_case.execute(subaccount_id)
        return "SubAccountCategories retrieved successfully", subacc_categories
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{subaccount_id}/{category_id}")
async def DeleteSubAccauntCategory(
    category_id: uuid.UUID,
    subaccount_id: uuid.UUID,
    subacc_category_to_delete: SubAccountCategoriesDTO,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    policy: AccessPolicy = Depends(get_access_policy),
) -> tuple[str, bool]:
    try:
        if (
            subacc_category_to_delete.sub_account_id != subaccount_id
            or subacc_category_to_delete.category_id != category_id
        ):
            raise AccessDenied()
        policy.require_member_of_sub_account(current_user.id, subaccount_id)
    except AccessDenied:
        raise forbidden()
    container: Container = request.app.state.container
    delete_subacc_category_use_case = (
        container.sub_account_categories().DeleteSubAccountCategoryProvider(
            SubAccountCategoriesRepository__db=db,
        )
    )

    try:
        result = delete_subacc_category_use_case.execute(subacc_category_to_delete)
        return "SubAccountCategory deleted successfully", result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
