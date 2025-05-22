from fastapi import APIRouter
from .endpoints import health, users, oauth, messages
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.messages import router as messages_router
from app.api.v1.endpoints.members import router as members_router
from app.api.v1.endpoints import objectives

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(oauth.router)
api_v1_router.include_router(messages.router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(messages_router)
api_v1_router.include_router(members_router)
api_v1_router.include_router(objectives.router)
