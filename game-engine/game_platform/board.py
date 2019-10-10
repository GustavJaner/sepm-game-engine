import time

from game_platform.piece import Piece


class Board():
    def __init__(self, str_board):
        self.pieces = self.str2board(str_board)

        self.size = {
            "width": max(len(r) for r in self.pieces),
            "height": len(self.pieces)
        }

        self.piece_to_move = None
        self.possible_targets_coords = []

    def str2board(self, str_board):
        board = []

        for x, str_row in enumerate(str_board.split("\n")):
            row = []

            for y, piece in enumerate(str_row.strip().split(" ")):
                team = None
                role = None
                corner = False

                if piece == "B":
                    team = "black"
                elif piece == "W" or piece == "K":
                    team = "white"

                if piece == "K":
                    role = "king"
                    corner = True
                    self.initial_king_coords = (x, y)

                elif piece == "B" or piece == "W":
                    role = "marker"

                if piece == "+":
                    corner = True

                p = Piece(team, role, corner)
                row.append(p)

            board.append(row)
        return board

    def check_cell(self, x, y, xo, yo):
        if not self.pieces[x][y].is_piece():
            if self.pieces[xo][yo].team == "black" and self.pieces[x][y].corner:
                return True
            self.pieces[x][y].set_possible_target(True)
            self.possible_targets_coords.append((x, y))
        else:
            return True

    def evaluate_possible_target(self, x, y):
        self.possible_targets_coords = []

        # It checks from the piece to the left
        for y2 in range(y-1, -1, -1):
            if self.check_cell(x, y2, x, y):
                break

        # It checks from the piece to the right
        for y2 in range(y+1, self.size["width"]):
            if self.check_cell(x, y2, x, y):
                break

        # It checks from the piece to the top
        for x2 in range(x-1, -1, -1):
            if self.check_cell(x2, y, x, y):
                break

        # It checks from the piece to the bottom
        for x2 in range(x+1, self.size["height"]):
            if self.check_cell(x2, y, x, y):
                break

        # avoid set the king in the same spot where he started
        if self.pieces[x][y].role == "king" and self.initial_king_coords in self.possible_targets_coords:
            xo, yo = self.initial_king_coords
            self.pieces[xo][yo].set_possible_target(False)
            self.possible_targets_coords.remove(self.initial_king_coords)

    def move_piece(self, dest_x, dest_y, board_ui, data, screen_api):
        orig_x, orig_y = self.piece_to_move
        team = self.pieces[orig_x][orig_y].team
        role = self.pieces[orig_x][orig_y].role

        if orig_x < dest_x:
            rang = [(x, dest_y) for x in range(orig_x, dest_x+1)]
        elif orig_x > dest_x:
            rang = [(x, dest_y) for x in range(orig_x, dest_x-1, -1)]
        elif orig_y < dest_y:
            rang = [(dest_x, y) for y in range(orig_y, dest_y+1)]
        elif orig_y > dest_y:
            rang = [(dest_x, y) for y in range(orig_y, dest_y-1, -1)]

        self.clear_targets()

        for (x1, y1), (x2, y2) in zip(rang[:-1], rang[1:]):
            self.pieces[x1][y1].remove_marker()
            self.pieces[x2][y2].set_marker(role, team)
            board_ui.print_board(data)
            screen_api.refresh()
            time.sleep(0.1)

    def move_piece_no_ui(self, orig_x, orig_y, dest_x, dest_y):
        destination = self.data.board[dest_x][dest_y]
        self.data.board[dest_x][dest_y] = self.data.board[orig_x][orig_y]
        self.data.board[orig_x][orig_y] = destination
        self.clear_targets()

    def clear_targets(self):
        self.piece_to_move = None
        self.possible_targets_coords = []
        for r in self.pieces:
            for c in r:
                c.set_possible_target(False)
