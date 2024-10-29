from typing import Annotated, Optional
from uuid import uuid4

import chess
from autogen import ConversableAgent, register_function

boards: dict[str, chess.Board] = {}

def count_pieces(board: chess.Board) -> int:
    # Get a dictionary of pieces on the board
    piece_map = board.piece_map()
    # Return the number of pieces
    return len(piece_map)

def create_new_board(
    board_fen: Annotated[Optional[str], "Starting board state in FEN format"] = None,
) -> Annotated[str, "A chess board UUID"]:
    board_fen = board_fen or chess.STARTING_BOARD_FEN

    board = chess.Board(board_fen)

    if count_pieces(board) > 10:
        return "ERROR: The board should have a maximum of 10 pieces."
    
    uuid = str(uuid4())

    boards[uuid] = board

    return uuid


def create_copy_board(
    board_uuid: Annotated[str, "A chess board UUID"],
) -> Annotated[str, "A chess board UUID"]:
    board = boards[board_uuid].copy()

    uuid = str(uuid4())

    boards[uuid] = board

    return uuid


def _possible_moves(board: chess.Board) -> str:
    return "Possible moves are: " + ",".join([str(move) for move in board.legal_moves])


def get_legal_moves(
    board_uuid: Annotated[str, "A chess board UUID"],
) -> Annotated[str, "A list of legal moves in UCI format"]:
    if board_uuid not in boards:
        return f"Board with the UUID='{board_uuid}' not found."
    board = boards[board_uuid]

    return _possible_moves(board)


def make_move(
    board_uuid: Annotated[str, "A chess board UUID"],
    move_uci: Annotated[str, "A move in UCI format"],
) -> str:
    if board_uuid not in boards:
        return f"Board with the UUID='{board_uuid}' not found."
    board = boards[board_uuid]

    move = chess.Move.from_uci(move_uci)
    if move not in board.legal_moves:
        return f"Move '{move_uci}' is not legal. {_possible_moves(board)}"

    board.push(move)

    return board.unicode()


def register_chess_functions(
    student_agent: ConversableAgent, teacher_agent: ConversableAgent
) -> None:
    for f, description in [
        (create_new_board, "Creates a new board"),
        (create_copy_board, "Creates a copy of the board"),
        (get_legal_moves, "Get legal moves"),
        (make_move, "Makes a move on the board"),
    ]:
        for caller, executor in [
            (student_agent, teacher_agent),
            (teacher_agent, student_agent),
        ]:
            register_function(
                f,
                description=description,
                caller=caller,
                executor=executor,
            )
