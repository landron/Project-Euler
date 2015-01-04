"""
    Problem 11 : Largest product in a grid
    http://projecteuler.net/problem=11
        What is the greatest product of four adjacent numbers in the same direction \
            (up, down, left, right, or diagonally) in the 20×20 grid?
    Version: 2015.01.04

    pylint.bat --version
        No config file found, using default configuration
        pylint 1.4.0,
        astroid 1.3.2, common 0.63.2
        Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  6 2014, 22:15:05) [MSC v.1600 32 bit (Intel)]
    Your code has been rated at 10.00/10
"""

from operator import mul
from functools import reduce

GRID = b"""\
08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48
"""

def get_grid(grid):
    """get integers matrix from the string grid"""
    return [[int(x) for x in l.split()] for l in grid.splitlines()]

def get_product(matrix, index, direction, size):
    """calculate hte product for a sequence"""
    sequence = [matrix[index[0]+direction[0]*i][index[1]+direction[1]*i] for i in range(size)]
    return reduce(mul, sequence)

def compare_products(matrix, index, direction, size, result):
    """compare the sequence to the current maximum"""
    prod = get_product(matrix, index, direction, size)
    if result.product < prod:
        result.index = index
        result.direction = direction
        result.product = prod
        # print([matrix[index[0]+direction[0]*i][index[1]+direction[1]*i] for i in range(size)])

def get_max_product(matrix, serie_size):
    """find the sequence with the maximum product"""
    assert len(matrix) >= serie_size
    for line in matrix:
        assert len(line) == len(matrix)
    size = len(matrix)

    result = lambda: None
    result.index = (0, 0)
    result.direction = (1, 0)
    result.product = 0

    # horizontal & vertical
    for i in range(size):
        for j in range(size-serie_size):
            compare_products(matrix, (i, j), (0, 1), serie_size, result)
            compare_products(matrix, (j, i), (1, 0), serie_size, result)

    # diagonals
    # unfortunately, we get the main diagonals two times
    for i in range(size-serie_size):
        for j in range(size-serie_size-i):
            compare_products(matrix, (i+j, j), (1, 1), serie_size, result) #left, bottom
            compare_products(matrix, (j, i+j), (1, 1), serie_size, result) #right, top
            compare_products(matrix, (size-(i+j)-1, j), (-1, 1), serie_size, result) #left, top
            compare_products(matrix, (size-j-1, i+j), (-1, 1), serie_size, result) #right, bottom

    return result

def calculate_max_product(grid, size):
    """find the best sequence given the grid and the size of the sequence"""
    matrix = get_grid(grid)
    result = get_max_product(matrix, size)
    assert result.product == get_product(matrix, result.index, result.direction, size)
    print("Max product for size {1}: {0}".format(result.__dict__, size))

def validate():
    """test units"""
    matrix = get_grid(GRID)
    assert 70600674 == get_max_product(matrix, 4).product
    assert 3318231678 == get_max_product(matrix, 5).product
    assert 188210512710 == get_max_product(matrix, 6).product
    assert 13927577940540 == get_max_product(matrix, 7).product
    assert 72356716950336000000 == get_max_product(matrix, 11).product

if __name__ == "__main__":
    validate()

    calculate_max_product(GRID, 4)
