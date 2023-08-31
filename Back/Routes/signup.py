from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Authentication.hash_pwd import HashPassword
from Authentication.auth import authenticate
from Models.sqlData import Users
from Models.schema import UserValidate
from Routes.crud import createRegisteredUser, findUser, get_user_by_email, get_current_user
from Database.connection import get_db


UserType = {
    "is_admin": 1,
    "is_user": 0,
}

HASH = HashPassword()
signup = APIRouter()


@signup.post("/auth/signup")
async def SignUp(user: UserValidate,
                 db: AsyncSession = Depends(get_db)):
    user_exist = await get_user_by_email(email=user.email, db=db)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User with email already exist")

    create_user = await createRegisteredUser(username=user.username,
                                             email=user.email,
                                             hashed_password=user.password,
                                             is_admin=False,
                                             db=db)
    return create_user


@signup.get("/auth/view_users")
async def View_All_Users(token: str = Depends(authenticate),
                         db: AsyncSession = Depends(get_db)):
    if token["is_admin"] == UserType["is_user"]:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an Admin")
    results = await db.execute(select(Users))
    users = results.scalars().all()
    return users


@signup.get("/auth/view_user")
async def ViewUser(current_user: str = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    user = await findUser(username=current_user, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "password": user.hash_password
    }
