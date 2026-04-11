from app.models.tasks import Task
from app.schemas.task_schemas import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from app.services.task_services import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    get_tasks_stats,
    get_users_tasks,
    update_task,
)
from flask import Blueprint, jsonify, request

# create blueprint : project related endpoints
tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks/")


@tasks_bp.route("/", methods=["POST"])
def create_new_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No Data Provided"}), 400

        task_data = TaskCreate(**data)
        created_task = create_task(task_data)
        return jsonify(created_task.model_dump(mode="json")), 201
    except Exception as e:
        return jsonify({"error": f"Faild to create new task: {str(e)}"}), 500


@tasks_bp.route("/", methods=["GET"])
def list_tasks():
    try:
        board_id = request.args.get("board_id")
        user_id = request.args.get("user_id")
        assigned_to = request.args.get("assigned_to")
        status_str = request.args.get("status")
        priority_str = request.args.get("priority")
        limit = request.args.get("limit", 50)
        offset = request.args.get("offset", 0)

        if not board_id:
            return jsonify({"error": "board_id is required"}), 400

        status = priority = None
        if status_str:
            try:
                status = TaskStatus(status_str)
            except Exception as e:
                return jsonify({"error": f"invalid status : {status_str}"}), 400

        if priority_str:
            try:
                priority = TaskPriority(priority_str)
            except Exception as e:
                return jsonify({"error": f"invalid priority : {priority_str}"}), 400

        # get tasks from db
        tasks = get_tasks(
            board_id=board_id,
            user_id=user_id,
            assigned_to=assigned_to,
            status=status,
            priority=priority,
            limit=limit,
            offset=offset,
        )

        tasks_data = [task.model_dump(mode="json") for task in tasks]
        return jsonify(tasks_data), 200

    except Exception as e:
        return jsonify({"error": f"Faild to get tasks: {str(e)}"}), 500


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_single_task(task_id):
    try:
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task.model_dump(mode="json")), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get task : {e}"}), 500


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_existing_task(task_id: int):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data provided"}), 400

        current_task = get_task_by_id(task_id)
        if not current_task:
            return jsonify({"error": "Task not found"}), 404

        task_update = TaskUpdate(**data)
        updated_task = update_task(task_id, task_update)
        return jsonify(updated_task.model_dump(mode="json")), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get task : {e}"}), 500


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_existing_task(task_id: int):
    try:
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        success = delete_task(task_id)

        if not success:
            return jsonify({"error": f"Task not found : {e}"}), 404

        return jsonify({f"message": "Task deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to delete task : {e}"}), 500


@tasks_bp.route("/stats", methods=["GET"])
def get_statistics():
    try:
        stats = get_tasks_stats()
        return jsonify(stats.model_dump()), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get tasks stats : {e}"}), 500


@tasks_bp.route("/users/<user_id>", methods=["GET"])
def get_tasks_for_user(user_id):
    try:
        status_str = request.args.get("status")
        status = None
        if status_str:
            try:
                status = TaskStatus(status_str)
            except Exception as e:
                return jsonify({"error": f"invalid status : {status_str}"}), 400

        tasks = get_users_tasks(user_id=user_id, status=status)
        tasks_data = [task.model_dump(mode="json") for task in tasks]
        return jsonify(tasks_data), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get user tasks : {e}"}), 500
