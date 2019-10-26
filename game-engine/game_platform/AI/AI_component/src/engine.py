# -*- coding: utf-8 -*-

import json

import board
import ia
import utils

import soft_strategy
import medium_strategy
import hard_strategy


class EngineNotInitialized(Exception):
    """Raised when the engine has not been initialized properly"""
    pass


class FileIntegrityError(Exception):
    """Raised when checking the content of an input json file"""
    pass


class GameEngine(metaclass=utils.Singleton):
    '''
    Wrapper class to manage the different strategies.
    '''
    def __init__(self):
        self.is_initialized = False

    def initialize(self, data):
        self.game_id = data.get('gameUID', None)
        self.game = data.get('game', None)
        self.description = data.get('description', None)

        try:
            self.game_config = data['gameConfig']

            if self.game_config['AIDifficulty'] == "Soft":
                self.strategy = soft_strategy.SoftStrategy()
            elif self.game_config['AIDifficulty'] == "Medium":
                self.strategy = medium_strategy.SoftStrategy()
            else:
                self.strategy = hard_strategy.HardStrategy()

        except Exception:
            raise Exception

        self.IA = ia.IA(self.strategy)

        self.board_state = board.BoardState()
        self.board_state.initialize(data)

        self.is_initialized = True

    def initialize_from_file(self, json_file):
        '''
        This is an alternative initialization method that reads a json file and
        uses it to call the initialize method.
        '''
        with open(json_file, 'r') as f:
            data = json.load(f)

        self.initialize(data)

    def compute(self):
        '''
        Main method to compute a move and return the original dictionary with
        the new move realized.
        '''
        if not self.is_initialized:
            raise EngineNotInitialized

        move = self.IA.calculate_move(self.board_state)
        self.board_state.process_move(move)

        board_coordinates = self.board_state.dump()

        res = {
            'gameUID': self.game_id,
            'game': self.game,
            'description': self.description,
            'gameConfig': self.game_config,
            'boardStatus': board_coordinates
        }

        return res

    def check_file_integrity(self, json_file):
        '''
        Helper method to check the integrity of an input file. Created for
        debugging purposes.
        '''
        with open(json_file, 'r') as f:
            data = json.load(f)

            if 'gameUID' not in data:
                raise FileIntegrityError

            if 'game' not in data:
                raise FileIntegrityError

            if 'description' not in data:
                raise FileIntegrityError

            game_config = data.get('gameConfig', None)
            if game_config is None:
                raise FileIntegrityError

            if 'maxTurns' not in game_config:
                raise FileIntegrityError

            if 'AIDifficulty' not in game_config:
                raise FileIntegrityError

            if game_config['AIDifficulty'] not in ["Hard", "Medium", "Soft"]:
                raise FileIntegrityError

            board_state = data.get('boardStatus', None)
            if board_state is None:
                raise FileIntegrityError

            size = board_state.get('size', None)
            if size is None:
                raise FileIntegrityError

            coordinates = board_state.get('coordinates', None)
            if coordinates is None:
                raise FileIntegrityError

            if board_state['nextPlayer'] not in ["WHITE", "BLACK"]:
                raise FileIntegrityError

            turn = board_state.get('nextTurn', None)
            if size is None:
                raise FileIntegrityError

            if turn > 200:
                raise FileIntegrityError

            self.check_coordinates_integrity(size, coordinates)

    def check_coordinates_integrity(self, board_size, coordinates):
        try:
            for coord in coordinates:
                x = coord['x']
                y = coord['y']
                piece = coord['piece']

                if x < 0 or x >= board_size:
                    raise FileIntegrityError

                if y < 0 or y >= board_size:
                    raise FileIntegrityError

                if piece not in ['WHITE', 'KING', 'BLACK', 'EMPTY']:
                    raise FileIntegrityError

        except Exception:
            raise FileIntegrityError
