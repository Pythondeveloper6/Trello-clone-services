from app.schemas.boards_schemas import BoardCreate, BoardUpdate
from app.services.boards_service import (
    create_board,
    delete_board,
    get_board_by_id,
    get_boards_by_project,
    update_board,
)
from flask import Blueprint, jsonify, request

# create blueprint : project related endpoints
board_bp = Blueprint("boards", __name__, url_prefix="/api/v1/boards/")


@board_bp.route("/", methods=["POST"])
def create_new_board():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        board_data = BoardCreate(**data)
        created_board = create_board(board_data)
        return jsonify(created_board.model_dump()), 201
    except Exception as e:
        return jsonify({"error": f"failed to create new board : {e}"}), 500


@board_bp.route("/", methods=["GET"])
def list_board():
    try:
        project_id = int(request.args.get("project_id"))
        limit = int(request.args.get("limit"))
        offset = int(request.args.get("offset"))

        if not project_id:
            return jsonify({"error": "project_id param is required"}), 400

        boards = get_boards_by_project(project_id, limit, offset)
        boards_data = [board.model_dump() for board in boards]
        return jsonify(boards_data), 200

    except Exception as e:
        return jsonify({"error": f"failed to fetch boards : {e}"}), 500


@board_bp.route("/<int:board_id>", methods=["GET"])
def get_board(board_id: int):
    try:
        board = get_board_by_id(board_id)
        if not board:
            return jsonify({"error": "board not found"})
        return jsonify(board.model_dump()), 200
    except Exception as e:
        return jsonify({"error": f"failed to fetch board : {e}"}), 500


@board_bp.route("/<int:board_id>", methods=["PUT"])
def board_update(board_id: int):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        board_data = BoardUpdate(**data)
        updated_board = update_board(board_id, board_data)
        if not updated_board:
            return jsonify({"error": "board not found"})

        return jsonify(updated_board.model_dump()), 200

    except Exception as e:
        return jsonify({"error": f"failed to fetch board : {e}"}), 500


@board_bp.route("/<int:board_id>", methods=["DELETE"])
def board_delete(board_id: int):
    try:
        selected_board = delete_board(board_id)
        if not selected_board:
            return jsonify({"error": "board not found"})
        return jsonify({"message": "board deletede successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"failed to delete board : {e}"}), 500
