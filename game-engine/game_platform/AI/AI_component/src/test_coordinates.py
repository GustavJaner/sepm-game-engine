# -*- coding: utf-8 -*-

import sys

from coordinates.coordinates import Coordinates


def main(argv):
    coordinates = Coordinates(11)
    print(coordinates.get(0, 6))


if __name__ == '__main__':
    main(sys.argv)
