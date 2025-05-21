from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.crud import crud_member
from app.api.v1.deps import get_db
from app.api.v1.endpoints.oauth import read_users_me

router = APIRouter()


@router.get(
    "/members",
    response_model=List[schemas.member.Member],
    summary="List members",
    tags=["Members"],
)
def read_members(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_member.get_members(db, skip=skip, limit=limit)


@router.post(
    "/members",
    response_model=schemas.member.Member,
    status_code=status.HTTP_201_CREATED,
    summary="Create member",
    tags=["Members"],
)
def create_member(
    member_in: schemas.member.MemberCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_member.create_member(db, member_in=member_in)


@router.get(
    "/members/{member_id}",
    response_model=schemas.member.Member,
    summary="Get member by ID",
    tags=["Members"],
)
def read_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_member = crud_member.get_member(db, member_id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.put(
    "/members/{member_id}",
    response_model=schemas.member.Member,
    summary="Update member",
    tags=["Members"],
)
def update_member(
    member_id: int,
    member_in: schemas.member.MemberUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_member = crud_member.get_member(db, member_id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud_member.update_member(db, db_member=db_member, member_in=member_in)


@router.delete(
    "/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete member",
    tags=["Members"],
)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_member = crud_member.get_member(db, member_id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    crud_member.delete_member(db, db_member=db_member)
    return None
