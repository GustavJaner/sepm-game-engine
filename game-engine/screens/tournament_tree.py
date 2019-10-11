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
