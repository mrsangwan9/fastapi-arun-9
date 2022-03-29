from fastapi import FastAPI
from . import module
from .database import engine
from .routers import post,users,auth
from .config import settings


app = FastAPI()

module.Base.metadata.create_all(bind=engine)





app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)


