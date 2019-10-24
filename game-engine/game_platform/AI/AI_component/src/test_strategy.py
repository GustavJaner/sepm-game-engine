# -*- coding: utf-8 -*-

import sys

import board
import soft_strategy
import medium_strategy
import hard_strategy
import ia


def main(argv):
    strategy = soft_strategy.SoftStrategy()
    strategy = medium_strategy.SoftStrategy()
    strategy = hard_strategy.HardStrategy()
    IA = ia.IA(strategy)

    '''
    Test the White move.
    In the position of the diagram (move 55), there is one move that guarantees
    the white pieces to win in the next turn, no matter what happens.
    '''
    '''
    b = board.BoardState()
    b.initialize_from_file("../data/test_end.json")

    res = IA.calculate_move(b)
    b.print_board()
    print(res)
    '''
    '''
    Test the Black move.
    In the position of the diagram (move 75) the black pieces can capture the
    white one or two white stones. At the same time, the king is quite close to
    arrive to one of the corners. This test allows us to tune the values of the
    policy.
    '''
    b2 = board.BoardState()
    b2.initialize_from_file("../data/test_end_black.json")

    res = IA.calculate_move(b2)
    b2.print_board()
    print(res)


if __name__ == '__main__':
    main(sys.argv)
