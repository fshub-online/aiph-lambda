from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.api.v1.deps import get_db
from app.crud import crud_user
from app.schemas.user import User as UserSchema, UserPasswordChange
from app.core.config import settings
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.OAUTH2_TOKEN_URL)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, user_name: str, password: str):
    user = (
        db.query(crud_user.User).filter(crud_user.User.user_name == user_name).first()
        if hasattr(crud_user, "User")
        else crud_user.get_user_by_email(db, email=user_name)
    )
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post(
    "/oauth/token",
    summary="Obtain access token",
    tags=["OAuth2"],
    response_description="JWT access token"
)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Obtain a JWT access token by providing user credentials (user_name and password).
    - **Returns**: access token and token type
    - **Raises**: 401 if authentication fails
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.user_name})
    refresh_token = create_refresh_token(data={"sub": user.user_name})
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="none",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES,
        path="/"
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/oauth/refresh",
    summary="Refresh access token",
    tags=["OAuth2"],
    response_description="New JWT access token"
)
def refresh_access_token(
    refresh_token: str = Cookie(None),
):
    """
    Refresh the JWT access token using a valid refresh token (from cookie).
    - **Returns**: new access token and token type
    - **Raises**: 401 if token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not refresh_token:
        raise credentials_exception
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_name is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Issue a new access token
    new_token = create_access_token(data={"sub": user_name})
    return {"access_token": new_token, "token_type": "bearer"}


@router.get(
    "/oauth/me",
    response_model=UserSchema,
    summary="Get current user info",
    tags=["OAuth2"],
    response_description="Current authenticated user info"
)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get information about the current authenticated user.
    - **Returns**: user details
    - **Raises**: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = (
        db.query(crud_user.User).filter(crud_user.User.user_name == user_name).first()
        if hasattr(crud_user, "User")
        else None
    )
    if user is None:
        raise credentials_exception
    return user

@router.patch(
    "/oauth/me",
    response_model=UserSchema,
    summary="Update current user profile",
    tags=["OAuth2"],
    response_description="Updated user profile"
)
def update_own_profile(
    user_update: dict, 
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(read_users_me)
):
    """
    Update the profile of the currently authenticated user.
    - **Requires authentication**
    """
    user_id = current_user.id
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert dict to UserUpdate model
    from app.schemas.user import UserUpdate
    user_update_model = UserUpdate(**user_update)
    
    return crud_user.update_user(db, db_user=db_user, user_in=user_update_model)


@router.post(
    "/oauth/me/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change current user password",
    tags=["OAuth2"],
    response_description="Password changed successfully"
)
def change_own_password(
    password_data: UserPasswordChange,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(read_users_me)
):
    """
    Change the password of the currently authenticated user.
    - **Requires authentication**
    - **current_password must match the current password**
    """
    user_id = current_user.id
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not pwd_context.verify(password_data.current_password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    hashed_password = pwd_context.hash(password_data.new_password)
    db_user.hashed_password = hashed_password
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Password updated successfully"}
