import time


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

        win.clear()
