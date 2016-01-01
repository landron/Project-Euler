"""
    Problem 666 : Large sum
    http://projecteuler.net/problem=666
        What is the value of the first triangle number to have over five hundred divisors?
    Version: 2016.01.01

    pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
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
