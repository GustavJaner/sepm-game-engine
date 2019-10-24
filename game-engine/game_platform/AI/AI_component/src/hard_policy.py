# -*- coding: utf-8 -*-

import move

from board import BoardState
from coordinates.coord import Coord

'''
This class is mostly used to keep methods that are used in the the game state
evaluation function used by Minimax.
'''


class Policy:

    def evaluation(board_state, player_id):
        opponent = board_state.get_opponent_id()
        my_pieces_value = board_state.get_num_player_pieces(player_id)
        opponent_pieces_value = board_state.get_num_player_pieces(opponent)

        turn = board_state.get_turn_number()

        '''
        The evaluation function is different when the player is White or
        Black.
        '''
        evaluation_value = 0.0

        if player_id == BoardState.Player.WHITE:
            '''
            The White player evaluation function becomes more aggressive as
            the game progresses in terms of: the number of moves for the king
            to reach a corner.
            '''
            if turn < 40:
                evaluation_value = my_pieces_value - \
                        opponent_pieces_value + \
                        Policy.king_value(board_state)
            elif turn < 70:
                evaluation_value = my_pieces_value - \
                        opponent_pieces_value + \
                        2.0 * Policy.king_value(board_state)
            else:
                evaluation_value = my_pieces_value - \
                        opponent_pieces_value + \
                        3.0 * Policy.king_value(board_state)

        else:
            '''
            The black player evaluation function becomes more aggressive as the
            game progresses in terms of: (i) the number of enemy pieces around
            the king and (ii) the number of moves for the king to reach corner.
            '''
            if turn < 40:
                evaluation_value = my_pieces_value - opponent_pieces_value + \
                        Policy.pieces_around_corner(board_state) - \
                        Policy.king_value(board_state) + \
                        Policy.enemy_pieces_around_king(board_state)
            elif turn < 70:
                evaluation_value = 2.0 * (my_pieces_value - opponent_pieces_value) + \
                        Policy.pieces_around_corner(board_state) - \
                        1.5 * Policy.king_value(board_state) + \
                        6 * Policy.enemy_pieces_around_king(board_state)
            else:
                evaluation_value = 3.0 * (my_pieces_value - opponent_pieces_value) + \
                        Policy.pieces_around_corner(board_state) - \
                        12 * Policy.king_value(board_state) + \
                        6 * Policy.enemy_pieces_around_king(board_state)

        return evaluation_value

    def enemy_pieces_around_king(board_state):
        '''
        Given a game state, this method returns a value used in board state
        evaluation which represents the number of enemy pieces surrounding the
        King.
        '''
        num_pieces = 0.0
        king_position = board_state.get_king_position()
        king_neighbors = BoardState.COORDINATES.get_neighbors(king_position)

        for coord in king_neighbors:
            if board_state.get_piece_at(coord) == board_state.Piece.BLACK:
                num_pieces = num_pieces + 0.25

        return num_pieces

    def pieces_around_corner(board_state):
        '''
        Given a game state, this method returns a value used in board state
        evaluation for the number of black pieces in key strategic locations
        near the corners.

        These locations were determined to be useful for the black player in
        maintaining an advantage during the game.
        '''
        value = 0.0

        crit_pos = board_state.DEFAULT_BOARD_SIZE - 1
        if board_state.get_piece_at(Coord(1, 1)) == board_state.Piece.BLACK:
            value = value + 0.25

        if board_state.get_piece_at(Coord(1, crit_pos)) == board_state.Piece.BLACK:
            value = value + 0.25

        if board_state.get_piece_at(Coord(crit_pos, 1)) == board_state.Piece.BLACK:
            value = value + 0.25

        if board_state.get_piece_at(Coord(1, crit_pos)) == board_state.Piece.BLACK:
            value = value + 0.25

        return value

    def king_value(board_state):
        '''
        This method returns a value representing the number of king moves to
        all the corners.

        Given a state, the method checks the min number of moves to
        each corner, and returns a positive value if we are within 1-2 moves to
        a certain corner, and an even higher value if we are withing 1-2 moves
        to more than one corner.
        '''
        king_position = board_state.get_king_position()

        # Retrieves all legal moves for the king based on its current position
        king_moves = Policy.get_all_legal_king_moves(
            king_position,
            board_state)

        move_distance_value = 0.0
        if len(king_moves) > 0:
            # Stores the min number of moves to reach each of the 4 corners
            distances = [0] * 4

            '''
            Iterate through all corners, calculating the min number of moves
            to reach each one.
            '''
            for idx, coord in enumerate(board_state.COORDINATES.get_corners()):
                distances[idx] = Policy.calculate_min_moves_to_corner(
                    board_state,
                    coord,
                    1,
                    king_position)

            # Generate the move's value based on proximity to the corner
            for i in range(len(distances)):
                if distances[i] == 1:
                    move_distance_value = move_distance_value + 15

                if distances[i] == 2:
                    move_distance_value = move_distance_value + 1

        return(move_distance_value)

    def calculate_min_moves_to_corner(board_state,
                                      corner,
                                      move_counter,
                                      king_position):
        '''
        This method calculates the min number of moves for the king to reach a
        given corner.

        This is done by ignoring opponent moves. We simply care about how many
        consecutive moves it would take the king to reach a specific corner.
        This is because it becomes very difficult (and costly) to predict
        opponent moves as well.

        This method projects a move onto the board state and recursively goes
        to the following move, but does not actually process the move in order
        to be more efficient (time and memory-wise).
        '''
        if move_counter == 3 or board_state.COORDINATES.is_corner(king_position):
            return move_counter

        king_moves = Policy.get_all_legal_king_moves(
            king_position,
            board_state)

        # We'll store the counts for each move here
        internal_move_counter = [0] * len(king_moves)

        '''
        Iterate through current possible king moves and see how much closer we
        can get to a corner.
        '''
        for idx, move in enumerate(king_moves):
            start_coord = move.get_start_pos()
            end_coord = move.get_end_pos()
            if start_coord.max_diff(corner) > end_coord.max_diff(corner):
                internal_move_counter[idx] = \
                        Policy.calculate_min_moves_to_corner(
                            board_state,
                            corner,
                            move_counter + 1,
                            king_position)

        '''
        Find the min number of moves to reach the corner, or return 50 if
        unreachable.
        '''
        min_value = 50
        for idx, move in enumerate(internal_move_counter):
            if move != 0 and move < min_value:
                min_value = move

        return min_value

    def get_all_legal_king_moves(start_coord, board_state):
        legal_moves = list()

        valid_coords = list()
        valid_coords = valid_coords + board_state.get_legal_coords_direction(
            start_coord,
            'N')
        valid_coords = valid_coords + board_state.get_legal_coords_direction(
            start_coord,
            'S')
        valid_coords = valid_coords + board_state.get_legal_coords_direction(
            start_coord,
            'E')
        valid_coords = valid_coords + board_state.get_legal_coords_direction(
            start_coord,
            'W')

        for end_coord in valid_coords:
            legal_moves.append(
                move.Move(start_coord, end_coord, board_state.get_turn_player))

        return legal_moves
