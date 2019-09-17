import math
import sys
import time
import platform

import curses


class UI:
    board_str = ""
    cursor_pos = (0, 0)

    def __init__(self):
        self.walls = {
            "v": "\u2502",  # │
            "h": "\u2500",  # ─
            "bl": "\u2514",  # └
            "br": "\u2518",  # ┘
            "tr": "\u2510",  # ┐
            "tl": "\u250c",   # ┌
            "t0": "\u252c",   # ┬
            "t90": "\u2524",  # ┤
            "t180": "\u2534",  # ┴
            "t240": "\u251c",  # ├,
            "cross": "\u253c"  # ┼
        }

        self.keys = {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "space": " ",
            "exit": "q"
        }

        self.win = curses.initscr()

    def print_bar(self, ncolumns, horizontal_wall, left_wall, middle_wall, right_wall):
        str_bar = left_wall

        horizontal_wall *= 3
        str_bar += f"{horizontal_wall}{middle_wall}" * (ncolumns - 1)
        str_bar += f"{horizontal_wall}"

        str_bar += right_wall

        self.board_str += str_bar + "\n\t"

    def print_row(self, row, i):

        vertical_wall = self.walls["v"]
        str_row = vertical_wall

        for j, c in enumerate(row):
            c = str(c)
            char_to_print = " " if c == "-" else c

            if (i, j) == self.cursor_pos:
                if char_to_print == " ":
                    str_row += f"█-█{vertical_wall}"
                else:
                    str_row += f"█{char_to_print}█{vertical_wall}"

            else:
                str_row += f" {char_to_print} {vertical_wall}"

        self.board_str += str_row + "\n\t"

    def listener(self):
        ch = self.win.getch()

        ch = chr(ch).lower()

        action = None

        if ch == self.keys["up"]:
            action = "up"
        elif ch == self.keys["down"]:
            action = "down"
        elif ch == self.keys["left"]:
            action = "left"
        elif ch == self.keys["right"]:
            action = "right"
        elif ch == self.keys["space"]:
            action = "space"
        elif ch == self.keys["exit"]:
            action = "exit"

        return action

    def print_board(self, board, turn, msg=""):
        # Empty the board before creating the new one
        self.board_str = "\t"

        # Get the length of the first row.
        if len(set(map(len, board))) not in (0, 1):
            return "The length of the rows in the board is not the same"
        ncolumns = len(board[0])

        # Set the top bar
        self.print_bar(
            ncolumns, self.walls["h"], self.walls["tl"], self.walls["t0"], self.walls["tr"])

        for i, row in enumerate(board):
            self.print_row(row, i)
            if i != len(board) - 1:
                self.print_bar(
                    ncolumns, self.walls["h"], self.walls["t240"], self.walls["cross"], self.walls["t90"])
            else:
                self.print_bar(
                    ncolumns, self.walls["h"], self.walls["bl"], self.walls["t180"], self.walls["br"])

        self.win.clear()
        self.win.scrollok(1)
        self.win.addstr(f"\n\tTurn: {turn}\t{msg}\n")
        self.win.addstr(self.board_str)
