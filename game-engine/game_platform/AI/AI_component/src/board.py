# -*- coding: utf-8 -*-

import enum
import json

import game_platform.AI.AI_component.src.constants as constants
import game_platform.AI.AI_component.src.move as move

from game_platform.AI.AI_component.src.coordinates.coordinates import Coordinates


class IllegalMoveException(Exception):
    """Raised when the internal move processed is illegal"""
    pass


class BoardState:
    '''
    The BoardState is the class responsible for both, keeping track of the
    status of a board and implementing the game logic.

    Internally, it uses an instance of the Coordinates class to pair each piece
    with a given square in the board.

    It also provides the methods Initialize and ... to.
    '''

    # Default UU-GAME version with 11x11
    DEFAULT_BOARD_SIZE = constants.DEFAULT_BOARD_SIZE

    # Maximum number of moves/player
    DEFAULT_MAX_TURNS = constants.DEFAULT_MAX_TURNS

    # Internal identifier for the players in the game
    class Player(enum.Enum):
        WHITE = 1
        BLACK = -1

    FIRST_PLAYER = Player.WHITE

    # Internal identifier for the pieces in the game
    class Piece(enum.Enum):
        KING = 0
        WHITE = 1
        BLACK = 2
        EMPTY = -1

    # Static pointer to the flyweight factory storing the coordinates
    COORDINATES = Coordinates(constants.DEFAULT_BOARD_SIZE)

    def __init__(self):
        self._board = [
            [self.Piece.EMPTY for x in range(self.DEFAULT_BOARD_SIZE)] for
            y in range(self.DEFAULT_BOARD_SIZE)
        ]
        self._white_coords = list()
        self._black_coords = list()
        self._king_coord = None
        self._next_player = None
        self._next_turn = None
        self.winner = None

    def initialize(self, data):
        '''
        This is one of the core methods, that must be called before trying any
        strategy. It reads an input dictionary with the description of the
        board status and populates this class.

        Note that this method (as most of the BoardState class) does not
        validate that the status sent is correct. For example, failing to add
        a King to the input file will end automatically the game, as
        self._king_coord = None.
        '''
        next_player = data['boardStatus'].get('nextPlayer', self.Player.WHITE)
        if next_player == 'BLACK':
            self._next_player = self.Player.BLACK
        else:
            self._next_player = self.Player.WHITE

        self._next_turn = data['boardStatus'].get('nextTurn', 1)

        for coord in data['boardStatus']['coordinates']:
            piece = coord['piece']
            x = coord['x']
            y = coord['y']

            if piece == "KING":
                self._board[x][y] = self.Piece.KING
                self._king_coord = self.COORDINATES.get(x, y)
                self._white_coords.append(self.COORDINATES.get(x, y))

            if piece == "WHITE":
                self._board[x][y] = self.Piece.WHITE
                self._white_coords.append(self.COORDINATES.get(x, y))

            if piece == "BLACK":
                self._board[x][y] = self.Piece.BLACK
                self._black_coords.append(self.COORDINATES.get(x, y))

    def initialize_from_file(self, json_file):
        '''
        This is an alternative initialization method that reads a json file and
        uses it to call the initialize method.
        '''
        with open(json_file, 'r') as f:
            data = json.load(f)

        self.initialize(data)

    def dump(self):
        coordinates = list()
        for coord in self.COORDINATES:
            piece = self.get_piece_at(coord)
            if piece == self.Piece.WHITE:
                piece_str = "WHITE"
            elif piece == self.Piece.KING:
                piece_str = "KING"
            elif piece == self.Piece.BLACK:
                piece_str = "BLACK"
            elif piece == self.Piece.EMPTY:
                piece_str = "EMPTY"

            coordinates.append(
                {
                    "x": coord.x,
                    "y": coord.y,
                    "piece": piece_str
                }
            )

        if self._next_player == self.Player.WHITE:
            player_str = "WHITE"
        else:
            player_str = "BLACK"

        res = {
            "size": self.DEFAULT_BOARD_SIZE,
            "coordinates": coordinates,
            "nextPlayer": player_str,
            "nextTurn": self._next_turn
        }

        return res

    def process_move(self, move):
        '''
        This method is responsible for cheching the logic of the game and to
        update the status of the board when a new legal move is received.
        '''
        if self.is_move_legal(move) is False:
            raise IllegalMoveException

        # Process move
        old_coord = move.get_start_pos()
        new_coord = move.get_end_pos()
        piece = self.get_piece_at(old_coord)

        # Update internal data structures
        player_coordinates = self.get_current_player_coordinates()
        player_coordinates.remove(old_coord)
        player_coordinates.append(new_coord)
        if piece == self.Piece.KING:
            self._king_coord = new_coord

        # Update the board
        self._board[old_coord.x][old_coord.y] = self.Piece.EMPTY
        self._board[new_coord.x][new_coord.y] = piece

        '''
        Check if a capture occured, knowing that only a piece next to the new
        position could be captured.
        '''
        captured_enemies = list()
        for enemy in self.COORDINATES.get_neighbors(new_coord):
            if self.is_opponent_piece_at(enemy):
                can_capture = True

                '''
                If the piece is a King, we need to check if is at the center
                or neighbors of the center. If it is true, it cannot be
                captured.
                '''
                if self.get_piece_at(enemy) == self.Piece.KING:
                    if self.COORDINATES.is_center_or_neighbor_center(
                        self._king_coord
                    ):
                        can_capture = False

                    # Then, we need 4 sides to capture.
                    for threat in self.COORDINATES.get_neighbors(enemy):
                        if self.get_piece_at(threat) != self.Piece.BLACK:
                            can_capture = False
                            break

                # It the piece is not a King, I just need two threats
                else:
                    threats = 0
                    for threat in self.COORDINATES.get_neighbors(enemy):
                        threat_player = self._piece_to_player(
                            self.get_piece_at(threat))
                        if threat_player == self._next_player:
                            threats = threats + 1

                    if threats < 2:
                        can_capture = False

                if can_capture:
                    captured_enemies.append(enemy)

        # Update internal data structures after captures.
        for coord in captured_enemies:
            if self.get_piece_at(coord) == self.Piece.KING:
                self._king_coord = None

            opponent_coordinates = self._get_player_coordinates(
                self.get_opponent_id()
            )
            opponent_coordinates.remove(coord)
            self._board[coord.x][coord.y] = self.Piece.EMPTY

        # Update turn counter
        if self._next_player != self.FIRST_PLAYER:
            self._next_turn = self._next_turn + 1

        # Update player and game status
        self._next_player = self.get_opponent_id()
        self._update_winner()

    def _update_winner(self):
        '''
        Determines if a player has won by updating the internal variables.
        '''
        if self._king_coord is None:
            self.winner = self.Player.BLACK

        elif not self._has_player_legal_move(self.Player.WHITE):
            self.winner = self.Player.BLACK

        elif self.COORDINATES.is_corner(self._king_coord):
            self.winner = self.Player.WHITE

        elif not self._has_player_legal_move(self.Player.BLACK):
            self.winner = self.Player.WHITE

    def get_all_legal_moves(self):
        '''
        Get all legal moves for the player. This may be expensive, so it may be
        more desirable to select a subset of moves from specific positions.
        '''
        all_moves = list()

        for coordinate in self._get_player_coordinates():
            all_moves = all_moves + self.get_position_legal_moves(coordinate)

        return all_moves
    def _has_player_legal_move(self, player_id):
        for coord in self._get_player_coordinates(player_id):
            for neighbor in self.COORDINATES.get_neighbors(coord):
                if self.get_piece_at(neighbor) == self.Piece.EMPTY:
                    if self._is_piece_allowed(
                        neighbor,
                        self.get_piece_at(coord)
                    ):
                        return True

                    if self.COORDINATES.is_center(neighbor):
                        x_diff = neighbor.x - coord.x
                        y_diff = neighbor.y - coord.y
                        new_coord = self.COORDINATES.get(
                            neighbor.x + x_diff,
                            neighbor.y + y_diff
                        )

                        if self.get_piece_at(new_coord) == self.Piece.EMPTY:
                            return True

            return False

    '''
     Get all legal moves for the passed position in the current board state.

     Returned moves are assumed to be moves for the player whose turn it
     currently is.
     '''

    def get_position_legal_moves(self, start_coord):
        legal_moves = list()
        piece = self.get_piece_at(start_coord)

        if self._piece_to_player(piece) is None:
            return legal_moves

        if self._piece_to_player(piece) != self._next_player:
            return legal_moves

        valid_coords = list()
        valid_coords = valid_coords +\
            self.get_legal_coords_direction(start_coord, 'N')
        valid_coords = valid_coords +\
            self.get_legal_coords_direction(start_coord, 'S')
        valid_coords = valid_coords +\
            self.get_legal_coords_direction(start_coord, 'E')
        valid_coords = valid_coords +\
            self.get_legal_coords_direction(start_coord, 'W')

        '''
        Add the real moves now. We do not call is_move_legal here; this is
        because we efficiently enforce legality by only adding those that are
        legal. This makes for a more efficient method so people aren't slowed
        down by just figuring out what they can do.
        '''
        for end_coord in valid_coords:
            if self._is_piece_allowed(end_coord, piece):
                legal_moves.append(
                    move.Move(start_coord, end_coord, self._next_player)
                )

        return legal_moves

    def get_legal_coords_direction(self, start_coord, direction):
        assert(direction in ['N', 'E', 'S', 'W'])
        coords = list()

        if direction in ['N', 'S']:
            if direction == 'N':
                candidates = range(start_coord.y + 1, self.DEFAULT_BOARD_SIZE)
            else:
                candidates = range(start_coord.y - 1, -1, -1)

            for y in candidates:
                coord = self.COORDINATES.get(start_coord.x, y)

                if self.is_coord_empty(coord):
                    coords.append(coord)
                else:
                    break

        if direction in ['E', 'W']:
            if direction == 'E':
                # if direction == 'E' and start_coord.x > 0:
                candidates = range(start_coord.x + 1, self.DEFAULT_BOARD_SIZE)
            else:
                # elif start_coord.x < self.DEFAULT_BOARD_SIZE:
                candidates = range(start_coord.x - 1, -1, -1)

            for x in candidates:
                coord = self.COORDINATES.get(x, start_coord.y)

                if self.is_coord_empty(coord):
                    coords.append(coord)
                else:
                    break

        return coords

    '''
    Helper functions to get players coordinates.
    '''

    def get_current_player_coordinates(self):
        return self._get_player_coordinates()

    def get_opponent_player_coordinates(self):
        opponent = self.PLAYER_WHITE

        if self._next_player == self.PLAYER_WHITE:
            opponent = self.PLAYER_BLACK

        return self._get_player_coordinates(player_id=opponent)

    def _get_player_coordinates(self, player_id=None):
        next_player = self._next_player

        if player_id is not None:
            next_player = player_id

        if next_player == self.Player.WHITE:
            return self._white_coords
        else:
            return self._black_coords

    '''
    Helper functions to check if a move is legal.
    '''

    def is_move_legal(self, move):
        # Make sure that this is the correct player.
        if self._next_player != move.player_id:
            return False

        start_coord = move.get_start_pos()
        end_coord = move.get_end_pos()
        piece = self.get_piece_at(start_coord)

        # Check that the piece being requested actually belongs to the player.
        if self._piece_to_player(piece) != self._next_player:
            return False

        # Next, make sure move doesn't end on a piece.
        if not self.is_coord_empty(end_coord):
            return False

        # Next, make sure the move is actually a move.
        coord_diff = start_coord.max_diff(end_coord)
        if coord_diff == 0:
            return False

        '''
        Now for the actual game logic.
        First we make sure it is moving like a rook.
        '''
        if not (start_coord.x == end_coord.x or start_coord.y == end_coord.y):
            return False

        '''
        Now we make sure it isn't moving through any other pieces or the
        center square.
        '''
        for intermediate_coord in start_coord.get_coords_between(end_coord):
            if not self.is_coord_empty(intermediate_coord):
                return False

            if self.COORDINATES.is_center(intermediate_coord):
                return False

        '''
        Finally make sure that if it is a corner, only the King is to able to
        go there.
        '''
        if not self._is_piece_allowed(end_coord, piece):
            return False

        return True

    '''
    Useful functions.
    '''

    def get_piece_at(self, coord):
        return self._board[coord.x][coord.y]

    def is_opponent_piece_at(self, coord):
        if self.is_coord_empty(coord):
            return False

        piece = self.get_piece_at(coord)
        if self._piece_to_player(piece) == self._next_player:
            return False

        return True

    def is_coord_empty(self, coord):
        return (self.get_piece_at(coord) == self.Piece.EMPTY)

    def get_opponent_id(self):
        if self._next_player == self.Player.WHITE:
            return self.Player.BLACK

        return self.Player.WHITE

    def get_num_player_pieces(self, player_id):
        return len(self._get_player_coordinates(player_id))

    def get_king_position(self):
        return self._king_coord

    def _is_piece_allowed(self, coord, piece):
        if self.COORDINATES.is_center(coord):
            return False

        if piece != self.Piece.KING:
            if self.COORDINATES.is_corner(coord):
                return False

        return True

    def get_turn_player(self):
        return self._next_player

    def get_turn_number(self):
        return self._next_turn

    def is_game_over(self):
        if self._next_turn > self.DEFAULT_MAX_TURNS:
            return True

        if self.winner is not None:
            return True

        return False

    def _piece_to_player(self, piece):
        if piece is self.Piece.WHITE:
            return self.Player.WHITE

        if piece is self.Piece.KING:
            return self.Player.WHITE

        if piece is self.Piece.BLACK:
            return self.Player.BLACK

        return None

    # Dirty debug function
    def print_board(self):
        for j in range(self.DEFAULT_BOARD_SIZE):
            print("==================================================")
            for i in range(self.DEFAULT_BOARD_SIZE):
                # print("({} {} ->)".format(i, j), end='')
                if self._board[i][j] == self.Piece.WHITE:
                    print("O", end='')
                elif self._board[i][j] == self.Piece.KING:
                    print("K", end='')
                if self._board[i][j] == self.Piece.BLACK:
                    print("X", end='')
                else:
                    print(" ", end='')

                print(" | ", end='')

            print("")
