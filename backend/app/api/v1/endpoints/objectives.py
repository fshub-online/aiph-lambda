from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.api.v1.deps import get_db
from app.crud import crud_objective
from app.api.v1.endpoints.oauth import read_users_me

router = APIRouter()

@router.get(
    "/objectives",
    response_model=List[schemas.objective.Objective],
    summary="List objectives",
    tags=["Objectives"],
)
def read_objectives(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_objective.get_objectives(db, skip=skip, limit=limit)

@router.post(
    "/objectives",
    response_model=schemas.objective.Objective,
    status_code=status.HTTP_201_CREATED,
    summary="Create objective",
    tags=["Objectives"],
)
def create_objective(
    objective_in: schemas.objective.ObjectiveCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_objective.create_objective(db, objective_in=objective_in)

@router.get(
    "/objectives/{objective_id}",
    response_model=schemas.objective.Objective,
    summary="Get objective by ID",
    tags=["Objectives"],
)
def read_objective(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_obj = crud_objective.get_objective(db, objective_id=objective_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    return db_obj

@router.put(
    "/objectives/{objective_id}",
    response_model=schemas.objective.Objective,
    summary="Update objective",
    tags=["Objectives"],
)
def update_objective(
    objective_id: int,
    objective_in: schemas.objective.ObjectiveUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_obj = crud_objective.get_objective(db, objective_id=objective_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    return crud_objective.update_objective(db, db_obj=db_obj, objective_in=objective_in)

@router.delete(
    "/objectives/{objective_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete objective",
    tags=["Objectives"],
)
def delete_objective(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_obj = crud_objective.get_objective(db, objective_id=objective_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Objective not found")
    crud_objective.delete_objective(db, db_obj=db_obj)
    return None
