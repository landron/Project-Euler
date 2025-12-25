"""
Purpose
    Add here various trips & tricks & subtleties of the language.

TODO
    * For the moment it is intimately related to proj_euler.py.
    * why open in __enter__, not __init__?

pylint, flake8
"""

from functools import reduce
from time import time
from dataclasses import dataclass
import collections
import typing

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
    __package__ = "Tests"  # pylint: disable=redefined-builtin

# how to include proj_euler in subfolders
PROJ_EULER = True
if PROJ_EULER:
    # pylint: disable=import-error
    import proj_euler


def context_manager():
    """
    The Context Manager way of "subclassing"
    """

    class PrettyFileWriter:
        """
        "A Gentle Introduction to Context Managers:
            The Pythonic Way of Managing Resources"
        https://alysivji.github.io/managing-resources-with-context-managers-pythonic.html

        "subclassing file objects"
        https://stackoverflow.com/questions/16085292
        """

        def __init__(self, file_name):
            self.file = None
            self.file_name = file_name

        def __enter__(self):
            # Not in __init__:
            # R1732: Consider using 'with' for resource-allocating operations
            #   (consider-using-with)
            self.file = open(self.file_name, "w", encoding="utf8")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.file.close()

        def writenl(self, line):
            """
            normal "write" function, but also add a new line
                (the reason of this "subclassing", PrettyFileWriter)
            """
            self.file.write(line)
            self.file.write("\n")

    path = "test.cm.txt"
    print("Subclassing with context manager to", path)
    with PrettyFileWriter(path) as fptr_w:
        fptr_w.writenl("Context manager is some nice feature!")


def eliminate_duplicates(alist):
    """
    eliminate duplicate elements from the given sorted list in-place

    remove while iterating
    https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating

    reverse to delete while not affecting the iteration
    """
    assert alist
    assert all(alist[i] <= alist[i + 1] for i in range(len(alist) - 1))

    last = alist[-1]
    size = len(alist)
    for i, val in enumerate(reversed(alist[:-1])):
        if val == last:
            # the indexes are reversed
            del alist[size - i - 1]
        else:
            last = val


def define_object():
    """
    rapidly define structures
        https://stackoverflow.com/questions/35988/c-like-structures-in-python
    """

    def change(point):
        """point.x++ does not work !!"""
        point.x -= 1
        point.y += 2

    print("\ndefine object")

    # lambda : DEPRECATED
    print("\t ... with lambda")

    def lambda_hack():
        # pylint: disable=unnecessary-lambda-assignment no-member
        something = lambda: 0  # noqa: E731
        something.x = 30
        something.y = 67
        change(something)
        print(something.x, something.y)
        print(something.__dict__)

    lambda_hack()

    # NamedTuple : they are immutable
    print("\t ...  with NamedTuple")

    class Point1(typing.NamedTuple):
        """
        Simple Point class
        """

        x: int
        y: int

    something = Point1(30, 67)
    #  cannot be changed: read only
    # change(something)
    print(something)

    Point2 = collections.namedtuple("Point2", "x y")
    something = Point2(30, 67)
    #  cannot be changed: read only
    # change(something)
    print(something)

    # dataclass
    print("\t ...  with dataclass: the winner!")

    # @dataclass(unsafe_hash=True)
    @dataclass
    class Point3:
        # pylint: disable=invalid-name, missing-class-docstring
        x: int = 0
        y: int = 0

    something = Point3(30, 67)
    change(something)
    print(something.x, something.y)

    # simple class
    print("\t ...  with just some class")

    def just_class():
        # pylint: disable=invalid-name attribute-defined-outside-init
        # pylint: disable=too-few-public-methods
        class Point4:
            """fake class"""

        something = Point4()
        something.x = 30
        something.y = 67
        change(something)
        print(something.x, something.y)

    just_class()


def list_comprehensions():
    """
    A list comprehension is a syntactic construct available in some
    programming languages for creating a list based on existing lists.

    DEPRECATED: the pythonic way is apparently to clearly express what
        what you mean instead of being smart.
    """
    print("Great functional programming")
    # "Removed reduce(). Use functools.reduce() if you really need it; \
    # however, 99 percent of the time an explicit for loop is more readable."
    smallest_number = reduce(
        lambda x, y: x if x[1] < y[1] else y,
        enumerate([6, 5, 8, 9, 13, 4, 6, 8, 13, 5, 15, 4, 8, 6]),
    )[1]
    print(smallest_number)
    some_table = [1, 3, 4, 0, 5, 6, 2, 0, 0, 0, 5, 0, 2, 4]
    zeros = [i + 1 for i in range(len(some_table)) if some_table[i] == 0]
    print("Zeros in", some_table, ":", zeros)
    print("No more zeros in", [i for i in some_table if i != 0])
    # everything should be a list
    some_table = [
        (1, 2),
        (3, 0),
        (4, 5),
        (0, 1),
        (5, 3),
        (6, 0),
        (2, 1),
        (0, 2),
        (0, 4),
        (0, 1),
        (5, 2),
        (0, 3),
        (2, 1),
        (4, 5),
    ]
    print("Sort 1", some_table, ":", sorted(some_table))
    print("Sort 2", some_table, ":", sorted(set(some_table)))
    print("Sort 3", some_table, ":", sorted(set(some_table), key=lambda x: x[1]))
    print(
        "Sort 4",
        some_table,
        ":",
        [i for (i, j) in sorted(set(some_table), key=lambda x: x[1])],
    )


def python_coding():
    """
    Various samples of python code
    """
    start = time()

    context_manager()
    define_object()
    print()
    list_comprehensions()
    print()

    value = 48
    result = proj_euler.get_divisors(value)
    print(f"get_divisors({value}): {result} in {time() - start:.2f} seconds")


def debug_validations():
    """module's assertions"""

    # +=: append vs extend

    test_l = ["abc"]
    test_l += ["def"]
    assert test_l == ["abc", "def"]
    test_l = ["abc"]
    test_l.append("def")
    assert test_l == ["abc", "def"]

    test_l = ["abc"]
    test_l += "def"
    assert test_l == ["abc", "d", "e", "f"]
    test_l = ["abc"]
    test_l.extend("def")
    assert test_l == ["abc", "d", "e", "f"]

    # eliminate_duplicates

    # 'str' object doesn't support item deletion
    test_l = [1, 2, 4, 4, 6, 7, 7, 7]
    eliminate_duplicates(test_l)
    assert test_l == [1, 2, 4, 6, 7]
    test_l = list("abccddde")
    eliminate_duplicates(test_l)
    assert "".join(test_l) == "abcde"
    test_l = list("aaabcdeee")
    eliminate_duplicates(test_l)
    assert "".join(test_l) == "abcde"
    test_l = ["abc", "c", "cer", "cer", "d", "e", "f", "f", "fert"]
    eliminate_duplicates(test_l)
    assert test_l == ["abc", "c", "cer", "d", "e", "f", "fert"]


if __name__ == "__main__":
    debug_validations()
    # python_coding()
