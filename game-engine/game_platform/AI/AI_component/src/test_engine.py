# -*- coding: utf-8 -*-

import sys

from engine import GameEngine


def main(argv):
    engine = GameEngine()
    engine.check_file_integrity("../data/test_init.json")

    engine.initialize_from_file("../data/test_init.json")
    result = engine.compute()

    print(result)


if __name__ == '__main__':
    main(sys.argv)
