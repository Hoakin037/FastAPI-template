from fastapi import APIRouter

from app.modules.users.routes import user_router

api = APIRouter(prefix="/api")
api.include_router(user_router)
