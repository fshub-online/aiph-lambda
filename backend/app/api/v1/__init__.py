from fastapi import APIRouter
from .endpoints import health, users, oauth, messages, members, objectives, key_results, meetings

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(oauth.router)
api_v1_router.include_router(messages.router)
api_v1_router.include_router(members.router)
api_v1_router.include_router(objectives.router)
api_v1_router.include_router(key_results.router)
api_v1_router.include_router(meetings.router)
