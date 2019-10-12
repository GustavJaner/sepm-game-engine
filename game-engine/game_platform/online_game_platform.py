import sys
import curses

from board.board_ui import BoardUI
from game_platform.board import Board
from game_platform.rules import check_movement

from screens import *


TURNS_IN_A_GAME = 200


class OnlineGamePlatform():
    possible_targets_coords = []
    event = None

    def __init__(self, screen, data, str_board):
        self.screen = screen

        self.data = data
        self.data.set_board(Board(str_board))
        self.data.board_ui = BoardUI(screen)

        self.data.turn = "white" # Always initiate at white
        self.data.turns_left = TURNS_IN_A_GAME # Reset every time a New Game Round is initiated

        # self.polling() # the old game loop

    def no_piece_selected(self, x, y):

        # The cell is empty
        if self.data.board.pieces[x][y].team == None:
            return

        if self.data.board.pieces[x][y].team == "white" and self.data.turn == "white" or self.data.board.pieces[x][y].team == "black" and self.data.turn == "black":
            # If the current cursor position has a piece
            if self.data.board.pieces[x][y].is_piece() and len(self.data.board.possible_targets_coords) == 0:
                possible_targets_coords = self.data.board.evaluate_possible_target(
                    x, y)
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
                x, y, self.data.board_ui, self.data, self.screen)
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

    def polling(self, current_turn_data):

        # Use the new turn data from the other player
        self.data = current_turn_data
        self.data.board_ui.print_board(self.data)

        action = None

        # while True:
        self.data.msg = ""

        won, team, captured = check_movement(self.data)

        # Same check in L221
        if won:
            return self.we_have_a_winner(team)

        if captured: # The turn has been automatically made for the player(capturing a marker)
            self.change_turn()
        else:
            # Wait to read a key
            action = self.data.board_ui.key_listener()

            if action != None:
                x, y = self.data.board_ui.cursor_pos[0], self.data.board_ui.cursor_pos[1]
                self.switch_action(action, x, y) # Makes the changes to the board

            # Something happened:
            # 1. User press q to open menu
            # 2. The game has finished: one of the player has won or tied
            if self.event != None:
                return self.data

        # self.data.board = self.data.board
        self.data.board_ui.print_board(self.data)

        # Return current turn data and send to the other player
        return self.data
