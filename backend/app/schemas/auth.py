import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

NICKNAME_PATTERN = re.compile(r"[가-힣A-Za-z0-9_]{2,20}")
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64
PASSWORD_MAX_BYTES = 72


def clean_email(value: str) -> str:
    return value.strip().lower()


def clean_nickname(value: str) -> str:
    value = value.strip()
    if not NICKNAME_PATTERN.fullmatch(value):
        raise ValueError("닉네임은 2~20자의 한글, 영문, 숫자, 밑줄(_)만 사용할 수 있습니다.")
    return value


def check_password(value: str) -> str:
    if not PASSWORD_MIN_LENGTH <= len(value) <= PASSWORD_MAX_LENGTH:
        raise ValueError("비밀번호는 8자 이상 64자 이하이어야 합니다.")
    if len(value.encode("utf-8")) > PASSWORD_MAX_BYTES:
        raise ValueError("비밀번호가 너무 깁니다. 한글 등 여러 바이트 글자는 길이를 줄여주세요.")
    return value


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str

    _clean_email = field_validator("email", mode="before")(clean_email)
    _clean_nickname = field_validator("nickname")(clean_nickname)
    _check_password = field_validator("password")(check_password)


class LoginRequest(BaseModel):
    email: str
    password: str

    _clean_email = field_validator("email")(clean_email)


class NicknameUpdateRequest(BaseModel):
    nickname: str

    _clean_nickname = field_validator("nickname")(clean_nickname)


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nickname: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class NicknameChangeResponse(TokenResponse):
    user: UserInfo
