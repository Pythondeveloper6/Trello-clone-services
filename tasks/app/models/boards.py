from datetime import datetime

from app.models.tasks import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    columns = Column(JSON, nullable=False, default=["ToDo", "InProgress", "Done"])

    # project
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)

    # timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    project = relationship("Project", back_populates="boards")
