from pydantic import BaseModel, Field
from typing import Optional

class AnalyzeResponse(BaseModel):
    sector: str
    report: str  # Markdown report
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

