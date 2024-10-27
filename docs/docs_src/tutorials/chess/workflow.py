import os
from typing import Annotated, Any
from uuid import uuid4

import chess
from autogen import ConversableAgent, register_function

from fastagency import UI
from fastagency.logging import get_logger
from fastagency.runtimes.autogen import AutoGenWorkflows

logger = get_logger(__name__)

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

wf = AutoGenWorkflows()

boards: dict[str, chess.Board] = {}


def create_new_board() -> Annotated[str, "A chess board UUID"]:
    board = chess.Board()
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
    try:
        if board_uuid not in boards:
            return f"Board with the UUID='{board_uuid}' not found."
        board = boards[board_uuid]

        move = chess.Move.from_uci(move_uci)
        if move not in board.legal_moves:
            return f"Move '{move_uci}' is not legal. {_possible_moves(board)}"

        board.push(move)
    except Exception as e:
        logger.warning(f"Error making move: {e}", stack_info=True)
        return f"Error making move: {e}"

    return board.unicode()


def register_chess_functions(
    student_agent: ConversableAgent, teacher_agent: ConversableAgent
) -> None:
    for f, description in [
        (create_new_board, "Creates a new board"),
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


@wf.register(name="chess", description="Chess playing between student and teacher")
def chess_workflow(ui: UI, params: dict[str, Any]) -> str:
    # initial_message = ui.text_input(
    #     sender="Workflow",
    #     recipient="User",
    #     prompt="I can play a game of chess with you. Would you like to play?",
    # )

    try:

        initial_message = "Please teach me basic openings in chess. Show me the moves using board functions."

        student_agent = ConversableAgent(
            name="Student_Agent",
            system_message="You are a student willing to learn to play chess.",
            llm_config=llm_config,
            # human_input_mode="ALWAYS",
        )
        teacher_agent = ConversableAgent(
            name="Teacher_Agent",
            system_message="You are a chess tutor.",
            llm_config=llm_config,
            # human_input_mode="ALWAYS",
        )

        register_chess_functions(student_agent, teacher_agent)

        chat_result = student_agent.initiate_chat(
            teacher_agent,
            message=initial_message,
            summary_method="reflection_with_llm",
            max_turns=10,
        )

        return chat_result.summary  # type: ignore[no-any-return]
    
    except Exception as e:
        logger.error(f"Error in chess_workflow: {e}", exc_info=True)
        raise

