"""
    Problem 666 : Large sum
    http://projecteuler.net/problem=666
        What is the value of the first triangle number to have over five hundred divisors?
    Version: 2015.01.24

    pylint.bat --version
        No config file found, using default configuration
        pylint 1.4.0,
        astroid 1.3.2, common 0.63.2
        Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  6 2014, 22:15:05) [MSC v.1600 32 bit (Intel)]
    Your code has been rated at 10.00/10
"""

from time import time

def debug_validations():
    """all the assertions"""
    pass

def problem_666():
    """solve the problem, print the needed time"""
    start = time()

    result = 666
    assert 666 == result
    print("Result {0} in {1:.2f} seconds".format(result, time()-start))

if __name__ == "__main__":
    debug_validations()

    problem_666()
