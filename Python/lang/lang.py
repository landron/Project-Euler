'''
    Add here various trips & tricks & subtleties of the language

    pylint, flake8
'''
from functools import reduce
from time import time
import proj_euler

# how to include proj_euler in subfolders
PROJ_EULER = True
if PROJ_EULER:
    import sys
    sys.path.append("..")  # Adds higher directory to python modules path.
    # pylint: disable=import-error


def increment(point):
    ''' point.x++ does not work !! '''
    point.x -= 1
    point.y += 2


def define_object():
    '''
        rapidly define structures using lambdas
    '''
    print("Passing simple objects")
    something = lambda: 0  # noqa: E731
    something.x = 30
    something.y = 67
    increment(something)
    print(something.x, ' ', end='')
    print(something.y)
    print(something.__dict__)


def list_comprehensions():
    '''
        A list comprehension is a syntactic construct available in some
        programming languages for creating a list based on existing lists.
    '''
    print("Great functional programming")
    # "Removed reduce(). Use functools.reduce() if you really need it; \
    # however, 99 percent of the time an explicit for loop is more readable."
    smallest_number = \
        reduce(lambda x, y: x if x[1] < y[1] else y,
               enumerate([6, 5, 8, 9, 13, 4, 6, 8, 13, 5, 15, 4, 8, 6]))[1]
    print(smallest_number)
    some_table = [1, 3, 4, 0, 5, 6, 2, 0, 0, 0, 5, 0, 2, 4]
    zeros = [i+1 for i in range(len(some_table)) if some_table[i] == 0]
    print("Zeros in", some_table, ':', zeros)
    print("No more zeros in", [i for i in some_table if i != 0])
    # everything should be a list
    some_table = [(1, 2), (3, 0), (4, 5), (0, 1), (5, 3), (6, 0), (2, 1),
                  (0, 2), (0, 4), (0, 1), (5, 2), (0, 3), (2, 1), (4, 5)]
    print("Sort 1", some_table, ':', sorted(some_table))
    print("Sort 2", some_table, ':', sorted(set(some_table)))
    print("Sort 3", some_table, ':',
          sorted(set(some_table), key=lambda x: x[1]))
    print("Sort 4", some_table, ':',
          [i for (i, j) in sorted(set(some_table), key=lambda x: x[1])])


def python_coding():
    '''
        Various samples of python code
    '''
    start = time()

    define_object()
    print()
    list_comprehensions()
    print()

    result = proj_euler.get_divisors(48)
    print("Result {0} in {1:.2f} seconds".format(result, time()-start))


if __name__ == "__main__":
    python_coding()
