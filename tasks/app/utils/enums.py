"""all enums in the system"""

from enum import Enum


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESSS = "in_progress"
    DONE = "done"


class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
