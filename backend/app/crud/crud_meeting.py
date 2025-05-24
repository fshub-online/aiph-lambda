from sqlalchemy.orm import Session
from app.models.meeting import (
    Meeting,
    MeetingParticipant,
    MeetingObjective,
    MeetingKeyResult,
)
from app.schemas.meeting import (
    MeetingCreate,
    MeetingUpdate,
    MeetingParticipantCreate,
    MeetingObjectiveCreate,
    MeetingKeyResultCreate,
)
from typing import List, Optional


def get_meeting(db: Session, meeting_id: int) -> Optional[Meeting]:
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()


def get_meetings(db: Session, skip: int = 0, limit: int = 100) -> List[Meeting]:
    return db.query(Meeting).offset(skip).limit(limit).all()


def create_meeting(db: Session, meeting_in: MeetingCreate) -> Meeting:
    db_meeting = Meeting(**meeting_in.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def update_meeting(
    db: Session, db_meeting: Meeting, meeting_in: MeetingUpdate
) -> Meeting:
    for field, value in meeting_in.dict(exclude_unset=True).items():
        setattr(db_meeting, field, value)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def delete_meeting(db: Session, db_meeting: Meeting) -> None:
    db.delete(db_meeting)
    db.commit()


def add_participant(
    db: Session, meeting_id: int, participant_in: MeetingParticipantCreate
) -> MeetingParticipant:
    participant = MeetingParticipant(
        meeting_id=meeting_id, member_id=participant_in.member_id
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def remove_participant(db: Session, meeting_id: int, member_id: int) -> None:
    db.query(MeetingParticipant).filter_by(
        meeting_id=meeting_id, member_id=member_id
    ).delete()
    db.commit()


def add_objective(
    db: Session, meeting_id: int, objective_in: MeetingObjectiveCreate
) -> MeetingObjective:
    obj = MeetingObjective(meeting_id=meeting_id, **objective_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def remove_objective(db: Session, meeting_id: int, objective_id: int) -> None:
    db.query(MeetingObjective).filter_by(
        meeting_id=meeting_id, objective_id=objective_id
    ).delete()
    db.commit()


def add_key_result(
    db: Session, meeting_id: int, key_result_in: MeetingKeyResultCreate
) -> MeetingKeyResult:
    kr = MeetingKeyResult(meeting_id=meeting_id, **key_result_in.dict())
    db.add(kr)
    db.commit()
    db.refresh(kr)
    return kr


def remove_key_result(db: Session, meeting_id: int, key_result_id: int) -> None:
    db.query(MeetingKeyResult).filter_by(
        meeting_id=meeting_id, key_result_id=key_result_id
    ).delete()
    db.commit()


def get_meeting_with_related_ids(db: Session, meeting_id: int):
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        return None
    participant_ids = [
        row.member_id
        for row in db.query(MeetingParticipant.member_id).filter_by(
            meeting_id=meeting_id
        )
    ]
    objective_ids = [
        row.objective_id
        for row in db.query(MeetingObjective.objective_id).filter_by(
            meeting_id=meeting_id
        )
    ]
    key_result_ids = [
        row.key_result_id
        for row in db.query(MeetingKeyResult.key_result_id).filter_by(
            meeting_id=meeting_id
        )
    ]
    # Return a dict with meeting fields and related IDs
    meeting_dict = meeting.__dict__.copy()
    # Remove SQLAlchemy internal state if present
    meeting_dict.pop("_sa_instance_state", None)
    meeting_dict["participant_ids"] = participant_ids
    meeting_dict["objective_ids"] = objective_ids
    meeting_dict["key_result_ids"] = key_result_ids
    return meeting_dict
