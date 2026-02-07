"""
Project data models using sql-alchemy
Projects serve as the top-level container for all work (boards and tasks).
"""

from datetime import datetime

from app.models.tasks import Base
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # project owner
    owner_id = Column(String(100), nullable=False, index=True)

    # timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
