from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserInfo

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserInfo)
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    if db.scalar(select(User.id).where(User.email == body.email)) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "이미 사용 중인 이메일입니다.")
    if db.scalar(select(User.id).where(User.nickname == body.nickname)) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "이미 사용 중인 닉네임입니다.")

    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        nickname=body.nickname,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "이미 사용 중인 이메일 또는 닉네임입니다.")
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email))
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "이메일 또는 비밀번호가 맞지 않습니다.")
    return TokenResponse(access_token=create_access_token(user.id))


@router.post("/logout")
def logout(_current_user: User = Depends(get_current_user)):
    # JWT는 서버에 저장하지 않으므로 클라이언트가 토큰을 지우는 것으로 로그아웃합니다.
    return {"message": "로그아웃되었습니다."}
