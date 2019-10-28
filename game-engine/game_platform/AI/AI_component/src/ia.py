# -*- coding: utf-8 -*-

import abc


class IA:
    def __init__(self, strategy):
        self._strategy = strategy

    def calculate_move(self, board_status):
        return self._strategy.calculate_move(board_status)


class IAStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def calculate_move(self, board_status):
        pass
