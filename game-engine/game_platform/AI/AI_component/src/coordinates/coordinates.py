# -*- coding: utf-8 -*-
import math

import game_platform.AI.AI_component.src.utils as utils

from game_platform.AI.AI_component.src.coordinates.coord import Coord


class Coordinates(metaclass=utils.Singleton):
    '''
    A Flyweight/Singleton factory class to create and manage connected points
    in a cartesian grid square of size x size.

    The (0, 0) point Coord is in the top left corner. In general, the
    methods of the class use the (i, j) parameters names to idnicate I/O
    attributes and (x, y) to indicate the interal value of the Coord.
    '''

    def __init__(self, size):
        self._size = size
        self._all_coordinates = [
            [Coord(y, x) for x in range(size)] for y in range(size)]

    def __len__(self):
        return(self._size * self._size)

    def __iter__(self):
        ''' Class method to make the class Iterable.'''
        self.i = 0
        self.j = 0

        return self

    def __next__(self):
        ''' Class method to make the class Iterable.'''
        if self.i != self._size:
            i01d = self.i
            j01d = self.j
            result = self._all_coordinates[i01d][j01d]

            self.j += 1
            if self.j == self._size:
                self.j = 0
                self.i += 1

            return result

        else:
            raise StopIteration

    def get(self, i, j):
        return self._all_coordinates[i][j]

    def get_corners(self):
        res = list()
        res.append(self.get(0, 0))
        res.append(self.get(0, self._size - 1))
        res.append(self.get(self._size - 1, 0))
        res.append(self.get(self._size - 1, self._size - 1))

        return res

    def get_neighbors(self, coord):
        neighbors = list()

        for i in [coord.x - 1, coord.x + 1]:
            try:
                neighbors.append(self.get(i, coord.y))
            except IndexError:
                pass

        for j in [coord.y - 1, coord.y + 1]:
            try:
                neighbors.append(self.get(coord.x, j))
            except IndexError:
                pass

        return neighbors

        

    def get_neighbors_x(self, coord):
        neighbors = list()

        for i in [coord.x - 1, coord.x + 1]:
            try:
                neighbors.append(self.get(i, coord.y))
            except IndexError:
                pass
            
        return neighbors
            
            
    def get_neighbors_y(self, coord):
        neighbors = list()
        for j in [coord.y - 1, coord.y + 1]:
            try:
                neighbors.append(self.get(coord.x, j))
            except IndexError:
                pass

        return neighbors

    def distance_to_corner(self, coord):
        '''
        Given a coordinate, returns the distance between it and the closest
        corner.
        '''
        corners = self.get_corners()
        min_distance = math.Inf

        for corner in corners:
            distance = coord.distance(corner)
            if distance < min_distance:
                min_distance = distance

        return distance

    def is_center(self, coord):
        center = int(self._size / 2)

        return(coord.x == center and coord.y == center)

    def is_corner(self, coord):
        i = coord.x
        j = coord.y

        if (i * j) != 0:
            return(i == self._size - 1 and j == self._size - 1)

        return(i + j == self._size - 1 or i + j == 0)

    def is_center_or_neighbor_center(self, coord):
        i = coord.x
        j = coord.y

        center = int(self._size / 2)
        if (not (i == center or j == center)):
            return(False)

        return(abs(i - j) <= 1)
