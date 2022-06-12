from datetime import timedelta, datetime

from fastapi import HTTPException, status, Request
from jose import jwt
from passlib.hash import pbkdf2_sha256

from app.config import settings


def verify_password(plain_password: str, encrypted_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, encrypted_password)


def encrypt_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def get_authorization_from_headers(request: Request) -> str:
    # refer https://jwt.io/introduction/
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无认证凭证, 请检查请求头中的 Authorization 字段")
    if "Bearer" not in authorization:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="认证凭证格式错误, Bearer <JWTToken>")
    token = authorization.removeprefix("Bearer ")
    return token


def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, "sub": subject}
    access_token = jwt.encode(payload, settings.SECRET_KEY)
    return access_token
