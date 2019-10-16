
from screens.general import show_home_screen

import curses


HOME_SCREEN = ["Local game", "Tournament", "Quit"]


if __name__ == "__main__":
    screen_api = curses.initscr()

    while True:
        option = show_home_screen(screen_api, HOME_SCREEN)
        if option == 0:
            from modes.local_game import LocalGame
            LocalGame(screen_api)

        elif option == 1:
            from modes.tournament import Tournament
            Tournament(screen_api)

        elif option == 2:
            screen_api.clear()
            break
