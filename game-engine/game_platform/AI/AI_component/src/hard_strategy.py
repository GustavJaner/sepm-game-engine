# -*- coding: utf-8 -*-

import copy
from datetime import datetime, timedelta
import math

from ia import IAStrategy
from hard_policy import Policy


class HardStrategy(IAStrategy):
    # Maximum depth search for the minimax algorithm
    DEFAULT_MAX_DEPTH = 2

    # Maximum evaluation time for a move 120000ms ~ 2min
    DEFAULT_TIME_LIMIT = 120000

    POLICY = Policy

    def calculate_move(self, board_state):
        # The id of the class is the original player type
        self.id = board_state.get_turn_player()

        # Min max algorithm with alpha beta prunning
        return self.minimax_decision(
            board_state.get_all_legal_moves(),
            board_state)

    def minimax_decision(self, moves, board_state):
        # Keeps track of when the move was started in order to avoid timeouts
        start_time = datetime.now()

        # Stores the value of every possible move for the current board state
        move_values = [-math.inf] * len(moves)

        # This was found to be the max depth value which causes min. timeouts
        max_depth = self.DEFAULT_MAX_DEPTH

        '''
        Iterate through all possible moves and assign a value to each of them
        using mimimax (with α - β pruning) and the evaluation function.
        '''
        for idx, current_move in enumerate(moves):
            '''
            Evaluating a move to depth 3 takes up to 60ms in most cases, thus
            if we reach 120000ms, return the best move found thus far.
            '''
            print("CURRENT MOVE: ", current_move)
            delta = timedelta(milliseconds=self.DEFAULT_TIME_LIMIT)
            if datetime.now() - start_time > delta:
                print("TIMEOUT!")
                return moves[move_values.index(max(move_values))]

            '''
            Clone the board state and apply the move to obtain the new game
            state and evaluate it using minimax.
            '''
            new_board_state = copy.deepcopy(board_state)
            new_board_state.process_move(current_move)

            if (new_board_state.winner == self.id):
                return current_move

            move_values[idx] = self.minimax_value(
                new_board_state,
                -10000,
                10000,
                1,
                max_depth
            )

        return moves[move_values.index(max(move_values))]

    def minimax_value(self,
                      board_state,
                      alpha,
                      beta,
                      depth,
                      max_depth):
        print(" - value = (a: {}, b: {}, d: {})".format(alpha, beta, depth))
        '''
        This implementation of the MiniMaxValue() method is a hybrid between
        the pseudocode of minimax used in the AI course and the code for alpha
        beta pruning.

        It traverses the game state tree by generating successor states
        recursively and evaluating "leaf" nodes when the maximum intended depth
        is reached.
        '''
        if board_state.is_game_over():
            winner = board_state.winner

            if winner == self.id:
                return math.inf

            return -math.inf

        if depth == max_depth:
            return self.POLICY.evaluation(
                board_state,
                board_state.get_turn_player())

        # Finally, continue to generate and explore the search tree.
        successors = self.get_successors(board_state)

        if self.id == board_state.get_turn_player():
            for state in successors:
                alpha = max(
                    alpha,
                    self.minimax_value(state,
                                       alpha,
                                       beta,
                                       depth + 1,
                                       max_depth)
                )

                if alpha >= beta:
                    return beta

            return alpha

        else:
            for state in successors:
                beta = min(
                    beta,
                    self.minimax_value(state,
                                       alpha,
                                       beta,
                                       depth + 1,
                                       max_depth)
                )

                if alpha >= beta:
                    return alpha

            return beta

    def get_successors(self, board_state):
        '''
        Retrieves all successor states for a given board state by applying
        all legal moves to clones of the current board state.
        '''
        successors = list()

        for move in board_state.get_all_legal_moves():
            new_board_state = copy.deepcopy(board_state)
            # print("Processing.... ", move)
            new_board_state.process_move(move)
            # print("Processed")
            successors.append(new_board_state)

        return successors

    '''
    Provisional evaluation used for testing purposes.
    '''
    def basic_eval(self, board_state, player_id):
        current_player = board_state.get_turn_player()
        opponent = board_state.get_opponent_id()

        piece_diff = float(
            board_state.get_num_player_pieces(current_player) -
            board_state.get_num_player_pieces(opponent))

        print(" - eval = ", piece_diff)
        return piece_diff
