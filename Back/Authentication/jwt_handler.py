import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from Database.connection import SECRET_KEY
from starlette.config import Config


config = Config(".env")


def create_access_token(username: str, is_admin: bool) -> str:
    payload = {
        "username": username,
        "is_admin": is_admin,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, SECRET_KEY,
                       algorithm=config.get("ALGORITHM"))
    return token


def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No access token supplied")
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Token expired!")
        return data

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token") from e
