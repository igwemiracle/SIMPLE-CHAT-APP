from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from Authentication.hash_pwd import HashPassword
from Authentication.jwt_handler import create_access_token
from Database.connection import get_db
from Models.schema import Token, UserValidate
from Routes.crud import findUser

login = APIRouter()
HASH = HashPassword()


@login.post("/auth/login/", response_model=Token)
async def LoginPage(auth: UserValidate,
                    db: AsyncSession = Depends(get_db)) -> dict:
    user = await findUser(auth.username, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong Credentials")

    if HASH.verify_hash(auth.password, user.hash_password):
        access_token = create_access_token(
            user.username, user.is_admin)

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User do not exist."
    )
