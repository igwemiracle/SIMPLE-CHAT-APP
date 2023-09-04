from fastapi import FastAPI
import uvicorn
from Routes.signup import signup
from Routes.login import login
from Routes.message_user import message_user


app = FastAPI()
app.include_router(signup)
app.include_router(login)
app.include_router(message_user)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port="8080")
