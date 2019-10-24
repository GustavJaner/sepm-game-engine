# -*- coding: utf-8 -*-

import sys

from coordinates.coord import Coord
from board import BoardState
from move import Move


def main(argv):
    b = BoardState()
    b.initialize_from_file("../data/test_init.json")

    '''
    for i in range(b.DEFAULT_BOARD_SIZE):
        for j in range(b.DEFAULT_BOARD_SIZE):
            print("({}, {}) -> {}".format(i, j, b._board[i][j]))
    '''

    for player in [BoardState.Player.WHITE, BoardState.Player.BLACK]:
        b._next_player = player
        total_moves = len(b.get_all_legal_moves())

        print("Player {}, {} possible moves.".format(player, total_moves))

    b.print_board()

    # Check captures
    moves = list()
    moves.append(Move(Coord(0, 3), Coord(2, 3), BoardState.Player.BLACK))
    moves.append(Move(Coord(4, 4), Coord(2, 4), BoardState.Player.WHITE))
    moves.append(Move(Coord(3, 0), Coord(3, 3), BoardState.Player.BLACK))
    moves.append(Move(Coord(5, 4), Coord(4, 4), BoardState.Player.WHITE))
    moves.append(Move(Coord(3, 3), Coord(3, 4), BoardState.Player.BLACK))

    for move in moves:
        print("")
        print("--------------------------------------------------------")
        print("")
        # print(str(move))
        b.process_move(move)
        b.print_board()


if __name__ == '__main__':
    main(sys.argv)
