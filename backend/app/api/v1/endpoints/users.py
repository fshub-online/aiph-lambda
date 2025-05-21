from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.api.v1.deps import get_db
from app.crud import crud_user
from app.api.v1.endpoints.oauth import read_users_me

router = APIRouter()


@router.get(
    "/users",
    response_model=List[schemas.user.User],
    summary="List users",
    tags=["Users"],
    response_description="List of users"
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.user.User = Depends(read_users_me)):
    """
    Retrieve a list of users.
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of users to return
    - **Requires authentication**
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.post(
    "/users",
    response_model=schemas.user.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    tags=["Users"],
    response_description="Created user"
)
def create_user(user_in: schemas.user.UserCreate, db: Session = Depends(get_db), current_user: schemas.user.User = Depends(read_users_me)):
    """
    Create a new user.
    - **Requires authentication**
    - **user_name and email must be unique**
    """
    db_user_by_email = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user_by_username = db.query(crud_user.User).filter(
        crud_user.User.user_name == user_in.user_name).first() if hasattr(crud_user, 'User') else None
    if db_user_by_username:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud_user.create_user(db, user_in=user_in)


@router.get(
    "/users/{user_id}",
    response_model=schemas.user.User,
    summary="Get user by ID",
    tags=["Users"],
    response_description="User details"
)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.user.User = Depends(read_users_me)):
    """
    Get a user by their ID.
    - **Requires authentication**
    - **404** if user not found
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put(
    "/users/{user_id}",
    response_model=schemas.user.User,
    summary="Update user",
    tags=["Users"],
    response_description="Updated user"
)
def update_user(user_id: int, user_in: schemas.user.UserUpdate, db: Session = Depends(get_db), current_user: schemas.user.User = Depends(read_users_me)):
    """
    Update a user's information.
    - **Requires authentication**
    - **404** if user not found
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db, db_user=db_user, user_in=user_in)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    tags=["Users"],
    response_description="User deleted"
)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.user.User = Depends(read_users_me)):
    """
    Delete a user by their ID.
    - **Requires authentication**
    - **404** if user not found
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, db_user=db_user)
    return None
