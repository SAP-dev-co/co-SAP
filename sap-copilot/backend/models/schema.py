from pydantic import BaseModel
from typing import List, Optional

class ErrorAnalysisRequest(BaseModel):
    traceback: str
    terminal_output: str
    files: dict  # {"filename.py": "contents"}

class ErrorAnalysisResponse(BaseModel):
    explanation: str
    fix_patch: str
    scope: str  # "internal" or "external"
    followups: List[str]
