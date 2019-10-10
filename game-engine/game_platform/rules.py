def check_movement(data):
    captured = False
    for row in range(data.board.size["height"]):
        for col in range(data.board.size["width"]):
            if data.board.pieces[row][col].is_piece():
                if data.board.pieces[row][col].team != data.turn:  # <- maybe useless
                    if data.board.pieces[row][col].role != "king":
                        if check_captured_marker(data.board.pieces, data.board.size, row, col):
                            captured = True
                    else:
                        if check_king_escape(data.board.pieces, data.board.size, row, col):
                            return True, "white", False
                        if check_captured_king(data.board.pieces, data.board.size, row, col):
                            return True, "black", False

    # return false as long as no player has won
    return False, "", captured


def check_captured_marker(board, board_size, row, col):
    team = board[row][col].team
    left, right, top, bot = None, None, None, None

    if (col-1 >= 0 and col+1 <= board_size["height"]-1):
        left = board[row][col-1].team
        right = board[row][col+1].team

    if (row-1 >= 0 and row+1 <= board_size["width"]-1):
        top = board[row+1][col].team
        bot = board[row-1][col].team

    if (left != None and right != None):
        if (left != team and right != team):
            board[row][col].remove_marker()
            return True

    if (top != None and bot != None):
        if (top != team and bot != team):
            board[row][col].remove_marker()
            return True


def check_captured_king(board, board_size, row, col):
    team = "white"
    sides = ["wall"] * 4  # [TOP, RIGHT, BOTTOM, LEFT]

    if row-1 >= 0:
        sides[0] = board[row - 1][col].team

    if col+1 <= board_size["height"]-1:
        sides[1] = board[row][col + 1].team

    if row+1 <= board_size["width"]-1:
        sides[2] = board[row+1][col].team

    if col-1 >= 0:
        sides[3] = board[row][col-1].team

    if None not in sides and team not in sides:
        board[row][col].remove_marker()
        return True


def check_king_escape(board, board_size, row, col):
    if ((row == 0 and col == 0)
        or (row == board_size["width"]-1 and col == 0)
        or (row == 0 and col == board_size["height"]-1)
            or (row == board_size["width"]-1 and col == board_size["height"]-1)):
        return True
