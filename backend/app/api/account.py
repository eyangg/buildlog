from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import NicknameChangeResponse, NicknameUpdateRequest, UserInfo

router = APIRouter(prefix="/api/account", tags=["account"])


@router.get("/info", response_model=UserInfo)
def get_account_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/nickname", response_model=NicknameChangeResponse)
def change_nickname(
    body: NicknameUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.nickname != current_user.nickname:
        taken = db.scalar(select(User.id).where(User.nickname == body.nickname))
        if taken is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, "이미 사용 중인 닉네임입니다.")

        current_user.nickname = body.nickname
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status.HTTP_409_CONFLICT, "이미 사용 중인 닉네임입니다.")
        db.refresh(current_user)

    return NicknameChangeResponse(
        access_token=create_access_token(current_user.id),
        user=UserInfo.model_validate(current_user),
    )
