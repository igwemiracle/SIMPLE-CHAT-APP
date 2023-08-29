from fastapi import Depends, HTTPException, status, APIRouter
from Authentication.hash_pwd import HashPassword
from Authentication.jwt_handler import verify_access_token
from Database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Authentication.auth import authenticate
from Models.sqlData import Users
from Models.schema import UserValidate, Token
from Routes.crud import createRegisteredUser, findUser, findUserExist, get_current_user
from Authentication.jwt_handler import create_access_token


UserType = {
    "is_admin": 1,
    "is_user": 0,
}

HASH = HashPassword()
user_route = APIRouter()


@user_route.post("/auth/signup")
async def SignUp(user: UserValidate,
                 db: AsyncSession = Depends(get_db)):
    user_exist = await findUserExist(email=user.email, db=db)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User with email already exist")

    create_user = await createRegisteredUser(username=user.username,
                                             email=user.email,
                                             hashed_password=user.password,
                                             is_admin=False,
                                             db=db)
    return create_user


@user_route.post("/auth/signin/", response_model=Token)
async def SignIn(auth: UserValidate,
                 db: AsyncSession = Depends(get_db)) -> dict:
    user = await findUser(auth.username, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong Credentials")

    if HASH.verify_hash(auth.password, user.hash_password):
        access_token = create_access_token(user.username, user.is_admin)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User do not exist."
    )


@user_route.get("/auth/view_users")
async def ViewAllUsers(token: str = Depends(authenticate),
                       db: AsyncSession = Depends(get_db)):
    if token["is_admin"] == UserType["is_user"]:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an Admin")
    # print("Is admin==============", token["is_admin"])
    results = await db.execute(select(Users))
    users = results.scalars().all()
    return users


@user_route.get("/auth/view_user")
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
