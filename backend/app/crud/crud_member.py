from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def get_member(db: Session, member_id: int) -> Optional[Member]:
    return db.query(Member).filter(Member.id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100) -> List[Member]:
    return db.query(Member).offset(skip).limit(limit).all()

def create_member(db: Session, member_in: MemberCreate) -> Member:
    db_member = Member(**member_in.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, db_member: Member, member_in: MemberUpdate) -> Member:
    for field, value in member_in.dict(exclude_unset=True).items():
        setattr(db_member, field, value)
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, db_member: Member) -> None:
    db.delete(db_member)
    db.commit()
