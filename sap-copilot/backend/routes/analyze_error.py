from fastapi import APIRouter, Request
from models.schema import ErrorAnalysisRequest, ErrorAnalysisResponse

router = APIRouter()

@router.post("/analyze-error", response_model=ErrorAnalysisResponse)
async def analyze_error(payload: ErrorAnalysisRequest):
    # TODO: Call LangGraph flow here
    return ErrorAnalysisResponse(
        explanation="Example explanation",
        fix_patch="--- \n+ fixed line here",
        scope="internal",
        followups=["How can I improve this further?"]
    )
