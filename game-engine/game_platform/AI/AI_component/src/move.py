# -*- coding: utf-8 -*-
from game_platform.AI.AI_component.src.coordinates.coordinates import Coordinates


class Move:
    def __init__(self, start, end, player_id):
        '''
        This call assumes that the Coordintaes singleton class has been
        created already.
        '''
        self.COORDINATES = Coordinates()

        self.x_start = start.x
        self.y_start = start.y
        self.x_end = end.x
        self.y_end = end.y

        self.player_id = player_id

    def __str__(self):
        return ("({}, {}) -> ({}, {})".format(
            self.x_start,
            self.y_start,
            self.x_end,
            self.y_end)
        )

    def get_start_pos(self):
        return self.COORDINATES.get(self.x_start, self.y_start)

    def get_end_pos(self):
        return self.COORDINATES.get(self.x_end, self.y_end)
