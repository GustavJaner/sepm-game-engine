class Data:

    def __init__(self, player1, player2, turn, n_times_played, turns_left, msg, type_of_game="1v1", round=None):

        self.players = [player1, player2]
        self.turn = turn
        self.turns_left = turns_left
        self.msg = msg
        self.type_of_game = type_of_game
        if self.type_of_game == "1v1":
            self.n_times_played = n_times_played
        else:
            self.players_str = f"Round {round}: {player1.name} - {player2.name}"

    def set_board(self, board):
        self.board = board
