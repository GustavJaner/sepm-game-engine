import curses


def host_or_join_screen(screen, options):
    screen.clear()
    screen.scrollok(1)

    current_selected = 0

    while True:

        screen.addstr("""
         _   _  _   _          ____     _     __  __  _____
        | | | || | | |        / ___|   / \   |  \/  || ____|
        | | | || | | | _____ | |  _   / _ \  | |\/| ||  _|
        | |_| || |_| ||_____|| |_| | / ___ \ | |  | || |___
         \___/  \___/         \____|/_/   \_\|_|  |_||_____|

        ====================================================
        """)

        screen.addstr("\n\n\t\t\t  ")
        screen.addstr("Play online", curses.A_BOLD)
        screen.refresh()

        screen.addstr("\n\n\n\t\t\t  ")

        for i, option in enumerate(options):
            if i == current_selected:
                screen.addstr(">  ")
            else:
                screen.addstr("   ")

            screen.addstr(option + "\n\n\t\t\t  ")

        curses.curs_set(0)

        ch = screen.getch()
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
        screen.clear()
