"""
    This is private code.

    https://projecteuler.net/problem=63
    https://www.hackerrank.com/contests/projecteuler/challenges/euler063

    pylint, flake8
"""
import time


USE_LIB = False

if USE_LIB:
    # from lib.proj_euler import get_primes
    pass
else:
    # import math
    pass


def parse_input():
    '''
        read input and solve the problem as defined on HackerRank
    '''
    limit, _ = (int(i) for i in input().strip().split())
    solution = solve(limit)
    solution.sort()
    for i in solution:
        print(i, end='')
    print()


def solve(limit):
    '''
        Return the solution of the problem.
    '''
    return limit


def problem():
    """
        Solve the problem as formulated on the original site.
    """
    start = time.time()

    result = solve(666)
    print("Result {0} in {1:.2f} seconds".format(result, time.time()-start))


def debug_validations():
    """all the assertions"""


if __name__ == "__main__":
    debug_validations()

    # original problem
    problem()

    # harden/generalized HackerRank problem
    # parse_input()
