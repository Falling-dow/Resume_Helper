import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from .base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    company_logo = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    experience_level = Column(String(50), nullable=True)
    industry = Column(String(100), nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)
    source_url = Column(Text, unique=True, nullable=True)
    source_platform = Column(String(50), nullable=True)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    posted_at = Column(DateTime, nullable=True)
    crawled_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

