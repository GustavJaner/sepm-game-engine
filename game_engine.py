
import sys

import curses

from ui import UI
from cell import Cell
from rules import check_movement


class GameEngine():
    board = []
    ui = None
    board_size = {"width": -1, "height": -1}
    possible_targets_coords = []
    piece_to_move = None
    turn = "white"

    def __init__(self):
        self.set_up_board()
        self.ui = UI()
        err = self.ui.print_board(self.board, self.turn)
        if err != None:
            self.finish_game(err)

        self.polling()

    def set_up_board(self):
        # Initial set up. It can be changed
        str_board = """ - - - B B B - - -
                        - - - - B - - - -
                        - - - - W - - - -
                        B - - - W - - - B
                        B B W W K W W B B
                        B - - - W - - - B
                        - - - - W - - - -
                        - - - - B - - - -
                        - - - B B B - - -"""
        self.str2board(str_board)

    def str2board(self, str_board):
        for str_row in str_board.split("\n"):
            row = []

            for piece in str_row.strip().split(" "):
                team = None
                role = None

                if piece == "B":
                    team = "black"
                elif piece == "W" or piece == "K":
                    team = "white"

                if piece == "K":
                    role = "king"
                elif piece == "B" or piece == "W":
                    role = "marker"

                p = Cell(team, role)
                row.append(p)

            self.board.append(row)

        self.board_size["width"] = max(len(r) for r in self.board)
        self.board_size["height"] = len(self.board)

    def evaluate_possible_target(self, x, y):
        self.possible_targets_coords = []
        # It checks from the piece to the left
        for x2 in range(x-1, -1, -1):
            if not self.board[x2][y].is_piece():
                self.board[x2][y].set_possible_target(True)
                self.possible_targets_coords.append((x2, y))
            else:
                break

        # It checks from the piece to the right
        for x2 in range(x+1, self.board_size["width"]):
            if not self.board[x2][y].is_piece():
                self.board[x2][y].set_possible_target(True)
                self.possible_targets_coords.append((x2, y))
            else:
                break

        # It checks from the piece to the top
        for y2 in range(y-1, -1, -1):
            if not self.board[x][y2].is_piece():
                self.board[x][y2].set_possible_target(True)
                self.possible_targets_coords.append((x, y2))
            else:
                break

        # It checks from the piece to the bottom
        for y2 in range(y+1, self.board_size["height"]):
            if not self.board[x][y2].is_piece():
                self.board[x][y2].set_possible_target(True)
                self.possible_targets_coords.append((x, y2))

            else:
                break

        if len(self.possible_targets_coords) != 0:
            self.piece_to_move = (x, y)

    def move_piece(self, dest_x, dest_y):
        destination = self.board[dest_x][dest_y]
        self.board[dest_x][dest_y] = self.board[self.piece_to_move[0]
                                                ][self.piece_to_move[1]]
        self.board[self.piece_to_move[0]][self.piece_to_move[1]] = destination
        self.clear_targets()

    def clear_targets(self):
        self.piece_to_move = None
        self.possible_targets_coords = []
        for r in self.board:
            for c in r:
                c.set_possible_target(False)

    def finish_game(self, msg):
        curses.endwin()
        print(msg)
        sys.exit()

    def no_piece_selected(self, x, y):
        msg = ""

        # The cell is empty
        if self.board[x][y].team == None:
            return ""

        if self.board[x][y].team == self.turn:
            # If the current cursor position has a piece
            if self.board[x][y].is_piece() and len(self.possible_targets_coords) == 0:
                self.evaluate_possible_target(x, y)
                if len(self.possible_targets_coords) == 0:
                    msg = "This piece has not any possible movement"
        else:
            msg = "You can't move a piece of the other team"
        return msg

    def one_piece_selected(self, x, y):
        msg = ""

        if len(self.possible_targets_coords) > 0 and self.piece_to_move != None:
            # We move the piece if the cursor coords is in one of the targets
            if (x, y) in self.possible_targets_coords:
                self.move_piece(x, y)
                self.turn = "white" if self.turn == "black" else "black"
            # If the cursor is the same as the selected cell, then we cancel the move
            elif self.piece_to_move == (x, y):
                self.clear_targets()
            else:
                msg = "You can't move to that cell"

        return msg

    def polling(self):
        msg = ""
        action = None
        while True:
            # Wait to read an arrow key
            action = self.ui.listener()

            x = self.ui.cursor_pos[0]
            y = self.ui.cursor_pos[1]

            if action == "up":
                x -= 1
                self.ui.cursor_pos = (max(0, x), y)

            if action == "down":
                x += 1
                self.ui.cursor_pos = (min(x, self.board_size["height"]-1), y)

            if action == "left":
                y -= 1
                self.ui.cursor_pos = (x, max(0, y))

            if action == "right":
                y += 1
                self.ui.cursor_pos = (x, min(y, self.board_size["width"]-1))

            if action == "space":
                if len(self.possible_targets_coords) == 0:
                    msg = self.no_piece_selected(x, y)
                else:
                    msg = self.one_piece_selected(x, y)

            if action == "exit":
                self.finish_game("FINISH")

            won, team = check_movement(self.board, self.board_size)

            if (won):
                # TODO keep the score of who won, increment the score here ++
                # TODO start new game
                self.finish_game(f"Team {team} won!")

            self.ui.print_board(self.board, self.turn, msg)
