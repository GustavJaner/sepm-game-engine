import curses
import random

from screens.general import *


AI_NAMES = ["Mariam", "Alice", "Amanda", "Gustav",
            "Jenny", "Matilda", "Michael", "Mikaela", "Max"]


def show_local_game_screen(win):
    '''
    This is a function that shows a form to get the names of the players
    '''

    player1 = ""
    player2 = ""

    underscores = "_" * 50
    selected = 1

    difficulties = [None, None]
    difficulties_options = ["Easy", "Medium", "Hard"]

    while True:
        curses.curs_set(0)
        win.clear()

        if selected == 1 or selected == 2:
            win.addstr(
                f"\n\n\n\tMmmm, I am afraid I don't know you.\n\n")
            win.addstr(
                f"\n\n\tWhat is the name of Player {selected}?\n\tIf the player is an AI, just type AI in the input field. Roger, roger.\n")

            if selected == 1:
                str2print = player1.ljust(50, "_")
            elif selected == 2:
                str2print = player2.ljust(50, "_")

            win.addstr(
                f"\n\t{str2print}\n")
        else:
            win.addstr(
                f"\n\n\n\tOk. So, you are:\n\n")

        if player1 != "" and selected >= 2:
            win.addstr(
                f"\n\n\n\tPlayer 1: {player1}.\n\n")

        if player2 != "" and selected == 3:
            win.addstr(
                f"\tPlayer 2: {player2}.\n\n")

        if selected >= 3:
            win.addstr(
                f"\n\n\n\t-------------------Press any key to start-------------------\n\n")
            win.getch()

            return player1, player2, difficulties

        ch = win.getch()

        # Delete key
        if ch == 127:
            if selected == 1:
                player1 = player1[:-1]
            elif selected == 2:
                player2 = player2[:-1]

        # New line
        elif ch == 10:
            if selected == 1 and player1 != "":
                if player1 == "AI":
                    option = show_home_screen(win, difficulties_options)
                    difficulties[0] = difficulties_options[option]
                    player1 = f"{random.choice(AI_NAMES)} (AI | {difficulties_options[option]})"
                selected += 1
            if selected == 2 and player2 != "":
                if player2 == "AI":
                    option = show_home_screen(win, difficulties_options)
                    difficulties[1] = difficulties_options[option]
                    player2 = f"{random.choice(AI_NAMES)} (AI | {difficulties_options[option]})"
                selected += 1
        # Any other char will be concatenated
        else:
            if len(player1) < 50 and selected == 1:
                player1 += chr(ch)
            if len(player2) < 50 and selected == 2:
                player2 += chr(ch)


def winning_menu(win, options, wp_name, bp_name, winner, winner_team, n_whites, n_blacks, n_ties):
    current_selected = 0

    while True:
        curses.curs_set(0)
        win.clear()

        if winner != "tie":
            win.addstr(
                f"\n\n\n\tOH YEAH! {winner} ({winner_team}) won!\n\n")
        else:
            win.addstr(
                f"\n\n\n\t:( Too much movements! This game is a tie.\n\n")

        for i, option in enumerate(options):
            win.addstr("\n\t\t")
            if i == current_selected:
                win.addstr("> ")
            else:
                win.addstr("  ")

            win.addstr(option + "\n")

        first_line = f"{wp_name} (white):"
        second_line = f"{bp_name} (black):"
        third_line = "Tie:"
        strlen = max(len(first_line), len(bp_name), len(third_line)) + 3

        first_line = first_line.ljust(strlen, " ") + str(n_whites) + "\n"
        second_line = second_line.ljust(strlen, " ") + str(n_blacks) + "\n"
        third_line = third_line.ljust(strlen, " ") + str(n_ties) + "\n"

        win.addstr("\n\n\n")
        win.addstr("\t\t" + first_line)
        win.addstr("\t\t" + second_line)
        win.addstr("\t\t" + third_line)

        ch = win.getch()
        ch = chr(ch).lower()

        if ch == "w":
            if current_selected == 0:
                current_selected = len(options) - 1
            else:
                current_selected -= 1
        elif ch == "s":
            if current_selected == len(options) - 1:
                current_selected = 0
            else:
                current_selected += 1
        elif ch == " ":
            return options[current_selected]

        curses.curs_set(0)

        win.clear()
