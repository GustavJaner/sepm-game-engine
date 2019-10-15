import random
import curses
from screens.tournament_tree import show_tournament_setup
from screens.tournament_tree import input_player_names
from screens.tournament_tree import show_tree


from screens.local_game import show_local_game_screen
from game_platform.game_platform import GamePlatform
from modes.player import Player
from game_platform.data import Data

TURNS_IN_A_GAME = 200
NUMBER_OF_PLAYERS = ['1','2','3','4','5','6','7','8'];

class Tournament():
    def __init__(self, screen_api):
        self.screen_api = screen_api
        names = []
        options = show_tournament_setup(screen_api, NUMBER_OF_PLAYERS);
        for i in range(options+1):
            screen_api.clear()
            screen_api.scrollok(1)
            names.append(input_player_names(screen_api, i))

        #show_tree(screen_api, names)

        self.players = []
        for name in names:
            self.players.append(Player(name))
        random.shuffle(self.players)
        self.tree = []

        # Initial set up. It can be changed
        self.str_board = """ + - K B B B - - +
                             - - - - B - - - -
                             - - - - W - - - -
                             B - - - W - - - B
                             B B W W - W W B B
                             B - - - W - - - B
                             - - - - W - - - -
                             - - - - B - - - -
                             + - - B B B - - +"""
        self.play_tournament()

    def play_tournament(self):
        rounds = []
        winners = [self.players.copy()]

        while len(winners[-1]) > 1:
            if len(winners[-1]) % 2 != 0:
                winners[-1].append(None)

            # Create pairs
            pairs = list(zip(winners[-1][::2],
                             winners[-1][1::2]))
            rounds.append(pairs)
            w = self.pairs_play(pairs)
            winners.append(w)
        rounds.append(w)
        return rounds

    def pairs_play(self, pairs):
        winners = []
        for (player1, player2) in pairs:
            if player2 == None:
                winners.append(player1)
                continue

            player1.team = "white"
            player2.team = "black"
            data = Data(player1, player2, "white",
                        0, TURNS_IN_A_GAME, "")

            game_platform = GamePlatform(self.screen_api, data, self.str_board)

            if game_platform.event == "pause":
                # TODO pause screen
                break

            if game_platform.event == player1:
                winners.append(player1)

            if game_platform.event == player2:
                winners.append(player2)

        return winners
