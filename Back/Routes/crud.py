from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from Authentication.hash_pwd import HashPassword
from Authentication.auth import oauth2_scheme
from Authentication.jwt_handler import verify_access_token
from Models.sqlData import Users
from Database.connection import get_db

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


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    query = select(Users).where(Users.email == email)
    result = await db.execute(query)
    return result.scalar()


async def findUser(username: str, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM signin WHERE username=:username")
    result = await db.execute(query, {"username": username})
    return result.fetchone()


async def findRecipient(recipient: str, db: AsyncSession = Depends(get_db)):
    query = select(Users).where(Users.username == recipient)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def findSender(sender: str, db: AsyncSession = Depends(get_db)):
    query = select(Users).where(Users.username == sender)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# ===============================================================================================
# async def SendMessageToUser(sender_username, recipient_username,
#                             message_text, db: AsyncSession = Depends(get_db)):
#     sender = await db.execute(select(Users).where(Users.username == sender_username))
#     recipient = await db.execute(select(Users).where(Users.username == recipient_username))

#     sender_user = sender.scalar_one_or_none()
#     recipient_user = recipient.scalar_one_or_none()

#     if not recipient_user:
#         return "Recipient user does not exist"

#     new_message = Message(
#         text=message_text,
#         timestamp=datetime.now(),
#         owner_id=sender_user.id,
#         user=recipient_user
#     )

#     db.add(new_message)
#     await db.commit()

#     return "Message sent successfully"

# async def createMessage(text: str, timestamp: datetime, owner_id: int, recipient_id: int, db: AsyncSession):
#     new_message = Message(
#         text=text,
#         timestamp=timestamp,
#         owner_id=owner_id,
#         recipient_id=recipient_id
#     )
#     db.add(new_message)
#     await db.commit()
#     await db.refresh(new_message)
#     return new_message


# ------ CONNECTED TO "" IN user.py USER FOR ACCESS TOKEN---------
# async def findUser(username: str, db: AsyncSession = Depends(get_db)):
#     query = select(Users).where(Users.username == username)
#     result = await db.execute(query)
#     return result.scalar()


# async def getSavedMessages(username: str, db: AsyncSession = Depends(get_db)):
#     saved_messages = text(
#         "SELECT * FROM saved_messages WHERE username=:username")
#     result = await db.execute(saved_messages, {"username": username})
#     return result.fetchall()

# async def getSavedMSG(sender_user: str, receiver_user: str, db: AsyncSession = Depends(get_db)):
#     saved_messages = text(
#         "SELECT * FROM saved_messages WHERE sender_username=:sender AND recipient_username=:receiver")
#     result = await db.execute(saved_messages, {"sender": sender_user, "receiver": receiver_user})
#     return result.fetchall()
