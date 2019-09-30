class Piece():
    def __init__(self, team, role, corner, possible_target=False, initial_king_pos=False):
        self.team = team
        self.role = role
        self.corner = corner
        self.possible_target = possible_target
        self.initial_king_pos = initial_king_pos

    def __str__(self):
        if self.role == "king":
            char = "K"
        elif self.team == "white":
            char = "\u25A0"
        elif self.team == "black":
            char = "\u25A1"
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
