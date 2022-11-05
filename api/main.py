from fastapi import FastAPI

from api.routers import log, user

app = FastAPI()
app.include_router(user.router)
app.include_router(log.router)