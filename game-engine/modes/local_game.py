from screens.local_game import show_local_game_screen
from game_platform.game_platform import GamePlatform
from modes.player import Player
from game_platform.data import Data


TURNS_IN_A_GAME = 200


class LocalGame():
    def __init__(self, screen_api):
        name_1, name_2, difficulties = show_local_game_screen(screen_api)

        player1 = Player(name_1, "white")
        player2 = Player(name_2, "black")

        n_times_played = 0

        # Initial set up. It can be changed
        str_board = """ + - - B B B - - +
                        - - - - B - - - -
                        - - - - W - - - -
                        B - - - W - - - B
                        B B W W K W W B B
                        B - - - W - - - B
                        - - - - W - - - -
                        - - - - B - - - -
                        + - - B B B - - +"""

        while True:

            data = Data(player1, player2, "white",
                        n_times_played, TURNS_IN_A_GAME, "")
            game_platform = GamePlatform(screen_api, data, str_board)

            if game_platform.event == "pause":
                # TODO pause screen
                break

            n_times_played += 1

            if game_platform.event == player1:
                data.players[0].n_wins += 1

            if game_platform.event == player2:
                data.players[1].n_wins += 1

            for p in data.players:
                p.change_team()
