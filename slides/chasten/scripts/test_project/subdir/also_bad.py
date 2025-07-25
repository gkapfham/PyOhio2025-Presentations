# This file also has a doubly-nested for loop.
class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def print_matrix(self):
        for row in self.matrix:
            for element in row:
                print(element, end=' ')
            print()
