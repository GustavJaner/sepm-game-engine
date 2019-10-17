
def get_json(board, max_turns, difficulty, next_player, next_turn):
    return {
        "gameUID": 0,
        "game": "UU-GAME",
        "description": "An unstarted game position for the 11x11 UU-GAME",

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
