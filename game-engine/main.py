
from screens.general import show_home_screen

import curses


HOME_SCREEN = ["Local game", "Quit"]


if __name__ == "__main__":
    screen_api = curses.initscr()
    option = show_home_screen(screen_api, HOME_SCREEN)

    if option == 0:
        from modes.local_game import LocalGame
        LocalGame(screen_api)

    elif option == 1:
        screen_api.clear()
