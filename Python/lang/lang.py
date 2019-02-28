'''
    Purpose
        Add here various trips & tricks & subtleties of the language.
        For the moment it is intimately related to proj_euler.py.

    pylint, flake8
'''
from functools import reduce
from time import time

if __name__ == "__main__" and __package__ is None:
    # https://stackoverflow.com/questions/6323860/sibling-package-imports
    #
    #   This is tough because:
    #     "The only use case seems to be running scripts that happen to be
    #     living inside a module's directory, which I've always seen as an
    #     antipattern."
    #
    #   from ... import proj_euler
    #   #   ValueError: attempted relative import beyond top-level package

    import sys
    import os
    sys.path.append(os.path.dirname(sys.path[0]))
    __package__ = 'Tests'  # pylint: disable=redefined-builtin
import proj_euler  # pylint: disable=wrong-import-position  # noqa: E402

# how to include proj_euler in subfolders
PROJ_EULER = True
if PROJ_EULER:
    # pylint: disable=unused-import
    from proj_euler import get_primes  # noqa: F401


def context_manager():
    '''
        The Context Manager way of "subclassing"
    '''
    class PrettyFileWriter:
        '''
            "A Gentle Introduction to Context Managers:
                The Pythonic Way of Managing Resources"
            https://alysivji.github.io/managing-resources-with-context-managers-pythonic.html

            "subclassing file objects"
            https://stackoverflow.com/questions/16085292
        '''
        def __init__(self, fileName):
            self.file = open(fileName, 'w')

        def __enter__(self):
            # return self.file
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.file.close()

        def writenl(self, line):
            '''
                normal "write" function, but also add a new line
                    (the reason of this "subclassing", PrettyFileWriter)
            '''
            self.file.write(line)
            self.file.write('\n')

    path = 'test.cm.txt'
    print("Subclassing with context manager to", path)
    with PrettyFileWriter(path) as fptr_w:
        fptr_w.writenl("Context manager is some nice feature!")


def eliminate_duplicates(lista):
    '''
        eliminate duplicate elements from the given sorted list in-place

        remove while iterating
        https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating

        reverse to delete while not affecting the iteration
    '''
    assert lista
    assert all(lista[i] <= lista[i+1] for i in range(len(lista)-1))

    last = lista[-1] + 1
    size = len(lista)
    for i, val in enumerate(reversed(lista)):
        if val == last:
            # the indexes are reversed
            del lista[size-i-1]
        else:
            last = val


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

        DEPRECATED: the pythonic way is apparently to clearly express what
            what you mean instead of being smart.
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

    context_manager()
    define_object()
    print()
    list_comprehensions()
    print()

    result = proj_euler.get_divisors(48)
    print("Result {0} in {1:.2f} seconds".format(result, time()-start))


if __name__ == "__main__":
    python_coding()
