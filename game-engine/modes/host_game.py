import pickle
from screens.local_game import show_local_game_screen
from game_platform.online_game_platform import OnlineGamePlatform
from modes.player import Player
from game_platform.data import Data


TOT_TURNS_PER_GAME = 200 # TODO see over the Data object and make changes


class HostGame:
    def __init__(self, screen, client_socket):
        self.screen = screen
        self.client_socket   = client_socket

        name_1, name_2 = "host", "client"
        self.player1 = Player(name_1, "white")
        self.player2 = Player(name_2, "black")

        self.n_times_played = 0

        self.str_board = """+ - - B B B - - +
                            - - - - B - - - -
                            - - - - W - - - -
                            B - - - W - - - B
                            B B W W K W W B B
                            B - - - W - - - B
                            - - - - W - - - -
                            - - - - B - - - -
                            + - - B B B - - +"""

        # data - the consistent Game Stats of an Online session. Updated by the Host
        self.data = Data(self.player1, self.player2, "white",
                    self.n_times_played, TOT_TURNS_PER_GAME, "")

    def game_loop(self):

        # Loop Game Rounds - loop until someone Quits the online session by: q
        while True:
            # Send Host's master copy of the game stats to Client
            self.send_obj(self.data)

            # Init and Reset a new Game Object each Round with updated data stats
            game_round = OnlineGamePlatform(self.screen, self.data, self.str_board)
            current_turn_data = game_round.data

            # Loop Game Turns - loop until someone wins/tie or quit
            while True:
                game_round.print_game(current_turn_data)

                # if it is the Host's turn
                if self.data.players[0].team == current_turn_data.turn:
                    current_turn_data = game_round.polling(current_turn_data) # Updated each key press

                    if current_turn_data.event != None:
                        if current_turn_data.event == "pause":
                            self.send_obj(current_turn_data)
                            return # End the online session in host_socket.py

                        elif current_turn_data.event == "host":
                            self.data.players[0].n_wins += 1 # Update game stats
                            self.send_obj(current_turn_data)
                            break

                        elif current_turn_data.event == "client":
                            self.data.players[1].n_wins += 1 # Update game stats
                            self.send_obj(current_turn_data)
                            break

                    # Send current turn data to Client
                    self.send_obj(current_turn_data)

                # Wait for Client to play his/her turn
                else:
                    current_turn_data = self.receive_obj()

                    if current_turn_data.event != None:
                        if current_turn_data.event == "pause":
                            return # End the online session in host_socket.py

                        elif current_turn_data.event == "host":
                            self.data.players[0].n_wins += 1
                            break

                        elif current_turn_data.event == "client":
                            self.data.players[1].n_wins += 1
                            break

            # After each Game Round has ended:
            self.update_stats()


    def send_obj(self, msg):
        self.client_socket.send( pickle.dumps(msg) ) # Send message to Client

    def receive_obj(self):
        client_msg = self.client_socket.recv(4096)   # Listen for message from Client

        current_turn_data = pickle.loads(client_msg)
        return current_turn_data

    def update_stats(self):
        self.data.n_times_played += 1
        self.data.turns_left = TOT_TURNS_PER_GAME

        for p in self.data.players:
            p.change_team()
