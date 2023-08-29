from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from Authentication.hash_pwd import HashPassword
from Authentication.auth import oauth2_scheme
from Authentication.jwt_handler import verify_access_token
from Database.connection import get_db
from Models.sqlData import Users

HASH = HashPassword()


async def createRegisteredUser(username: str, email: str, hashed_password: str, is_admin: bool, db: AsyncSession):
    hash_this_pwd = HASH.create_hash(hashed_password)
    new_user = Users(username=username, email=email,
                     hash_password=hash_this_pwd, is_admin=is_admin)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sign in for access")

    decoded_token = verify_access_token(token)
    return decoded_token["username"]


async def findUserExist(email: str, db: AsyncSession = Depends(get_db)):
    query = select(Users).where(Users.email == email)
    result = await db.execute(query)
    return result.scalar()


async def findUser(username: str, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM signin WHERE username=:username")
    result = await db.execute(query, {"username": username})
    return result.fetchone()


# ------ CONNECTED TO "" IN user.py USER FOR ACCESS TOKEN---------
# async def findUser(username: str, db: AsyncSession = Depends(get_db)):
#     query = select(Users).where(Users.username == username)
#     result = await db.execute(query)
#     return result.scalar()
