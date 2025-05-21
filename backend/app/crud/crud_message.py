from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate
from typing import List, Optional


def get_message(db: Session, message_id: int) -> Optional[Message]:
    return db.query(Message).filter(Message.id == message_id).first()


def get_messages(db: Session, skip: int = 0, limit: int = 100) -> List[Message]:
    return db.query(Message).offset(skip).limit(limit).all()


def create_message(db: Session, message_in: MessageCreate) -> Message:
    db_message = Message(**message_in.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(
    db: Session, db_message: Message, message_in: MessageUpdate
) -> Message:
    for field, value in message_in.dict(exclude_unset=True).items():
        setattr(db_message, field, value)
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, db_message: Message) -> None:
    db.delete(db_message)
    db.commit()
