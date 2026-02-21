from datetime import datetime
from typing import List, Optional

from app.utils.enums import TaskPriority, TaskStatus
from pydantic import BaseModel, Field

# langhcain : code
# langchain : db


class TaskBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=500, description="task title")
    description: Optional[str] = Field(None, description="task description")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="task status")
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="task priority"
    )
    user_id: str = Field(..., description="id of the user who created the task")
    assigned_to: str = Field(..., description="id of the user who assigned to the task")
    board_id: int = Field(..., description="task board id ")
    due_date: Optional[datetime] = Field(None, description="iwhen the task is due")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=500)
    description: Optional[str] = Field(None)
    status: Optional[TaskStatus] = Field(None)
    priority: Optional[TaskPriority] = Field(None)
    assigned_to: Optional[str] = Field(None)
    due_date: Optional[datetime] = Field(None)


class TaskResponse(TaskBase):
    id: int = Field(..., description="task id")
    created_at: datetime = Field(..., description="task creation date")
    updated_at: datetime = Field(..., description="task laast update date")

    class Config:
        from_attributes = True


class TaskStats(BaseModel):
    total_tasks: int = Field(..., description="Toal number of tasks ")
    tasks_by_status: dict = Field(..., description="count of tasks for each status")
    tasks_by_priority: dict = Field(..., description="count of tasks for each priority")
    tasks_by_users: dict = Field(..., description="count of tasks for each user")
