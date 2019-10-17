import random
import curses
from screens.tournament import *


from screens.local_game import show_local_game_screen
from game_platform.game_platform import GamePlatform
from modes.player import Player
from game_platform.data import Data

TURNS_IN_A_GAME = 200


class Tournament():
    def __init__(self, screen_api):
        self.screen_api = screen_api

        names = show_tournament_setup(screen_api)

        self.players = []
        for name in names:
            self.players.append(Player(name))

        random.shuffle(self.players)
        self.tree = []

        # Initial set up. It can be changed
        self.str_board = """ + - - B B B - - +
                             - - - - B - - - -
                             - - - - W - - - -
                             B - - - W - - - B
                             B B W W K W W B B
                             B - - - W - - - B
                             - - - - W - - - -
                             - - - - B - - - -
                             + - - B B B - - +"""
        self.play_tournament()

    def play_tournament(self):
        rounds = []
        winners = [self.players.copy()]

        n_round = 1

        show_tree(self.screen_api, [[x for x in self.players]])
        self.screen_api.addstr(f"\n\n\tRound {n_round}")
        self.screen_api.addstr("\n\tPress any key to play next round")
        self.screen_api.getch()

        w = []
        while len(winners[-1]) > 1:
            if len(winners[-1]) % 2 != 0:
                winners[-1].append(None)

            # Create pairs
            pairs = list(zip(winners[-1][::2],
                             winners[-1][1::2]))
            rounds.append(pairs)

            w = self.pairs_play(pairs, n_round)
            winners.append(w)

            if len(w) > 1:
                show_tree(self.screen_api, winners)
                self.screen_api.addstr(f"\n\n\tRound {n_round}")
                self.screen_api.addstr("\n\tPress any key to play next round")
                self.screen_api.getch()
                n_round += 1
            elif len(w) == 1:
                rounds.append(w)
                show_tree(self.screen_api, winners)
                self.screen_api.addstr(
                    f"\n\n\tEnd of the tournament. Congratulations {w[0].name}")
                self.screen_api.addstr(
                    "\n\tPress any key to go to the main menu")

                self.screen_api.getch()

        return rounds

    def pairs_play(self, pairs, n):
        winners = []
        for (player1, player2) in pairs:
            if player2 == None:
                winners.append(player1)
                continue

            player1.team = "white"
            player2.team = "black"
            data = Data(player1, player2, "white",
                        0, TURNS_IN_A_GAME, "", "tournament", n)

            game_platform = GamePlatform(self.screen_api, data, self.str_board)

            if game_platform.event == "pause":
                # TODO pause screen
                break

            if game_platform.event == player1:
                winners.append(player1)
            else:  # In case of tie, player 2 wins. We don't have the specification for this case!
                winners.append(player2)

        return winners
