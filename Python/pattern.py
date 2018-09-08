"""
    Problem 666 : Large sum
    http://projecteuler.net/problem=666
        What is the value of the first triangle number to have over
        five hundred divisors?
    Version: 2018.09.08

    pylint, flake8
"""

from time import time


def problem_666():
    """solve the problem, print the needed time"""
    start = time()

    result = 666
    assert result == 666
    print("Result {0} in {1:.2f} seconds".format(result, time()-start))


def debug_validations():
    """all the assertions"""
    pass


if __name__ == "__main__":
    debug_validations()

    problem_666()
