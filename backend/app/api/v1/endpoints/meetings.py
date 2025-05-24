from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.api.v1.deps import get_db
from app.crud import crud_meeting
from app.api.v1.endpoints.oauth import read_users_me
from app.schemas.meeting import MeetingWithIDs
from app.crud.crud_meeting import MeetingParticipant, MeetingObjective, MeetingKeyResult

router = APIRouter()


@router.get(
    "/meetings",
    response_model=List[MeetingWithIDs],
    summary="List meetings",
    tags=["Meetings"],
)
def read_meetings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meetings = crud_meeting.get_meetings(db, skip=skip, limit=limit)
    return [crud_meeting.get_meeting_with_related_ids(db, m.id) for m in meetings]


@router.get(
    "/meetings/{meeting_id}",
    response_model=MeetingWithIDs,
    summary="Get meeting by ID",
    tags=["Meetings"],
)
def read_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting_with_related_ids(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post(
    "/meetings",
    response_model=schemas.meeting.Meeting,
    status_code=status.HTTP_201_CREATED,
    summary="Create meeting",
    tags=["Meetings"],
)
def create_meeting(
    meeting_in: schemas.meeting.MeetingCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_meeting.create_meeting(db, meeting_in=meeting_in)


@router.put(
    "/meetings/{meeting_id}",
    response_model=schemas.meeting.Meeting,
    summary="Update meeting",
    tags=["Meetings"],
)
def update_meeting(
    meeting_id: int,
    meeting_in: schemas.meeting.MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return crud_meeting.update_meeting(db, db_meeting=db_meeting, meeting_in=meeting_in)


@router.delete(
    "/meetings/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meeting",
    tags=["Meetings"],
)
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    db_meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    crud_meeting.delete_meeting(db, db_meeting=db_meeting)
    return None


# Participants
@router.post(
    "/meetings/{meeting_id}/participants",
    response_model=schemas.meeting.MeetingParticipant,
    status_code=status.HTTP_201_CREATED,
    summary="Add participant",
    tags=["Meetings"],
)
def add_participant(
    meeting_id: int,
    participant_in: schemas.meeting.MeetingParticipantCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_meeting.add_participant(
        db, meeting_id=meeting_id, participant_in=participant_in
    )


@router.delete(
    "/meetings/{meeting_id}/participants/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove participant",
    tags=["Meetings"],
)
def remove_participant(
    meeting_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    crud_meeting.remove_participant(db, meeting_id=meeting_id, member_id=member_id)
    return None


@router.put(
    "/meetings/{meeting_id}/participants/{member_id}",
    response_model=schemas.meeting.MeetingParticipant,
    summary="Update participant association (replace member)",
    tags=["Meetings"],
)
def update_participant(
    meeting_id: int,
    member_id: int,
    participant_in: schemas.meeting.MeetingParticipantCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    crud_meeting.remove_participant(db, meeting_id=meeting_id, member_id=member_id)
    return crud_meeting.add_participant(
        db, meeting_id=meeting_id, participant_in=participant_in
    )


@router.get(
    "/meetings/{meeting_id}/participants",
    response_model=List[schemas.meeting.MeetingParticipant],
    summary="Get all participants for a meeting",
    tags=["Meetings"],
)
def get_meeting_participants(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    participants = db.query(MeetingParticipant).filter_by(meeting_id=meeting_id).all()
    return [schemas.meeting.MeetingParticipant.model_validate(p) for p in participants]


@router.get(
    "/meetings/{meeting_id}/participants/{member_id}",
    response_model=schemas.meeting.MeetingParticipant,
    summary="Get a specific participant for a meeting",
    tags=["Meetings"],
)
def get_meeting_participant(
    meeting_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    participant = (
        db.query(MeetingParticipant)
        .filter_by(meeting_id=meeting_id, member_id=member_id)
        .first()
    )
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return schemas.meeting.MeetingParticipant.model_validate(participant)


# Objectives
@router.post(
    "/meetings/{meeting_id}/objectives",
    response_model=schemas.meeting.MeetingObjective,
    status_code=status.HTTP_201_CREATED,
    summary="Add objective association",
    tags=["Meetings"],
)
def add_objective(
    meeting_id: int,
    objective_in: schemas.meeting.MeetingObjectiveCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_meeting.add_objective(
        db, meeting_id=meeting_id, objective_in=objective_in
    )


@router.delete(
    "/meetings/{meeting_id}/objectives/{objective_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove objective association",
    tags=["Meetings"],
)
def remove_objective(
    meeting_id: int,
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    crud_meeting.remove_objective(db, meeting_id=meeting_id, objective_id=objective_id)
    return None


@router.put(
    "/meetings/{meeting_id}/objectives/{objective_id}",
    response_model=schemas.meeting.MeetingObjective,
    summary="Update meeting-objective association note",
    tags=["Meetings"],
)
def update_objective_association(
    meeting_id: int,
    objective_id: int,
    update_in: schemas.meeting.MeetingObjectiveCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    obj = (
        db.query(crud_meeting.MeetingObjective)
        .filter_by(meeting_id=meeting_id, objective_id=objective_id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Association not found")
    obj.note = update_in.note
    db.commit()
    db.refresh(obj)
    return obj


@router.get(
    "/meetings/{meeting_id}/objectives",
    response_model=List[schemas.meeting.MeetingObjective],
    summary="Get all objective associations for a meeting",
    tags=["Meetings"],
)
def get_meeting_objectives(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    objectives = db.query(MeetingObjective).filter_by(meeting_id=meeting_id).all()
    return [schemas.meeting.MeetingObjective.model_validate(o) for o in objectives]


@router.get(
    "/meetings/{meeting_id}/objectives/{objective_id}",
    response_model=schemas.meeting.MeetingObjective,
    summary="Get a specific objective association for a meeting",
    tags=["Meetings"],
)
def get_meeting_objective(
    meeting_id: int,
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    objective = (
        db.query(MeetingObjective)
        .filter_by(meeting_id=meeting_id, objective_id=objective_id)
        .first()
    )
    if not objective:
        raise HTTPException(status_code=404, detail="Objective association not found")
    return schemas.meeting.MeetingObjective.model_validate(objective)


# Key Results
@router.post(
    "/meetings/{meeting_id}/key-results",
    response_model=schemas.meeting.MeetingKeyResult,
    status_code=status.HTTP_201_CREATED,
    summary="Add key result association",
    tags=["Meetings"],
)
def add_key_result(
    meeting_id: int,
    key_result_in: schemas.meeting.MeetingKeyResultCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    return crud_meeting.add_key_result(
        db, meeting_id=meeting_id, key_result_in=key_result_in
    )


@router.delete(
    "/meetings/{meeting_id}/key-results/{key_result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove key result association",
    tags=["Meetings"],
)
def remove_key_result(
    meeting_id: int,
    key_result_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    crud_meeting.remove_key_result(
        db, meeting_id=meeting_id, key_result_id=key_result_id
    )
    return None


@router.put(
    "/meetings/{meeting_id}/key-results/{key_result_id}",
    response_model=schemas.meeting.MeetingKeyResult,
    summary="Update meeting-key_result association note",
    tags=["Meetings"],
)
def update_key_result_association(
    meeting_id: int,
    key_result_id: int,
    update_in: schemas.meeting.MeetingKeyResultCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    kr = (
        db.query(crud_meeting.MeetingKeyResult)
        .filter_by(meeting_id=meeting_id, key_result_id=key_result_id)
        .first()
    )
    if not kr:
        raise HTTPException(status_code=404, detail="Association not found")
    kr.note = update_in.note
    db.commit()
    db.refresh(kr)
    return kr


@router.get(
    "/meetings/{meeting_id}/key-results",
    response_model=List[schemas.meeting.MeetingKeyResult],
    summary="Get all key result associations for a meeting",
    tags=["Meetings"],
)
def get_meeting_key_results(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    key_results = db.query(MeetingKeyResult).filter_by(meeting_id=meeting_id).all()
    return [schemas.meeting.MeetingKeyResult.model_validate(kr) for kr in key_results]


@router.get(
    "/meetings/{meeting_id}/key-results/{key_result_id}",
    response_model=schemas.meeting.MeetingKeyResult,
    summary="Get a specific key result association for a meeting",
    tags=["Meetings"],
)
def get_meeting_key_result(
    meeting_id: int,
    key_result_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    key_result = (
        db.query(MeetingKeyResult)
        .filter_by(meeting_id=meeting_id, key_result_id=key_result_id)
        .first()
    )
    if not key_result:
        raise HTTPException(status_code=404, detail="Key result association not found")
    return schemas.meeting.MeetingKeyResult.model_validate(key_result)


@router.get(
    "/meetings/{meeting_id}/associations",
    response_model=dict,
    summary="Get all associations for a meeting",
    tags=["Meetings"],
)
def get_meeting_associations(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(read_users_me),
):
    meeting = crud_meeting.get_meeting(db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    participants = db.query(MeetingParticipant).filter_by(meeting_id=meeting_id).all()
    objectives = db.query(MeetingObjective).filter_by(meeting_id=meeting_id).all()
    key_results = db.query(MeetingKeyResult).filter_by(meeting_id=meeting_id).all()
    return {
        "participants": [
            schemas.meeting.MeetingParticipant.model_validate(p) for p in participants
        ],
        "objectives": [
            schemas.meeting.MeetingObjective.model_validate(o) for o in objectives
        ],
        "key_results": [
            schemas.meeting.MeetingKeyResult.model_validate(kr) for kr in key_results
        ],
    }
