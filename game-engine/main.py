from screens.general import show_home_screen
from modes.local_game import LocalGame
from screens.online_game import host_or_join_screen
from modes.host_game import hostGame
from modes.join_game import joinGame

import curses


<<<<<<< HEAD
HOME_SCREEN = ["Local game", "Tournament", "Quit"]
=======
HOME_SCREEN = ["Local game", "Online game", "Quit"]
>>>>>>> [P2P] Started the integration of the communication platform


if __name__ == "__main__":
    screen_api = curses.initscr()

<<<<<<< HEAD
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
=======
    if option == 0:
        LocalGame(screen_api)

    elif option == 1:
        h_or_j = host_or_join_screen(screen_api, ["Host game", "Join game"])

        if h_or_j == 0:
            hostGame(screen_api)
        elif h_or_j == 1:
            joinGame(screen_api)


    elif option == 2:
        screen_api.clear()
>>>>>>> [P2P] Started the integration of the communication platform
