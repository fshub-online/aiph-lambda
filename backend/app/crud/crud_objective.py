from sqlalchemy.orm import Session
from app.models.objective import Objective
from app.schemas.objective import ObjectiveCreate, ObjectiveUpdate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def get_objective(db: Session, objective_id: int) -> Optional[Objective]:
    return db.query(Objective).filter(Objective.id == objective_id).first()

def get_objectives(db: Session, skip: int = 0, limit: int = 100) -> List[Objective]:
    return db.query(Objective).offset(skip).limit(limit).all()

def create_objective(db: Session, objective_in: ObjectiveCreate) -> Objective:
    db_obj = Objective(**objective_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_objective(db: Session, db_obj: Objective, objective_in: ObjectiveUpdate) -> Objective:
    update_data = objective_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_objective(db: Session, db_obj: Objective) -> None:
    db.delete(db_obj)
    db.commit()
