import math
import sys
import time
import platform

import curses


class BoardUI:
    board_str = ""
    cursor_pos = (0, 0)

    def __init__(self, screen_api):
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
            "pause": "q"
        }

        self.screen_api = screen_api

    def print_bar(self, n_columns, horizontal_wall, left_wall, middle_wall, right_wall):
        str_bar = left_wall

        horizontal_wall *= 7
        str_bar += f"{horizontal_wall}{middle_wall}" * (n_columns - 1)
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
                    str_row += f"  █-█  {vertical_wall}"
                else:
                    str_row += f"  █{char_to_print}█  {vertical_wall}"

            else:
                str_row += f"   {char_to_print}   {vertical_wall}"

        self.board_str += str_row + "\n\t"

    def key_listener(self):
        ch = self.screen_api.getch()

        ch = chr(ch).lower()

        if ch == self.keys["up"]:
            return "up"
        elif ch == self.keys["down"]:
            return "down"
        elif ch == self.keys["left"]:
            return "left"
        elif ch == self.keys["right"]:
            return "right"
        elif ch == self.keys["space"]:
            return "space"
        elif ch == self.keys["pause"]:
            return "pause"

        return None

    def print_board(self, data):
        # Empty the board before creating the new one
        self.board_str = "\t"

        # Get the length of the first row.
        if len(set(map(len, data.board.pieces))) not in (0, 1):
            return "The length of the rows in the board is not the same"
        n_columns = len(data.board.pieces[0])

        # Set the top bar
        self.print_bar(
            n_columns, self.walls["h"], self.walls["tl"], self.walls["t0"], self.walls["tr"])

        for i, row in enumerate(data.board.pieces):
            self.print_bar(
                n_columns, " ", self.walls["v"], self.walls["v"], self.walls["v"])
            self.print_row(row, i)
            self.print_bar(
                n_columns, " ", self.walls["v"], self.walls["v"], self.walls["v"])
            if i != len(data.board.pieces) - 1:
                self.print_bar(
                    n_columns, self.walls["h"], self.walls["t240"], self.walls["cross"], self.walls["t90"])
            else:
                self.print_bar(
                    n_columns, self.walls["h"], self.walls["bl"], self.walls["t180"], self.walls["br"])

        self.screen_api.clear()
        curses.curs_set(0)
        self.screen_api.scrollok(1)

        name = data.players[0].name if data.players[0].team == data.turn else data.players[1].name
        self.screen_api.addstr(f"\n\tTurn: {name} | {data.turn}\t{data.msg}\n")
        self.screen_api.addstr(self.board_str)
        self.screen_api.addstr(f"Turns left: {data.turns_left}")

        # List showing the options
        first_line = "\n\n\tMove cursor: WASD".ljust(
            51) + f"Player 1: {data.players[0].n_wins}"
        second_line = "\n\tSelect / Deselect / Move piece: space".ljust(
            50) + f"Player 2: {data.players[1].n_wins}"
        third_line = "\n\tOpen menu: Q".ljust(
            50) + f"Tie: {data.n_times_played - data.players[0].n_wins - data.players[1].n_wins}"

        self.screen_api.addstr(first_line + second_line + third_line)
