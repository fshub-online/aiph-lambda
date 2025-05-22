from sqlalchemy.orm import Session
from app.models.key_result import KeyResult
from app.schemas.key_result import KeyResultCreate, KeyResultUpdate
from typing import List, Optional

def get_key_result(db: Session, key_result_id: int) -> Optional[KeyResult]:
    return db.query(KeyResult).filter(KeyResult.id == key_result_id).first()

def get_key_results(db: Session, skip: int = 0, limit: int = 100) -> List[KeyResult]:
    return db.query(KeyResult).offset(skip).limit(limit).all()

def create_key_result(db: Session, key_result_in: KeyResultCreate) -> KeyResult:
    db_obj = KeyResult(**key_result_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_key_result(db: Session, db_obj: KeyResult, key_result_in: KeyResultUpdate) -> KeyResult:
    update_data = key_result_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_key_result(db: Session, db_obj: KeyResult) -> None:
    db.delete(db_obj)
    db.commit()
