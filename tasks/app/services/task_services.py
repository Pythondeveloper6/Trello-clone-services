from typing import List, Optional

from app.db.database import get_db_session
from app.models.tasks import Task
from app.schemas.task_schemas import TaskCreate, TaskResponse, TaskStats, TaskUpdate
from app.utils.enums import TaskPriority, TaskStatus
from sqlalchemy.sql.functions import user


def get_tasks(
    board_id: int,
    user_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[TaskResponse]:

    with get_db_session() as db:
        query = db.query(Task).filter(Task.board_id == board_id)

        if user_id:
            query = query.filter(Task.user_id == user_id)

        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)

        if status:
            query = query.filter(Task.status == status)

        if priority:
            query = query.filter(Task.priority == priority)

        tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()

        return [TaskResponse.model_validate(task) for task in tasks]


def get_task_by_id(task_id: int) -> Optional[TaskResponse]:
    with get_db_session() as db:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        return TaskResponse.model_validate(db_task)


def get_users_tasks(user_id: str, status: Optional[TaskStats]) -> List[TaskResponse]:
    with get_db_session() as db:
        query = (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .all()
        )

        if status:
            query = query.filter(Task.status == status)

        return [TaskResponse.model_validate(task) for task in query]


def create_task(task_data: TaskCreate) -> TaskResponse:
    with get_db_session() as db:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            user_id=task_data.user_id,
            assigned_to=task_data.assigned_to,
            border_id=task_data.board_id,
            due_date=task_data.due_date,
        )
        db.add(db_task)
        db.flush()
        db.refresh(db_task)

        return TaskResponse.model_validate(db_task)


def update_task(task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
    with get_db_session() as db:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None

        updated_data = task_update.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(db_task, field, value)

        db.flush()
        db.refresh(db_task)
        return TaskResponse.model_validate(db_task)


def delete_task(task_id: int) -> bool:
    with get_db_session() as db:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return False

        db.delete(db_task)

        return True


def get_tasks_stats() -> TaskStats:
    with get_db_session() as db:
        rows = db.query(Task.status, Task.priority, Task.user_id).all()

        # intialise counters
        status_count = {s.value: 0 for s in TaskStatus}
        priority_count = {p.value: 0 for p in TaskPriority}
        user_count = {}

        for status, priority, user_id in rows:
            status_count[status.value] += 1
            priority_count[priority.value] += 1
            user_count[user_id] = user_count.get(user_id, 0) + 1

        return TaskStats(
            total_tasks=len(rows),
            tasks_by_status=status_count,
            tasks_by_priority=priority_count,
            tasks_by_users=user_count,
        )
