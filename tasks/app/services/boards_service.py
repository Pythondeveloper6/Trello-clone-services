from typing import List, Optional

from app.db.database import get_db_session
from app.models.boards import Board
from app.models.projects import Project
from app.schemas.boards_schemas import BoardCreate, BoardResponse, BoardUpdate


def create_board(board_data: BoardCreate) -> BoardResponse:
    with get_db_session() as db:
        db_board = Board(
            name=board_data.name,
            description=board_data.description,
            columns=board_data.columns,
            project_id=board_data.project_id,
        )

        db.add(db_board)
        db.flush()
        db.refresh(db_board)

        return BoardResponse.model_validate(db_board)


def get_board_by_id(board_id: int) -> Optional[BoardResponse]:
    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()
        if db_board:
            return BoardResponse.model_validate(db_board)
        return None


def get_boards_by_project(
    project_id: int, limit: int = 50, offset: int = 0
) -> List[BoardResponse]:
    with get_db_session() as db:
        db_boards = (
            db.query(Board)
            .filter(Board.project_id == project_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [BoardResponse.model_validate(board) for board in db_boards]


def update_board(board_id: int, board_data: BoardUpdate) -> Optional[BoardResponse]:
    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()
        if not db_board:
            return None
        if board_data.name is not None:
            db_board.name = board_data.name

        if board_data.description is not None:
            db_board.description = board_data.description

        if board_data.columns is not None:
            db_board.columns = board_data.columns

        db.flush()
        db.refresh(db_board)

        return BoardResponse.model_validate(db_board)


def delete_board(board_id: int) -> bool:
    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()
        if db_board:
            db.delete(db_board)
            return True
        return False
