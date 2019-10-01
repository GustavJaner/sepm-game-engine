import sys
import curses

from board.board_ui import BoardUI
from game_platform.piece import Piece
from game_platform.rules import check_movement

from screens import *


class GamePlatform():
    possible_targets_coords = []
    piece_to_move = None
    event = None

    def __init__(self, screen_api, data, str_board):
        self.screen_api = screen_api

        self.data = data
        self.data.set_board(self.str2board(str_board))
        self.data.board_ui = BoardUI(screen_api)

        # maybe return
        self.polling()

    def str2board(self, str_board):
        board = []

        for str_row in str_board.split("\n"):
            row = []

            for piece in str_row.strip().split(" "):
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

                elif piece == "B" or piece == "W":
                    role = "marker"

                if piece == "+":
                    corner = True

                p = Piece(team, role, corner)
                row.append(p)

            board.append(row)
        return board

    def check_cell(self, x, y):

        if not self.data.board[x][y].is_piece():
            if self.data.turn == "black" and self.data.board[x][y].corner:
                return True
            self.data.board[x][y].set_possible_target(True)
            self.possible_targets_coords.append((x, y))
        else:
            return True

    def evaluate_possible_target(self, x, y):
        self.possible_targets_coords = []

        # It checks from the piece to the left
        for y2 in range(y-1, -1, -1):
            if self.check_cell(x, y2):
                break

        # It checks from the piece to the right
        for y2 in range(y+1, self.data.board_size["width"]):
            if self.check_cell(x, y2):
                break

        # It checks from the piece to the top
        for x2 in range(x-1, -1, -1):
            if self.check_cell(x2, y):
                break

        # It checks from the piece to the bottom
        for x2 in range(x+1, self.data.board_size["height"]):
            if self.check_cell(x2, y):
                break

        # avoid set the king in the same spot where he started
        if self.data.board[x][y].role == "king" and self.data.initial_king_coords in self.possible_targets_coords:
            (xo, yo) = self.data.initial_king_coords
            self.data.board[xo][yo].set_possible_target(False)
            self.possible_targets_coords.remove(self.data.initial_king_coords)

        if len(self.possible_targets_coords) != 0:
            self.piece_to_move = (x, y)

    def move_piece(self, dest_x, dest_y):
        orig_x, orig_y = self.piece_to_move[0], self.piece_to_move[1]
        destination = self.data.board[dest_x][dest_y]
        self.data.board[dest_x][dest_y] = self.data.board[orig_x][orig_y]
        self.data.board[orig_x][orig_y] = destination
        self.clear_targets()

    def clear_targets(self):
        self.piece_to_move = None
        self.possible_targets_coords = []
        for r in self.data.board:
            for c in r:
                c.set_possible_target(False)

    def no_piece_selected(self, x, y):

        # The cell is empty
        if self.data.board[x][y].team == None:
            return

        if self.data.board[x][y].team == "white" and self.data.turn == "white" or self.data.board[x][y].team == "black" and self.data.turn == "black":
            # If the current cursor position has a piece
            if self.data.board[x][y].is_piece() and len(self.possible_targets_coords) == 0:
                self.evaluate_possible_target(x, y)
                if len(self.possible_targets_coords) == 0:
                    self.data.msg = "This piece has not any possible movement"
        else:
            self.data.msg = "You can't move a piece of the other team"

    def we_have_a_winner(self, team):
        for player in self.data.players:
            if player.did_i_won(team):
                self.event = player

    def one_piece_selected(self, x, y):
        # We move the piece if the cursor coords is in one of the targets
        if (x, y) in self.possible_targets_coords:
            self.move_piece(x, y)
            won, team, captured = check_movement(self.data)
            self.change_turn()

            self.data.turns_left -= 1

            if won:
                self.we_have_a_winner(team)

            if self.data.turns_left == 0:
                self.event = "tie"

        # If the cursor is the same as the selected cell, then we cancel the move
        elif self.piece_to_move == (x, y):
            self.clear_targets()
        else:
            self.data.msg = "You can't move to that cell"

    def change_turn(self):
        self.data.turn = "white" if self.data.turn == "black" else "black"

    def switch_action(self, action, x, y):
        if action == "up":
            x -= 1
            self.data.board_ui.cursor_pos = (max(0, x), y)

        if action == "down":
            x += 1
            self.data.board_ui.cursor_pos = (
                min(x, self.data.board_size["height"]-1), y)

        if action == "left":
            y -= 1
            self.data.board_ui.cursor_pos = (x, max(0, y))

        if action == "right":
            y += 1
            self.data.board_ui.cursor_pos = (
                x, min(y, self.data.board_size["width"] - 1))

        if action == "space":
            if len(self.possible_targets_coords) == 0:
                self.no_piece_selected(x, y)
            elif self.piece_to_move != None:
                self.one_piece_selected(x, y)

        if action == "pause":
            self.event = "pause"

    def polling(self):
        self.data.board_ui.print_board(self.data)

        action = None

        while True:
            self.data.msg = ""

            won, team, captured = check_movement(self.data)

            # Same check in L221
            if won:
                return self.we_have_a_winner(team)

            if captured:
                self.change_turn()
            else:
                # Wait to read a key
                action = self.data.board_ui.key_listener()

                if action != None:
                    x, y = self.data.board_ui.cursor_pos[0], self.data.board_ui.cursor_pos[1]
                    self.switch_action(action, x, y)

                if self.event != None:
                    break

            # Same check in L207
            # if (won):
            #    return self.we_have_a_winner(team)

            self.data.board = self.data.board
            self.data.board_ui.print_board(self.data)
