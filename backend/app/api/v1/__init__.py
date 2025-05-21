from fastapi import APIRouter
from .endpoints import health, users, oauth, messages

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(oauth.router)
api_v1_router.include_router(messages.router)

