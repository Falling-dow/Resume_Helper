from typing import Optional

from pydantic import BaseModel


class JobRead(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience_level: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None

