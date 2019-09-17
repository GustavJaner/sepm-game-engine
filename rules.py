
def check_movement(board, board_size):
    # if invalid move -> return False, "reason"

    for row in range(board_size["height"]):
        for col in range(board_size["width"]):
            if(board[row][col].is_piece()):
                if board[row][col].role != "king":
                    check_captured(board, board_size, row, col)
                else:
                    check_king_escape(board, board_size,row,col)

    return True, "valid move"

def check_captured(board, board_size, row, col):
    team = board[row][col].team

    left  = None
    right = None
    top   = None
    bot   = None

    if (col-1 >= 0 and col+1 <= board_size["height"]-1):
        left  = board[row][col-1].team
        right = board[row][col+1].team

    if (row-1 >= 0 and row+1 <= board_size["width"]-1):
        top = board[row+1][col].team
        bot = board[row-1][col].team

    if (left != None and right!= None):
        if (left != team and right != team):
            board[row][col].remove_marker()

    if (top != None and bot!= None):
        if (top != team and bot != team):
            board[row][col].remove_marker()
            
def check_king_escape(board, board_size, row, col):
    if( (row == 0 and col == 0)
    or (row == board_size["width"]-1 and col == 0)
    or (row == 0 and col == board_size["height"]-1)
    or (row == board_size["width"]-1 and col == board_size["height"]-1)):
        print("King escaped, white win")
        
# 1. Check if move result in capturing a marker
# --> remove that marker

# 3 Win condition:
# a: king in the corner -- White win
# b: King is captureed -- Black win
