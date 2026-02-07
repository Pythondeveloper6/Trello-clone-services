"""
contains all project managment endpoints
"""

from app.schemas.project_schemas import ProjectCreate, ProjectUpdate
from app.services.project_service import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects_by_owner,
    update_project,
)
from flask import Blueprint, jsonify, request

# create blueprint : project related endpoints
projects_bp = Blueprint("projects", __name__, url_prefix="/api/v1/projects/")


@projects_bp.route("/", methods=["GET"])
def list_projects():
    """get list of projects for the current user"""

    owner_id = request.args.get("owner_id")
    limit = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))

    if not owner_id:
        return jsonify({"error": "owner_id parameter is required"}), 400

    projects = get_projects_by_owner(owner_id, limit, offset)
    projects_data = [project.model_dump() for project in projects]
    return jsonify(projects_data), 200


@projects_bp.route("/<int:project_id>", methods=["GET"])
def project_detail(project_id: int):
    """get project details"""

    project = get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    return jsonify(project.model_dump()), 200


@projects_bp.route("/", methods=["POST"])
def project_create():
    """create new project"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data provided"}), 400

        project_data = ProjectCreate(**data)
        created_project = create_project(project_data)
        return jsonify(created_project.model_dump()), 201
    except Exception as e:
        return jsonify({"error": f"failed to create project - {str(e)}"}), 500


@projects_bp.route("/<int:project_id>", methods=["PUT"])
def project_update(project_id: int):
    """update project data"""

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data provided"}), 400

        project_data = ProjectUpdate(**data)
        updated_project = update_project(project_id, project_data)

        if not update_project:
            return jsonify({"error": "project not found"}), 404

        return jsonify(updated_project.model_dump()), 200
    except Exception as e:
        return jsonify({"error": f"failed to create project - {str(e)}"}), 500


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
def project_delete(project_id: int):
    """delete project data"""

    deleted_project = delete_project(project_id)
    if not deleted_project:
        return jsonify({"error": "project not found"}), 404

    return jsonify({"message": "project deleted successfully"}), 200
