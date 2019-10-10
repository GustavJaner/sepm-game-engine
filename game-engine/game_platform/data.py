

class Data():

    def __init__(self, player1, player2, turn, n_times_played, turns_left, msg):

        self.players = [player1, player2]
        self.turn = turn
        self.n_times_played = n_times_played
        self.turns_left = turns_left
        self.msg = msg

    def set_board(self, board):
        self.board = board
