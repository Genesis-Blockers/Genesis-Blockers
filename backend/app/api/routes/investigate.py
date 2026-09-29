from fastapi import APIRouter

from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
)
from app.services.orchestrator import orchestrator

router = APIRouter(
    prefix="/investigate",
    tags=["Investigation"],
)


@router.post("", response_model=InvestigationResponse)
def investigate(request: InvestigationRequest):
    return orchestrator.run_investigation(request)
