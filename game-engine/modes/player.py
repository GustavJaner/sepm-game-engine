class Player():
    def __init__(self, name, team=None, n_wins=0, difficulty=None):
        self.name = name
        self.team = team
        self.n_wins = n_wins

        if difficulty == None:
            self.is_AI = False
        else:
            self.difficulty = difficulty
            self.is_AI = True

    def change_team(self):
        self.team = "white" if self.team == "black" else "black"

    def did_i_won(self, winner):
        return winner == self.team

    def __str__(self):
        return self.name
