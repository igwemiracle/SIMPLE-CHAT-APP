import time
from fastapi import HTTPException, status
from jose import jwt
from jwt.exceptions import DecodeError
from Database.connection import SECRET_KEY
from starlette.config import Config


config = Config(".env")


def create_access_token(username: str, is_admin: bool) -> str:
    payload = {
        "username": username,
        "is_admin": is_admin,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, SECRET_KEY,
                       algorithm=config.get("ALGORITHM"))
    return token


def verify_access_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=config.get("ALGORITHM"))
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except DecodeError as e:
        print("JWT Decode Error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
