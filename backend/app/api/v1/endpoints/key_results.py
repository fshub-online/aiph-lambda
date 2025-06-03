from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.api.v1.deps import get_db
from app.crud import crud_key_result
from app.api.v1.endpoints.oauth import read_users_me
from app.models.key_result import KeyResultStatus, KeyResultPriority, KeyResultComplexity
import logging

logger = logging.getLogger(__name__)


router = APIRouter()

@router.get(
    "/key-results",
    response_model=List[schemas.key_result.KeyResult],
    summary="List key results",
    tags=["KeyResults"],
)
def read_key_results(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_key_result.get_key_results(db, skip=skip, limit=limit)

@router.post(
    "/key-results",
    response_model=schemas.key_result.KeyResult,
    status_code=status.HTTP_201_CREATED,
    summary="Create key result",
    tags=["KeyResults"],
)
def create_key_result(
    key_result_in: schemas.key_result.KeyResultCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_key_result.create_key_result(db, key_result_in=key_result_in)

@router.get(
    "/key-results/{key_result_id}",
    response_model=schemas.key_result.KeyResult,
    summary="Get key result by ID",
    tags=["KeyResults"],
)
def read_key_result(
    key_result_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_obj = crud_key_result.get_key_result(db, key_result_id=key_result_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Key result not found")
    return db_obj

@router.put(
    "/key-results/{key_result_id}",
    response_model=schemas.key_result.KeyResult,
    summary="Update key result",
    tags=["KeyResults"],
)
def update_key_result(
    key_result_id: int,
    key_result_in: schemas.key_result.KeyResultUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_obj = crud_key_result.get_key_result(db, key_result_id=key_result_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Key result not found")
    return crud_key_result.update_key_result(db, db_obj=db_obj, key_result_in=key_result_in)

@router.delete(
    "/key-results/{key_result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete key result",
    tags=["KeyResults"],
)
def delete_key_result(
    key_result_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_obj = crud_key_result.get_key_result(db, key_result_id=key_result_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Key result not found")
    crud_key_result.delete_key_result(db, db_obj=db_obj)
    return None

@router.get(
    "/key-result-enums/statuses",
    response_model=list[str],
    summary="Get all key result statuses",
    tags=["KeyResults"],
)
def get_key_result_statuses():
    return [e.value for e in KeyResultStatus]

@router.get(
    "/key-result-enums/priorities",
    response_model=list[str],
    summary="Get all key result priorities",
    tags=["KeyResults"],
)
def get_key_result_priorities():
    return [e.value for e in KeyResultPriority]

@router.get(
    "/key-result-enums/complexities",
    response_model=list[str],
    summary="Get all key result complexities",
    tags=["KeyResults"],
)
def get_key_result_complexities():
    return [e.value for e in KeyResultComplexity]
