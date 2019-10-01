import sys
import curses

from board.board_ui import BoardUI
from game_platform.board import Board
from game_platform.rules import check_movement

from screens import *


class GamePlatform():
    possible_targets_coords = []
    event = None

    def __init__(self, screen_api, data, str_board):
        self.screen_api = screen_api

        self.data = data
        self.data.set_board(Board(str_board))
        self.data.board_ui = BoardUI(screen_api)

        self.polling()

    def no_piece_selected(self, x, y):

        # The cell is empty
        if self.data.board.pieces[x][y].team == None:
            return

        if self.data.board.pieces[x][y].team == "white" and self.data.turn == "white" or self.data.board.pieces[x][y].team == "black" and self.data.turn == "black":
            # If the current cursor position has a piece
            if self.data.board.pieces[x][y].is_piece() and len(self.data.board.possible_targets_coords) == 0:
                self.data.board.evaluate_possible_target(x, y)
                if len(self.data.board.possible_targets_coords) == 0:
                    self.data.msg = "This piece has not any possible movement"
                else:
                    self.data.board.piece_to_move = (x, y)
        else:
            self.data.msg = "You can't move a piece of the other team"

    def we_have_a_winner(self, team):
        for player in self.data.players:
            if player.did_i_won(team):
                self.event = player

    def one_piece_selected(self, x, y):
        # We move the piece if the cursor coords is in one of the targets
        if (x, y) in self.data.board.possible_targets_coords:
            self.data.board.move_piece(
                x, y, self.data.board_ui, self.data, self.screen_api)
            won, team, captured = check_movement(self.data)
            self.change_turn()

            self.data.turns_left -= 1

            if won:
                self.we_have_a_winner(team)

            if self.data.turns_left == 0:
                self.event = "tie"

        # If the cursor is the same as the selected cell, then we cancel the move
        elif self.data.board.piece_to_move == (x, y):
            self.data.board.clear_targets()
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
                min(x, self.data.board.size["height"]-1), y)

        if action == "left":
            y -= 1
            self.data.board_ui.cursor_pos = (x, max(0, y))

        if action == "right":
            y += 1
            self.data.board_ui.cursor_pos = (
                x, min(y, self.data.board.size["width"] - 1))

        if action == "space":
            if len(self.data.board.possible_targets_coords) == 0:
                self.no_piece_selected(x, y)
            elif self.data.board.piece_to_move != None:
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
                    # Something happened:
                    # 1. User press q to open menu
                    # 2. The game has finished: one of the player has won or tied
                    break

            # Same check in L207
            # if (won):
            #    return self.we_have_a_winner(team)

            # self.data.board = self.data.board
            self.data.board_ui.print_board(self.data)
