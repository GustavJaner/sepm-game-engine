# -*- coding: utf-8 -*-


class Coord:
    '''
    A small class to store pairs (x, y). This class is part of the Flyweight
    factory class Coordinates, which provides auxiliary functions to walk
    between Coords.
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )

    def max_diff(self, other):
        # Retuns the maximum coordinate difference with another Coord.
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def get_coords_between(self, other):
        '''
        Returns a list of all the coordinates between this coord and another
        coordinate. Note that it assumes they are either in the same row or
        same column, otherwise it will return an empty list.
        '''
        coords = list()

        update_x = self.x == other.x
        update_y = self.y == self.y

        if update_x and not update_y:
            start = self.x
            end = other.x

        elif update_y and not update_x:
            start = self.y
            end = other.y

        else:
            return coords

        if start > end:
            increment = -1
        else:
            increment = 1

        i = start
        while i != end:
            i = i + increment
            if update_x:
                coords.append(Coord(i, self.y))
            elif update_y:
                coords.append(Coord(self.x, i))

        return coords
