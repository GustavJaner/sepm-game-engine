import curses
import time

COORDS_NAMES = [
    # For 2 players
    [[(0, 0), (0, 2)], [(1, 1)]],
    # For 3 players
    [[(0, 0), (0, 2), (0, 4)], [(1, 1), (1, 3)], [(2, 2)]],
    # For 4 players
    [[(0, 0), (0, 2), (0, 4), (0, 6)], [(1, 1), (1, 5)], [(2, 3)]],
    # For 5 players
    [[(0, 0), (0, 2), (0, 4), (0, 6), (0, 8)], [
        (1, 1), (1, 5), (1, 7)], [(2, 3), (2, 6)], [(3, 4)]],
    # For 6 players
    [[(0, 0), (0, 2), (0, 4), (0, 6), (0, 8), (0, 10)], [
        (1, 1), (1, 5), (1, 9)], [(2, 3), (2, 5)], [(3, 4)]],
    # For 7 players
    [[(0, 0), (0, 2), (0, 4), (0, 6), (0, 8), (0, 10), (0, 12)], [
        (1, 1), (1, 5), (1, 9), (1, 11)], [(2, 3), (2, 10)], [(3, 6)]],
    # For 8 players
    [[(0, 0), (0, 2), (0, 4), (0, 6), (0, 8), (0, 10), (0, 12), (0, 14)], [
        (1, 1), (1, 5), (1, 9), (1, 13)], [(2, 3), (2, 11)], [(3, 6)]],
]


def show_tree(win, rounds):
    win.scrollok(1)

    temp = [[]] * len(rounds)
    for i, r in enumerate(rounds):
        temp[i] = [""] * len(r)

    # Max length of the names
    lj = len(max(rounds[0], key=len))

    for i, r in enumerate(rounds):
        for j, c in enumerate(r):
            temp[i][j] = rounds[i][j]
            print_tree(win, temp, lj)
            time.sleep(.3)
def show_tournament_setup(screen_api, options):
    screen_api.clear()
    screen_api.scrollok(1)

    current_selected = 0

    while True:

        screen_api.addstr("""
         _   _  _   _          ____     _     __  __  _____ 
        | | | || | | |        / ___|   / \   |  \/  || ____|
        | | | || | | | _____ | |  _   / _ \  | |\/| ||  _|  
        | |_| || |_| ||_____|| |_| | / ___ \ | |  | || |___ 
         \___/  \___/         \____|/_/   \_\|_|  |_||_____|

        ====================================================
        """)

        screen_api.addstr("\n\n\t\t\t  ")
        screen_api.addstr("How many players are going to play this wonderful tournament", curses.A_BOLD)
        screen_api.refresh()

        screen_api.addstr("\n\n\n\t\t\t  ")

        for i, option in enumerate(options):
            if i == current_selected:
                screen_api.addstr(">  ")
            else:
                screen_api.addstr("   ")

            screen_api.addstr(option + "\n\n\t\t\t  ")

        curses.curs_set(0)

        ch = screen_api.getch()
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
            return current_selected
        screen_api.clear()

def input_player_names(win, player):
    '''
    This is a function that shows a form to get the names of the players
    '''

    player1 = ""

    underscores = "_" * 50
    selected = 1

    while True:
        curses.curs_set(0)
        win.clear()

        if selected == 1:
            win.addstr(
                f"\n\n\n\tMmmm, I am afraid I don't know you.\n\n")
            win.addstr(f"\n\n\tWhat is the name of Player {player}?\n")

            if selected == 1:
                str2print = player1.ljust(50, "_")
            win.addstr(
                f"\n\t{str2print}\n")
        else:
            win.addstr(
                f"\n\n\n\tOk. So, you are:\n\n")

        if player1 != "" and selected >= 2:
            win.addstr(
                f"\n\n\n\tPlayer 1: {player1}.\n\n")

        if selected >= 2:
            return player1

        ch = win.getch()

        # Delete key
        if ch == 127:
            if selected == 1:
                player1 = player1[:-1]
        # New line
        elif ch == 10:
            if selected == 1 and player1 != "":
                selected += 1
        # Any other char will be concatenated
        else:
            if len(player1) < 50 and selected == 1:
                player1 += chr(ch)

def print_tree(win, rounds, lj):
    win.clear()
    win.addstr("\n\n\t\t\tTournament\n\n\n")

    grid_size = {
        "height": len(rounds[0]) * 4,
        "width": len(rounds)
    }

    grid = []

    for r in range(grid_size["height"]):
        grid.append([" " * lj] * grid_size["width"])

    for i, r in enumerate(rounds):
        for name, (x, y) in list(zip(r, COORDS_NAMES[len(rounds[0]) - 2][i])):
            grid[y * 2][x] = name.ljust(lj, " ")

    tree = []
    for row in grid:
        players = [p for p in row]
        tree.append("  |  ".join(players))

    tree = "\t" + "\n\t".join(tree)

    r_titles = ["First round", "Second round", "Third round", "Fourth round"]
    header = ""
    if len(rounds[0]) <= 2:
        header += "  " + r_titles[0].ljust(lj, " ") + "  "
        header += "  " + "Winner".ljust(lj, " ") + "  "
    elif len(rounds[0]) > 2 and len(rounds[0]) <= 4:
        header += "  " + r_titles[0].ljust(lj, " ") + "  "
        header += "  " + r_titles[1].ljust(lj, " ") + "  "
        header += "  " + "Winner".ljust(lj, " ") + "  "
    else:
        header += "  " + r_titles[0].ljust(lj, " ") + "  "
        header += "  " + r_titles[1].ljust(lj, " ") + "  "
        header += "  " + r_titles[2].ljust(lj, " ") + "  "
        header += "  " + "Winner".ljust(lj, " ") + "  "

    win.addstr("\t" + header + "\n\t" + "_" * len(header) + "\n\n" + tree)
    win.refresh()
