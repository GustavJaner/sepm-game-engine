from screens.general import show_home_screen
from modes.local_game import LocalGame
from screens.online_game import host_or_join_screen
from modes.host_socket import host_socket
from modes.client_socket import client_socket

import curses


HOME_SCREEN = ["Local game", "Online game", "Tournament", "Quit"]

if __name__ == "__main__":
    screen_api = curses.initscr()

    while True:
        option = show_home_screen(screen_api, HOME_SCREEN)
        if option == 0:
            from modes.local_game import LocalGame
            LocalGame(screen_api)

        elif option == 1:
            h_or_j = host_or_join_screen(screen_api, ["Host game", "Join game"])

            if h_or_j == 0:
                host_socket(screen_api)
            elif h_or_j == 1:
                client_socket(screen_api)

        elif option == 2:
            from modes.tournament import Tournament
            Tournament(screen_api)

        elif option == 3:
            screen_api.clear()
            break
