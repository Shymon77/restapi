from fastapi import FastAPI
from . import models
from .database import engine
from .routes.routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

from fastapi import FastAPI
from app.routes import auth, contacts

app = FastAPI()

app.include_router(auth.router)
app.include_router(contacts.router)
