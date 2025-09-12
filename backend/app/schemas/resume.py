from typing import Any, Optional

from pydantic import BaseModel


class ResumeRead(BaseModel):
    id: str
    title: Optional[str] = None
    file_url: Optional[str] = None
    version: int = 1


class ResumeUploadResponse(BaseModel):
    id: str
    file_url: str
    file_type: str


class OptimizeRequest(BaseModel):
    resume_content: dict
    job_description: str
    user_preferences: dict | None = None


class OptimizeResponse(BaseModel):
    optimized_content: dict[str, Any]
    match_score: float
    suggestions: dict[str, Any] | None = None
    keywords_to_add: list[str] | None = None

