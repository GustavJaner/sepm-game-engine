# -*- coding: utf-8 -*-

import copy
import random

from game_platform.AI.AI_component.src.ia import IAStrategy, IA
from game_platform.AI.AI_component.src.hard_strategy import HardStrategy
from game_platform.AI.AI_component.src.soft_strategy import SoftStrategy


class MediumStrategy(IAStrategy):

    def calculate_move(self, board_state):
        # The id of the class is the original player type
        self.id = board_state.get_turn_player()

        # Store an internal HardStrategy
        self.hard_strategy = HardStrategy()
        self.hard_IA = IA(self.hard_strategy)

        # Store an internal SoftStrategy
        self.soft_strategy = SoftStrategy()
        self.soft_IA = IA(self.soft_strategy)

        # Decide with 50% probability what strategy to follow
        roll = random.randint(1, 100)

        if roll <= 50:
            return self.soft_IA.calculate_move(board_state)
        else:
            return self.hard_IA.calculate_move(board_state)
