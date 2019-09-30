class Player():
    def __init__(self, name, team, n_wins=0):
        self.name = name
        self.team = team
        self.n_wins = n_wins

    def change_team(self):
        self.team = "white" if self.team == "black" else "black"

    def did_i_won(self, winner):
        return winner == self.team
