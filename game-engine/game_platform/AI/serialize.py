import json

import game_platform.AI.AI_component.src.soft_strategy as soft_strategy
import game_platform.AI.AI_component.src.medium_strategy as medium_strategy
import game_platform.AI.AI_component.src.hard_strategy as hard_strategy
import game_platform.AI.AI_component.src.ia as ia
import game_platform.AI.AI_component.src.board as board


def get_json(board, max_turns, difficulty, next_player, next_turn):
    return {
        "gameUID": 0,
        "game": "UU-GAME",
        "description": "An unstarted game position for the 9x9 UU-GAME",

        "gameConfig":
        {
            "maxTurns": max_turns,
            "AIDifficulty": difficulty
        },
        "boardStatus": {
            "size": 9,
            "coordinates": serialize(board),
            "nextPlayer": next_player.upper(),
            "nextTurn": next_turn
        }
    }


def serialize(board):
    board_serialized = []
    size = 9
    for x, row in enumerate(board):
        for y, piece in enumerate(row):
            if piece.role == "king":
                piece = "KING"
            elif piece.team == "white":
                piece = "WHITE"
            elif piece.team == "black":
                piece = "BLACK"
            else:
                piece = "EMPTY"
            board_serialized.append(
                {"x": size - x - 1, "y": y, "piece": piece})

    return board_serialized


def get_move(board_game, max_turns, difficulty, next_player, next_turn):
    jsonstr = get_json(board_game, max_turns, difficulty,
                       next_player, next_turn)

    with open("./tmp/state.json", "w+") as fd:
        fd.write(json.dumps(jsonstr))

    strategy = soft_strategy.SoftStrategy()
    strategy = medium_strategy.SoftStrategy()
    strategy = hard_strategy.HardStrategy()

    IA = ia.IA(strategy)

    state = board.BoardState()
    state.initialize_from_file("./tmp/state.json")

    res = IA.calculate_move(state)
    origin = (8 - res.x_start, 8 - res.y_start)
    destination = (8 - res.x_end, 8 - res.y_end)

    return origin, destination
