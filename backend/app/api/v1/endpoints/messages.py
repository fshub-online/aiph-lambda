from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.message import Message, MessageCreate, MessageUpdate
from app.crud import crud_message
from app.api.v1.deps import get_db
from app.api.v1.endpoints.oauth import read_users_me
from app.models.message_priority import MessagePriority

router = APIRouter()


@router.get(
    "/messages",
    response_model=List[Message],
    summary="List messages",
    tags=["Messages"],
)
def list_messages(db: Session = Depends(get_db)):
    return crud_message.get_messages(db)


@router.get(
    "/messages/{message_id}",
    response_model=Message,
    summary="Get message",
    tags=["Messages"],
)
def get_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud_message.get_message(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message


@router.post(
    "/messages",
    response_model=Message,
    status_code=status.HTTP_201_CREATED,
    summary="Create message",
    tags=["Messages"],
)
def create_message(
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(read_users_me),
):
    return crud_message.create_message(db, message_in)


@router.put(
    "/messages/{message_id}",
    response_model=Message,
    summary="Update message",
    tags=["Messages"],
)
def update_message(
    message_id: int,
    message_in: MessageUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(read_users_me),
):
    db_message = crud_message.get_message(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return crud_message.update_message(db, db_message, message_in)


@router.delete(
    "/messages/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete message",
    tags=["Messages"],
)
def delete_message(
    message_id: int, db: Session = Depends(get_db), current_user=Depends(read_users_me)
):
    db_message = crud_message.get_message(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    crud_message.delete_message(db, db_message)
    return None


@router.get("/message-priorities", response_model=list[str], tags=["Messages"], summary="Get possible message priorities")
def get_message_priorities():
    """
    Get all possible values for MessagePriority enum.
    """
    return [priority.value for priority in MessagePriority]
