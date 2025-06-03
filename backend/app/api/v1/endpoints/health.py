from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)


router = APIRouter()

@router.get(
    "/health",
    tags=["health"],
    summary="Healthcheck endpoint",
    response_description="Service health status"
)
def healthcheck():
    """
    Healthcheck endpoint to verify the service is running.
    
    Returns a simple status message.
    """
    return {"status": "ok"}
