import pickle
from screens.local_game import show_local_game_screen
from game_platform.online_game_platform import OnlineGamePlatform
from modes.player import Player
from game_platform.data import Data


class ClientGame:
    def __init__(self, screen, client_socket):
        self.screen = screen
        self.client_socket = client_socket

        self.str_board = """+ - - B B B - - +
                            - - - - B - - - -
                            - - - - W - - - -
                            B - - - W - - - B
                            B B W W K W W B B
                            B - - - W - - - B
                            - - - - W - - - -
                            - - - - B - - - -
                            + - - B B B - - +"""

    def game_loop(self):

        # Loop Game Rounds - loop until someone Quits the online session by: q
        while True:
            # Receive data with game stats from Host
            host_data = self.receive_obj()

            # Init and Reset a new Game Object each Round with updated data stats
            game_round = OnlineGamePlatform(self.screen, host_data, self.str_board)
            current_turn_data = game_round.data

            # Loop Game Turns - loop until someone wins/tie or quit
            while True:
                game_round.print_game(current_turn_data)

                # if it is the Client's turn
                if host_data.players[1].team == current_turn_data.turn:
                    current_turn_data = game_round.polling(current_turn_data) # Updated each key press

                    if current_turn_data.event != None:
                        if current_turn_data.event == "pause":
                            self.send_obj(current_turn_data)
                            return # End the online session in client_socket.py

                        elif current_turn_data.event == "host":
                            self.send_obj(current_turn_data) # Let host update the game stats
                            break

                        elif current_turn_data.event == "client":
                            self.send_obj(current_turn_data) # Let host update the game stats
                            break

                    # Send current turn data to Host
                    self.send_obj(current_turn_data)

                # Wait for Host to play his/her turn
                else:
                    current_turn_data = self.receive_obj()

                    if current_turn_data.event != None:
                        if current_turn_data.event == "pause":
                            return # End the online session in client_socket.py

                        elif current_turn_data.event == "host":
                            break

                        elif current_turn_data.event == "client":
                            break


    def send_obj(self, msg):
        self.client_socket.send( pickle.dumps(msg) ) # Send message to Host

    def receive_obj(self):
        host_msg = self.client_socket.recv()         # Listen for message from Host

        current_turn_data = pickle.loads(host_msg)
        return current_turn_data
