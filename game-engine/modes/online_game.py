from screens.local_game import show_local_game_screen
from game_platform.online_game_platform import OnlineGamePlatform
from modes.player import Player
from game_platform.data import Data


TURNS_IN_A_GAME = 0 # TODO just remove this from data and adjust in all classes.


class OnlineGame:
    def __init__(self, screen, conn):
        self.screen = screen
        self.conn   = conn

        name_1, name_2 = "Host", "Client"
        self.player1 = Player(name_1, "white")
        self.player2 = Player(name_2, "black")

        self.n_times_played = 0

        self.str_board = """ + - - B B B - - +
                        - - - - B - - - -
                        - - - - W - - - -
                        B - - - W - - - B
                        B B W W K W W B B
                        B - - - W - - - B
                        - - - - W - - - -
                        - - - - B - - - -
                        + - - B B B - - +"""

    def game_loop(self):

        # data - the consistent Game Stats of an Online session
        data = Data(self.player1, self.player2, "",
                    self.n_times_played, TURNS_IN_A_GAME, "")

        # Loop Game Rounds - loop until someone Quits the online session by: Q
        while True:
            # Init and Reset a new Game Object each Round
            game_round = OnlineGamePlatform(self.screen, data, self.str_board)
            current_turn_data = game_round.data

            # Loop Game Turns - loop until someone wins/tie
            while True:
                current_turn_data = game_round.polling(current_turn_data) # Polling should be ONE turn

                if game_round.event == "pause":
                    return # End the online session in host_game.py

                if game_round.event == self.player1:
                    data.players[0].n_wins += 1
                    break

                if game_round.event == self.player2:
                    data.players[1].n_wins += 1
                    break

                # Send current_turn_data to Client and await the next response
                self.conn.send(str.encode("your turn!"))

                # Wait for Client to play his/her turn
                from_client = self.conn.recv(4096).decode()
                print("from_client:\n" + from_client)

            # After each Game Round has ended:
            data.n_times_played += 1

            #
            for p in data.players:
                p.change_team()
