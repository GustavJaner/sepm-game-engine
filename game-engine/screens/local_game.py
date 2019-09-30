import curses


def show_local_game_screen(win):
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
                f"\n\n\n\t-------------------Press any key to start-------------------\n\n")
            win.getch()

            return player1, player2

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
                selected += 1
            if selected == 2 and player2 != "":
                selected += 1
        # Any other char will be concatenated
        else:
            if len(player1) < 50 and selected == 1:
                player1 += chr(ch)
            if len(player2) < 50 and selected == 2:
                player2 += chr(ch)
