# -*- coding: utf-8 -*-

import random

from game_platform.AI.AI_component.src.ia import IAStrategy


class SoftStrategy(IAStrategy):

    def calculate_move(self, board_state):
        # The id of the class is the original player type
        self.id = board_state.get_turn_player()

        # Get candidates moves
        candidates = board_state.get_all_legal_moves()

        # Randomly choose one of them
        choice = random.choice(candidates)

        return choice
