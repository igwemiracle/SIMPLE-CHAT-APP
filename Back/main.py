import uvicorn
from fastapi import FastAPI
from Routes.user import user_route


app = FastAPI()
app.include_router(user_route)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port="8080")
