from contextlib import asynccontextmanager

import flet as ft
import flet_fastapi
from fastapi import FastAPI

import router.chat
import view.main_view

from router.chat import chat_router
from router.topics import topics_router
from router.user import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)	
app.include_router(topics_router)
app.include_router(user_router)

app.mount('/', flet_fastapi.app(view.main_view.main))