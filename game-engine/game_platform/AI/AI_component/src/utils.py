# -*- coding: utf-8 -*-


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


class BinaryHeap:
    """
    Simple implementation of a binary Max Heap.
    Currently not used.
    """
    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def parent(self, i):
        return (i - 1)//2

    def left(self, i):
        return 2*i + 1

    def right(self, i):
        return 2*i + 2

    def get(self, i):
        return self.items[i]

    def get_max(self):
        if self.size() == 0:
            return None
        return self.items[0]

    def extract_max(self):
        if self.size() == 0:
            return None

        largest = self.get_max()
        self.items[0] = self.items[-1]

        del self.items[-1]

        self.max_heapify(0)
        return largest

    def max_heapify(self, i):
        left = self.left(i)
        right = self.right(i)

        if (left <= self.size() - 1 and self.get(left) > self.get(i)):
            largest = left
        else:
            largest = i

        if (right <= self.size() - 1 and self.get(right) > self.get(largest)):
            largest = right

        if (largest != i):
            self.swap(largest, i)
            self.max_heapify(largest)

    def swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def insert(self, key):
        index = self.size()
        self.items.append(key)

        while (index != 0):
            p = self.parent(index)

            if self.get(p) < self.get(index):
                self.swap(p, index)

            index = p
