from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.crud import crud_member
from app.api.v1.deps import get_db
from app.api.v1.endpoints.oauth import read_users_me
import logging

logger = logging.getLogger(__name__)


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


@router.get(
    "/members/{member_id}/supervisor",
    response_model=schemas.member.Member,
    summary="Get supervisor of a member",
    tags=["Members"],
)
def get_member_supervisor(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_member = crud_member.get_member(db, member_id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    supervisor_id = getattr(db_member, "supervisor_id", None)
    if not supervisor_id:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    db_supervisor = crud_member.get_member(db, member_id=supervisor_id)
    if not db_supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return db_supervisor


@router.get(
    "/members/{member_id}/subordinates",
    response_model=List[schemas.member.Member],
    summary="Get subordinates of a member",
    tags=["Members"],
)
def get_member_subordinates(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    subordinates = crud_member.get_members_by_supervisor(db, supervisor_id=member_id)
    return subordinates


@router.get(
    "/members/{member_id}/top-manager",
    response_model=schemas.member.Member,
    summary="Get top manager for a member (recursive supervisor lookup)",
    tags=["Members"],
)
def get_top_manager(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    current_id = member_id
    visited = set()
    while True:
        db_member = crud_member.get_member(db, member_id=current_id)
        if not db_member:
            raise HTTPException(status_code=404, detail="Member not found")
        supervisor_id = getattr(db_member, "supervisor_id", None)
        if not supervisor_id or supervisor_id in visited:
            # No supervisor or circular reference, return current member as top manager
            return db_member
        visited.add(current_id)
        current_id = supervisor_id


@router.get(
    "/members/by-user/{user_id}",
    response_model=schemas.member.Member,
    summary="Get member by user id",
    tags=["Members"],
)
def get_member_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_member = crud_member.get_member_by_user_id(db, user_id=user_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found for user")
    return db_member


@router.get(
    "/members/{member_id}/org-tree",
    response_model=List[schemas.member.Member],
    summary="Get organization tree for a member (all subordinates recursively)",
    tags=["Members"],
)
def get_org_tree(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    def collect_subtree(mid, visited):
        if mid in visited:
            return []
        visited.add(mid)
        member = crud_member.get_member(db, member_id=mid)
        if not member:
            return []
        subs = crud_member.get_members_by_supervisor(db, supervisor_id=mid)
        subtree = [member]
        for sub in subs:
            subtree.extend(collect_subtree(sub.id, visited))
        return subtree

    return collect_subtree(member_id, set())
