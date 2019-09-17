class Cell():
    def __init__(self, team, role, possible_target=False):
        self.team = team
        self.role = role
        self.possible_target = possible_target

    def __str__(self):
        if self.role == "king":
            char = "K"
        elif self.team == "white":
            char = "W"
        elif self.team == "black":
            char = "B"
        elif self.possible_target:
            char = "·"
        else:
            char = " "
        return char

    def is_piece(self):
        return self.role in ["marker", "king"]

    def set_possible_target(self, status):
        self.possible_target = status

    def remove_marker(self):
        self.role = None
        self.team = None
