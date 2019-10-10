import time
import curses


def show_home_screen(screen_api, options):
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
        screen_api.addstr("Main menu", curses.A_BOLD)
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
