from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from pydantic import UUID4

from config import Container

from infrastructure.databases.database import get_db

from application.dto.sub_account_dto import CreateSubAccountDTO, UpdateSubAccountDTO, SubAccountDTO, DeleteSubAccountDTO, RotateSubAccountDeksDTO

router = APIRouter()

@router.post("/{team_id}")
async def CreateSubAccount(
    interactor_id: uuid.UUID,
    subaccountObj: CreateSubAccountDTO,
    request: Request,
    db: Session = Depends(get_db),
):
    container: Container = request.app.state.container
    create_subaccount_use_case = container.subaccount().CreateSubAccountProvider(
        SubAccountRepository__db=db,
    )

    try:
        created = create_subaccount_use_case.execute(interactor_id, subaccountObj)
        if created:
            return {"message": "SubAccount created successfully", "subaccount_id": str(created.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{subaccount_id}")
async def GetSubAccountById(
    subaccount_id: uuid.UUID, 
    request: Request,
    db: Session = Depends(get_db), 
) -> dict[str, str | SubAccountDTO]:
    container: Container = request.app.state.container
    get_subaccount_use_case = container.subaccount().GetSubAccountByIdProvider(
        SubAccountRepository__db=db,
    )

    try:
        subaccount = get_subaccount_use_case.execute(subaccount_id)
        return {"message": "SubAccount retrieved successfully", "subaccount": subaccount}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e) + "\n SubAccount not found")

@router.get("/team/{team_id}")
async def GetAllSubAccountsByTeamId(
    team_id: uuid.UUID, 
    request: Request,
    db: Session = Depends(get_db), 
) -> dict[str, str | list[SubAccountDTO]]:
    container: Container = request.app.state.container
    get_subaccounts_use_case = container.subaccount().GetAllSubAccountsByTeamIdProvider(
        SubAccountRepository__db=db,
    )

    try:
        subaccounts = get_subaccounts_use_case.execute(team_id)
        return {"message": "SubAccounts retrieved successfully", "subaccounts": subaccounts}
    except Exception as e:
        raise HTTPException(status_code=404, detail= str(e) + "\n SubAccounts not found")

@router.put("/{subaccount_id}")
async def UpdateSubAccountById(
    interactor_id: uuid.UUID,
    subaccount_id: uuid.UUID,
    updated_data: UpdateSubAccountDTO,
    request: Request,
    db: Session = Depends(get_db),
):
    container: Container = request.app.state.container
    update_subaccount_use_case = container.subaccount().UpdateSubAccountByIdProvider(
        SubAccountRepository__db=db,
        SubAccountHistoryRepository__db=db,
    )

    try:
        if update_subaccount_use_case.execute(interactor_id, updated_data):
            return {"message": "SubAccount updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{subaccount_id}")
async def DeleteSubAccount(
    interactor_id: uuid.UUID,
    subaccount_id: UUID4, 
    request: Request,
    db: Session = Depends(get_db), 
):
    container: Container = request.app.state.container
    delete_subaccount_use_case = container.subaccount().DeleteSubAccountByIdProvider(
        SubAccountRepository__db=db,
    )

    delete_dto = DeleteSubAccountDTO(id=subaccount_id)
    try:
        if delete_subaccount_use_case.execute(interactor_id, delete_dto):
            return {"message": "SubAccount deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/team/{team_id}/rotate-deks")
async def RotateSubAccountDeks(
    interactor_id: uuid.UUID,
    team_id: uuid.UUID,
    rotation: RotateSubAccountDeksDTO,
    request: Request,
    db: Session = Depends(get_db),
):
    container: Container = request.app.state.container
    rotate_deks_use_case = container.subaccount().RotateSubAccountDeksProvider(
        SubAccountRepository__db=db,
        SubAccountHistoryRepository__db=db,
    )

    try:
        return rotate_deks_use_case.execute(interactor_id, rotation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
