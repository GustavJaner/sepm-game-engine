import time
import curses


def set_home_screen(win, options):
    win.clear()

    current_selected = 0

    while True:
        win.addstr(
            f"\n\n\n\tWelcome to UU_GAME. Please select an option.\n\n")
        for i, option in enumerate(options):
            win.addstr("\n\t\t")
            if i == current_selected:
                win.addstr("> ")
            else:
                win.addstr("  ")

            win.addstr(option + "\n")

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


def set_local_game_screen(win):
    '''
    This is a function that shows a form to get the names of the players
    '''

    player1 = ""
    player2 = ""

    underscores = "_" * 50
    selected = 1

    while True:
        curses.curs_set(0)
        win.clear()

        if selected == 1 or selected == 2:
            win.addstr(
                f"\n\n\n\tMmmm, I am afraid I don't know you.\n\n")
            win.addstr(f"\n\n\tWhat is the name of Player {selected}?\n")

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
                f"\n\n\n\t-------------------Press any key to start:-------------------\n\n")
            win.getch()

            return player1, player2

        ch = win.getch()

        # Delete key
        if ch == 127:
            player1 = player1[:-1]
        # New line
        elif ch == 10:
            if selected == 1 and player1 != "":
                selected += 1
            if selected == 2 and player2 != "":
                selected += 1
        # Any other char will be concatenated
        else:
            if len(player1) < 50 and selected == 1:
                player1 += chr(ch)
            if len(player2) < 50 and selected == 2:
                player2 += chr(ch)
