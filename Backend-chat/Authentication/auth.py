from Authentication.jwt_handler import verify_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from Authentication.hash_pwd import HashPassword
from Models.sqlData import Users
from Database.connection import engine
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin/")
HASH = HashPassword()


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Sign in for access")
    decoded_token = verify_access_token(token)
    return decoded_token
